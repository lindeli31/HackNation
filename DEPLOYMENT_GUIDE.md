# 🚀 Guida al Deployment - Photo-to-Video AI

**Per Team di 4 Persone - Dividi il Lavoro!**

---

## ✅ Prerequisiti

- [ ] Account GitHub (gratuito)
- [ ] Account Streamlit Cloud (gratuito)
- [ ] API Key Gemini funzionante: `AIzaSyBaB1f1Zf05yIwK3UOMLUTAlsYrjaKFVvw`
- [ ] 30 minuti di tempo

---

## 👥 DIVISIONE DEL LAVORO (4 Persone)

### **Persona 1: GitHub Setup** ⏱️ 10 minuti
Responsabile: Push del codice su GitHub

### **Persona 2: Streamlit Cloud Setup** ⏱️ 10 minuti
Responsabile: Configurazione deployment

### **Persona 3: Testing & QA** ⏱️ 15 minuti
Responsabile: Test dell'app deployata

### **Persona 4: Documentazione Demo** ⏱️ 20 minuti
Responsabile: Preparazione materiale per presentazione

---

## 📋 TASK PERSONA 1: GitHub Setup

### Step 1.1: Crea Repository GitHub

```bash
# Nel terminale, nella cartella hacknation/
cd /home/deli/Projects/HackNation/hacknation

# Inizializza git
git init

# Aggiungi tutti i file
git add .

# Primo commit
git commit -m "Initial commit - Photo to Video AI MVP"
```

### Step 1.2: Crea Repo su GitHub

1. Vai su https://github.com
2. Click su "New repository" (bottone verde)
3. Nome: `photo-to-video-ai`
4. Descrizione: `AI-powered photo to video animation for HackNation 2025`
5. **Pubblico** (per Streamlit Cloud free tier)
6. **NON** aggiungere README, .gitignore, license (già presenti)
7. Click "Create repository"

### Step 1.3: Push del Codice

```bash
# Collega al repo remoto (sostituisci YOUR-USERNAME)
git remote add origin https://github.com/YOUR-USERNAME/photo-to-video-ai.git

# Push
git branch -M main
git push -u origin main
```

### Step 1.4: Verifica

- [ ] Vai su https://github.com/YOUR-USERNAME/photo-to-video-ai
- [ ] Vedi tutti i file: `app.py`, `requirements.txt`, `.gitignore`
- [ ] ⚠️ **IMPORTANTE:** `.streamlit/secrets.toml` NON deve essere visibile (è in .gitignore)

✅ **Checkpoint:** Repository pronto! Passa URL a Persona 2.

---

## 📋 TASK PERSONA 2: Streamlit Cloud Deployment

### Step 2.1: Crea Account Streamlit Cloud

1. Vai su https://streamlit.io/cloud
2. Click "Sign up" o "Get started"
3. **Sign in with GitHub** (consigliato)
4. Autorizza Streamlit ad accedere a GitHub

### Step 2.2: Crea Nuova App

1. Click "New app" (in alto a destra)
2. **Repository:** Seleziona `YOUR-USERNAME/photo-to-video-ai`
3. **Branch:** `main`
4. **Main file path:** `app.py`
5. **App URL:** Scegli un nome (es: `photo-video-ai-hacknation`)
6. **NON cliccare Deploy ancora!**

### Step 2.3: Configura Secrets (IMPORTANTE!)

1. Click su "Advanced settings"
2. Nella sezione **Secrets**, incolla:

```toml
GEMINI_API_KEY = "AIzaSyBaB1f1Zf05yIwK3UOMLUTAlsYrjaKFVvw"
```

3. **Verifica** che l'API key sia corretta
4. Click "Save"

### Step 2.4: Deploy!

1. Click **"Deploy!"**
2. Aspetta 2-3 minuti (installazione dipendenze)
3. Guarda i logs in tempo reale

### Step 2.5: Verifica Deployment

- [ ] App si avvia senza errori
- [ ] Vedi la home page con titolo "🎬 Photo-to-Video AI Animation"
- [ ] Sidebar mostra "✅ API Key caricata"
- [ ] No errori rossi

✅ **Checkpoint:** App live! Copia URL e passa a Persona 3.

**URL sarà tipo:** `https://photo-video-ai-hacknation.streamlit.app`

---

## 📋 TASK PERSONA 3: Testing & Quality Assurance

### Step 3.1: Test Funzionalità Base

1. Apri l'app: `https://your-app.streamlit.app`
2. Verifica elementi UI:
   - [ ] Titolo visibile
   - [ ] File uploader presente
   - [ ] Dropdown stili funziona
   - [ ] Bottone "Crea" presente

### Step 3.2: Test Upload Foto

1. Prepara 3-5 foto di test (JPG/PNG)
   - Scarica da Unsplash.com se serve
   - Dimensione: almeno 1024x768
2. Upload le foto
3. Verifica:
   - [ ] Preview delle foto appare
   - [ ] Messaggio "✅ X foto pronte!"

### Step 3.3: Test Generazione Storyboard

1. Seleziona stile: "Cinematic Adventure"
2. Click "✨ Crea il Mio Video! ✨"
3. Aspetta 30-60 secondi
4. Verifica output:
   - [ ] Storyboard appare con titolo
   - [ ] Shots descritti (caption, motion, mood)
   - [ ] Quality check completato
   - [ ] Presentazione finale mostra foto + descrizioni

### Step 3.4: Test Stili Diversi

Ripeti test con:
- [ ] Dreamy Memories
- [ ] Urban Exploration
- [ ] Nature Journey

Verifica che ogni stile produca storyboard diversi.

### Step 3.5: Test Error Handling

1. Prova upload 1 sola foto → deve dare warning
2. Prova upload 10 foto → limita a 5
3. Prova senza foto → errore chiaro

### Step 3.6: Documenta Issues

Crea file `BUGS.md`:

```markdown
# Bug & Issues Found

## ✅ Funzionanti
- Upload foto OK
- Storyboard generation OK
- ...

## ❌ Da Fixare
- (se trovi problemi, lista qui)

## 💡 Miglioramenti
- (suggerimenti)
```

✅ **Checkpoint:** App testata! Passa report a Persona 4.

---

## 📋 TASK PERSONA 4: Preparazione Demo

### Step 4.1: Crea Slide Pitch (5 slide)

**Slide 1: Titolo**
```
🎬 Photo-to-Video AI
Trasforma foto in storie cinematografiche

Team: [I vostri nomi]
HackNation 2025
```

**Slide 2: Il Problema**
```
❌ Le foto sono statiche
❌ Servono skill di video editing
❌ Tempo e software costosi

✅ Soluzione: AI automatica!
```

**Slide 3: La Tecnologia**
```
🤖 Gemini 2.5 Pro - Storyboarding AI
🔍 Gemini Vision - Quality Check
🎨 AI Cinematography
📊 Cloud-native (Streamlit)
```

**Slide 4: Demo Live**
```
[Screenshot dell'app]
1. Upload 3-5 foto
2. Scegli stile
3. AI genera storyboard
```

**Slide 5: Roadmap**
```
✅ MVP: Storyboard generation
🚧 Next: Video generation (Veo 3)
🚧 Future: Editing, music, sharing
```

### Step 4.2: Prepara Demo Video (Backup)

Se live demo fallisce, registra:
1. **Screen recording** dell'app funzionante
2. Upload foto → generazione → risultato
3. Durata: 1-2 minuti
4. Tool: OBS Studio / Kazam / QuickTime

### Step 4.3: Prepara Foto Demo di Alta Qualità

Scarica set di foto professionali:
- **Set 1:** Nature (montagna, lago, foresta)
- **Set 2:** Urban (città, street, architettura)
- **Set 3:** Travel (landmarks, culture)

Fonti:
- Unsplash.com
- Pexels.com
- Pixabay.com

Salva in `demo_photos/`

### Step 4.4: Script Presentazione (2 minuti)

```
[0:00-0:20] Intro
"Ciao! Siamo [team]. Abbiamo creato un'AI che trasforma
foto in storie cinematografiche. Il problema? Le foto
sono statiche e creare video richiede skill complesse."

[0:20-0:50] Tech
"Usiamo Gemini 2.5 Pro per analizzare le foto e creare
uno storyboard cinematografico. L'AI decide la narrativa,
i movimenti camera, e il mood di ogni scena."

[0:50-1:30] Demo Live
"Vi mostro com'è semplice. Upload 3 foto di un viaggio.
Scelgo 'Cinematic Adventure'. Click. In 30 secondi l'AI
ha creato una storia completa con 3 scene, descrizioni,
e movimenti camera."

[1:30-2:00] Vision
"Questo è l'MVP. Prossimi step: generazione video vera
con Veo 3, animazioni depth-aware, export MP4. Immaginate:
carica le foto delle vacanze, ottieni un video da
condividere su Instagram. Tutto automatico."
```

### Step 4.5: FAQ Preparate

**Q: Quanto costa?**
A: ~$0.08 per video con Gemini API. Scalabile.

**Q: Quanto tempo ci vuole?**
A: 30 secondi per storyboard. Video completo: 2-5 min (in futuro).

**Q: Posso usare mie foto?**
A: Sì! Qualsiasi foto JPG/PNG.

**Q: Dove gira?**
A: Cloud (Streamlit). Zero installazione per utenti.

**Q: E la privacy?**
A: Foto processate temporaneamente, poi cancellate.

✅ **Checkpoint:** Demo pronta!

---

## 🎯 CHECKLIST FINALE (Tutti Insieme)

### 1 Ora Prima della Presentazione

- [ ] **Persona 1:** Verifica repo GitHub aggiornato
- [ ] **Persona 2:** Verifica app Streamlit online e funzionante
- [ ] **Persona 3:** Test finale con foto fresche
- [ ] **Persona 4:** Slide e script pronti

### Setup Demo Day

- [ ] Laptop carico + charger
- [ ] Backup video demo su USB
- [ ] Foto demo pre-caricate
- [ ] URL app bookmarkato
- [ ] Slide aperte e pronte
- [ ] Internet testato (wifi + hotspot backup)

### Durante la Demo

1. **Apri l'app** (già caricata)
2. **Mostra upload** 3 foto
3. **Scegli stile** rapidamente
4. **Click genera** e **parla durante attesa** (30s)
5. **Mostra storyboard** generato
6. **Spiega ogni scena**

**Se fallisce:** Usa backup video!

---

## 🐛 Troubleshooting Rapido

### App non si carica

**Problema:** Errore 500 / App not found

**Fix:**
1. Controlla logs su Streamlit Cloud dashboard
2. Verifica `requirements.txt` sia committato
3. Redeploy da Streamlit Cloud UI

### API Key error

**Problema:** "❌ GEMINI_API_KEY non trovata"

**Fix:**
1. Streamlit Cloud → App Settings → Secrets
2. Verifica che `GEMINI_API_KEY = "AIza..."` sia presente
3. Salva e redeploy

### Generazione fallisce

**Problema:** Storyboard non creato

**Fix:**
- Verifica foto siano JPG/PNG validi
- Prova con foto diverse
- Controlla quota API Gemini (max 60/min)

### Slow generation

**Problema:** Ci vuole troppo tempo

**Fix:**
- Normale! Gemini può richiedere 30-60s
- Usa foto più piccole (<2MB)
- Mostra progress bar durante wait

---

## 📊 Metriche da Menzionare

Nella presentazione, cita:

- ✅ **Tempo sviluppo:** 1 giornata (hackathon)
- ✅ **Linee di codice:** ~600 (ben commentate)
- ✅ **API usate:** Gemini 2.5 Pro (ultima versione!)
- ✅ **Costo per video:** $0.08 (super economico)
- ✅ **Deploy:** Cloud-native, scala automaticamente
- ✅ **Tempo generazione:** 30s storyboard, 2-5min video (futuro)

---

## 🏆 Tips per Vincere

1. **Sottolinea l'innovazione:**
   - Primo uso di Gemini 2.5 Pro per storyboarding
   - AI cinematographer (non solo slideshow)
   - Quality checks automatici

2. **Mostra codice:**
   - Ben commentato
   - Professionale
   - Pronto per produzione

3. **Vision chiara:**
   - MVP funzionante oggi
   - Roadmap dettagliato
   - Market potential (Instagram creators, marketers)

4. **Live demo confident:**
   - Pratica 3 volte prima
   - Parla mentre aspetti (non silenzio awkward)
   - Backup plan pronto

---

## 📞 Supporto Last-Minute

Se qualcosa va storto:

1. **Controlla BUGS.md** (persona 3)
2. **Redeploy rapido:** Streamlit Cloud → Reboot app
3. **Usa backup video** se necessario
4. **Fallback:** Mostra slide + spiega architettura

**Ricorda:** Anche se demo fallisce, hai:
- Codice funzionante su GitHub
- Architettura solida
- Vision chiara
- Questo conta!

---

## ✅ Success Criteria

Demo di successo se:
- [ ] App carica senza errori
- [ ] Upload foto funziona
- [ ] Storyboard generato con AI
- [ ] Team sicuro e preparato
- [ ] Pitch chiaro sotto 2 minuti

---

**GOOD LUCK! 🚀🎬**

Avete tutto quello che serve. Ora è solo questione di esecuzione!

---

*Last updated: November 8, 2025*
*For HackNation 2025 Team*
