#!/usr/bin/env python3
"""
Test completo MedGemma-4B-IT
Analisi immagini mediche con AI specializzata
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from huggingface_hub import login
from transformers import pipeline
from PIL import Image
import requests
import torch

class MedGemmaTest:
    def __init__(self):
        """Inizializza il sistema MedGemma"""
        print("INIZIALIZZAZIONE MEDGEMMA")
        print("=" * 50)
        
        # Carica configurazione
        self._load_config()
        
        # Autentica Hugging Face
        self._authenticate()
        
        # Verifica hardware
        self._check_hardware()
        
        # Carica modello
        self._load_model()
        
        print("MedGemma pronto per l'uso!")
        print("=" * 50)

    def _load_config(self):
        """Carica configurazione da .env"""
        load_dotenv()
        
        self.hf_token = os.getenv("HF_TOKEN")
        self.model_name = os.getenv("MODEL_NAME", "google/medgemma-4b-it")
        self.device = os.getenv("DEVICE", "auto")
        self.torch_dtype = os.getenv("TORCH_DTYPE", "bfloat16")
        self.max_tokens = int(os.getenv("MAX_NEW_TOKENS", "500"))
        self.temperature = float(os.getenv("TEMPERATURE", "0.1"))
        self.debug = os.getenv("DEBUG", "true").lower() == "true"
        
        if not self.hf_token or self.hf_token.startswith("hf_xxx"):
            print("ERRORE: HF_TOKEN non configurato!")
            print("Vai su https://huggingface.co/settings/tokens")
            print("Crea un nuovo token e aggiorna il file .env")
            sys.exit(1)
        
        if self.debug:
            print(f"Modello: {self.model_name}")
            print(f"Device: {self.device}")
            print(f"Dtype: {self.torch_dtype}")

    def _authenticate(self):
        """Autentica con Hugging Face"""
        try:
            print("Autenticazione Hugging Face...")
            login(token=self.hf_token, add_to_git_credential=False)
            print("Autenticazione riuscita")
        except Exception as e:
            print(f"Errore autenticazione: {e}")
            sys.exit(1)

    def _check_hardware(self):
        """Verifica hardware disponibile"""
        print("Controllo hardware...")
        
        # Check CUDA
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
            print(f"GPU: {gpu_name}")
            print(f"VRAM: {gpu_memory:.1f} GB")
            
            if gpu_memory < 6:
                print("ATTENZIONE: VRAM bassa, possibili problemi di memoria")
                print("Considera device='cpu' nel .env se hai errori")
        else:
            print("GPU non disponibile, usando CPU")
            print("Il processing sarà più lento ma funziona")
        
        # Check RAM
        try:
            import psutil
            ram_gb = psutil.virtual_memory().total / 1024**3
            print(f"RAM: {ram_gb:.1f} GB")
            
            if ram_gb < 8:
                print("ATTENZIONE: RAM limitata, possibili problemi")
        except ImportError:
            print("Installa psutil per monitoraggio RAM: pip install psutil")

    def _load_model(self):
        """Carica il modello MedGemma"""
        try:
            print(f"Caricamento {self.model_name}...")
            print("Questo può richiedere alcuni minuti la prima volta...")
            
            # Configura dtype
            dtype_map = {
                "bfloat16": torch.bfloat16,
                "float16": torch.float16,
                "float32": torch.float32
            }
            torch_dtype = dtype_map.get(self.torch_dtype, torch.bfloat16)
            
            # Carica pipeline
            self.pipe = pipeline(
                "image-text-to-text",
                model=self.model_name,
                torch_dtype=torch_dtype,
                device_map=self.device,
                trust_remote_code=True  # Necessario per alcuni modelli
            )
            
            print("Modello caricato con successo!")
            
        except Exception as e:
            print(f"Errore caricamento modello: {e}")
            
            # Suggerimenti troubleshooting
            if "gated" in str(e).lower():
                print("\nMODELLO GATED - RICHIEDI ACCESSO:")
                print(f"1. Vai su https://huggingface.co/{self.model_name}")
                print("2. Click 'Request access'")
                print("3. Compila il form e aspetta approvazione")
                
            elif "memory" in str(e).lower() or "cuda out of memory" in str(e).lower():
                print("\nERRORE MEMORIA - SOLUZIONI:")
                print("1. Chiudi altre applicazioni")
                print("2. Cambia DEVICE=cpu nel .env")
                print("3. Cambia TORCH_DTYPE=float16 nel .env")
                
            sys.exit(1)

    def analyze_image_from_url(self, image_url, question="Describe this medical image"):
        """Analizza immagine da URL"""
        try:
            print(f"\nScaricamento immagine da: {image_url}")
            
            # Scarica immagine
            headers = {"User-Agent": "MedGemma-Test/1.0"}
            response = requests.get(image_url, headers=headers, stream=True)
            response.raise_for_status()
            
            image = Image.open(response.raw)
            print(f"Immagine caricata: {image.size}")
            
            return self.analyze_image(image, question)
            
        except Exception as e:
            return f"Errore download immagine: {e}"

    def analyze_image_from_file(self, image_path, question="Describe this medical image"):
        """Analizza immagine da file locale"""
        try:
            if not os.path.exists(image_path):
                return f"File non trovato: {image_path}"
            
            print(f"\nCaricamento da: {image_path}")
            image = Image.open(image_path)
            print(f"Immagine caricata: {image.size}")
            
            return self.analyze_image(image, question)
            
        except Exception as e:
            return f"Errore caricamento file: {e}"

    def analyze_image(self, image, question):
        """Analizza immagine con MedGemma"""
        try:
            print(f"Analisi in corso...")
            print(f"Domanda: {question}")
            
            # Prepara messagi per MedGemma
            messages = [
                {
                    "role": "system",
                    "content": [{"type": "text", "text": "You are an expert medical AI assistant. Provide detailed, accurate analysis of medical images. Always mention limitations and recommend professional consultation."}]
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question},
                        {"type": "image", "image": image}
                    ]
                }
            ]
            
            # Genera risposta
            output = self.pipe(
                text=messages, 
                max_new_tokens=self.max_tokens,
                temperature=self.temperature,
                do_sample=False  # Deterministico per uso medico
            )
            
            # Estrai risposta
            response = output[0]["generated_text"][-1]["content"]
            
            print("Analisi completata!")
            return response
            
        except Exception as e:
            return f"Errore durante analisi: {e}"

    def interactive_mode(self):
        """Modalità interattiva per test"""
        print("\nMODALITA' INTERATTIVA MEDGEMMA")
        print("=" * 50)
        print("Comandi disponibili:")
        print("  url <URL> <domanda>     - Analizza immagine da URL")
        print("  file <path> <domanda>   - Analizza file locale")
        print("  test                    - Test con radiografia di esempio")
        print("  quit                    - Esci")
        print("=" * 50)
        
        while True:
            try:
                command = input("\nComando: ").strip()
                
                if command.lower() == "quit":
                    print("Arrivederci!")
                    break
                
                elif command.lower() == "test":
                    # Test con immagine di esempio
                    test_url = "https://upload.wikimedia.org/wikipedia/commons/c/c8/Chest_Xray_PA_3-8-2010.png"
                    question = "Describe this chest X-ray. What can you observe?"
                    
                    result = self.analyze_image_from_url(test_url, question)
                    print(f"\nRISPOSTA MEDGEMMA:\n{result}")
                
                elif command.startswith("url "):
                    parts = command[4:].split(" ", 1)
                    if len(parts) >= 2:
                        url, question = parts[0], parts[1]
                    else:
                        url = parts[0]
                        question = "Describe this medical image in detail"
                    
                    result = self.analyze_image_from_url(url, question)
                    print(f"\nRISPOSTA MEDGEMMA:\n{result}")
                
                elif command.startswith("file "):
                    parts = command[5:].split(" ", 1)
                    if len(parts) >= 2:
                        filepath, question = parts[0], parts[1]
                    else:
                        filepath = parts[0]
                        question = "Describe this medical image in detail"
                    
                    result = self.analyze_image_from_file(filepath, question)
                    print(f"\nRISPOSTA MEDGEMMA:\n{result}")
                
                else:
                    print("Comando non riconosciuto. Usa 'test', 'url', 'file' o 'quit'")
                    
            except KeyboardInterrupt:
                print("\nInterruzione utente. Arrivederci!")
                break
            except Exception as e:
                print(f"Errore: {e}")


def main():
    """Funzione principale"""
    print("MEDGEMMA TEST SUITE")
    print("=" * 50)
    
    try:
        # Inizializza MedGemma
        medgemma = MedGemmaTest()
        
        # Avvia modalità interattiva
        medgemma.interactive_mode()
        
    except KeyboardInterrupt:
        print("\nTest interrotto. Arrivederci!")
    except Exception as e:
        print(f"Errore fatale: {e}")
        if "ModuleNotFoundError" in str(e):
            print("\nSOLUZIONE: Installa le dipendenze")
            print("pip install -r requirements.txt")


if __name__ == "__main__":
    main()