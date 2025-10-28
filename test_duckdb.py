#!/usr/bin/env python3
"""
Script de test avec DuckDB pour vérifier les données Pipedrive
avant la migration vers BigQuery
"""

import dlt
from pipedrive import pipedrive_source


def test_with_duckdb():
    """Teste le chargement avec DuckDB local"""
    print("🦆 Test avec DuckDB local...")
    
    # Créer un pipeline avec DuckDB
    pipeline = dlt.pipeline(
        pipeline_name="pipedrive_test",
        destination='duckdb',
        dataset_name="pipedrive_data"
    )
    
    print("📊 Chargement d'un échantillon de données...")
    
    # Charger seulement quelques ressources pour le test
    source = pipedrive_source().with_resources(
        "persons", "deals", "organizations", "custom_fields_mapping"
    )
    
    load_info = pipeline.run(source)
    print("✅ Chargement terminé!")
    print(load_info)
    
    # Afficher les statistiques
    print("\n📈 Statistiques du chargement:")
    for table_name, table_info in load_info.load_packages[0].schema_update.items():
        if hasattr(table_info, 'table_name'):
            print(f"  - {table_info.table_name}: {table_info.row_count} lignes")
    
    return pipeline


def explore_data(pipeline):
    """Explore les données chargées"""
    print("\n🔍 Exploration des données...")
    
    # Se connecter à la base DuckDB
    with pipeline.sql_client() as client:
        # Lister les tables
        tables = client.execute_sql("SHOW TABLES;")
        print(f"\n📋 Tables créées: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Exemple de requête sur les deals
        try:
            deals_count = client.execute_sql("SELECT COUNT(*) FROM deals;")
            print(f"\n💼 Nombre de deals: {deals_count[0][0]}")
            
            # Afficher quelques deals
            sample_deals = client.execute_sql("SELECT id, title, value, stage_id FROM deals LIMIT 5;")
            print("\n📋 Échantillon de deals:")
            for deal in sample_deals:
                print(f"  - ID: {deal[0]}, Titre: {deal[1]}, Valeur: {deal[2]}, Stage: {deal[3]}")
                
        except Exception as e:
            print(f"⚠️  Erreur lors de l'exploration des deals: {e}")
        
        # Exemple de requête sur les personnes
        try:
            persons_count = client.execute_sql("SELECT COUNT(*) FROM persons;")
            print(f"\n👥 Nombre de personnes: {persons_count[0][0]}")
            
        except Exception as e:
            print(f"⚠️  Erreur lors de l'exploration des personnes: {e}")


def main():
    """Fonction principale de test"""
    print("🧪 Test du pipeline Pipedrive avec DuckDB")
    print("=" * 50)
    
    try:
        # Test du chargement
        pipeline = test_with_duckdb()
        
        # Exploration des données
        explore_data(pipeline)
        
        print("\n🎉 Test réussi!")
        print("\nProchaines étapes:")
        print("1. Vos données Pipedrive sont correctement chargées")
        print("2. Vous pouvez maintenant configurer BigQuery")
        print("3. Exécuter le chargement complet vers BigQuery")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

