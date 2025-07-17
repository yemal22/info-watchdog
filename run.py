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

def main():
    """Fonction principale."""
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
    
    args = parser.parse_args()
    
    try:
        # Initialise InfoWatchdog
        watchdog = InfoWatchdog(config_path=args.config)
        
        if args.test_only:
            # Test des connexions uniquement
            print("Testing connections...")
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
            print("System Statistics:")
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
            print("Starting InfoWatchdog collection cycle...")
            
            report = watchdog.run_collection_cycle()
            
            print(f"\nCollection Report:")
            print(f"  Duration: {report['duration_seconds']:.2f} seconds")
            print(f"  Articles collected: {report['articles_collected']}")
            print(f"  Storage success: {'✅' if report['storage_success'] else '❌'}")
            
            return 0 if report['storage_success'] else 1
            
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)