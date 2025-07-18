#!/usr/bin/env python3
"""
Script principal pour lancer InfoWatchdog.
Usage: python run.py [--test-only] [--config path/to/config.yml]
"""

import argparse
import sys
import os

# Ajoute le répertoire src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import InfoWatchdog
from src.utils.logo import (
    display_watchdog_logo, display_status_banner, display_working_banner,
    display_collection_report, display_alert_banner
)

def main():
    """Fonction principale."""
    # Affiche le logo watchdog au démarrage
    print(display_watchdog_logo())
    
    parser = argparse.ArgumentParser(description="InfoWatchdog - Agent de veille environnementale")
    parser.add_argument(
        "--test-only", 
        action="store_true", 
        help="Teste uniquement les connexions sans collecter de données"
    )
    parser.add_argument(
        "--config", 
        default="config/config.yml", 
        help="Chemin vers le fichier de configuration"
    )
    parser.add_argument(
        "--stats", 
        action="store_true", 
        help="Affiche les statistiques du système"
    )
    parser.add_argument(
        "--no-logo", 
        action="store_true", 
        help="Désactive l'affichage du logo"
    )
    parser.add_argument(
        "--alert-mode", 
        action="store_true", 
        help="Active les alertes visuelles"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialise InfoWatchdog
        config_file = args.config if args.config else "config/config.yml"
        watchdog = InfoWatchdog(config_file)
        
        if args.test_only:
            # Test des connexions uniquement
            print("\n🧪 Testing connections...")
            if not args.no_logo:
                print(display_working_banner())
            results = watchdog.test_connections()
            
            print("\nConnection Test Results:")
            for component, status in results.items():
                status_icon = "✅" if status else "❌"
                print(f"  {status_icon} {component}: {'OK' if status else 'FAILED'}")
            
            # Vérifie si tous les tests ont réussi
            all_passed = all(results.values())
            print(f"\nOverall status: {'✅ All tests passed' if all_passed else '❌ Some tests failed'}")
            
            return 0 if all_passed else 1
        
        elif args.stats:
            # Affiche les statistiques
            print("\n📊 InfoWatchdog Statistics...")
            stats = watchdog.get_stats()
            
            print(f"\nCollectors:")
            print(f"  Total: {stats['collectors']['total']}")
            print(f"  Enabled: {stats['collectors']['enabled']}")
            
            if 'storage' in stats:
                storage_stats = stats['storage']
                print(f"\nStorage:")
                if 'total_articles' in storage_stats:
                    print(f"  Total articles: {storage_stats['total_articles']}")
                if 'recent_articles_7days' in storage_stats:
                    print(f"  Recent articles (7 days): {storage_stats['recent_articles_7days']}")
                if 'articles_by_source' in storage_stats:
                    print(f"  Sources: {list(storage_stats['articles_by_source'].keys())}")
            
            return 0
        
        else:
            # Exécute un cycle de collecte complet
            print("\n🐕‍🦺 Starting InfoWatchdog patrol mission...")
            
            # Affiche la bannière de travail
            if not args.no_logo:
                print(display_working_banner())
            
            # Lance la collecte
            success = watchdog.run_collection_cycle()
            
            # Récupère les métriques
            duration = getattr(watchdog, '_last_cycle_duration', 0)
            total_articles = getattr(watchdog, '_last_articles_collected', 0)
            
            # Affiche le rapport avec chien gardien
            if not args.no_logo:
                print(display_collection_report(total_articles, duration, success))
            else:
                storage_success = "✅" if success else "❌"
                print(f"\nCollection Report:")
                print(f"  Duration: {duration:.2f} seconds")
                print(f"  Articles collected: {total_articles}")
                print(f"  Storage success: {storage_success}")
            
            # Alerte si articles trouvés et mode alerte activé
            if args.alert_mode and total_articles > 0:
                print(display_alert_banner())
            
            if success:
                print("\n🎉 Woof! Mission accomplished successfully!")
            else:
                print("\n⚠️  Woof woof... Mission completed with some issues.")
                
    except KeyboardInterrupt:
        print("\n\n⚠️  Patrol interrupted by human! 🐕")
        print("    *sad puppy eyes* - InfoWatchdog going to sleep...")
    except Exception as e:
        print(f"\n❌ Critical error detected! Watchdog needs help: {str(e)}")
        print("    *whimper* - Please check the logs...")
        sys.exit(1)

if __name__ == "__main__":
    main()