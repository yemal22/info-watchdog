#!/usr/bin/env python3
"""
Script de configuration automatique des tâches pour InfoWatchdog.
"""
import os
import sys
import platform
import subprocess
from pathlib import Path

def get_project_path():
    """Retourne le chemin absolu du projet."""
    return Path(__file__).parent.absolute()

def get_python_path():
    """Retourne le chemin de l'exécutable Python."""
    venv_python = Path("venv/bin/python")
    if venv_python.exists():
        return str(venv_python.absolute())
    
    venv_python_alt = Path(".venv/bin/python/")
    if venv_python_alt.exists():
        return str(venv_python_alt.absolute())
    
    # Windows
    venv_python_win = Path("venv/Scripts/python.exe")
    if venv_python_win.exists():
        return str(venv_python_win.absolute())
    
    venv_python_win_alt = Path(".venv/Scripts/python.exe")
    if venv_python_win_alt.exists():
        return str(venv_python_win_alt.absolute())
    

def setup_cron_job(interval="hourly"):
    """Configure une tâche cron (Linux/macOS)"""
    project_path = get_project_path()
    python_path = get_python_path()
    log_path = project_path / "logs" / "cron.log"
    
    log_path.parent.mkdir(exist_ok=True)
    
    cron_expressions = {
        "hourly": "0 * * * *",
        "daily": "0 0 * * *",
        "twice_daily": "0 8,20 * * *",
        "every_6h": "0 */6 * * *",
    }
    
    if interval not in cron_expressions:
        interval = "hourly"
        
    cron_line = f"{cron_expressions[interval]} cd {project_path} && {python_path} run.py >> {log_path} 2>&1"
    
     # Affiche les instructions pour l'utilisateur
    print(f"🔧 Configuration cron pour {interval}")
    print(f"📁 Projet: {project_path}")
    print(f"🐍 Python: {python_path}")
    print(f"📄 Logs: {log_path}")
    print("\n" + "="*60)
    print("Pour configurer la tâche cron, exécutez :")
    print("crontab -e")
    print("\nPuis ajoutez cette ligne :")
    print(f"{cron_line}")
    print("="*60)

    # Tentative d'ajout automatique
    try:
        response = input("\n❓ Voulez-vous que le script ajoute automatiquement cette tâche cron ? (y/N): ")
        if response.lower() in ['y', 'yes', 'oui']:
            result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
            current_crontab = result.stdout if result.returncode == 0 else ""
            
            if "InfoWatchdog" in current_crontab or str(project_path) in current_crontab:
                print("⚠️  Une tâche InfoWatchdog existe déjà dans crontab")
                return
            
            new_crontab = current_crontab + f"\n# InfoWatchdog - Collecte automatique\n{cron_line}\n"
            
            process = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE, text=True)
            process.communicate(input=new_crontab)
            
            if process.returncode == 0:
                print("✅ Tâche cron ajoutée avec succès !")
                print("📋 Vérifiez avec : crontab -l")
            else:
                print("❌ Échec de l'ajout de la tâche cron.")
                
    except Exception as e:
        print(f"⚠️  Ajout automatique échoué: {e}")
        print("💡 Veuillez ajouter manuellement la tâche cron")
        
def setup_systemd_service():
    """Configure un service systemd (Linux)"""
    project_path = get_project_path()
    python_path = get_python_path()
    user = os.getenv('USER', 'infowatchdog')
    
    service_content = f"""[Unit]
Description=InfoWatchdog - Agent de veille environnementale
After=network.target

[Service]
Type=oneshot
User={user}
WorkingDirectory={project_path}
ExecStart={python_path} {project_path}/run.py
Environment=PATH={Path(python_path).parent}:$PATH

[Install]
WantedBy=multi-user.target
"""

    timer_content = """[Unit]
Description=Exécute InfoWatchdog toutes les heures
Requires=infowatchdog.service

[Timer]
OnCalendar=hourly
Persistent=true

[Install]
WantedBy=timers.target
"""

    print("🔧 Configuration systemd")
    print("📄 Contenu du fichier service (/etc/systemd/system/infowatchdog.service):")
    print("="*60)
    print(service_content)
    print("="*60)
    print("\n📄 Contenu du fichier timer (/etc/systemd/system/infowatchdog.timer):")
    print("="*60)
    print(timer_content)
    print("="*60)
    
    print("\n📋 Commandes à exécuter (en tant que root ou avec sudo):")
    print("sudo nano /etc/systemd/system/infowatchdog.service")
    print("sudo nano /etc/systemd/system/infowatchdog.timer")
    print("sudo systemctl daemon-reload")
    print("sudo systemctl enable infowatchdog.timer")
    print("sudo systemctl start infowatchdog.timer")
    print("sudo systemctl status infowatchdog.timer")


def setup_windows_task():
    """Configure une tâche planifiée Windows"""
    project_path = get_project_path()
    python_path = get_python_path()
    
    # Script PowerShell pour créer la tâche
    ps_script = f'''
$TaskName = "InfoWatchdog"
$TaskPath = "\\InfoWatchdog\\"
$PythonPath = "{python_path}"
$ScriptPath = "{project_path}\\run.py"
$WorkingDir = "{project_path}"

# Supprime la tâche si elle existe
if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {{
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}}

# Crée l'action
$Action = New-ScheduledTaskAction -Execute $PythonPath -Argument $ScriptPath -WorkingDirectory $WorkingDir

# Crée le déclencheur (toutes les heures)
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 1) -RepetitionDuration ([TimeSpan]::MaxValue)

# Crée les paramètres
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Enregistre la tâche
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Description "InfoWatchdog - Collecte automatique d'actualités environnementales"

Write-Host "✅ Tâche InfoWatchdog créée avec succès !"
Write-Host "📋 Vérifiez dans le Planificateur de tâches Windows"
'''
    
    print("🔧 Configuration Planificateur de tâches Windows")
    print("💡 Script PowerShell automatique:")
    print("="*60)
    print(ps_script)
    print("="*60)
    
    # Sauvegarde le script
    ps_file = project_path / "setup_windows_task.ps1"
    with open(ps_file, 'w', encoding='utf-8') as f:
        f.write(ps_script)
    
    print(f"\n📄 Script sauvegardé: {ps_file}")
    print("\n📋 Pour exécuter:")
    print("1. Ouvrez PowerShell en tant qu'Administrateur")
    print("2. Naviguez vers le dossier du projet")
    print("3. Exécutez: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser")
    print("4. Exécutez: .\\setup_windows_task.ps1")
    
    # Alternative manuelle
    print("\n🔧 Configuration manuelle alternative:")
    print("1. Ouvrez le Planificateur de tâches (taskschd.msc)")
    print("2. Créez une tâche de base")
    print("3. Nom: InfoWatchdog")
    print("4. Déclencheur: Quotidien, répéter toutes les 1 heures")
    print(f"5. Action: {python_path}")
    print(f"6. Arguments: {project_path}\\run.py")
    print(f"7. Dossier de démarrage: {project_path}")
    
def main():
    """Fonction principale"""
    print("🤖 InfoWatchdog - Configuration des tâches automatiques")
    print("="*60)
    
    system = platform.system().lower()
    print(f"🖥️  Système détecté: {platform.system()}")
    print(f"📁 Projet: {get_project_path()}")
    print(f"🐍 Python: {get_python_path()}")
    
    if system in ['linux', 'darwin']:  # Linux ou macOS
        print("\n🔧 Options disponibles:")
        print("1. Cron job (recommandé)")
        print("2. Service systemd (Linux uniquement)")
        print("3. Afficher les deux options")
        
        choice = input("\nChoisissez une option (1-3): ").strip()
        
        if choice == "1":
            interval = input("Intervalle (hourly/daily/twice_daily/every_6h) [hourly]: ").strip() or "hourly"
            setup_cron_job(interval)
        elif choice == "2" and system == "linux":
            setup_systemd_service()
        elif choice == "3":
            interval = input("Intervalle pour cron (hourly/daily/twice_daily/every_6h) [hourly]: ").strip() or "hourly"
            setup_cron_job(interval)
            print("\n" + "="*60 + "\n")
            if system == "linux":
                setup_systemd_service()
        else:
            print("❌ Option invalide")
            
    elif system == 'windows':
        setup_windows_task()
    else:
        print(f"❌ Système non supporté: {system}")
        return

if __name__ == "__main__":
    main()