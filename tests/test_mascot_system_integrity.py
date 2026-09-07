import os
import sys
import json
import zipfile
from PIL import Image

def test_mascot_system_integrity(state_id="00_idle"):
    print(f"\n=======================================================")
    print(f"🧪 SUITE DE TESTS AUTOMATISÉE : ÉTAT '{state_id}'")
    print(f"=======================================================")
    
    mascots = ["aituko", "owluko", "luneko", "usako", "inuko", "hatoko"]
    required_files = [
        ("static.png", "PNG 512x512 RGBA"),
        ("static.webp", "WebP 512x512"),
        ("animated.gif", "GIF Animé transparent"),
        ("animated.webp", "WebP Animé transparent"),
        ("animated.png", "APNG Animé transparent"),
        ("looped_video.mp4", "Vidéo MP4 H.264 bouclée"),
        ("snippet.json", "Snippets de code multi-frameworks"),
        (f"bundle_{{m}}_{state_id}.zip", "Archive ZIP de téléchargement")
    ]
    
    total_checks = 0
    passed_checks = 0
    errors = []
    
    for m in mascots:
        m_dir = f"assets/{state_id}" if m == "aituko" else f"mascots/{m}/assets/{state_id}"
        print(f"\n🔍 Audit de la mascotte : {m.upper()} ({m_dir})")
        
        for file_pattern, desc in required_files:
            total_checks += 1
            filename = file_pattern.format(m=m)
            filepath = f"{m_dir}/{filename}"
            
            # 1. File existence
            if not os.path.exists(filepath):
                errors.append(f"❌ [{m}] Fichier manquant : {filepath} ({desc})")
                continue
                
            # 2. File size > 0
            size = os.path.getsize(filepath)
            if size == 0:
                errors.append(f"❌ [{m}] Fichier vide (0 octets) : {filepath}")
                continue
                
            # 3. Image dimensions & alpha check
            if filename.endswith((".png", ".webp", ".gif")):
                try:
                    im = Image.open(filepath)
                    w, h = im.size
                    if w != 512 or h != 512:
                        errors.append(f"⚠️ [{m}] Dimensions non conformes pour {filename} : {w}x{h} (attendu: 512x512)")
                    if filename == "static.png" and im.mode != "RGBA":
                        errors.append(f"⚠️ [{m}] Mode de couleur invalide pour {filename} : {im.mode} (attendu: RGBA)")
                except Exception as e:
                    errors.append(f"❌ [{m}] Fichier image corrompu {filename} : {e}")
                    continue
                    
            # 4. Snippet JSON check
            if filename == "snippet.json":
                try:
                    with open(filepath, "r") as f:
                        data = json.load(f)
                    for key in ["react", "vue", "html"]:
                        if key not in data or not data[key]:
                            errors.append(f"⚠️ [{m}] Snippet manquant ou vide pour '{key}' dans {filename}")
                except Exception as e:
                    errors.append(f"❌ [{m}] JSON de snippets invalide {filename} : {e}")
                    continue
                    
            # 5. Zip bundle check
            if filename.endswith(".zip"):
                try:
                    with zipfile.ZipFile(filepath, "r") as zipf:
                        zip_contents = zipf.namelist()
                        if len(zip_contents) < 5:
                            errors.append(f"⚠️ [{m}] ZIP incomplet ({len(zip_contents)} fichiers) : {zip_contents}")
                except Exception as e:
                    errors.append(f"❌ [{m}] Archive ZIP corrompue {filename} : {e}")
                    continue
                    
            print(f"  ✅ {desc:36} : OK ({size/1024:.1f} KB)")
            passed_checks += 1

    print(f"\n=======================================================")
    print(f"📊 RÉSULTAT DE L'AUDIT QUALITÉ : {passed_checks}/{total_checks} TESTS RÉUSSIS ({passed_checks/total_checks*100:.1f}%)")
    print(f"=======================================================")
    
    if errors:
        print("\n⚠️ ANOMALIES DÉTECTÉES :")
        for err in errors:
            print(f"  • {err}")
        return False
    else:
        print(f"🎉 AUCUNE ANOMALIE : TOUS LES FORMATS ET ARCHIVES DE '{state_id}' SONT 100% CONFORMES !")
        return True

if __name__ == "__main__":
    target_state = sys.argv[1] if len(sys.argv) > 1 else "00_idle"
    success = test_mascot_system_integrity(target_state)
    sys.exit(0 if success else 1)
