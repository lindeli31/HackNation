"""
Photo-to-Video AI Animation MVP - Cloud Version
Hackathon Project - Cinematic Video Generator

Versione ottimizzata per deployment su Streamlit Cloud
API: Gemini 2.5 Pro testata e funzionante!

Team: 4 Computer Engineers
"""

# ============================================================================
# IMPORTS
# ============================================================================

import os
import json
import time
import base64
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import tempfile

# Streamlit per web interface
import streamlit as st

# Immagini
from PIL import Image
import numpy as np

# Google Gemini AI
import google.generativeai as genai

# ============================================================================
# CONFIGURAZIONE
# ============================================================================

# API Key da Streamlit secrets (per cloud) o environment variable (locale)
# Nel cloud: .streamlit/secrets.toml
# In locale: export GEMINI_API_KEY="your-key"
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Cartelle (usa temp per cloud compatibility)
UPLOAD_FOLDER = Path(tempfile.gettempdir()) / "photo_video_uploads"
OUTPUT_FOLDER = Path(tempfile.gettempdir()) / "photo_video_outputs"
TEMP_FOLDER = Path(tempfile.gettempdir()) / "photo_video_temp"

# Crea cartelle se non esistono
for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER, TEMP_FOLDER]:
    folder.mkdir(exist_ok=True, parents=True)

# Impostazioni video
MIN_PHOTOS = 3
MAX_PHOTOS = 5
CLIP_DURATION = 8
QUALITY_THRESHOLD = 7  # Abbassato a 7 per MVP (8 era troppo strict)

# Stili disponibili
STYLE_PRESETS = {
    "Cinematic Adventure": "Epic cinematic style with dramatic camera movements, adventure theme, movie-like quality",
    "Dreamy Memories": "Soft, nostalgic atmosphere with gentle movements, warm colors, emotional storytelling",
    "Urban Exploration": "Modern urban vibes, street photography aesthetic, dynamic city energy",
    "Nature Journey": "Natural documentary style, serene landscapes, organic flowing movements",
    "Artistic Abstract": "Creative artistic interpretation, bold movements, experimental visual style"
}

# ============================================================================
# SETUP GEMINI API
# ============================================================================

def setup_gemini_api():
    """Inizializza Gemini API con la key."""
    if not GEMINI_API_KEY:
        st.error("❌ GEMINI_API_KEY non trovata!")
        st.info("In locale: export GEMINI_API_KEY='your-key'")
        st.info("Su Streamlit Cloud: aggiungi a .streamlit/secrets.toml")
        return False

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        return True
    except Exception as e:
        st.error(f"❌ Errore configurazione Gemini: {str(e)}")
        return False

# ============================================================================
# FUNZIONI UTILITY
# ============================================================================

def save_uploaded_file(uploaded_file, save_path: Path) -> bool:
    """Salva file uploadato da Streamlit."""
    try:
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return True
    except Exception as e:
        st.error(f"❌ Errore salvataggio {save_path.name}: {str(e)}")
        return False

# ============================================================================
# STEP 1: STORYBOARD CON GEMINI
# ============================================================================

def rank_and_storyboard_photos(photo_paths: List[Path], style: str) -> Dict:
    """
    Usa Gemini 2.5 Pro per analizzare le foto e creare uno storyboard.

    Input: Lista di foto + stile
    Output: JSON con title, theme, shots (sequenza di scene)
    """
    try:
        st.info("🎬 Gemini AI sta analizzando le tue foto...")

        # Usa Gemini 2.5 Pro (testato e funzionante!)
        model = genai.GenerativeModel('gemini-2.5-pro')

        # Prompt per generare lo storyboard
        prompt = f"""You are a professional cinematographer. Analyze these {len(photo_paths)} photos and create a cinematic storyboard.

Style: {style}
Description: {STYLE_PRESETS.get(style, style)}

Create a narrative connecting these photos with {len(photo_paths)} shots (8 seconds each).

Return ONLY this JSON structure (no markdown, no extra text):
{{
    "title": "Creative video title",
    "theme": "One sentence describing the narrative",
    "shots": [
        {{
            "photo_index": 0,
            "caption": "Vivid description of this shot",
            "motion": "Camera movement (e.g., 'slow dolly zoom in', 'pan right', 'parallax effect')",
            "duration": 8,
            "mood": "Mood of the shot"
        }}
    ]
}}

Important: Return ONLY valid JSON."""

        # Carica le immagini
        image_parts = []
        for photo_path in photo_paths:
            img = Image.open(photo_path)
            img.thumbnail((1024, 1024))  # Ridimensiona per risparmiare quota API
            image_parts.append(img)

        # Chiamata a Gemini con immagini
        full_prompt = [prompt] + image_parts

        with st.spinner("🤖 Gemini sta creando lo storyboard..."):
            response = model.generate_content(full_prompt)

        # Parsing JSON
        response_text = response.text

        # Rimuovi markdown se presente
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]

        storyboard = json.loads(response_text.strip())

        st.success(f"✅ Storyboard creato: '{storyboard.get('title', 'Untitled')}'")

        return storyboard

    except json.JSONDecodeError as e:
        st.error(f"❌ Errore parsing JSON: {str(e)}")
        st.code(response_text)
        return create_fallback_storyboard(photo_paths, style)

    except Exception as e:
        st.error(f"❌ Errore storyboard: {str(e)}")
        return create_fallback_storyboard(photo_paths, style)

def create_fallback_storyboard(photo_paths: List[Path], style: str) -> Dict:
    """Storyboard di fallback se Gemini fallisce."""
    shots = []
    for i, photo_path in enumerate(photo_paths):
        shots.append({
            "photo_index": i,
            "caption": f"Scene {i+1} - {photo_path.stem}",
            "motion": "slow pan right" if i % 2 == 0 else "slow zoom in",
            "duration": 8,
            "mood": style
        })

    return {
        "title": f"My {style} Story",
        "theme": f"A {style.lower()} journey through memories",
        "shots": shots
    }

# ============================================================================
# STEP 2: SIMULAZIONE VIDEO GENERATION
# ============================================================================

def generate_video_clip_simulation(photo_path: Path, shot_info: Dict) -> Optional[Path]:
    """
    VERSIONE MVP SEMPLIFICATA:
    Per l'hackathon, simuliamo la generazione video.

    In produzione, qui useresti:
    - Veo 3 API (quando disponibile)
    - AnimateDiff (richiede GPU e tempo)
    - Runway ML API
    - Stable Video Diffusion

    Per ora: mostriamo le foto con le info dello storyboard.
    """
    try:
        st.info(f"🎥 Clip per: {shot_info.get('caption', 'Scene')[:50]}...")

        # Simula processing
        time.sleep(1)

        # In una versione completa, qui genereresti il video
        # Per MVP, torniamo il path della foto originale
        # L'importante è che lo storyboard funzioni!

        st.success(f"✅ Clip simulata: {photo_path.name}")

        return photo_path  # Ritorna foto originale per MVP

    except Exception as e:
        st.error(f"❌ Errore generazione clip: {str(e)}")
        return None

# ============================================================================
# STEP 3: QUALITY CHECK CON GEMINI VISION
# ============================================================================

def quality_check_image(image_path: Path, expected_style: str) -> Tuple[int, str]:
    """
    Usa Gemini Vision per valutare la qualità dell'immagine.

    Input: Immagine + stile atteso
    Output: Score 1-10 + feedback
    """
    try:
        st.info(f"🔍 Quality check su {image_path.name}...")

        model = genai.GenerativeModel('gemini-2.5-pro')

        # Carica immagine
        img = Image.open(image_path)

        prompt = f"""Analyze this image for video animation suitability.
Expected style: {expected_style}

Rate 1-10 based on:
1. Image quality and clarity
2. Composition for animation
3. Style match with {expected_style}

Return ONLY this JSON:
{{
    "score": 8,
    "feedback": "Brief explanation"
}}"""

        response = model.generate_content([prompt, img])
        response_text = response.text

        # Parse JSON
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]

        result = json.loads(response_text.strip())

        score = result.get("score", 7)
        feedback = result.get("feedback", "Quality check completed")

        st.success(f"✅ Score: {score}/10 - {feedback}")

        return score, feedback

    except Exception as e:
        st.warning(f"⚠️ Quality check fallito: {str(e)}")
        return 7, "Quality check unavailable"

# ============================================================================
# STEP 4: CREAZIONE PRESENTAZIONE FINALE
# ============================================================================

def create_final_presentation(storyboard: Dict, photo_paths: List[Path]) -> Dict:
    """
    Crea una presentazione delle foto con lo storyboard.

    Per MVP: mostriamo foto + storyboard invece di video completo.
    In produzione: qui faresti il merge video con FFmpeg.
    """
    try:
        st.info("🎬 Creando presentazione finale...")

        presentation = {
            "title": storyboard.get("title", "My Video"),
            "theme": storyboard.get("theme", ""),
            "shots": []
        }

        for shot in storyboard.get("shots", []):
            photo_idx = shot.get("photo_index", 0)
            if photo_idx < len(photo_paths):
                presentation["shots"].append({
                    "image": photo_paths[photo_idx],
                    "caption": shot.get("caption", ""),
                    "motion": shot.get("motion", ""),
                    "mood": shot.get("mood", "")
                })

        st.success("✅ Presentazione creata!")

        return presentation

    except Exception as e:
        st.error(f"❌ Errore creazione presentazione: {str(e)}")
        return None

# ============================================================================
# MAIN PIPELINE
# ============================================================================

def process_photos_to_video(photo_paths: List[Path], style: str, session_id: str) -> Optional[Dict]:
    """
    Pipeline principale (versione MVP semplificata per hackathon).

    Steps:
    1. Storyboard con Gemini 2.5 Pro ✅
    2. Quality check con Gemini Vision ✅
    3. Presentazione finale (invece di video per MVP) ✅

    In produzione aggiungerai:
    4. Video generation con Veo/AnimateDiff
    5. Video merging con FFmpeg
    """
    try:
        progress_bar = st.progress(0)
        status_text = st.empty()

        # STEP 1: Storyboard
        status_text.text("🎬 Step 1/3: Creazione storyboard...")
        progress_bar.progress(0.1)

        storyboard = rank_and_storyboard_photos(photo_paths, style)

        if not storyboard or 'shots' not in storyboard:
            st.error("❌ Fallimento storyboard")
            return None

        # Mostra storyboard
        st.subheader("📋 Storyboard Generato")
        st.write(f"**Titolo:** {storyboard.get('title', 'N/A')}")
        st.write(f"**Tema:** {storyboard.get('theme', 'N/A')}")

        with st.expander("📖 Dettagli Scene", expanded=True):
            for i, shot in enumerate(storyboard['shots']):
                st.markdown(f"""
**Scena {i+1}:**
- 📝 {shot.get('caption', 'N/A')}
- 🎥 Motion: {shot.get('motion', 'N/A')}
- 🎭 Mood: {shot.get('mood', 'N/A')}
                """)

        progress_bar.progress(0.4)

        # STEP 2: Quality checks
        status_text.text("🔍 Step 2/3: Quality check...")

        quality_scores = []
        for i, photo_path in enumerate(photo_paths):
            score, feedback = quality_check_image(photo_path, style)
            quality_scores.append(score)

            progress_bar.progress(0.4 + (0.3 * (i+1) / len(photo_paths)))

        avg_score = sum(quality_scores) / len(quality_scores)
        st.info(f"📊 Quality media: {avg_score:.1f}/10")

        progress_bar.progress(0.7)

        # STEP 3: Presentazione finale
        status_text.text("🎨 Step 3/3: Creazione presentazione...")

        presentation = create_final_presentation(storyboard, photo_paths)

        progress_bar.progress(1.0)
        status_text.text("✅ Completato!")

        return presentation

    except Exception as e:
        st.error(f"❌ Errore pipeline: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
        return None

# ============================================================================
# STREAMLIT UI
# ============================================================================

def main():
    """Applicazione Streamlit principale."""

    # Configurazione pagina
    st.set_page_config(
        page_title="Photo to Video AI",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Header
    st.title("🎬 Photo-to-Video AI Animation")
    st.markdown("**Transform your photos into cinematic stories with AI!**")

    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.write("""
        Questo progetto usa AI per trasformare foto in video:

        - 🤖 **Gemini 2.5 Pro** per storyboarding
        - 🔍 **Gemini Vision** per quality check
        - 🎨 AI-powered cinematography

        **Versione:** MVP per Hackathon
        **Team:** 4 Computer Engineers
        """)

        st.header("🔑 API Status")
        if GEMINI_API_KEY:
            st.success("✅ API Key caricata")
            st.info(f"Key: {GEMINI_API_KEY[:12]}...")
        else:
            st.error("❌ API Key mancante")
            st.code("Aggiungi a .streamlit/secrets.toml")

        st.header("⚙️ Settings")
        st.info(f"Foto: {MIN_PHOTOS}-{MAX_PHOTOS}")
        st.info(f"Durata clip: {CLIP_DURATION}s")
        st.info(f"Quality threshold: {QUALITY_THRESHOLD}/10")

    # Setup API
    if not setup_gemini_api():
        st.stop()

    # Upload foto
    st.header("📸 Upload Your Photos")

    uploaded_files = st.file_uploader(
        f"Carica {MIN_PHOTOS}-{MAX_PHOTOS} foto",
        type=['jpg', 'jpeg', 'png', 'webp'],
        accept_multiple_files=True,
        help="Foto di alta qualità per risultati migliori"
    )

    # Validazione
    if uploaded_files:
        if len(uploaded_files) < MIN_PHOTOS:
            st.warning(f"⚠️ Carica almeno {MIN_PHOTOS} foto (hai: {len(uploaded_files)})")
        elif len(uploaded_files) > MAX_PHOTOS:
            st.warning(f"⚠️ Massimo {MAX_PHOTOS} foto (hai: {len(uploaded_files)})")
            uploaded_files = uploaded_files[:MAX_PHOTOS]
        else:
            st.success(f"✅ {len(uploaded_files)} foto pronte!")

    # Preview
    if uploaded_files:
        st.subheader("👀 Preview")
        cols = st.columns(min(len(uploaded_files), 5))
        for idx, (col, file) in enumerate(zip(cols, uploaded_files)):
            with col:
                img = Image.open(file)
                st.image(img, caption=f"Foto {idx+1}", use_container_width=True)

    # Selezione stile
    st.header("🎨 Choose Your Style")

    style = st.selectbox(
        "Stile Video",
        options=list(STYLE_PRESETS.keys()),
        help="Scegli lo stile cinematografico"
    )

    if style:
        st.info(f"**{style}:** {STYLE_PRESETS[style]}")

    # Bottone genera
    st.header("🚀 Generate")

    if st.button("✨ Crea il Mio Video! ✨", type="primary", use_container_width=True):

        if not uploaded_files:
            st.error("❌ Carica prima le foto!")
            st.stop()

        if len(uploaded_files) < MIN_PHOTOS or len(uploaded_files) > MAX_PHOTOS:
            st.error(f"❌ Serve {MIN_PHOTOS}-{MAX_PHOTOS} foto")
            st.stop()

        # Salva foto
        st.info("💾 Salvando le foto...")
        photo_paths = []
        session_id = f"session_{int(time.time())}"

        for idx, file in enumerate(uploaded_files):
            save_path = UPLOAD_FOLDER / f"{session_id}_photo_{idx}_{file.name}"
            if save_uploaded_file(file, save_path):
                photo_paths.append(save_path)

        if len(photo_paths) != len(uploaded_files):
            st.error("❌ Errore salvataggio foto")
            st.stop()

        # Messaggio entusiasta!
        st.balloons()
        st.success("🎥 Trasformiamo i tuoi ricordi in un film!")

        # Esegui pipeline
        with st.spinner("🎬 AI al lavoro..."):
            presentation = process_photos_to_video(photo_paths, style, session_id)

        # Mostra risultato
        if presentation:
            st.success("🎉 La tua presentazione è pronta!")

            st.header("🎬 Risultato Finale")

            st.subheader(f"🎭 {presentation['title']}")
            st.write(f"*{presentation['theme']}*")

            st.markdown("---")

            # Mostra ogni scena
            for i, shot in enumerate(presentation['shots']):
                st.subheader(f"Scena {i+1}")

                col1, col2 = st.columns([1, 1])

                with col1:
                    img = Image.open(shot['image'])
                    st.image(img, use_container_width=True)

                with col2:
                    st.markdown(f"""
**📝 Descrizione:**
{shot['caption']}

**🎥 Camera Motion:**
{shot['motion']}

**🎭 Mood:**
{shot['mood']}

**⏱️ Durata:** {CLIP_DURATION} secondi
                    """)

                st.markdown("---")

            # Note per produzione
            st.info("""
💡 **Versione MVP:** Questa è una presentazione dello storyboard.

**Prossimi step per produzione:**
- Generazione video con Veo 3 / AnimateDiff
- Animazioni depth-aware con MiDaS
- Video merging con FFmpeg
- Export MP4 scaricabile
            """)

            st.balloons()

        else:
            st.error("❌ Errore generazione. Controlla i log sopra.")

    # Footer
    st.markdown("---")
    st.markdown("""
<div style='text-align: center'>
    <p>Made with ❤️ for HackNation 2025 | Powered by Gemini 2.5 Pro</p>
    <p><small>MVP Version - Storyboard Generation Demo</small></p>
</div>
    """, unsafe_allow_html=True)

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
