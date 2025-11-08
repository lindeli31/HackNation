# ⚡ QUICK START - 15 Minuti al Deploy!

**Obiettivo:** App live su internet in 15 minuti!

---

## ✅ Hai Bisogno Di:

- [ ] Account GitHub (gratuito)
- [ ] Account Streamlit Cloud (gratuito - login con GitHub)
- [ ] API Key Gemini: `AIzaSyBaB1f1Zf05yIwK3UOMLUTAlsYrjaKFVvw`

---

## 🚀 3 Steps Deployment

### Step 1: Push su GitHub (5 min)

```bash
# Nella cartella hacknation/
cd /home/deli/Projects/HackNation/hacknation

git init
git add .
git commit -m "Initial commit"

# Crea repo su github.com (chiamalo "photo-to-video-ai")
# Poi:
git remote add origin https://github.com/TUO-USERNAME/photo-to-video-ai.git
git push -u origin main
```

### Step 2: Deploy su Streamlit (5 min)

1. Vai su https://streamlit.io/cloud
2. Login con GitHub
3. Click "New app"
4. Seleziona repository: `photo-to-video-ai`
5. Main file: `app.py`
6. **Advanced settings** → **Secrets:**
   ```toml
   GEMINI_API_KEY = "AIzaSyBaB1f1Zf05yIwK3UOMLUTAlsYrjaKFVvw"
   ```
7. Click "Deploy!"

### Step 3: Test (5 min)

1. Aspetta che app si avvii (2-3 min)
2. Apri l'URL (tipo: `https://photo-video-ai.streamlit.app`)
3. Upload 3 foto di test
4. Select "Cinematic Adventure"
5. Click "Crea!"
6. ✅ Funziona!

---

## 🎯 Quick Test Locale (Opzionale)

Se vuoi testare prima del deploy:

```bash
# Installa dipendenze
pip install streamlit google-generativeai Pillow numpy

# Set API key
export GEMINI_API_KEY="AIzaSyBaB1f1Zf05yIwK3UOMLUTAlsYrjaKFVvw"

# Run
streamlit run app.py

# Apri http://localhost:8501
```

---

## 🐛 Problemi Comuni

### "Repository not found"
→ Verifica di aver fatto `git push` correttamente

### "GEMINI_API_KEY not found"
→ Controlla Secrets in Streamlit Cloud settings

### App non si carica
→ Guarda logs in Streamlit Cloud dashboard
→ Verifica requirements.txt sia nel repo

---

## 📱 Condividi la Tua App

Dopo deployment, ottieni URL tipo:
`https://your-app-name.streamlit.app`

Condividi con:
- Team members
- Giudici hackathon
- Social media
- Portfolio

---

## 💡 Tips

- **Nome app descrittivo:** `photo-video-hacknation` meglio di `app123`
- **Test con foto vere:** Risultati migliori con foto di qualità
- **Prova tutti gli stili:** Ogni stile genera narrative diverse
- **Salva screenshot:** Per presentazione/portfolio

---

## 🎬 Demo Photos

Scarica foto di test da:
- https://unsplash.com
- https://pexels.com
- https://pixabay.com

Cerca: "landscape", "travel", "urban", "nature"

---

## ✅ Checklist Successo

- [ ] App deployata e raggiungibile
- [ ] Upload foto funziona
- [ ] Storyboard generato
- [ ] Nessun errore rosso
- [ ] Sidebar mostra "✅ API Key caricata"

---

**FATTO! Ora hai un'app AI live su internet! 🎉**

Per dettagli completi → [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

*Tempo totale: ~15 minuti*
*Costo: $0 (tutto free tier!)*
