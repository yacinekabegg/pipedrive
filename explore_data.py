#!/usr/bin/env python3
"""
Script d'exploration des données Pipedrive dans BigQuery
Ce script vous permet d'explorer facilement vos données
"""

import subprocess
import sys
import json
from datetime import datetime


def run_bq_query(query, description=""):
    """Exécute une requête BigQuery et affiche les résultats"""
    if description:
        print(f"\n📊 {description}")
        print("=" * 50)
    
    try:
        result = subprocess.run([
            "bq", "query", "--use_legacy_sql=false", 
            "--format=prettyjson", "--max_rows=20", query
        ], capture_output=True, text=True, check=True)
        
        data = json.loads(result.stdout)
        if isinstance(data, list) and len(data) > 0:
            # Afficher les résultats de manière lisible
            if isinstance(data[0], dict):
                # Afficher les clés comme en-têtes
                headers = list(data[0].keys())
                print(" | ".join(f"{h:^15}" for h in headers))
                print("-" * (len(headers) * 17))
                
                for row in data[:10]:  # Limiter à 10 lignes
                    values = [str(row.get(h, ""))[:15] for h in headers]
                    print(" | ".join(f"{v:^15}" for v in values))
            else:
                print(data)
        else:
            print("Aucun résultat trouvé")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur: {e.stderr}")
    except json.JSONDecodeError:
        print("❌ Erreur de format JSON")


def explore_deals():
    """Explore les données des deals"""
    print("\n🎯 EXPLORATION DES DEALS")
    print("=" * 50)
    
    # Top deals par valeur
    run_bq_query(
        "SELECT title, value, stage_id, add_time FROM `pipedrive-476423.pipedrive_data.deals` WHERE value > 0 ORDER BY value DESC LIMIT 10",
        "Top 10 des deals par valeur"
    )
    
    # Deals par stage
    run_bq_query(
        "SELECT stage_id, COUNT(*) as nb_deals FROM `pipedrive-476423.pipedrive_data.deals` GROUP BY stage_id ORDER BY nb_deals DESC LIMIT 10",
        "Deals par stage"
    )


def explore_persons():
    """Explore les données des personnes"""
    print("\n👥 EXPLORATION DES PERSONNES")
    print("=" * 50)
    
    # Organisations avec le plus de personnes
    run_bq_query(
        "SELECT org_name, COUNT(*) as nb_personnes FROM `pipedrive-476423.pipedrive_data.persons` WHERE org_name IS NOT NULL GROUP BY org_name ORDER BY nb_personnes DESC LIMIT 10",
        "Organisations avec le plus de personnes"
    )
    
    # Personnes récemment ajoutées
    run_bq_query(
        "SELECT name, org_name, add_time FROM `pipedrive-476423.pipedrive_data.persons` ORDER BY add_time DESC LIMIT 10",
        "Personnes récemment ajoutées"
    )


def explore_activities():
    """Explore les données des activités"""
    print("\n📈 EXPLORATION DES ACTIVITÉS")
    print("=" * 50)
    
    # Activités par type
    run_bq_query(
        "SELECT type, COUNT(*) as nb_activites FROM `pipedrive-476423.pipedrive_data.activities` GROUP BY type ORDER BY nb_activites DESC LIMIT 10",
        "Activités par type"
    )
    
    # Activités par mois
    run_bq_query(
        "SELECT EXTRACT(YEAR FROM PARSE_DATE('%Y-%m-%d', due_date)) as annee, EXTRACT(MONTH FROM PARSE_DATE('%Y-%m-%d', due_date)) as mois, COUNT(*) as nb_activites FROM `pipedrive-476423.pipedrive_data.activities` WHERE due_date IS NOT NULL GROUP BY annee, mois ORDER BY annee DESC, mois DESC LIMIT 10",
        "Activités par mois"
    )


def explore_organizations():
    """Explore les données des organisations"""
    print("\n🏢 EXPLORATION DES ORGANISATIONS")
    print("=" * 50)
    
    # Organisations récemment ajoutées
    run_bq_query(
        "SELECT name, add_time FROM `pipedrive-476423.pipedrive_data.organizations` ORDER BY add_time DESC LIMIT 10",
        "Organisations récemment ajoutées"
    )


def custom_query():
    """Permet d'exécuter une requête personnalisée"""
    print("\n🔍 REQUÊTE PERSONNALISÉE")
    print("=" * 50)
    print("Entrez votre requête SQL (ou 'quit' pour quitter):")
    
    while True:
        query = input("\nSQL> ").strip()
        if query.lower() == 'quit':
            break
        if query:
            run_bq_query(query, "Résultat de votre requête")


def main():
    """Menu principal"""
    print("🚀 EXPLORATEUR DE DONNÉES PIPEDRIVE")
    print("=" * 50)
    print("Vos données sont maintenant dans BigQuery !")
    print(f"Projet: pipedrive-476423")
    print(f"Dataset: pipedrive_data")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    while True:
        print("\n📋 MENU D'EXPLORATION:")
        print("1. 🎯 Explorer les deals")
        print("2. 👥 Explorer les personnes")
        print("3. 📈 Explorer les activités")
        print("4. 🏢 Explorer les organisations")
        print("5. 🔍 Requête personnalisée")
        print("6. ❌ Quitter")
        
        choice = input("\nVotre choix (1-6): ").strip()
        
        if choice == "1":
            explore_deals()
        elif choice == "2":
            explore_persons()
        elif choice == "3":
            explore_activities()
        elif choice == "4":
            explore_organizations()
        elif choice == "5":
            custom_query()
        elif choice == "6":
            print("👋 Au revoir !")
            break
        else:
            print("❌ Choix invalide, veuillez réessayer")


if __name__ == "__main__":
    main()

