#!/usr/bin/env python3
"""
Setup automatico per MedGemma con Virtual Environment
Crea venv, installa dipendenze e configura tutto automaticamente
"""

import os
import sys
import subprocess
import venv
from pathlib import Path

class MedGemmaSetup:
    def __init__(self):
        self.project_dir = Path.cwd()
        self.venv_dir = self.project_dir / "venv"
        self.venv_python = self._get_venv_python()
        self.venv_pip = self._get_venv_pip()
        
    def _get_venv_python(self):
        """Path Python nel venv"""
        if os.name == 'nt':  # Windows
            return self.venv_dir / "Scripts" / "python.exe"
        else:  # Linux/Mac
            return self.venv_dir / "bin" / "python"
    
    def _get_venv_pip(self):
        """Path pip nel venv"""
        if os.name == 'nt':  # Windows
            return self.venv_dir / "Scripts" / "pip.exe"
        else:  # Linux/Mac
            return self.venv_dir / "bin" / "pip"
    
    def _get_activate_script(self):
        """Path script di attivazione venv"""
        if os.name == 'nt':  # Windows
            return self.venv_dir / "Scripts" / "activate.bat"
        else:  # Linux/Mac
            return self.venv_dir / "bin" / "activate"

    def check_python_version(self):
        """Verifica versione Python"""
        if sys.version_info < (3, 8):
            print("Python 3.8+ richiesto")
            print(f"   Versione attuale: {sys.version}")
            return False
        print(f"Python {sys.version.split()[0]}")
        return True

    def create_venv(self):
        """Crea virtual environment"""
        if self.venv_dir.exists():
            print("Virtual environment già esistente")
            return True
        
        print("Creazione virtual environment...")
        try:
            # Crea venv
            venv.create(self.venv_dir, with_pip=True)
            print("Virtual environment creato")
            
            # Upgrade pip nel venv
            subprocess.check_call([
                str(self.venv_python), "-m", "pip", "install", "--upgrade", "pip"
            ])
            print("pip aggiornato nel venv")
            
            return True
        except Exception as e:
            print(f"Errore creazione venv: {e}")
            return False

    def install_requirements(self):
        """Installa requirements nel venv"""
        if not Path("requirements.txt").exists():
            print("File requirements.txt non trovato")
            return False
        
        print("Installazione dipendenze nel virtual environment...")
        
        try:
            # Installa nel venv
            subprocess.check_call([
                str(self.venv_python), "-m", "pip", "install", "-r", "requirements.txt"
            ])
            print("Dipendenze installate nel venv")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Errore installazione: {e}")
            return False

    def check_env_file(self):
        """Verifica file .env"""
        env_path = Path(".env")
        
        if not env_path.exists():
            print("File .env non trovato")
            print("Crea il file .env e aggiungi il tuo HF_TOKEN")
            return False
        
        # Leggi .env
        env_content = env_path.read_text()
        
        if "hf_xxx" in env_content or "HF_TOKEN=" not in env_content:
            print("HF_TOKEN non configurato in .env")
            print("Aggiorna HF_TOKEN con il tuo token da huggingface.co")
            return False
        
        print("File .env configurato")
        return True

    def check_gpu_in_venv(self):
        """Verifica GPU usando Python del venv"""
        try:
            # Test PyTorch nel venv
            result = subprocess.run([
                str(self.venv_python), "-c", 
                "import torch; print('CUDA:', torch.cuda.is_available()); "
                "print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None')"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                output_lines = result.stdout.strip().split('\n')
                for line in output_lines:
                    if 'CUDA:' in line:
                        cuda_available = 'True' in line
                    elif 'GPU:' in line:
                        gpu_name = line.split('GPU: ')[1]
                
                if cuda_available and gpu_name != 'None':
                    print(f"GPU: {gpu_name}")
                else:
                    print("GPU non disponibile (modalità CPU)")
                return True
            else:
                print("PyTorch non ancora installato nel venv")
                return False
                
        except Exception as e:
            print(f"Errore verifica GPU: {e}")
            return False

    def generate_activation_scripts(self):
        """Genera script di attivazione personalizzati"""
        
        # Script Windows
        windows_script = self.project_dir / "activate_venv.bat"
        windows_content = f"""@echo off
echo Attivazione ambiente MedGemma...
call "{self.venv_dir}\\Scripts\\activate.bat"
echo Virtual environment attivato!
echo Ora puoi eseguire: python test_medgemma.py
cmd /k
"""
        
        # Script Linux/Mac
        unix_script = self.project_dir / "activate_venv.sh"
        unix_content = f"""#!/bin/bash
echo "Attivazione ambiente MedGemma..."
source "{self.venv_dir}/bin/activate"
echo "Virtual environment attivato!"
echo "Ora puoi eseguire: python test_medgemma.py"
exec bash
"""
        
        try:
            windows_script.write_text(windows_content)
            unix_script.write_text(unix_content)
            
            # Rendi eseguibile su Unix
            if os.name != 'nt':
                os.chmod(unix_script, 0o755)
            
            print("Script di attivazione generati")
            return True
        except Exception as e:
            print(f"Errore generazione script: {e}")
            return False

    def create_run_script(self):
        """Crea script per eseguire MedGemma direttamente"""
        
        # Script Windows
        windows_run = self.project_dir / "run_medgemma.bat"
        windows_run_content = f"""@echo off
echo Avvio MedGemma...
call "{self.venv_dir}\\Scripts\\activate.bat"
python test_medgemma.py
pause
"""
        
        # Script Linux/Mac
        unix_run = self.project_dir / "run_medgemma.sh"
        unix_run_content = f"""#!/bin/bash
echo "Avvio MedGemma..."
source "{self.venv_dir}/bin/activate"
python test_medgemma.py
"""
        
        try:
            windows_run.write_text(windows_run_content)
            unix_run.write_text(unix_run_content)
            
            # Rendi eseguibile su Unix
            if os.name != 'nt':
                os.chmod(unix_run, 0o755)
            
            print("Script di esecuzione generati")
            return True
        except Exception as e:
            print(f"Errore generazione script run: {e}")
            return False

    def test_installation(self):
        """Test installazione nel venv"""
        print("Test installazione...")
        
        try:
            # Test import nel venv
            test_cmd = [
                str(self.venv_python), "-c",
                "import torch, transformers, huggingface_hub; print('Import successful')"
            ]
            
            result = subprocess.run(test_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("Tutti i moduli importati correttamente")
                return True
            else:
                print(f"Errore import: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Errore test: {e}")
            return False

    def run_setup(self):
        """Esegue setup completo"""
        print("SETUP AUTOMATICO MEDGEMMA CON VENV")
        print("=" * 50)
        
        setup_steps = [
            ("Versione Python", self.check_python_version),
            ("Virtual Environment", self.create_venv),
            ("Dipendenze", self.install_requirements),
            ("File .env", self.check_env_file),
            ("GPU Support", self.check_gpu_in_venv),
            ("Script attivazione", self.generate_activation_scripts),
            ("Script esecuzione", self.create_run_script),
            ("Test installazione", self.test_installation),
        ]
        
        all_passed = True
        
        for name, step_func in setup_steps:
            print(f"\n{name}...")
            if not step_func():
                all_passed = False
        
        print("\n" + "=" * 50)
        
        if all_passed:
            self._print_success_message()
        else:
            self._print_failure_message()
        
        print("=" * 50)

    def _print_success_message(self):
        """Messaggio di successo con istruzioni"""
        print("SETUP COMPLETATO CON SUCCESSO!")
        print()
        print("COME USARE MEDGEMMA:")
        print()
        
        if os.name == 'nt':  # Windows
            print("OPZIONE 1 - Doppio click:")
            print("   Doppio click su 'run_medgemma.bat'")
            print()
            print("OPZIONE 2 - Da terminale:")
            print("   activate_venv.bat")
            print("   python test_medgemma.py")
        else:  # Linux/Mac
            print("OPZIONE 1 - Script diretto:")
            print("   ./run_medgemma.sh")
            print()
            print("OPZIONE 2 - Attivazione manuale:")
            print("   source activate_venv.sh")
            print("   python test_medgemma.py")
        
        print()
        print("PRIMO TEST:")
        print("   1. Avvia MedGemma")
        print("   2. Digita: test")
        print("   3. Aspetta l'analisi della radiografia di esempio")
        print()
        print("Virtual Environment:")
        print(f"   Posizione: {self.venv_dir}")
        print("   Gestito automaticamente dagli script")

    def _print_failure_message(self):
        """Messaggio di errore con troubleshooting"""
        print("SETUP INCOMPLETO")
        print()
        print("TROUBLESHOOTING:")
        print("1. Verifica che Python 3.8+ sia installato")
        print("2. Controlla che il file .env esista con HF_TOKEN valido")
        print("3. Assicurati di avere connessione internet")
        print("4. Se problemi di memoria, prova:")
        print("   - Chiudi altre applicazioni")
        print("   - Modifica DEVICE=cpu nel .env")
        print()
        print("Per rifare il setup: python setup.py")


def main():
    """Funzione principale"""
    try:
        setup = MedGemmaSetup()
        setup.run_setup()
    except KeyboardInterrupt:
        print("\nSetup interrotto dall'utente")
    except Exception as e:
        print(f"\nErrore inaspettato: {e}")
        print("Riprova o verifica i prerequisiti")


if __name__ == "__main__":
    main()