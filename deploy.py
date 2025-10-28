#!/usr/bin/env python3
"""
Script de déploiement pour le pipeline Pipedrive
Ce script peut être utilisé pour automatiser le déploiement
"""

import os
import sys
import subprocess
import json
from datetime import datetime


def check_requirements():
    """Vérifie que tous les prérequis sont installés"""
    print("🔍 Vérification des prérequis...")
    
    # Vérifier Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ requis")
        return False
    
    # Vérifier dlt
    try:
        import dlt
        print(f"✅ dlt version {dlt.__version__} installé")
    except ImportError:
        print("❌ dlt non installé")
        return False
    
    # Vérifier les fichiers requis
    required_files = [
        "requirements.txt",
        "pipedrive_pipeline.py",
        "pipedrive_main.py",
        ".dlt/secrets.toml"
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Fichier manquant: {file}")
            return False
        else:
            print(f"✅ {file} trouvé")
    
    return True


def install_dependencies():
    """Installe les dépendances"""
    print("📦 Installation des dépendances...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True)
        print("✅ Dépendances installées")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'installation: {e}")
        return False


def test_configuration():
    """Teste la configuration"""
    print("🧪 Test de la configuration...")
    
    try:
        from pipedrive import pipedrive_source
        source = pipedrive_source()
        print("✅ Configuration Pipedrive OK")
        
        import dlt
        pipeline = dlt.pipeline(
            pipeline_name="test",
            destination='bigquery',
            dataset_name="test"
        )
        print("✅ Configuration BigQuery OK")
        
        return True
    except Exception as e:
        print(f"❌ Erreur de configuration: {e}")
        return False


def run_sample_load():
    """Exécute un chargement d'échantillon"""
    print("🚀 Exécution d'un chargement d'échantillon...")
    
    try:
        # Charger seulement quelques ressources pour tester
        result = subprocess.run([
            sys.executable, "pipedrive_main.py", 
            "--mode", "selected",
            "--resources", "persons", "custom_fields_mapping"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Chargement d'échantillon réussi")
            return True
        else:
            print(f"❌ Erreur lors du chargement: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        return False


def create_deployment_log():
    """Crée un log de déploiement"""
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "python_version": sys.version,
        "dlt_version": None,
        "status": "unknown"
    }
    
    try:
        import dlt
        log_data["dlt_version"] = dlt.__version__
    except ImportError:
        pass
    
    with open("deployment_log.json", "w") as f:
        json.dump(log_data, f, indent=2)
    
    print("📝 Log de déploiement créé")


def main():
    """Fonction principale de déploiement"""
    print("🚀 Déploiement du pipeline Pipedrive vers BigQuery")
    print("=" * 50)
    
    steps = [
        ("Vérification des prérequis", check_requirements),
        ("Installation des dépendances", install_dependencies),
        ("Test de configuration", test_configuration),
        ("Chargement d'échantillon", run_sample_load),
    ]
    
    for step_name, step_func in steps:
        print(f"\n--- {step_name} ---")
        if not step_func():
            print(f"❌ Échec à l'étape: {step_name}")
            print("Veuillez corriger les erreurs et réessayer")
            return 1
    
    print("\n🎉 Déploiement terminé avec succès!")
    print("\nProchaines étapes:")
    print("1. Configurez vos credentials dans .dlt/secrets.toml")
    print("2. Exécutez: python3 pipedrive_main.py --mode all")
    print("3. Vérifiez vos données dans BigQuery")
    
    create_deployment_log()
    return 0


if __name__ == "__main__":
    exit(main())

