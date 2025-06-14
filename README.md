# 🏥 MedGemma Test Suite

**Sistema di test per MedGemma-4B-IT** - Modello AI specializzato nell'analisi di immagini mediche sviluppato da Google DeepMind.

---

## 📋 Panoramica

Questo progetto ti permette di testare **MedGemma**, un modello AI all'avanguardia per l'analisi di immagini mediche. MedGemma può:

- 🩻 **Analizzare radiografie** (torace, arti, etc.)
- 🔬 **Esaminare immagini istologiche**
- 👁️ **Valutare immagini oftalmologiche**
- 🫀 **Interpretare ECG e altre immagini cardiologiche**
- 🧠 **Descrivere scansioni neurologiche**

⚠️ **DISCLAIMER**: Questo è un tool di test/ricerca. Non sostituisce il giudizio clinico professionale.

---

## 📁 Struttura del Progetto

```
medgemma-test/
├── README.md                 # 📖 Questa guida
├── .env                      # 🔑 Configurazione e token (PRIVATO)
├── requirements.txt          # 📦 Dipendenze Python
├── setup.py                  # 🔧 Script setup automatico
├── test_medgemma.py          # 🧪 Script principale di test
├── examples/                 # 📁 Immagini di esempio (opzionale)
│   ├── chest_xray.jpg
│   ├── dermatology.jpg
│   └── histology.jpg
└── results/                  # 📁 Output e log (generato automaticamente)
    ├── analysis_log.txt
    └── responses/
```

### 📄 Descrizione File

| File | Descrizione | Editabile |
|------|-------------|-----------|
| `.env` | Configurazione tokens e parametri | ✅ **RICHIESTO** |
| `requirements.txt` | Dipendenze Python da installare | ❌ |
| `setup.py` | Verifica setup e installa dipendenze | ❌ |
| `test_medgemma.py` | Script principale per test interattivi | ❌ |
| `README.md` | Questa guida | ❌ |

---

## 🚀 Setup Rapido (5 minuti)

### **STEP 1: Crea la cartella del progetto**
Puoi utilizzare la root principale

### **STEP 2: Ottieni token Hugging Face**

1. **Registrati/Login** su → [huggingface.co](https://huggingface.co/join)
2. **Vai su Settings** → [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
3. **Clicca** "New token"
4. **Configura**:
   - Name: `MedGemma-Test`
   - Type: `Read`
   - Scopes: Default
5. **Clicca** "Generate" 
6. **COPIA** il token (formato: `hf_xxxxxxxxxxxxxxxxxxxxxxx`)

⚠️ **IMPORTANTE**: Il token appare UNA SOLA VOLTA!

### **STEP 3: Scarica i file del progetto**

Crea questi file nella cartella `medgemma-test/`:

**File `.env`:**
```bash
# Token Hugging Face (SOSTITUISCI con il tuo)
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Configurazioni modello
MODEL_NAME=google/medgemma-4b-it
DEVICE=auto
TORCH_DTYPE=bfloat16

# Parametri generazione
MAX_NEW_TOKENS=500
TEMPERATURE=0.1
DO_SAMPLE=false

# Debug
DEBUG=true
```

**File `requirements.txt`:**
```txt
torch>=2.0.0
transformers>=4.40.0
accelerate>=0.20.0
huggingface-hub>=0.20.0
Pillow>=9.0.0
requests>=2.28.0
python-dotenv>=1.0.0
```

📥 **Altri file**: Usa gli script forniti nel progetto (`setup.py`, `test_medgemma.py`)

### **STEP 4: Setup automatico**

```bash
# Verifica e installa tutto automaticamente
python setup.py
```

Se tutto va bene vedrai:
```
🎉 SETUP COMPLETATO!
```

Se ci sono problemi, il script ti dirà cosa sistemare.

### **STEP 5: Primo test**

```bash
# Avvia il sistema
python test_medgemma.py

# Nel prompt che appare, digita:
test
```

Se funziona, vedrai l'analisi di una radiografia di esempio! 🎉

---

## 💻 Guida all'Uso

### **🎮 Modalità Interattiva**

Quando lanci `python test_medgemma.py`, entri in modalità interattiva:

```
🩺 MODALITÀ INTERATTIVA MEDGEMMA
==================================================
Comandi disponibili:
  url <URL> <domanda>     - Analizza immagine da URL
  file <path> <domanda>   - Analizza file locale  
  test                    - Test con radiografia di esempio
  quit                    - Esci
==================================================

🏥 Comando: _
```

### **📋 Comandi Disponibili**

#### **1. `test` - Test veloce**
```bash
🏥 Comando: test
```
Analizza una radiografia toracica di esempio per verificare che tutto funzioni.

#### **2. `url` - Analisi da internet**
```bash
🏥 Comando: url https://example.com/xray.jpg "Describe this X-ray"
🏥 Comando: url https://example.com/scan.jpg "Any abnormalities visible?"
```

#### **3. `file` - Analisi file locale**
```bash
🏥 Comando: file ./chest_xray.jpg "What do you see?"
🏥 Comando: file /path/to/medical_image.png "Analyze this scan"
```

#### **4. `quit` - Esci**
```bash
🏥 Comando: quit
```

### **🖼️ Tipi di Immagini Supportate**

MedGemma può analizzare:

| Tipo | Formati | Esempi |
|------|---------|---------|
| **Radiografie** | JPG, PNG, DICOM | Torace, arti, addome |
| **Scansioni CT/MRI** | JPG, PNG | Cervello, addome, torace |
| **Dermatologia** | JPG, PNG | Lesioni cutanee, nei |
| **Oftalmologia** | JPG, PNG | Fundus, OCT |
| **Istologia** | JPG, PNG | Microscopia |

### **💡 Esempi di Domande Efficaci**

#### **Per Radiografie:**
```
"Describe this chest X-ray in detail"
"Are there any signs of pneumonia?"
"What is the cardiac silhouette like?"
"Any fractures visible in this bone X-ray?"
```

#### **Per Scansioni:**
```
"Analyze this CT scan"
"What structures are visible in this MRI?"
"Any abnormal findings in this scan?"
```

#### **Per Dermatologia:**
```
"Describe this skin lesion"
"What are the characteristics of this mole?"
"Any concerning features in this image?"
```

---

## 🔧 Configurazione Avanzata

### **⚙️ File `.env` - Parametri Personalizzabili**

```bash
# === MODELLO ===
MODEL_NAME=google/medgemma-4b-it    # Nome del modello
DEVICE=auto                         # auto | cpu | cuda:0
TORCH_DTYPE=bfloat16               # bfloat16 | float16 | float32

# === GENERAZIONE ===
MAX_NEW_TOKENS=500                 # Lunghezza massima risposta
TEMPERATURE=0.1                    # Creatività (0.0-1.0, più basso = più conservativo)
DO_SAMPLE=false                    # true | false (deterministic vs random)

# === DEBUG ===
DEBUG=true                         # Mostra info dettagliate
VERBOSE=true                       # Log estesi
```

### **🖥️ Configurazioni Hardware**

#### **Se hai GPU potente (8GB+ VRAM):**
```bash
DEVICE=auto
TORCH_DTYPE=bfloat16
```

#### **Se hai GPU limitata (4-8GB VRAM):**
```bash
DEVICE=auto
TORCH_DTYPE=float16
```

#### **Se hai solo CPU:**
```bash
DEVICE=cpu
TORCH_DTYPE=float32
MAX_NEW_TOKENS=200  # Riduci per velocità
```

---

## 🐛 Troubleshooting

### **❌ Errori Comuni e Soluzioni**

#### **1. "HF_TOKEN non configurato"**
```
❌ ERRORE: HF_TOKEN non configurato!
💡 Vai su https://huggingface.co/settings/tokens
```
**Soluzione**: Aggiorna il file `.env` con il tuo token valido.

#### **2. "Repository is gated"**
```
Repository google/medgemma-4b-it is gated
```
**Soluzione**: 
1. Vai su [huggingface.co/google/medgemma-4b-it](https://huggingface.co/google/medgemma-4b-it)
2. Clicca "Request access"
3. Compila il form
4. Aspetta approvazione (può richiedere ore/giorni)

#### **3. "CUDA out of memory"**
```
torch.cuda.OutOfMemoryError: CUDA out of memory
```
**Soluzioni**:
```bash
# Opzione 1: Usa CPU
DEVICE=cpu

# Opzione 2: Usa precision minore
TORCH_DTYPE=float16

# Opzione 3: Riduci token
MAX_NEW_TOKENS=200
```

#### **4. "ModuleNotFoundError"**
```
ModuleNotFoundError: No module named 'transformers'
```
**Soluzione**:
```bash
pip install -r requirements.txt
```

#### **5. Modello troppo lento**
**Soluzioni**:
- Usa GPU se disponibile
- Riduci `MAX_NEW_TOKENS`
- Considera modelli più piccoli per test

### **🔍 Verifica Stato Sistema**

```bash
# Ri-esegui setup per diagnostica
python setup.py

# Controlla versioni
pip list | grep torch
pip list | grep transformers
```

---

## 📊 Performance e Limitazioni

### **⚡ Performance Attese**

| Hardware | Tempo per Analisi | Note |
|----------|------------------|------|
| **RTX 4090** | 10-30 secondi | Ideale |
| **RTX 3080** | 20-45 secondi | Ottimo |
| **GTX 1080** | 45-90 secondi | Accettabile |
| **CPU moderno** | 2-10 minuti | Lento ma funziona |

### **🚫 Limitazioni**

- **Non è clinical-grade**: Solo per ricerca/test
- **Richiede supervisione umana**: Mai usare senza verifica medica
- **Lingue**: Ottimizzato per inglese
- **Formato immagini**: DICOM non nativamente supportato (converti in JPG/PNG)

---

## 🔐 Sicurezza e Privacy

### **🛡️ Dati Locali**
- ✅ **Tutto locale**: Nessun dato inviato a server esterni
- ✅ **Privacy garantita**: Immagini processate solo sul tuo computer
- ✅ **No telemetria**: Zero tracking o analytics

### **🔑 Token Security**
- ⚠️ **Non condividere** il file `.env`
- ⚠️ **Aggiungi `.env` al `.gitignore`** se usi Git
- ⚠️ **Rigenera token** se compromesso

---

## 📚 Risorse Aggiuntive

### **🔗 Link Utili**
- [MedGemma Official](https://medgemma.org)
- [Hugging Face Model](https://huggingface.co/google/medgemma-4b-it)
- [Documentazione Transformers](https://huggingface.co/docs/transformers)
- [PyTorch Documentation](https://pytorch.org/docs/)

### **🆘 Supporto**
- **Issues tecnici**: Controlla troubleshooting sopra
- **Domande modello**: [Discussions Hugging Face](https://huggingface.co/google/medgemma-4b-it/discussions)
- **Bug del codice**: Controlla logs e re-esegui setup

---

## 📜 Licenza e Disclaimer

### **⚖️ Uso Responsabile**
- Questo strumento è per **ricerca ed educazione**
- **NON sostituisce** diagnosi medica professionale
- **Sempre consultare** personale medico qualificato
- **Non usare** per decisioni cliniche critiche

### **📋 Licenze**
- **MedGemma**: Soggetto a [Health AI Developer Foundations terms](https://developers.google.com/terms/health-ai-developer-foundations)
- **Questo codice**: MIT License (modificabile liberamente)

---

## 🎯 Quick Start Summary

```bash
# 1. Setup
mkdir medgemma-test && cd medgemma-test

# 2. Ottieni token da huggingface.co/settings/tokens

# 3. Crea file .env con il tuo token

# 4. Setup automatico
python setup.py

# 5. Test
python test_medgemma.py
# Poi digita: test

# 🎉 Se vedi l'analisi della radiografia, tutto funziona!
```

**🏥 Buon testing con MedGemma!** 🚀

---

*Ultima modifica: Giugno 2025 | Versione: 1.0*