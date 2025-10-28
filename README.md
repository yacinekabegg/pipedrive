# Pipeline Pipedrive vers BigQuery avec dlt

Ce projet utilise dlt pour ingérer les données de Pipedrive dans BigQuery.

## Configuration des Credentials

### 1. Configuration Pipedrive

1. Connectez-vous à votre compte Pipedrive
2. Allez dans **Paramètres** → **Préférences personnelles** → **API**
3. Copiez votre **API Token**
4. Remplacez `<configure me>` dans `.dlt/secrets.toml` par votre token :

```toml
[sources.pipedrive]
pipedrive_api_key = "votre_token_pipedrive_ici"
```

### 2. Configuration BigQuery

#### Option A : Service Account (Recommandé)

1. Allez dans [Google Cloud Console](https://console.cloud.google.com/)
2. Sélectionnez votre projet BigQuery
3. Allez dans **IAM & Admin** → **Service Accounts**
4. Créez un nouveau service account ou utilisez un existant
5. Ajoutez les rôles suivants :
   - `BigQuery Data Editor`
   - `BigQuery Job User`
6. Créez une clé JSON pour ce service account
7. Téléchargez le fichier JSON

Configurez ensuite `.dlt/secrets.toml` :

```toml
[destination.bigquery]
location = "US"  # ou votre région préférée

[destination.bigquery.credentials]
project_id = "votre-project-id"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "votre-service-account@votre-project.iam.gserviceaccount.com"
```

#### Option B : Authentification par défaut

Si vous avez configuré `gcloud` CLI, vous pouvez utiliser l'authentification par défaut :

```toml
[destination.bigquery]
location = "US"
```

Dans ce cas, dlt utilisera automatiquement les credentials de votre environnement.

## Installation des dépendances

```bash
pip3 install -r requirements.txt
```

## Exécution du pipeline

### Chargement complet des données

```bash
python3 pipedrive_pipeline.py
```

### Chargement sélectif

Modifiez `pipedrive_pipeline.py` pour charger seulement certaines tables :

```python
def load_selected_data():
    pipeline = dlt.pipeline(
        pipeline_name="pipedrive", 
        destination='bigquery', 
        dataset_name="pipedrive_data"
    )
    
    load_info = pipeline.run(
        pipedrive_source().with_resources(
            "products", "deals", "persons", "custom_fields_mapping"
        )
    )
    print(load_info)
```

## Tables disponibles

Le pipeline charge les tables suivantes de Pipedrive :

- `activities` - Activités et tâches
- `organizations` - Organisations/entreprises
- `persons` - Contacts individuels
- `products` - Produits/services
- `deals` - Opportunités de vente
- `pipelines` - Processus de vente
- `stages` - Étapes du processus
- `users` - Utilisateurs de la plateforme
- `custom_fields_mapping` - Mapping des champs personnalisés

## Vérification des données

Après l'exécution, vous pouvez vérifier les données dans BigQuery :

```sql
SELECT * FROM `votre-project.pipedrive_data.deals` LIMIT 10;
```

## Chargement incrémental

Pour charger seulement les données mises à jour depuis une date donnée :

```python
def load_from_start_date():
    pipeline = dlt.pipeline(
        pipeline_name="pipedrive", 
        destination='bigquery', 
        dataset_name="pipedrive_data"
    )
    
    activities_source = pipedrive_source(
        since_timestamp="2023-03-01 00:00:00Z"
    ).with_resources("activities", "custom_fields_mapping")
    
    load_info = pipeline.run(activities_source)
    print(load_info)
```

