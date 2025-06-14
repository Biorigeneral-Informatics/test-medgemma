# =================================
# CONFIGURAZIONE MEDGEMMA TEST
# =================================

# Token Hugging Face (SOSTITUISCI con il tuo)
HF_TOKEN=

# Configurazioni modello
MODEL_NAME=google/medgemma-4b-it
DEVICE=auto
TORCH_DTYPE=bfloat16

# Configurazioni generazione
MAX_NEW_TOKENS=500
TEMPERATURE=0.1
DO_SAMPLE=false

# Debug
DEBUG=true
VERBOSE=true

# =================================
# ISTRUZIONI:
# 1. Sostituisci HF_TOKEN con il tuo token da huggingface.co/settings/tokens
# 2. Se non hai GPU, cambia DEVICE=cpu
# 3. Se hai problemi di memoria, cambia TORCH_DTYPE=float16
# =================================