#!/usr/bin/env python3
"""
Script de configuration pour le pipeline Pipedrive vers BigQuery
Ce script aide à configurer les credentials et tester la connexion
"""

import os
import json
import dlt
from pipedrive import pipedrive_source


def configure_pipedrive_token():
    """Configure le token Pipedrive"""
    print("=== Configuration du token Pipedrive ===")
    print("1. Allez dans Pipedrive → Paramètres → Préférences personnelles → API")
    print("2. Copiez votre API Token")
    
    token = input("Entrez votre token Pipedrive: ").strip()
    
    if not token:
        print("❌ Token vide, configuration annulée")
        return False
    
    # Mettre à jour le fichier secrets.toml
    secrets_path = ".dlt/secrets.toml"
    if os.path.exists(secrets_path):
        with open(secrets_path, 'r') as f:
            content = f.read()
        
        # Remplacer le token
        content = content.replace('pipedrive_api_key = "<configure me>"', f'pipedrive_api_key = "{token}"')
        
        with open(secrets_path, 'w') as f:
            f.write(content)
        
        print("✅ Token Pipedrive configuré")
        return True
    else:
        print("❌ Fichier secrets.toml non trouvé")
        return False


def configure_bigquery():
    """Configure les credentials BigQuery"""
    print("\n=== Configuration BigQuery ===")
    print("Choisissez votre méthode d'authentification :")
    print("1. Service Account (fichier JSON)")
    print("2. Authentification par défaut (gcloud CLI)")
    
    choice = input("Votre choix (1 ou 2): ").strip()
    
    secrets_path = ".dlt/secrets.toml"
    
    if choice == "1":
        print("\n--- Configuration Service Account ---")
        project_id = input("Entrez votre Project ID: ").strip()
        client_email = input("Entrez l'email du service account: ").strip()
        
        print("Entrez votre clé privée (copiez-collez tout le contenu du fichier JSON):")
        print("(Terminez par Ctrl+D sur Mac/Linux ou Ctrl+Z sur Windows)")
        
        try:
            private_key_lines = []
            while True:
                try:
                    line = input()
                    private_key_lines.append(line)
                except EOFError:
                    break
            private_key = "\n".join(private_key_lines)
            
            if not project_id or not client_email or not private_key:
                print("❌ Configuration incomplète")
                return False
            
            # Mettre à jour le fichier secrets.toml
            if os.path.exists(secrets_path):
                with open(secrets_path, 'r') as f:
                    content = f.read()
                
                # Remplacer les valeurs BigQuery
                content = content.replace('project_id = "<configure me>"', f'project_id = "{project_id}"')
                content = content.replace('private_key = "<configure me>"', f'private_key = "{private_key}"')
                content = content.replace('client_email = "<configure me>"', f'client_email = "{client_email}"')
                
                with open(secrets_path, 'w') as f:
                    f.write(content)
                
                print("✅ Credentials BigQuery configurés")
                return True
            else:
                print("❌ Fichier secrets.toml non trouvé")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors de la configuration: {e}")
            return False
    
    elif choice == "2":
        print("\n--- Authentification par défaut ---")
        print("Assurez-vous que gcloud CLI est configuré :")
        print("gcloud auth application-default login")
        
        # Supprimer les credentials spécifiques pour utiliser l'auth par défaut
        if os.path.exists(secrets_path):
            with open(secrets_path, 'r') as f:
                content = f.read()
            
            # Supprimer les lignes de credentials spécifiques
            lines = content.split('\n')
            filtered_lines = []
            skip_credentials = False
            
            for line in lines:
                if '[destination.bigquery.credentials]' in line:
                    skip_credentials = True
                    continue
                elif line.startswith('[') and skip_credentials:
                    skip_credentials = False
                    filtered_lines.append(line)
                elif not skip_credentials:
                    filtered_lines.append(line)
            
            with open(secrets_path, 'w') as f:
                f.write('\n'.join(filtered_lines))
            
            print("✅ Configuration pour authentification par défaut")
            return True
        else:
            print("❌ Fichier secrets.toml non trouvé")
            return False
    
    else:
        print("❌ Choix invalide")
        return False


def test_pipedrive_connection():
    """Teste la connexion Pipedrive"""
    print("\n=== Test de connexion Pipedrive ===")
    try:
        source = pipedrive_source()
        print("✅ Connexion Pipedrive réussie")
        print(f"Ressources disponibles: {list(source.resources.keys())}")
        return True
    except Exception as e:
        print(f"❌ Erreur de connexion Pipedrive: {e}")
        return False


def test_bigquery_connection():
    """Teste la connexion BigQuery"""
    print("\n=== Test de connexion BigQuery ===")
    try:
        pipeline = dlt.pipeline(
            pipeline_name="test_pipedrive",
            destination='bigquery',
            dataset_name="test_dataset"
        )
        print("✅ Connexion BigQuery réussie")
        return True
    except Exception as e:
        print(f"❌ Erreur de connexion BigQuery: {e}")
        return False


def main():
    """Fonction principale de configuration"""
    print("🚀 Configuration du pipeline Pipedrive vers BigQuery")
    print("=" * 50)
    
    # Configuration Pipedrive
    pipedrive_ok = configure_pipedrive_token()
    
    # Configuration BigQuery
    bigquery_ok = configure_bigquery()
    
    if pipedrive_ok and bigquery_ok:
        print("\n=== Tests de connexion ===")
        
        # Test Pipedrive
        pipedrive_test = test_pipedrive_connection()
        
        # Test BigQuery
        bigquery_test = test_bigquery_connection()
        
        if pipedrive_test and bigquery_test:
            print("\n🎉 Configuration terminée avec succès!")
            print("\nProchaines étapes:")
            print("1. Exécutez: python3 pipedrive_pipeline.py")
            print("2. Vérifiez vos données dans BigQuery")
        else:
            print("\n⚠️  Configuration terminée mais certains tests ont échoué")
            print("Vérifiez vos credentials et réessayez")
    else:
        print("\n❌ Configuration incomplète")
        print("Veuillez réessayer avec des credentials valides")


if __name__ == "__main__":
    main()

