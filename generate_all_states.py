import os
import sys
import time
import glob
import json
import zipfile
import subprocess
import base64
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from google import genai
from google.genai import types
from core_pipeline.keyer import key_greenscreen_master

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/richard/Developer/Stickers Uko/stickers-3d-7659bde46f1f.json"
client = genai.Client(vertexai=True, project="stickers-3d", location="us-central1")
brain_dir = "/Users/richard/.gemini/antigravity/brain/b08b93a2-3f91-4648-84ae-790dd87c0c68"

MASTER_IMAGES = {
    "aituko": "mascots/aituko/master/aituko_greenscreen_master.jpg",
    "owluko": "mascots/owluko/master/owleko_greenscreen_master.jpg",
    "luneko": "mascots/luneko/master/luneko_greenscreen_master.jpg",
    "usako": "mascots/usako/master/usako_greenscreen_master.jpg",
    "inuko": "mascots/inuko/master/inuko_greenscreen_master.jpg",
    "hatoko": "mascots/hatoko/master/hatoko_greenscreen_master.jpg"
}

STATE_PROMPTS = {
    "02_celebrating": {
        "title": "Victoire / Fête",
        "aituko": "A high-end 3D character animation of this cute white porcelain robot mascot AItuko on uniform solid chroma green screen background (#00FF00). The robot jumps joyfully with both arms raised in a cheerful victory celebration, floating smoothly, glowing cyan (#00E5FF) eyes and smile, colorful confetti gently floating around. Seamless white porcelain pods floating underneath without feet or toes. High-end Pixar 3D animation, 24fps.",
        "owluko": "A high-end 3D character animation of this cute cream owl mascot Owluko on uniform solid chroma green screen background (#00FF00). The owl flaps its fluffy wings joyfully in a victory celebration, big golden eyes gleaming with happiness, small colorful confetti floating gently. High-end Pixar 3D animation, 24fps.",
        "luneko": "A high-end 3D character animation of this cute ginger tabby cat mascot Luneko on uniform solid chroma green screen background (#00FF00). The cat jumps with cheerful excitement, raising its front paws in victory, big happy smile, colorful confetti floating. Solid white chest fur, high-end Pixar 3D animation, 24fps.",
        "usako": "A high-end 3D character animation of this cute white bunny mascot Usako with its signature brown patch and sage green headband on uniform solid chroma green screen background (#00FF00). The bunny hops happily in celebration, raising its paws with a cheerful victory smile, soft confetti drifting. High-end Pixar 3D animation, 24fps.",
        "inuko": "A high-end 3D character animation of this noble black and tan Doberman mascot Inuko on uniform solid chroma green screen background (#00FF00). The dog barks happily and wags its tail, sitting tall and proud in victory celebration with a joyful friendly expression. Sleek fur, high-end Pixar 3D animation, 24fps.",
        "hatoko": "A high-end 3D character animation of this cute round messenger pigeon mascot Hatoko with its closed leather satchel on uniform solid chroma green screen background (#00FF00). The pigeon hops and flaps its wings in a joyful celebration dance, smiling happily with colorful confetti drifting. High-end Pixar 3D animation, 24fps."
    },
    "03_ai_thinking": {
        "title": "Réflexion IA / Analyse",
        "aituko": "A high-end 3D character animation of this cute white porcelain robot mascot AItuko on uniform solid chroma green screen background (#00FF00). The robot tilts its head thoughtfully, placing a delicate 4-fingered porcelain hand to its chin in deep smart problem-solving thought, cyan (#00E5FF) eyes pulsing softly. Clean porcelain pods underneath. High-end Pixar 3D animation, 24fps.",
        "owluko": "A high-end 3D character animation of this cute cream owl mascot Owluko on uniform solid chroma green screen background (#00FF00). The owl tilts its head from side to side wisely, blinking its big golden amber eyes in thoughtful contemplative analysis. High-end Pixar 3D animation, 24fps.",
        "luneko": "A high-end 3D character animation of this cute ginger tabby cat mascot Luneko on uniform solid chroma green screen background (#00FF00). The cat sits thoughtfully, tilting its head with an inquisitive curious expression, gently tapping its chin with a front paw. High-end Pixar 3D animation, 24fps.",
        "usako": "A high-end 3D character animation of this cute white bunny mascot Usako with sage green headband on uniform solid chroma green screen background (#00FF00). The bunny taps its chin thoughtfully, ears gently twitching in smart contemplative thought. High-end Pixar 3D animation, 24fps.",
        "inuko": "A high-end 3D character animation of this noble black and tan Doberman mascot Inuko on uniform solid chroma green screen background (#00FF00). The dog tilts its head inquisitively with an alert, intelligent problem-solving expression, ears perked up sharply. High-end Pixar 3D animation, 24fps.",
        "hatoko": "A high-end 3D character animation of this cute round messenger pigeon mascot Hatoko with closed leather satchel on uniform solid chroma green screen background (#00FF00). The pigeon tilts its round head thoughtfully, touching its beak with its wing tip in deep reflection. High-end Pixar 3D animation, 24fps."
    },
    "04_error_404": {
        "title": "Erreur 404 / Confusion",
        "aituko": "A high-end 3D character animation of this cute white porcelain robot mascot AItuko on uniform solid chroma green screen background (#00FF00). The robot holds a small cute wooden sign with '404' written on it, tilting its head with a sweet apologetic shrug, eyes displaying soft cyan question marks. Clean porcelain pods. High-end Pixar 3D animation, 24fps.",
        "owluko": "A high-end 3D character animation of this cute cream owl mascot Owluko on uniform solid chroma green screen background (#00FF00). The owl holds a small cute wooden '404' sign in its wing, looking slightly puzzled and apologetic with big round eyes. High-end Pixar 3D animation, 24fps.",
        "luneko": "A high-end 3D character animation of this cute ginger tabby cat mascot Luneko on uniform solid chroma green screen background (#00FF00). The cat holds a small cute wooden '404' sign with its paws, scratching its head with an apologetic, cute confused look. High-end Pixar 3D animation, 24fps.",
        "usako": "A high-end 3D character animation of this cute white bunny mascot Usako on uniform solid chroma green screen background (#00FF00). The bunny holds a small cute wooden '404' sign, looking slightly embarrassed with drooped ears and a cute shrug. High-end Pixar 3D animation, 24fps.",
        "inuko": "A high-end 3D character animation of this noble black and tan Doberman mascot Inuko on uniform solid chroma green screen background (#00FF00). The dog sits politely beside a small neat wooden '404' sign, tilting its head with an apologetic, gentle expression. High-end Pixar 3D animation, 24fps.",
        "hatoko": "A high-end 3D character animation of this cute round messenger pigeon mascot Hatoko on uniform solid chroma green screen background (#00FF00). The pigeon holds a small cute wooden '404' sign in its wing, looking around quizzically with a cute puzzled expression. High-end Pixar 3D animation, 24fps."
    },
    "05_thumbs_up": {
        "title": "Pouce en l'Air / Validation",
        "aituko": "A high-end 3D character animation of this cute white porcelain robot mascot AItuko on uniform solid chroma green screen background (#00FF00). The robot gives a confident, solid thumbs-up gesture with its right 4-fingered hand, smiling brightly with glowing cyan (#00E5FF) eyes. Smooth floating porcelain pods. High-end Pixar 3D animation, 24fps.",
        "owluko": "A high-end 3D character animation of this cute cream owl mascot Owluko on uniform solid chroma green screen background (#00FF00). The owl raises its right wing in an encouraging, solid wing-thumb approval gesture, winking warmly with golden eyes. High-end Pixar 3D animation, 24fps.",
        "luneko": "A high-end 3D character animation of this cute ginger tabby cat mascot Luneko on uniform solid chroma green screen background (#00FF00). The cat gives an enthusiastic thumbs-up with its right paw, smiling with confident cheerful brown eyes. High-end Pixar 3D animation, 24fps.",
        "usako": "A high-end 3D character animation of this cute white bunny mascot Usako on uniform solid chroma green screen background (#00FF00). The bunny gives a cute thumbs-up paw gesture, nodding approvingly with a confident smile. High-end Pixar 3D animation, 24fps.",
        "inuko": "A high-end 3D character animation of this noble black and tan Doberman mascot Inuko on uniform solid chroma green screen background (#00FF00). The dog gives a firm nod of approval and raises a front paw in a confident validation gesture with a proud smile. High-end Pixar 3D animation, 24fps.",
        "hatoko": "A high-end 3D character animation of this cute round messenger pigeon mascot Hatoko with closed leather satchel on uniform solid chroma green screen background (#00FF00). The pigeon gives an enthusiastic thumbs-up wing gesture, smiling happily with a confident nod. High-end Pixar 3D animation, 24fps."
    },
    "06_sleeping": {
        "title": "Veille / Sommeil Zzz",
        "aituko": "A high-end 3D character animation of this cute white porcelain robot mascot AItuko on uniform solid chroma green screen background (#00FF00). The robot enters a peaceful sleep standby mode, eyes dimmed to soft gentle cyan lines, breathing rhythmically and floating gently with tiny floating stylized cyan 'Zzz' bubbles, zero sudden waking. High-end Pixar 3D animation, 24fps.",
        "owluko": "A high-end 3D character animation of this cute cream owl mascot Owluko on uniform solid chroma green screen background (#00FF00). The owl is peacefully asleep with closed eyes, head tucked gently, breathing softly with tiny floating golden 'Zzz' bubbles, continuous deep sleep. High-end Pixar 3D animation, 24fps.",
        "luneko": "A high-end 3D character animation of this cute ginger tabby cat mascot Luneko on uniform solid chroma green screen background (#00FF00). The cat is curled up in a continuous peaceful sleep, tail tucked warmly, chest rising softly with breathing, tiny floating 'Zzz' bubbles. High-end Pixar 3D animation, 24fps.",
        "usako": "A high-end 3D character animation of this cute white bunny mascot Usako on uniform solid chroma green screen background (#00FF00). The bunny is resting peacefully asleep, ears draped back comfortably, nose gently twitching in continuous calm sleep with tiny 'Zzz' bubbles. High-end Pixar 3D animation, 24fps.",
        "inuko": "A high-end 3D character animation of this noble black and tan Doberman mascot Inuko on uniform solid chroma green screen background (#00FF00). The dog lies down gracefully with paws crossed, eyes gently closed in continuous calm resting sleep, breathing peacefully with tiny 'Zzz' bubbles. High-end Pixar 3D animation, 24fps.",
        "hatoko": "A high-end 3D character animation of this cute round messenger pigeon mascot Hatoko on uniform solid chroma green screen background (#00FF00). The round pigeon is peacefully asleep on its perch, head tucked snugly into its feathers, breathing calmly with tiny 'Zzz' bubbles. High-end Pixar 3D animation, 24fps."
    },
    "07_pointing": {
        "title": "Guidage / Pointage",
        "aituko": "A high-end 3D character animation of this cute white porcelain robot mascot AItuko on uniform solid chroma green screen background (#00FF00). The robot clearly points to the right side with its right index finger in a friendly, precise guiding gesture, smiling with cyan eyes. Smooth porcelain pods. High-end Pixar 3D animation, 24fps.",
        "owluko": "A high-end 3D character animation of this cute cream owl mascot Owluko on uniform solid chroma green screen background (#00FF00). The owl points clearly to the right side with its right wing tip in a wise, helpful guiding gesture, looking warmly to the viewer. High-end Pixar 3D animation, 24fps.",
        "luneko": "A high-end 3D character animation of this cute ginger tabby cat mascot Luneko on uniform solid chroma green screen background (#00FF00). The cat extends its right paw, pointing clearly to the right with an inviting cheerful expression. High-end Pixar 3D animation, 24fps.",
        "usako": "A high-end 3D character animation of this cute white bunny mascot Usako on uniform solid chroma green screen background (#00FF00). The bunny points directly to the right with its paw, smiling enthusiastically to guide the user. High-end Pixar 3D animation, 24fps.",
        "inuko": "A high-end 3D character animation of this noble black and tan Doberman mascot Inuko on uniform solid chroma green screen background (#00FF00). The dog points its muzzle and right paw firmly towards the right side in a confident, clear directing gesture. High-end Pixar 3D animation, 24fps.",
        "hatoko": "A high-end 3D character animation of this cute round messenger pigeon mascot Hatoko on uniform solid chroma green screen background (#00FF00). The pigeon points its right wing firmly to the right side, guiding the viewer with a friendly helpful smile. High-end Pixar 3D animation, 24fps."
    },
    "08_searching": {
        "title": "Recherche / Loupe",
        "aituko": "A high-end 3D character animation of this cute white porcelain robot mascot AItuko on uniform solid chroma green screen background (#00FF00). The robot holds a stylish modern 3D orange magnifying glass, moving it smoothly to inspect and scan back and forth with curious glowing cyan eyes. Clean floating pods. High-end Pixar 3D animation, 24fps.",
        "owluko": "A high-end 3D character animation of this cute cream owl mascot Owluko on uniform solid chroma green screen background (#00FF00). The owl holds a cute stylized magnifying glass, peering through it with an inquisitive enlarged golden eye, scanning smoothly. High-end Pixar 3D animation, 24fps.",
        "luneko": "A high-end 3D character animation of this cute ginger tabby cat mascot Luneko on uniform solid chroma green screen background (#00FF00). The cat holds a 3D magnifying glass with its paws, curiously looking around and tracking clues in a playful search animation. High-end Pixar 3D animation, 24fps.",
        "usako": "A high-end 3D character animation of this cute white bunny mascot Usako on uniform solid chroma green screen background (#00FF00). The bunny holds a small cute magnifying glass, sniffing and looking around carefully in a smart focused search. High-end Pixar 3D animation, 24fps.",
        "inuko": "A high-end 3D character animation of this noble black and tan Doberman mascot Inuko on uniform solid chroma green screen background (#00FF00). The dog holds a sleek magnifying glass with one paw, sniffing attentively and scanning carefully like a master detective. High-end Pixar 3D animation, 24fps.",
        "hatoko": "A high-end 3D character animation of this cute round messenger pigeon mascot Hatoko on uniform solid chroma green screen background (#00FF00). The pigeon holds a magnifying glass in its wing, inspecting the area with sharp, curious detective focus. High-end Pixar 3D animation, 24fps."
    },
    "09_loading": {
        "title": "Chargement / Attente",
        "aituko": "A high-end 3D character animation of this cute white porcelain robot mascot AItuko on uniform solid chroma green screen background (#00FF00). The robot watches happily as a small glowing golden 3D star orbits smoothly around its head in a continuous celestial loop. Floating porcelain pods. High-end Pixar 3D animation, 24fps.",
        "owluko": "A high-end 3D character animation of this cute cream owl mascot Owluko on uniform solid chroma green screen background (#00FF00). The owl follows a gentle golden star orbiting softly above its head, tilting its head in a smooth rhythmic loading loop. High-end Pixar 3D animation, 24fps.",
        "luneko": "A high-end 3D character animation of this cute ginger tabby cat mascot Luneko on uniform solid chroma green screen background (#00FF00). The cat playfully tracks a glowing golden star orbiting around its head, swaying gently in a smooth mesmerizing loop. High-end Pixar 3D animation, 24fps.",
        "usako": "A high-end 3D character animation of this cute white bunny mascot Usako on uniform solid chroma green screen background (#00FF00). The bunny looks up with sparkling eyes as a cute golden star orbits continuously above its ears in a seamless loading loop. High-end Pixar 3D animation, 24fps.",
        "inuko": "A high-end 3D character animation of this noble black and tan Doberman mascot Inuko on uniform solid chroma green screen background (#00FF00). The dog watches a noble golden star orbit smoothly above its head, maintaining a calm, patient, rhythmic loading posture. High-end Pixar 3D animation, 24fps.",
        "hatoko": "A high-end 3D character animation of this cute round messenger pigeon mascot Hatoko on uniform solid chroma green screen background (#00FF00). The pigeon watches a small golden mail star orbit softly around its head in a gentle, hypnotic loading loop. High-end Pixar 3D animation, 24fps."
    },
    "10_idea": {
        "title": "Idée Trouvée / Ampoule",
        "aituko": "A high-end 3D character animation of this cute white porcelain robot mascot AItuko on uniform solid chroma green screen background (#00FF00). A small stylized 3D lightbulb appears above its head and illuminates with bright electric cyan (#00E5FF) light, robot gasps happily and snaps fingers in eureka moment. High-end Pixar 3D animation, 24fps.",
        "owluko": "A high-end 3D character animation of this cute cream owl mascot Owluko on uniform solid chroma green screen background (#00FF00). A bright golden 3D lightbulb lights up above its head with a soft click, owl's eyes widen with sudden brilliant inspiration and delight. High-end Pixar 3D animation, 24fps.",
        "luneko": "A high-end 3D character animation of this cute ginger tabby cat mascot Luneko on uniform solid chroma green screen background (#00FF00). A bright lightbulb pops up above the cat's head, cat's eyes light up with sudden playful realization and a big delighted smile. High-end Pixar 3D animation, 24fps.",
        "usako": "A high-end 3D character animation of this cute white bunny mascot Usako on uniform solid chroma green screen background (#00FF00). A small glowing lightbulb illuminates above its ears, bunny claps paws in a brilliant eureka revelation. High-end Pixar 3D animation, 24fps.",
        "inuko": "A high-end 3D character animation of this noble black and tan Doberman mascot Inuko on uniform solid chroma green screen background (#00FF00). A glowing lightbulb clicks on above the dog's head, dog perks up ears and gives a smart, triumphant grin of sudden clarity. High-end Pixar 3D animation, 24fps.",
        "hatoko": "A high-end 3D character animation of this cute round messenger pigeon mascot Hatoko on uniform solid chroma green screen background (#00FF00). A bright lightbulb clicks on above the pigeon's head, pigeon hops excitedly with wings spread in an instant eureka discovery. High-end Pixar 3D animation, 24fps."
    },
    "11_security": {
        "title": "Sécurité / Protection",
        "aituko": "A high-end 3D character animation of this cute white porcelain robot mascot AItuko on uniform solid chroma green screen background (#00FF00). The robot raises both hands in a solid, firm protective stop and guarding posture, cyan eyes glowing with resolute authority. NO prop shield, NO holographic barrier. Clean floating pods. High-end Pixar 3D animation, 24fps.",
        "owluko": "A high-end 3D character animation of this cute cream owl mascot Owluko on uniform solid chroma green screen background (#00FF00). The owl spreads its wings firmly in a protective guarding boundary stance, looking forward with wise resolute security. NO props. High-end Pixar 3D animation, 24fps.",
        "luneko": "A high-end 3D character animation of this cute ginger tabby cat mascot Luneko on uniform solid chroma green screen background (#00FF00). The cat stands firm with paws raised in a cute martial arts guarding security stance, looking confident and protective. High-end Pixar 3D animation, 24fps.",
        "usako": "A high-end 3D character animation of this cute white bunny mascot Usako on uniform solid chroma green screen background (#00FF00). The bunny stands in a resolute martial ninja guarding stance with headband tied, projecting calm impenetrable defense. High-end Pixar 3D animation, 24fps.",
        "inuko": "A high-end 3D character animation of this noble black and tan Doberman mascot Inuko on uniform solid chroma green screen background (#00FF00). The dog stands tall and vigilant in a master guardian protective stance, chest forward, embodying ultimate loyalty and security. High-end Pixar 3D animation, 24fps.",
        "hatoko": "A high-end 3D character animation of this cute round messenger pigeon mascot Hatoko with closed leather satchel on uniform solid chroma green screen background (#00FF00). The pigeon holds its bag safely behind its wings, standing in a firm vigilant protective security stance. High-end Pixar 3D animation, 24fps."
    },
    "12_goodbye": {
        "title": "Au Revoir / Départ",
        "aituko": "A high-end 3D character animation of this cute white porcelain robot mascot AItuko on uniform solid chroma green screen background (#00FF00). The robot waves a gentle, comforting goodbye with its right hand, eyes displaying a sweet warm cyan crescent smile, floating softly. Clean porcelain pods. High-end Pixar 3D animation, 24fps.",
        "owluko": "A high-end 3D character animation of this cute cream owl mascot Owluko on uniform solid chroma green screen background (#00FF00). The owl gives a gentle, warm farewell wave with its wing, looking kindly at the viewer with a sweet comforting smile. High-end Pixar 3D animation, 24fps.",
        "luneko": "A high-end 3D character animation of this cute ginger tabby cat mascot Luneko on uniform solid chroma green screen background (#00FF00). The cat waves a sweet, friendly goodbye with its right paw, smiling with affectionate brown eyes. High-end Pixar 3D animation, 24fps.",
        "usako": "A high-end 3D character animation of this cute white bunny mascot Usako on uniform solid chroma green screen background (#00FF00). The bunny waves both paws warmly in a cute friendly farewell, smiling sweetly. High-end Pixar 3D animation, 24fps.",
        "inuko": "A high-end 3D character animation of this noble black and tan Doberman mascot Inuko on uniform solid chroma green screen background (#00FF00). The dog bows politely with a gentle, loyal farewell nod and soft tail wag. High-end Pixar 3D animation, 24fps.",
        "hatoko": "A high-end 3D character animation of this cute round messenger pigeon mascot Hatoko on uniform solid chroma green screen background (#00FF00). The pigeon waves a cheerful wing goodbye, fluttering its feathers warmly before turning to fly. High-end Pixar 3D animation, 24fps."
    }
}

def generate_video_veo(m_key, prompt, output_mp4):
    master_p = MASTER_IMAGES[m_key]
    with open(master_p, "rb") as f:
        m_bytes = f.read()
    img_input = types.Image(image_bytes=m_bytes, mime_type="image/jpeg")
    
    print(f"   🎬 Envoi de la requête Veo 3.1 pour {m_key.upper()}...")
    t0 = time.time()
    op = client.models.generate_videos(
        model="veo-3.1-fast-generate-001",
        prompt=prompt,
        image=img_input,
        config=types.GenerateVideosConfig(
            aspect_ratio="16:9",
            duration_seconds=4,
            person_generation="allow_all"
        )
    )
    
    while not op.done:
        elapsed = int(time.time() - t0)
        print(f"      ... ({elapsed}s) Rendu Veo 3.1 en cours ({m_key})...")
        time.sleep(5)
        op = client.operations.get(op)
        
    if not op.response or not op.response.generated_videos:
        raise RuntimeError(f"Erreur Veo pour {m_key}: {op.error}")
        
    vid = op.response.generated_videos[0].video
    if hasattr(vid, "video_bytes") and vid.video_bytes:
        with open(output_mp4, "wb") as f:
            f.write(vid.video_bytes)
    elif hasattr(vid, "uri"):
        client.files.download(file=vid.uri, destination=output_mp4)
        
    print(f"   ✅ Vidéo Veo 3.1 enregistrée ({int(time.time() - t0)}s) : {output_mp4}")

def package_state_mascot(m_key, state_id, video_src):
    m_dir = f"assets/{state_id}" if m_key == "aituko" else f"mascots/{m_key}/assets/{state_id}"
    os.makedirs(m_dir, exist_ok=True)
    
    tmp_raw = f"{m_dir}/_tmp_raw"
    tmp_clean = f"{m_dir}/_tmp_clean"
    os.makedirs(tmp_raw, exist_ok=True)
    os.makedirs(tmp_clean, exist_ok=True)
    
    # 1. Extract frames 24fps
    subprocess.run([
        "ffmpeg", "-y", "-i", video_src,
        "-vf", "fps=24", f"{tmp_raw}/f_%03d.png"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    raw_files = sorted(glob.glob(f"{tmp_raw}/f_*.png"))
    if not raw_files:
        raise RuntimeError(f"Extraction de frames échouée pour {m_key} {state_id}")
        
    clean_frames = []
    for idx, rf in enumerate(raw_files):
        im = Image.open(rf)
        w, h = im.size
        if w != h:
            left = (w - h) // 2
            im = im.crop((left, 0, left + h, h))
        clean = key_greenscreen_master(im)
        clean_frames.append(clean)
        clean.save(f"{tmp_clean}/f_{idx+1:03d}.png", "PNG")
        
    # 2. Static PNG (Frame 0 or 24)
    mid_idx = min(24, len(clean_frames) - 1)
    clean_frames[mid_idx].save(f"{m_dir}/static.png", "PNG")
    clean_frames[mid_idx].save(f"{m_dir}/static.webp", "WEBP", quality=92)
    
    # 3. Animated WebP (PIL Native 100% Alpha)
    clean_frames[0].save(
        f"{m_dir}/animated.webp",
        format="WEBP",
        save_all=True,
        append_images=clean_frames[1:],
        duration=int(1000 / 24),
        loop=0,
        quality=88,
        method=4
    )
    
    # 4. Animated GIF (ffmpeg palettegen transparent)
    gif_path = f"{m_dir}/animated.gif"
    subprocess.run([
        "ffmpeg", "-y", "-framerate", "24", "-i", f"{tmp_clean}/f_%03d.png",
        "-lavfi", "split[s0][s1];[s0]palettegen=reserve_transparent=on:transparency_color=ffffff[p];[s1][p]paletteuse=alpha_threshold=128",
        "-loop", "0", gif_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 5. Animated PNG (APNG)
    clean_frames[0].save(
        f"{m_dir}/animated.png",
        format="PNG",
        save_all=True,
        append_images=clean_frames[1:],
        duration=int(1000 / 24),
        loop=0
    )
    
    # 6. Looped video MP4
    looped_mp4 = f"{m_dir}/looped_video.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-t", "2.0", "-i", video_src,
        "-filter_complex", "[0:v]split[v1][v2];[v2]reverse[v2rev];[v1][v2rev]concat=n=2:v=1[v]",
        "-map", "[v]", "-r", "24", "-c:v", "libx264", "-pix_fmt", "yuv420p", looped_mp4
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 7. Code snippets JSON
    snippet_data = {
        "mascot": m_key,
        "state": state_id,
        "react": f'<{m_key.capitalize()} state="{state_id}" size={{180}} animated />',
        "vue": f'<UkoMascot name="{m_key}" state="{state_id}" :size="180" :animated="true" />',
        "flutter": f'{m_key.capitalize()}Mascot(state: {m_key.capitalize()}State.{state_id}, size: 180.0)',
        "html": f'<img src="assets/{state_id}/animated.webp" width="180" height="180" alt="{m_key.capitalize()}" />'
    }
    with open(f"{m_dir}/snippet.json", "w") as f:
        json.dump(snippet_data, f, indent=2)
        
    # 8. ZIP Bundle
    zip_path = f"{m_dir}/bundle_{m_key}_{state_id}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for item in ["static.png", "static.webp", "animated.gif", "animated.webp", "animated.png", "looped_video.mp4", "snippet.json"]:
            p_item = f"{m_dir}/{item}"
            if os.path.exists(p_item):
                zipf.write(p_item, arcname=f"{m_key}_{state_id}/{item}")
                
    # Clean temp
    for f in glob.glob(f"{tmp_raw}/*"): os.remove(f)
    for f in glob.glob(f"{tmp_clean}/*"): os.remove(f)
    os.rmdir(tmp_raw)
    os.rmdir(tmp_clean)
    
    # Verification
    test_w = Image.open(f"{m_dir}/animated.webp")
    arr_w = np.array(test_w.convert("RGBA"))
    assert arr_w[10, 10, 3] == 0, f"Alpha failure at corner in {m_dir}/animated.webp"
    print(f"   ✨ {m_key.upper()} ({state_id}): Validé & Certifié 100% Alpha Transparent !")

def run_state(state_id):
    cfg = STATE_PROMPTS[state_id]
    title = cfg["title"]
    print(f"\n=================================================================")
    print(f"🚀 PRODUCTION INTÉGRALE : {state_id.upper()} ({title})")
    print(f"=================================================================")
    
    mascots = ["aituko", "owluko", "luneko", "usako", "inuko", "hatoko"]
    
    for m in mascots:
        m_dir = f"assets/{state_id}" if m == "aituko" else f"mascots/{m}/assets/{state_id}"
        os.makedirs(m_dir, exist_ok=True)
        raw_video = f"{m_dir}/source_video.mp4"
        
        prompt = cfg[m]
        print(f"\n🌟 Mascotte: {m.upper()}...")
        generate_video_veo(m, prompt, raw_video)
        package_state_mascot(m, state_id, raw_video)
        
    # Synchronize aituko
    subprocess.run(["cp", "-rf", f"assets/{state_id}", f"mascots/aituko/assets/{state_id}"])
    # Synchronize dist_vercel
    subprocess.run(["cp", "-rf", "assets", "dist_vercel/"])
    subprocess.run(["cp", "-rf", "mascots", "dist_vercel/"])
    
    # Run test suite
    res = subprocess.run(["python3", "tests/test_mascot_system_integrity.py", state_id], capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        raise RuntimeError(f"Échec des tests d'intégrité pour {state_id}")
    print(f"🎉 ÉTAT {state_id.upper()} COMPLÈTEMENT VALIDÉ (48/48 TESTS RÉUSSIS) !")

if __name__ == "__main__":
    target_state = sys.argv[1] if len(sys.argv) > 1 else None
    if target_state:
        run_state(target_state)
    else:
        for st in sorted(STATE_PROMPTS.keys()):
            run_state(st)
