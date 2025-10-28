#!/usr/bin/env python3
"""
Script pour configurer les secrets GitHub Actions
Ce script vous guide pour configurer les secrets nécessaires
"""

import os
import json
import subprocess
import sys


def check_git_repo():
    """Vérifie si nous sommes dans un repo Git"""
    try:
        result = subprocess.run(['git', 'rev-parse', '--git-dir'], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def init_git_repo():
    """Initialise un repo Git si nécessaire"""
    if not check_git_repo():
        print("🔧 Initialisation du repository Git...")
        subprocess.run(['git', 'init'], check=True)
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit: Pipedrive to BigQuery pipeline'], check=True)
        print("✅ Repository Git initialisé")
    else:
        print("✅ Repository Git déjà initialisé")


def create_service_account_key():
    """Guide pour créer une clé de service account"""
    print("\n🔑 CONFIGURATION DU SERVICE ACCOUNT GOOGLE CLOUD")
    print("=" * 60)
    print("1. Allez sur Google Cloud Console:")
    print("   https://console.cloud.google.com/iam-admin/serviceaccounts")
    print("2. Sélectionnez votre projet: pipedrive-476423")
    print("3. Cliquez sur 'Créer un service account'")
    print("4. Nom: pipedrive-github-actions")
    print("5. Description: Service account pour GitHub Actions")
    print("6. Cliquez sur 'Créer et continuer'")
    print("7. Rôles à ajouter:")
    print("   - BigQuery Data Editor")
    print("   - BigQuery Job User")
    print("8. Cliquez sur 'Terminé'")
    print("9. Cliquez sur le service account créé")
    print("10. Allez dans l'onglet 'Clés'")
    print("11. Cliquez sur 'Ajouter une clé' > 'Créer une nouvelle clé'")
    print("12. Type: JSON")
    print("13. Téléchargez le fichier JSON")
    print("\n⚠️  IMPORTANT: Gardez ce fichier JSON en sécurité!")
    print("   Ne le commitez JAMAIS dans Git!")


def setup_github_secrets():
    """Guide pour configurer les secrets GitHub"""
    print("\n🔐 CONFIGURATION DES SECRETS GITHUB")
    print("=" * 60)
    print("1. Allez sur votre repository GitHub")
    print("2. Cliquez sur 'Settings' (Paramètres)")
    print("3. Dans le menu de gauche, cliquez sur 'Secrets and variables' > 'Actions'")
    print("4. Cliquez sur 'New repository secret'")
    print("\n📋 Secrets à créer:")
    print("\n🔑 PIPEDRIVE_API_KEY")
    print("   Valeur: votre_token_pipedrive")
    print("   (celui que vous avez déjà: 75dd800edb5c4a0da9860a789b0b6c47aeebcc8d)")
    
    print("\n🔑 GCP_PROJECT_ID")
    print("   Valeur: pipedrive-476423")
    
    print("\n🔑 GCP_SA_KEY")
    print("   Valeur: le contenu complet du fichier JSON du service account")
    print("   (copiez-collez tout le contenu du fichier JSON)")
    
    print("\n⚠️  IMPORTANT:")
    print("   - Ne partagez JAMAIS ces secrets")
    print("   - Ils sont chiffrés par GitHub")
    print("   - Seuls les workflows GitHub Actions peuvent y accéder")


def create_env_example():
    """Crée un fichier .env.example"""
    env_example = """# Configuration pour GitHub Actions
# Ces valeurs doivent être configurées comme secrets GitHub

# Token API Pipedrive
PIPEDRIVE_API_KEY=your_pipedrive_api_key_here

# Projet Google Cloud
GCP_PROJECT_ID=pipedrive-476423

# Service Account Key (contenu JSON complet)
GCP_SA_KEY={"type": "service_account", "project_id": "pipedrive-476423", ...}

# Configuration BigQuery
BIGQUERY_LOCATION=US
BIGQUERY_DATASET_NAME=pipedrive_data
"""
    
    with open('.env.example', 'w') as f:
        f.write(env_example)
    
    print("✅ Fichier .env.example créé")


def create_gitignore():
    """Crée un fichier .gitignore approprié"""
    gitignore_content = """# Secrets et credentials
.env
*.json
secrets.toml
.dlt/secrets.toml

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log

# DuckDB files
*.duckdb
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    
    print("✅ Fichier .gitignore créé")


def main():
    """Fonction principale de configuration"""
    print("🚀 CONFIGURATION DU SCHEDULER GITHUB ACTIONS")
    print("=" * 60)
    print("Ce script vous guide pour configurer l'automatisation")
    print("de vos données Pipedrive vers BigQuery")
    
    # Initialiser Git
    init_git_repo()
    
    # Créer les fichiers de configuration
    create_env_example()
    create_gitignore()
    
    # Guide pour le service account
    create_service_account_key()
    
    # Guide pour les secrets GitHub
    setup_github_secrets()
    
    print("\n🎉 CONFIGURATION TERMINÉE!")
    print("=" * 60)
    print("Prochaines étapes:")
    print("1. ✅ Créez le service account Google Cloud")
    print("2. ✅ Configurez les secrets GitHub")
    print("3. ✅ Commitez et poussez votre code:")
    print("   git add .")
    print("   git commit -m 'Add GitHub Actions workflow'")
    print("   git push origin main")
    print("4. ✅ Le workflow s'exécutera automatiquement chaque jour à 6h UTC")
    print("5. ✅ Vous pouvez aussi l'exécuter manuellement dans GitHub Actions")
    
    print("\n📚 Documentation:")
    print("- Workflow principal: .github/workflows/pipedrive-sync.yml")
    print("- Workflow de test: .github/workflows/test-sync.yml")
    print("- Script d'exécution: github_actions_sync.py")


if __name__ == "__main__":
    main()
