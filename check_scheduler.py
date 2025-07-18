#!/usr/bin/env python3
"""
Script de vérification et gestion des tâches planifiées InfoWatchdog
"""
import platform
import subprocess
import json
from pathlib import Path
from datetime import datetime

def check_cron_jobs():
    """Vérifie les tâches cron existantes"""
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        if result.returncode == 0:
            crontab_lines = result.stdout.split('\n')
            infowatchdog_jobs = [line for line in crontab_lines if 'InfoWatchdog' in line or 'run.py' in line]
            
            if infowatchdog_jobs:
                print("✅ Tâches cron InfoWatchdog trouvées:")
                for job in infowatchdog_jobs:
                    print(f"   {job}")
                return True
            else:
                print("❌ Aucune tâche cron InfoWatchdog trouvée")
                return False
        else:
            print("⚠️  Impossible de lire crontab")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la vérification cron: {e}")
        return False

def check_systemd_services():
    """Vérifie les services systemd"""
    try:
        # Vérifie le service
        result = subprocess.run(['systemctl', 'status', 'infowatchdog.service'], 
                              capture_output=True, text=True)
        service_exists = result.returncode == 0
        
        # Vérifie le timer
        result = subprocess.run(['systemctl', 'status', 'infowatchdog.timer'], 
                              capture_output=True, text=True)
        timer_exists = result.returncode == 0
        
        if service_exists and timer_exists:
            print("✅ Service et timer systemd InfoWatchdog trouvés")
            
            # Vérifie si le timer est actif
            result = subprocess.run(['systemctl', 'is-active', 'infowatchdog.timer'], 
                                  capture_output=True, text=True)
            if result.stdout.strip() == 'active':
                print("✅ Timer systemd actif")
            else:
                print("⚠️  Timer systemd inactif")
            
            return True
        else:
            print("❌ Service ou timer systemd InfoWatchdog non trouvé")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification systemd: {e}")
        return False

def check_windows_tasks():
    """Vérifie les tâches planifiées Windows"""
    try:
        # PowerShell command pour lister les tâches
        ps_command = 'Get-ScheduledTask -TaskName "*InfoWatchdog*" | Select-Object TaskName, State | ConvertTo-Json'
        
        result = subprocess.run(['powershell', '-Command', ps_command], 
                              capture_output=True, text=True)
        
        if result.returncode == 0 and result.stdout.strip():
            tasks = json.loads(result.stdout)
            if not isinstance(tasks, list):
                tasks = [tasks]
            
            print("✅ Tâches Windows InfoWatchdog trouvées:")
            for task in tasks:
                state = "🟢 Activée" if task['State'] == 'Ready' else f"🔴 {task['State']}"
                print(f"   {task['TaskName']}: {state}")
            return True
        else:
            print("❌ Aucune tâche Windows InfoWatchdog trouvée")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification Windows: {e}")
        return False

def check_last_execution():
    """Vérifie la dernière exécution en consultant les logs"""
    log_file = Path("logs/cron.log")
    
    if log_file.exists():
        try:
            with open(log_file, 'r') as f:
                lines = f.readlines()
            
            if lines:
                # Cherche la dernière ligne avec un timestamp
                for line in reversed(lines):
                    if "Collection Report:" in line or "Starting InfoWatchdog" in line:
                        print(f"📄 Dernière exécution détectée dans les logs")
                        print(f"   {line.strip()}")
                        break
                
                # Statistiques du fichier
                file_stats = log_file.stat()
                last_modified = datetime.fromtimestamp(file_stats.st_mtime)
                print(f"📅 Dernière modification des logs: {last_modified}")
                return True
            else:
                print("⚠️  Fichier de logs vide")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors de la lecture des logs: {e}")
            return False
    else:
        print("❌ Fichier de logs non trouvé (logs/cron.log)")
        return False

def remove_scheduled_tasks():
    """Supprime les tâches planifiées"""
    system = platform.system().lower()
    
    if system in ['linux', 'darwin']:
        print("🗑️  Suppression des tâches cron...")
        try:
            # Lit le crontab actuel
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                # Filtre les lignes InfoWatchdog
                filtered_lines = [line for line in lines if 'InfoWatchdog' not in line and 'run.py' not in line]
                
                # Réapplique le crontab
                new_crontab = '\n'.join(filtered_lines)
                process = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE, text=True)
                process.communicate(input=new_crontab)
                
                if process.returncode == 0:
                    print("✅ Tâches cron supprimées")
                else:
                    print("❌ Erreur lors de la suppression des tâches cron")
        except Exception as e:
            print(f"❌ Erreur: {e}")
            
        # Systemd (Linux uniquement)
        if system == 'linux':
            print("\n🗑️  Suppression du service systemd...")
            try:
                subprocess.run(['sudo', 'systemctl', 'stop', 'infowatchdog.timer'], check=False)
                subprocess.run(['sudo', 'systemctl', 'disable', 'infowatchdog.timer'], check=False)
                subprocess.run(['sudo', 'rm', '/etc/systemd/system/infowatchdog.service'], check=False)
                subprocess.run(['sudo', 'rm', '/etc/systemd/system/infowatchdog.timer'], check=False)
                subprocess.run(['sudo', 'systemctl', 'daemon-reload'], check=False)
                print("✅ Service systemd supprimé")
            except Exception as e:
                print(f"⚠️  Erreur systemd: {e}")
                
    elif system == 'windows':
        print("🗑️  Suppression des tâches Windows...")
        try:
            ps_command = 'Unregister-ScheduledTask -TaskName "InfoWatchdog" -Confirm:$false'
            result = subprocess.run(['powershell', '-Command', ps_command], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Tâche Windows supprimée")
            else:
                print("❌ Erreur lors de la suppression de la tâche Windows")
        except Exception as e:
            print(f"❌ Erreur: {e}")

def main():
    """Fonction principale"""
    print("🔍 InfoWatchdog - Vérification des tâches planifiées")
    print("="*60)
    
    system = platform.system().lower()
    print(f"🖥️  Système: {platform.system()}")
    
    # Vérification selon le système
    tasks_found = False
    
    if system in ['linux', 'darwin']:
        print("\n📋 Vérification des tâches cron...")
        tasks_found |= check_cron_jobs()
        
        if system == 'linux':
            print("\n📋 Vérification des services systemd...")
            tasks_found |= check_systemd_services()
            
    elif system == 'windows':
        print("\n📋 Vérification des tâches Windows...")
        tasks_found |= check_windows_tasks()
    
    print("\n📄 Vérification des logs d'exécution...")
    check_last_execution()
    
    # Menu d'actions
    if tasks_found:
        print("\n🔧 Actions disponibles:")
        print("1. Voir les logs récents")
        print("2. Tester une exécution manuelle")
        print("3. Supprimer toutes les tâches planifiées")
        print("4. Quitter")
        
        choice = input("\nChoisissez une action (1-4): ").strip()
        
        if choice == "1":
            show_recent_logs()
        elif choice == "2":
            test_manual_execution()
        elif choice == "3":
            confirm = input("⚠️  Êtes-vous sûr de vouloir supprimer toutes les tâches ? (y/N): ")
            if confirm.lower() in ['y', 'yes', 'oui']:
                remove_scheduled_tasks()
        elif choice == "4":
            pass
    else:
        print("\n💡 Aucune tâche planifiée trouvée.")
        print("   Exécutez 'python setup_scheduler.py' pour en créer une.")

def show_recent_logs():
    """Affiche les logs récents"""
    log_file = Path("logs/cron.log")
    if log_file.exists():
        try:
            with open(log_file, 'r') as f:
                lines = f.readlines()
            
            print("\n📄 20 dernières lignes des logs:")
            print("="*60)
            for line in lines[-20:]:
                print(line.rstrip())
            print("="*60)
        except Exception as e:
            print(f"❌ Erreur lecture logs: {e}")
    else:
        print("❌ Fichier de logs non trouvé")

def test_manual_execution():
    """Teste une exécution manuelle"""
    print("\n🧪 Test d'exécution manuelle...")
    try:
        result = subprocess.run([get_python_path(), "run.py", "--test-only"], 
                              capture_output=True, text=True)
        
        print("📤 STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("📤 STDERR:")
            print(result.stderr)
            
        print(f"📊 Code de retour: {result.returncode}")
        
        if result.returncode == 0:
            print("✅ Test réussi")
        else:
            print("❌ Test échoué")
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")

def get_python_path():
    """Retourne le chemin Python (même logique que setup_scheduler.py)"""
    from pathlib import Path
    import sys
    
    # Essaie de détecter l'environnement virtuel
    venv_python = Path("venv/bin/python")
    if venv_python.exists():
        return str(venv_python.absolute())
    
    venv_python_alt = Path(".venv/bin/python")
    if venv_python_alt.exists():
        return str(venv_python_alt.absolute())
    
    # Windows
    venv_python_win = Path("venv/Scripts/python.exe")
    if venv_python_win.exists():
        return str(venv_python_win.absolute())
    
    venv_python_win_alt = Path(".venv/Scripts/python.exe")
    if venv_python_win_alt.exists():
        return str(venv_python_win_alt.absolute())
    
    return sys.executable

if __name__ == "__main__":
    main()