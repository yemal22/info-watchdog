#!/usr/bin/env python3
"""
Script de lancement du Dashboard Streamlit InfoWatchdog
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Vérifie et installe les dépendances nécessaires"""
    required_packages = [
        "streamlit",
        "plotly", 
        "pandas",
        "numpy"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} installé")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} manquant")
    
    if missing_packages:
        print(f"\n📦 Installation des dépendances manquantes...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install"
            ] + missing_packages)
            print("✅ Dépendances installées avec succès!")
        except subprocess.CalledProcessError:
            print("❌ Erreur lors de l'installation des dépendances")
            return False
    
    return True

def check_environment():
    """Vérifie la configuration de l'environnement"""
    required_vars = [
        "AIRTABLE_API_KEY",
        "AIRTABLE_BASE_ID", 
        "AIRTABLE_TABLE_NAME"
    ]
    
    # Charge le .env s'il existe
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv()
            print("✅ Fichier .env chargé")
        except ImportError:
            print("⚠️  python-dotenv non installé, variables d'environnement système utilisées")
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variables d'environnement manquantes: {', '.join(missing_vars)}")
        print("💡 Assurez-vous que votre fichier .env contient ces variables")
        return False
    
    print("✅ Configuration environnement OK")
    return True

def main():
    """Lance le dashboard Streamlit"""
    print("🐕‍🦺 InfoWatchdog Dashboard Launcher")
    print("=" * 50)
    
    # Vérifications préliminaires
    if not check_dependencies():
        print("❌ Impossible de continuer sans les dépendances")
        return 1
    
    if not check_environment():
        print("❌ Configuration environnement incomplète")
        return 1
    
    # Lance Streamlit
    dashboard_path = Path(__file__).parent / "dashboard_streamlit.py"
    
    if not dashboard_path.exists():
        print(f"❌ Dashboard non trouvé: {dashboard_path}")
        return 1
    
    print("🚀 Lancement du dashboard Streamlit...")
    print("📊 URL: http://localhost:8501")
    print("🔄 Actualisation automatique disponible")
    print("⚠️  Ctrl+C pour arrêter")
    print("-" * 50)
    
    try:
        # Lance Streamlit avec configuration optimisée
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            str(dashboard_path),
            "--server.port=8501",
            "--server.address=0.0.0.0",
            "--browser.gatherUsageStats=false",
            "--server.headless=false"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Dashboard arrêté par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())