#!/usr/bin/env python3
"""
Pipeline Pipedrive vers BigQuery avec dlt
Script principal pour l'ingestion des données
"""

import dlt
import argparse
from datetime import datetime, timedelta
from pipedrive import pipedrive_source


def load_all_data(pipeline_name="pipedrive", dataset_name="pipedrive_data"):
    """Charge toutes les données Pipedrive"""
    print("🔄 Chargement de toutes les données Pipedrive...")
    
    pipeline = dlt.pipeline(
        pipeline_name=pipeline_name,
        destination='bigquery',
        dataset_name=dataset_name
    )
    
    load_info = pipeline.run(pipedrive_source())
    print("✅ Chargement terminé!")
    print(load_info)
    return load_info


def load_selected_resources(resources, pipeline_name="pipedrive", dataset_name="pipedrive_data"):
    """Charge seulement les ressources sélectionnées"""
    print(f"🔄 Chargement des ressources: {', '.join(resources)}")
    
    pipeline = dlt.pipeline(
        pipeline_name=pipeline_name,
        destination='bigquery',
        dataset_name=dataset_name
    )
    
    # Toujours inclure custom_fields_mapping pour la traduction des champs
    if "custom_fields_mapping" not in resources:
        resources.append("custom_fields_mapping")
    
    source = pipedrive_source().with_resources(*resources)
    load_info = pipeline.run(source)
    print("✅ Chargement terminé!")
    print(load_info)
    return load_info


def load_incremental(since_date, resources=None, pipeline_name="pipedrive", dataset_name="pipedrive_data"):
    """Charge les données de manière incrémentale depuis une date donnée"""
    print(f"🔄 Chargement incrémental depuis {since_date}...")
    
    pipeline = dlt.pipeline(
        pipeline_name=pipeline_name,
        destination='bigquery',
        dataset_name=dataset_name
    )
    
    if resources:
        # Charger seulement les ressources spécifiées
        if "custom_fields_mapping" not in resources:
            resources.append("custom_fields_mapping")
        source = pipedrive_source(since_timestamp=since_date).with_resources(*resources)
    else:
        # Charger toutes les ressources
        source = pipedrive_source(since_timestamp=since_date)
    
    load_info = pipeline.run(source)
    print("✅ Chargement incrémental terminé!")
    print(load_info)
    return load_info


def show_available_resources():
    """Affiche les ressources disponibles"""
    print("📋 Ressources disponibles dans Pipedrive:")
    
    source = pipedrive_source()
    resources = list(source.resources.keys())
    
    for i, resource in enumerate(resources, 1):
        print(f"{i:2d}. {resource}")
    
    print(f"\nTotal: {len(resources)} ressources")
    return resources


def get_pipeline_info(pipeline_name="pipedrive"):
    """Affiche les informations du pipeline"""
    try:
        pipeline = dlt.pipeline(pipeline_name=pipeline_name)
        print(f"📊 Informations du pipeline '{pipeline_name}':")
        print(f"   Destination: {pipeline.destination}")
        print(f"   Dataset: {pipeline.dataset_name}")
        print(f"   Dernière exécution: {pipeline.last_trace}")
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des infos: {e}")


def main():
    parser = argparse.ArgumentParser(description="Pipeline Pipedrive vers BigQuery")
    parser.add_argument("--mode", choices=["all", "selected", "incremental", "info", "resources"], 
                       default="all", help="Mode d'exécution")
    parser.add_argument("--resources", nargs="+", 
                       help="Ressources à charger (pour mode 'selected')")
    parser.add_argument("--since", 
                       help="Date de début pour le chargement incrémental (format: YYYY-MM-DD)")
    parser.add_argument("--pipeline-name", default="pipedrive",
                       help="Nom du pipeline")
    parser.add_argument("--dataset-name", default="pipedrive_data",
                       help="Nom du dataset BigQuery")
    
    args = parser.parse_args()
    
    print("🚀 Pipeline Pipedrive vers BigQuery")
    print("=" * 40)
    
    try:
        if args.mode == "all":
            load_all_data(args.pipeline_name, args.dataset_name)
            
        elif args.mode == "selected":
            if not args.resources:
                print("❌ Veuillez spécifier les ressources avec --resources")
                print("Exemple: --resources deals persons products")
                return
            load_selected_resources(args.resources, args.pipeline_name, args.dataset_name)
            
        elif args.mode == "incremental":
            if not args.since:
                # Par défaut, charger depuis il y a 7 jours
                since_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%SZ")
                print(f"📅 Aucune date spécifiée, utilisation de la date par défaut: {since_date}")
            else:
                since_date = f"{args.since} 00:00:00Z"
            
            load_incremental(since_date, args.resources, args.pipeline_name, args.dataset_name)
            
        elif args.mode == "resources":
            show_available_resources()
            
        elif args.mode == "info":
            get_pipeline_info(args.pipeline_name)
            
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

