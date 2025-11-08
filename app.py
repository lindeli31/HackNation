"""
Photo-to-Video AI - VEO 2 VERSION
Genera VIDEO VERI animati usando Veo 2 da Vertex AI

IMPORTANTE: Questa versione usa Veo 2 per generare video animati reali!
"""

import os
import json
import time
from pathlib import Path
from typing import List, Dict, Optional
import tempfile

import streamlit as st
from PIL import Image
import numpy as np

# Google AI
import google.generativeai as genai

# Vertex AI per Veo 2
try:
    from google.cloud import aiplatform
    from google.cloud.aiplatform import gapic
    VERTEX_AVAILABLE = True
except ImportError:
    VERTEX_AVAILABLE = False
    st.warning("⚠️ google-cloud-aiplatform non installato. Aggiungi a requirements.txt")

# ============================================================================
# CONFIGURAZIONE
# ============================================================================

# API Keys
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    GCP_PROJECT_ID = st.secrets.get("GCP_PROJECT_ID", "")
    GCP_LOCATION = st.secrets.get("GCP_LOCATION", "us-central1")
except:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID', '')
    GCP_LOCATION = os.getenv('GCP_LOCATION', 'us-central1')

# Folders
UPLOAD_FOLDER = Path(tempfile.gettempdir()) / "photo_video_uploads"
OUTPUT_FOLDER = Path(tempfile.gettempdir()) / "photo_video_outputs"
TEMP_FOLDER = Path(tempfile.gettempdir()) / "photo_video_temp"

for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER, TEMP_FOLDER]:
    folder.mkdir(exist_ok=True, parents=True)

# Video settings
MIN_PHOTOS = 3
MAX_PHOTOS = 8  # Veo 2 può usare più foto per storia più ricca
CLIP_DURATION = 5  # Veo 2 genera 5 secondi
VIDEO_FPS = 24

STYLE_PRESETS = {
    "Cinematic Adventure": "Epic cinematic adventure with dramatic camera movements and heroic atmosphere",
    "Dreamy Memories": "Soft dreamy memories with gentle movements and nostalgic warm atmosphere",
    "Urban Journey": "Modern urban exploration with dynamic street energy and city vibes",
    "Nature Documentary": "Natural documentary style with serene landscapes and organic flow",
    "Artistic Story": "Creative artistic narrative with bold experimental visual storytelling"
}

# ============================================================================
# SETUP APIs
# ============================================================================

def setup_gemini_api():
    """Setup Gemini per storyboarding."""
    if not GEMINI_API_KEY:
        st.error("❌ GEMINI_API_KEY mancante!")
        return False
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        return True
    except Exception as e:
        st.error(f"❌ Gemini error: {e}")
        return False

def setup_vertex_ai():
    """Setup Vertex AI per Veo 2."""
    if not GCP_PROJECT_ID:
        st.error("❌ GCP_PROJECT_ID mancante! Serve per Veo 2")
        st.info("Aggiungi a secrets.toml: GCP_PROJECT_ID = 'your-project-id'")
        return False

    if not VERTEX_AVAILABLE:
        st.error("❌ google-cloud-aiplatform non installato")
        return False

    try:
        aiplatform.init(project=GCP_PROJECT_ID, location=GCP_LOCATION)
        st.success(f"✅ Vertex AI setup: {GCP_PROJECT_ID} @ {GCP_LOCATION}")
        return True
    except Exception as e:
        st.error(f"❌ Vertex AI error: {e}")
        return False

def save_uploaded_file(uploaded_file, save_path: Path) -> bool:
    """Salva file uploadato."""
    try:
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return True
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return False

# ============================================================================
# STEP 1: STORIA con Gemini (descrizione narrativa lunga)
# ============================================================================

def create_story_from_photos(photo_paths: List[Path], style: str) -> Dict:
    """
    Usa Gemini per creare una STORIA NARRATIVA dalle foto.

    Non solo storyboard tecnico, ma vera storia con:
    - Descrizione dettagliata di ogni scena
    - Connessioni narrative tra le foto
    - Prompts ricchi per Veo 2
    """
    try:
        st.info("📖 Gemini sta creando la tua storia...")

        model = genai.GenerativeModel('gemini-2.5-pro')

        prompt = f"""Sei uno storyteller cinematografico. Analizza queste {len(photo_paths)} foto e crea una STORIA NARRATIVA coinvolgente.

Stile: {style}
Descrizione stile: {STYLE_PRESETS.get(style, style)}

Per ogni foto, crea:
1. **Descrizione scena dettagliata** (3-4 frasi): Cosa succede, atmosfera, emozioni
2. **Video prompt ricco** per AI video generation: Descrivi movimenti camera, azione, dettagli visivi
3. **Connessione narrativa** con scena precedente/successiva

Crea una storia che LEGA tutte le foto in un video continuo e fluido.

Return ONLY valid JSON:
{{
    "title": "Titolo creativo del video",
    "story_summary": "Riassunto storia completa in 2-3 frasi",
    "narrative_arc": "Tipo di arco narrativo (e.g., 'journey', 'transformation', 'discovery')",
    "scenes": [
        {{
            "photo_index": 0,
            "scene_title": "Titolo scena",
            "description": "Descrizione dettagliata cosa succede in questa scena (3-4 frasi)",
            "veo_prompt": "Prompt DETTAGLIATO per Veo 2 video generation - include: azione, movimento camera, atmosfera, dettagli visivi, stile cinematografico. Min 20 parole.",
            "camera_movement": "Tipo movimento (dolly, pan, tilt, zoom, orbit)",
            "duration": {CLIP_DURATION},
            "transition_to_next": "Come questa scena si collega alla prossima"
        }}
    ],
    "final_message": "Messaggio/emozione finale del video"
}}

IMPORTANTE:
- Veo prompts devono essere MOLTO DETTAGLIATI (20+ parole)
- Includi sempre: movimento camera, azione, atmosfera
- Usa linguaggio cinematografico
"""

        # Carica foto per Gemini
        images = []
        for photo_path in photo_paths:
            img = Image.open(photo_path)
            img.thumbnail((1024, 1024))
            images.append(img)

        # Chiamata Gemini
        with st.spinner("🤖 Gemini sta analizzando le foto e creando la storia..."):
            response = model.generate_content([prompt] + images)

        response_text = response.text

        # Parse JSON
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]

        story = json.loads(response_text.strip())

        st.success(f"✅ Storia creata: '{story.get('title', 'Untitled')}'")

        return story

    except json.JSONDecodeError as e:
        st.error(f"❌ JSON parse error: {e}")
        st.code(response_text[:500])
        return create_fallback_story(photo_paths, style)
    except Exception as e:
        st.error(f"❌ Story generation error: {e}")
        return create_fallback_story(photo_paths, style)

def create_fallback_story(photo_paths: List[Path], style: str) -> Dict:
    """Fallback story se Gemini fallisce."""
    scenes = []

    for i, photo_path in enumerate(photo_paths):
        scenes.append({
            "photo_index": i,
            "scene_title": f"Scene {i+1}",
            "description": f"A {style.lower()} scene captured in this moment",
            "veo_prompt": f"Cinematic {style.lower()} scene with smooth camera movement, professional cinematography, high quality, dramatic lighting",
            "camera_movement": "dolly forward",
            "duration": CLIP_DURATION,
            "transition_to_next": "Flows naturally into next scene"
        })

    return {
        "title": f"My {style} Story",
        "story_summary": f"A {style.lower()} journey through captured moments",
        "narrative_arc": "journey",
        "scenes": scenes,
        "final_message": "A memorable journey"
    }

# ============================================================================
# STEP 2: VIDEO GENERATION con Veo 2
# ============================================================================

def generate_video_with_veo2(photo_path: Path, scene: Dict, style: str) -> Optional[Path]:
    """
    Genera VIDEO ANIMATO usando Veo 2 da Vertex AI.

    Veo 2 genera video veri con movimento, non foto statiche!

    Args:
        photo_path: Foto di riferimento
        scene: Dati scena con veo_prompt
        style: Stile video

    Returns:
        Path al video generato (MP4)
    """
    try:
        st.info(f"🎥 Veo 2 sta generando video per: {scene['scene_title']}")

        # Prepara prompt per Veo 2
        veo_prompt = scene.get('veo_prompt', scene.get('description', ''))

        # Arricchisci prompt con stile
        full_prompt = f"{veo_prompt}. Style: {STYLE_PRESETS.get(style, style)}. Cinematic quality, smooth motion, {scene.get('camera_movement', 'slow movement')}"

        st.write(f"📝 Prompt Veo: {full_prompt[:100]}...")

        # Carica immagine di riferimento
        with open(photo_path, "rb") as f:
            image_bytes = f.read()

        # CHIAMA VEO 2 API via Vertex AI
        # Documentazione: https://cloud.google.com/vertex-ai/docs/generative-ai/video/generate-videos

        client = aiplatform.gapic.PredictionServiceClient(
            client_options={"api_endpoint": f"{GCP_LOCATION}-aiplatform.googleapis.com"}
        )

        # Endpoint Veo 2
        endpoint = f"projects/{GCP_PROJECT_ID}/locations/{GCP_LOCATION}/publishers/google/models/veo-2"

        # Prepara richiesta
        import base64
        image_b64 = base64.b64encode(image_bytes).decode('utf-8')

        instances = [{
            "prompt": full_prompt,
            "reference_image": {
                "bytesBase64Encoded": image_b64
            },
            "parameters": {
                "duration": f"{CLIP_DURATION}s",
                "aspectRatio": "16:9",
                "fps": VIDEO_FPS
            }
        }]

        # Esegui predizione
        with st.spinner(f"⏳ Veo 2 sta generando video... (~30-60s)"):
            response = client.predict(
                endpoint=endpoint,
                instances=instances
            )

        # Estrai video generato
        if response.predictions:
            prediction = response.predictions[0]

            # Veo ritorna video in base64
            video_b64 = prediction.get('videoBase64', '')
            if video_b64:
                video_bytes = base64.b64decode(video_b64)

                # Salva video
                output_path = TEMP_FOLDER / f"veo_clip_{int(time.time())}_{scene['photo_index']}.mp4"
                with open(output_path, "wb") as f:
                    f.write(video_bytes)

                st.success(f"✅ Video generato: {output_path.name} ({len(video_bytes) / 1024 / 1024:.1f} MB)")
                return output_path
            else:
                st.error("❌ Veo non ha ritornato video")
                return None
        else:
            st.error("❌ Nessuna prediction da Veo")
            return None

    except Exception as e:
        st.error(f"❌ Veo 2 generation failed: {e}")
        st.info("💡 Possibili cause: Quota API, Veo non abilitato, credenziali errate")

        # Fallback: crea clip semplice con FFmpeg
        return create_simple_clip_ffmpeg(photo_path, scene)

def create_simple_clip_ffmpeg(photo_path: Path, scene: Dict) -> Optional[Path]:
    """Fallback: clip semplice con FFmpeg se Veo fallisce."""
    try:
        import subprocess

        st.warning("⚠️ Usando FFmpeg fallback (foto statica)")

        output_path = TEMP_FOLDER / f"clip_{int(time.time())}_{scene['photo_index']}.mp4"

        # FFmpeg: foto → video con zoom
        cmd = [
            'ffmpeg', '-y',
            '-loop', '1',
            '-i', str(photo_path),
            '-vf', f'scale=1280:720,zoompan=z=\'min(zoom+0.0015,1.5)\':d={CLIP_DURATION * VIDEO_FPS}:s=1280x720',
            '-t', str(scene['duration']),
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-r', str(VIDEO_FPS),
            str(output_path)
        ]

        subprocess.run(cmd, capture_output=True, check=True, timeout=60)

        if output_path.exists():
            return output_path
        return None

    except Exception as e:
        st.error(f"❌ FFmpeg fallback failed: {e}")
        return None

# ============================================================================
# STEP 3: MERGE VIDEO
# ============================================================================

def merge_videos_ffmpeg(video_paths: List[Path], story: Dict) -> Optional[Path]:
    """Merge tutti i clip in video continuo."""
    try:
        import subprocess

        st.info("🎬 Merging video clips in video continuo...")

        # Filtra clip validi
        valid_clips = [p for p in video_paths if p and p.exists()]

        if not valid_clips:
            st.error("❌ Nessun clip da mergare")
            return None

        # Crea concat list
        concat_file = TEMP_FOLDER / "concat.txt"
        with open(concat_file, "w") as f:
            for clip in valid_clips:
                f.write(f"file '{clip.absolute()}'\n")

        # Output
        title_safe = story.get('title', 'video').replace(' ', '_')[:30]
        output_path = OUTPUT_FOLDER / f"{title_safe}_{int(time.time())}.mp4"

        # Merge con crossfade
        cmd = [
            'ffmpeg', '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', str(concat_file),
            '-c', 'copy',
            str(output_path)
        ]

        with st.spinner("⏳ Merging... (~30s)"):
            subprocess.run(cmd, capture_output=True, check=True, timeout=120)

        if output_path.exists():
            file_size = output_path.stat().st_size / 1024 / 1024
            st.success(f"✅ Video finale: {output_path.name} ({file_size:.1f} MB)")
            return output_path

        return None

    except Exception as e:
        st.error(f"❌ Merge failed: {e}")
        return None

# ============================================================================
# MAIN PIPELINE
# ============================================================================

def process_photos_to_video(photo_paths: List[Path], style: str) -> Optional[Path]:
    """Pipeline completa."""
    try:
        progress = st.progress(0)

        # Step 1: Storia
        st.header("📖 Step 1: Creazione Storia")
        progress.progress(0.1)

        story = create_story_from_photos(photo_paths, style)

        if not story or 'scenes' not in story:
            st.error("❌ Storia fallita")
            return None

        # Mostra storia
        st.subheader(f"🎬 {story['title']}")
        st.write(f"**Tema:** {story.get('story_summary', '')}")
        st.write(f"**Arco narrativo:** {story.get('narrative_arc', 'journey')}")

        with st.expander("📋 Scene Dettagliate", expanded=True):
            for i, scene in enumerate(story['scenes']):
                st.markdown(f"""
**Scena {i+1}: {scene.get('scene_title', 'Untitled')}**

📝 **Descrizione:** {scene.get('description', 'N/A')}

🎥 **Camera:** {scene.get('camera_movement', 'N/A')}

🔗 **Transizione:** {scene.get('transition_to_next', 'N/A')}
                """)

        progress.progress(0.3)

        # Step 2: Video generation
        st.header("🎥 Step 2: Generazione Video con Veo 2")

        generated_videos = []

        for i, scene in enumerate(story['scenes']):
            photo_idx = scene.get('photo_index', i)

            if photo_idx >= len(photo_paths):
                photo_idx = i % len(photo_paths)

            photo_path = photo_paths[photo_idx]

            st.write(f"🎬 Generando scena {i+1}/{len(story['scenes'])}: {scene['scene_title']}")

            video_path = generate_video_with_veo2(photo_path, scene, style)

            if video_path:
                generated_videos.append(video_path)
                st.success(f"✅ Scena {i+1} completata")
            else:
                st.warning(f"⚠️ Scena {i+1} fallita - continuo")

            progress.progress(0.3 + (0.5 * (i+1) / len(story['scenes'])))

        if not generated_videos:
            st.error("❌ Nessun video generato")
            return None

        progress.progress(0.8)

        # Step 3: Merge
        st.header("🎬 Step 3: Creazione Video Finale")

        final_video = merge_videos_ffmpeg(generated_videos, story)

        progress.progress(1.0)

        return final_video

    except Exception as e:
        st.error(f"❌ Pipeline error: {e}")
        import traceback
        st.code(traceback.format_exc())
        return None

# ============================================================================
# STREAMLIT UI
# ============================================================================

def main():
    st.set_page_config(
        page_title="Photo to Video AI - Veo 2",
        page_icon="🎬",
        layout="wide"
    )

    st.title("🎬 Photo-to-Video AI - Powered by Veo 2")
    st.markdown("**Crea VIDEO ANIMATI da foto con AI! 🎥**")

    # Sidebar
    with st.sidebar:
        st.header("ℹ️ Info")
        st.write("""
        **Tecnologie:**
        - Gemini 2.5 Pro (storytelling)
        - Veo 2 (video generation)
        - FFmpeg (merging)

        **Requirements:**
        - Gemini API key
        - Google Cloud Project ID
        - Veo 2 abilitato su Vertex AI
        """)

        st.header("🔑 Status")

        if GEMINI_API_KEY:
            st.success("✅ Gemini OK")
        else:
            st.error("❌ Gemini key mancante")

        if GCP_PROJECT_ID:
            st.success(f"✅ GCP: {GCP_PROJECT_ID}")
        else:
            st.error("❌ GCP project mancante")

    # Setup
    if not setup_gemini_api():
        st.stop()

    if not setup_vertex_ai():
        st.warning("⚠️ Vertex AI non configurato - userò fallback FFmpeg")

    # Upload
    st.header("📸 Upload Photos")

    uploaded_files = st.file_uploader(
        f"Carica {MIN_PHOTOS}-{MAX_PHOTOS} foto (più foto = storia più ricca!)",
        type=['jpg', 'jpeg', 'png'],
        accept_multiple_files=True,
        help="Veo 2 può usare fino a 8 foto per creare storie complesse"
    )

    if uploaded_files:
        if len(uploaded_files) < MIN_PHOTOS:
            st.warning(f"⚠️ Almeno {MIN_PHOTOS} foto")
        elif len(uploaded_files) > MAX_PHOTOS:
            st.warning(f"⚠️ Max {MAX_PHOTOS} foto")
            uploaded_files = uploaded_files[:MAX_PHOTOS]
        else:
            st.success(f"✅ {len(uploaded_files)} foto - ottimo per storia ricca!")

    # Preview
    if uploaded_files:
        cols = st.columns(min(len(uploaded_files), 4))
        for idx, (col, file) in enumerate(zip(cols, uploaded_files)):
            with col:
                st.image(Image.open(file), caption=f"#{idx+1}", use_container_width=True)

    # Style
    st.header("🎨 Style")
    style = st.selectbox("Stile narrativo", list(STYLE_PRESETS.keys()))

    # Generate
    st.header("🚀 Generate")

    if st.button("✨ Crea Video con Veo 2! ✨", type="primary", use_container_width=True):

        if not uploaded_files or len(uploaded_files) < MIN_PHOTOS:
            st.error(f"❌ Carica almeno {MIN_PHOTOS} foto!")
            st.stop()

        # Save photos
        photo_paths = []
        session_id = int(time.time())

        for idx, file in enumerate(uploaded_files):
            save_path = UPLOAD_FOLDER / f"{session_id}_{idx}.jpg"
            if save_uploaded_file(file, save_path):
                photo_paths.append(save_path)

        if not photo_paths:
            st.error("❌ Errore salvataggio")
            st.stop()

        # Process
        st.balloons()

        with st.spinner("🎬 Generando video con Veo 2... (5-10 minuti)"):
            final_video = process_photos_to_video(photo_paths, style)

        # Result
        if final_video and final_video.exists():
            st.success("🎉 VIDEO PRONTO!")

            st.header("🎬 Il Tuo Video")

            # Player
            with open(final_video, "rb") as f:
                video_bytes = f.read()

            st.video(video_bytes)

            # Download
            st.download_button(
                label="📥 Scarica MP4",
                data=video_bytes,
                file_name=final_video.name,
                mime="video/mp4",
                use_container_width=True
            )

            st.balloons()

        else:
            st.error("❌ Generazione fallita - controlla setup Veo 2")

    # Footer
    st.markdown("---")
    st.markdown("*Powered by Veo 2 + Gemini 2.5 Pro | HackNation 2025*")

if __name__ == "__main__":
    main()
