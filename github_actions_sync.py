#!/usr/bin/env python3
"""
Script optimisé pour GitHub Actions
Chargement incrémental des données Pipedrive vers BigQuery
"""

import os
import sys
import dlt
from datetime import datetime, timedelta
from pipedrive import pipedrive_source


def load_incremental_data():
    """Charge les données de manière incrémentale depuis les 7 derniers jours"""
    print("🔄 Chargement incrémental des données Pipedrive...")
    
    # Calculer la date de début (7 jours en arrière)
    since_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%SZ")
    print(f"📅 Chargement des données depuis: {since_date}")
    
    # Configuration du pipeline
    pipeline = dlt.pipeline(
        pipeline_name="pipedrive_github_actions",
        destination='bigquery',
        dataset_name="pipedrive_data"
    )
    
    # Charger les données incrémentales
    source = pipedrive_source(since_timestamp=since_date)
    load_info = pipeline.run(source)
    
    print("✅ Chargement incrémental terminé!")
    print(f"📊 Package chargé: {load_info.load_packages[0].load_id}")
    
    # Afficher les statistiques
    for table_name, table_info in load_info.load_packages[0].schema_update.items():
        if hasattr(table_info, 'table_name') and hasattr(table_info, 'row_count'):
            print(f"  - {table_info.table_name}: {table_info.row_count} lignes")
    
    return load_info


def main():
    """Fonction principale"""
    print("🚀 Pipeline Pipedrive vers BigQuery (GitHub Actions)")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Environment: {os.getenv('GITHUB_ACTIONS', 'local')}")
    
    try:
        # Vérifier les variables d'environnement
        required_vars = ['PIPEDRIVE_API_KEY', 'GCP_PROJECT_ID']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            print(f"❌ Variables d'environnement manquantes: {missing_vars}")
            return 1
        
        print("✅ Variables d'environnement configurées")
        
        # Exécuter le chargement
        load_info = load_incremental_data()
        
        print("\n🎉 Synchronisation terminée avec succès!")
        print(f"📈 Données synchronisées vers BigQuery")
        
        return 0
        
    except Exception as e:
        print(f"❌ Erreur lors de la synchronisation: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
