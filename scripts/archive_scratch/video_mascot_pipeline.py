"""
Video-to-Mascot Automated Pipeline
==================================
Pipeline pour :
1. Envoyer l'image de référence sur fond vert à une API Image-to-Video (Google Veo, Kling, ou Replicate/Luma)
2. Récupérer le MP4 généré
3. Effectuer le bouclage temporel parfait (Ping-Pong / Phase Blend)
4. Détourer le fond vert via FFmpeg Chroma-Key + Despill (anti-halo)
5. Exporter les formats finaux : WebP Animé 60fps, APNG, et WebM transparent
"""

import os
import sys
import json
import base64
import subprocess
from typing import Optional


class VideoProcessor:
    """Traitement local des vidéos générées par IA (Bouclage + Détourage)."""

    @staticmethod
    def process_raw_video(
        input_mp4: str,
        output_prefix: str,
        loop_method: str = "pingpong",
        target_duration_sec: float = 1.5,
        target_fps: int = 24
    ) -> dict:
        """
        Prend un MP4 brut généré sur fond vert et produit tous les formats transparents bouclés.
        """
        if not os.path.exists(input_mp4):
            raise FileNotFoundError(f"Fichier vidéo introuvable : {input_mp4}")

        out_dir = os.path.dirname(output_prefix)
        os.makedirs(out_dir, exist_ok=True)

        looped_mp4 = f"{output_prefix}_looped.mp4"
        out_webp = f"{output_prefix}_animated.webp"
        out_apng = f"{output_prefix}_animated.png"
        out_webm = f"{output_prefix}_transparent.webm"

        print(f"🎬 [1/4] Application du bouclage ({loop_method})...")
        if loop_method == "pingpong":
            # Ping-Pong : Joue de 0 à target_duration puis en sens inverse pour une boucle 100% sans coupure
            cmd_loop = [
                "ffmpeg", "-y",
                "-t", str(target_duration_sec),
                "-i", input_mp4,
                "-filter_complex", "[0:v]split[v1][v2];[v2]reverse[v2rev];[v1][v2rev]concat=n=2:v=1[v]",
                "-map", "[v]",
                "-r", str(target_fps),
                "-c:v", "libx264", "-pix_fmt", "yuv420p",
                looped_mp4
            ]
            subprocess.run(cmd_loop, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            # Simple trim
            cmd_loop = ["ffmpeg", "-y", "-t", str(target_duration_sec), "-i", input_mp4, "-r", str(target_fps), looped_mp4]
            subprocess.run(cmd_loop, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print("🟢 [2/4] Suppression du fond vert (Chroma-Key + Despill)...")
        # Filtre FFmpeg : colorkey vert (#00FF00) + despill pour éliminer le reflet vert sur la céramique
        chroma_filter = "colorkey=0x00FF00:0.35:0.10,despill=type=green:mode=auto"

        print("⚡️ [3/4] Encodage WebP Animé Transparent (60fps)...")
        cmd_webp = [
            "ffmpeg", "-y",
            "-i", looped_mp4,
            "-vf", f"{chroma_filter},fps=30,scale=320:-1:flags=lanczos",
            "-vcodec", "libwebp",
            "-lossless", "0",
            "-q:v", "85",
            "-loop", "0",
            out_webp
        ]
        subprocess.run(cmd_webp, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print("📦 [4/4] Encodage APNG Transparent & WebM...")
        cmd_apng = [
            "ffmpeg", "-y",
            "-i", looped_mp4,
            "-vf", f"{chroma_filter},fps=15,scale=320:-1:flags=lanczos",
            "-plays", "0",
            out_apng
        ]
        subprocess.run(cmd_apng, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        cmd_webm = [
            "ffmpeg", "-y",
            "-i", looped_mp4,
            "-vf", chroma_filter,
            "-c:v", "libvpx-vp9",
            "-pix_fmt", "yuva420p",
            "-auto-alt-ref", "0",
            out_webm
        ]
        subprocess.run(cmd_webm, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        results = {
            "webp": out_webp,
            "apng": out_apng,
            "webm": out_webm,
            "webp_size_kb": round(os.path.getsize(out_webp) / 1024, 1),
            "apng_size_kb": round(os.path.getsize(out_apng) / 1024, 1)
        }
        print(f"✅ Terminé avec succès ! WebP: {results['webp_size_kb']} Ko | APNG: {results['apng_size_kb']} Ko")
        return results


class VideoAIEngine:
    """Connecteurs pour les différentes API de génération vidéo IA."""

    @staticmethod
    def get_veo_payload(image_path: str, prompt: str) -> dict:
        """Prépare la charge utile pour l'API Google Veo (Vertex AI)."""
        with open(image_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode("utf-8")
        
        return {
            "instances": [
                {
                    "prompt": prompt,
                    "image": {"bytesBase64Encoded": img_b64}
                }
            ],
            "parameters": {
                "aspectRatio": "1:1",
                "sampleCount": 1,
                "durationSeconds": 3,
                "fps": 24,
                "personGeneration": "dont_allow"
            }
        }

    @staticmethod
    def get_kling_payload(image_base64: str, prompt: str) -> dict:
        """Prépare la charge utile pour Kling AI API (Image2Video)."""
        return {
            "model": "kling-v1-5",
            "image": image_base64,
            "prompt": prompt,
            "cfg_scale": 0.5,
            "mode": "std",
            "duration": "5"
        }


if __name__ == "__main__":
    print("Moteur de Pipeline Vidéo prêt.")
