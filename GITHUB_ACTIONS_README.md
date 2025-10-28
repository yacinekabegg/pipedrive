# 🚀 Pipeline Pipedrive vers BigQuery avec GitHub Actions

Ce projet automatise la synchronisation quotidienne de vos données Pipedrive vers BigQuery en utilisant GitHub Actions.

## 📋 Fonctionnalités

- ✅ **Synchronisation quotidienne** automatique (6h00 UTC)
- ✅ **Chargement incrémental** (seulement les données récentes)
- ✅ **Exécution manuelle** possible
- ✅ **Tests automatisés** avec DuckDB
- ✅ **Notifications** en cas d'erreur
- ✅ **Logs détaillés** pour le debugging

## 🔧 Configuration

### 1. Prérequis

- Repository GitHub
- Projet Google Cloud avec facturation activée
- Token API Pipedrive

### 2. Configuration automatique

Exécutez le script de configuration :

```bash
python3 setup_github_actions.py
```

### 3. Configuration manuelle

#### A. Créer un Service Account Google Cloud

1. Allez sur [Google Cloud Console](https://console.cloud.google.com/iam-admin/serviceaccounts)
2. Sélectionnez votre projet : `pipedrive-476423`
3. Créez un service account : `pipedrive-github-actions`
4. Ajoutez les rôles :
   - `BigQuery Data Editor`
   - `BigQuery Job User`
5. Créez une clé JSON et téléchargez-la

#### B. Configurer les secrets GitHub

Dans votre repository GitHub > Settings > Secrets and variables > Actions :

| Secret | Description | Exemple |
|--------|-------------|---------|
| `PIPEDRIVE_API_KEY` | Token API Pipedrive | `75dd800edb5c4a0da9860a789b0b6c47aeebcc8d` |
| `GCP_PROJECT_ID` | ID du projet Google Cloud | `pipedrive-476423` |
| `GCP_SA_KEY` | Contenu JSON du service account | `{"type": "service_account", ...}` |

## 📅 Planification

Le workflow s'exécute automatiquement :

- **Quotidien** : Tous les jours à 6h00 UTC (8h00 heure française)
- **Manuel** : Via l'interface GitHub Actions
- **Push** : À chaque push sur main/master

## 🔍 Monitoring

### Vérifier l'exécution

1. Allez dans votre repository GitHub
2. Cliquez sur l'onglet "Actions"
3. Consultez les logs du workflow "Pipedrive to BigQuery Daily Sync"

### Logs en cas d'erreur

En cas d'échec, les logs sont automatiquement sauvegardés comme artefacts.

## 📊 Données synchronisées

Le pipeline charge toutes les ressources Pipedrive :

- **Deals** : Opportunités de vente
- **Persons** : Contacts individuels
- **Organizations** : Organisations/entreprises
- **Activities** : Activités et tâches
- **Products** : Produits/services
- **Et plus...** (18 ressources au total)

## 🛠️ Développement

### Tests locaux

```bash
# Test avec DuckDB
python3 test_duckdb.py

# Test de configuration
python3 pipedrive_main.py --mode resources
```

### Tests GitHub Actions

Le workflow de test s'exécute automatiquement sur :
- Pull requests
- Exécution manuelle

## 📈 Performance

- **Chargement initial** : ~3-5 minutes
- **Chargement incrémental** : ~1-2 minutes
- **Fréquence** : Quotidienne
- **Données** : Seulement les modifications des 7 derniers jours

## 🔧 Dépannage

### Erreurs courantes

1. **"Billing not enabled"**
   - Solution : Activez la facturation sur Google Cloud

2. **"Authentication failed"**
   - Solution : Vérifiez les secrets GitHub

3. **"Permission denied"**
   - Solution : Vérifiez les rôles du service account

### Logs utiles

```bash
# Vérifier les données dans BigQuery
bq ls pipedrive-476423:pipedrive_data

# Compter les lignes
bq query --use_legacy_sql=false "SELECT COUNT(*) FROM \`pipedrive-476423.pipedrive_data.deals\`"
```

## 📚 Structure du projet

```
.github/workflows/
├── pipedrive-sync.yml      # Workflow principal
└── test-sync.yml          # Workflow de test

Scripts:
├── github_actions_sync.py  # Script optimisé pour GitHub Actions
├── setup_github_actions.py # Configuration automatique
└── explore_data.py         # Exploration des données
```

## 🎯 Prochaines étapes

1. **Monitoring avancé** : Intégration avec Slack/Teams
2. **Alertes** : Notifications en cas d'anomalies
3. **Dashboards** : Visualisation des données dans Looker/Tableau
4. **Backup** : Sauvegarde automatique des données

## 📞 Support

- **Documentation dlt** : https://dlthub.com/docs
- **GitHub Actions** : https://docs.github.com/en/actions
- **BigQuery** : https://cloud.google.com/bigquery/docs

---

**🎉 Votre pipeline est maintenant entièrement automatisé !**

Vos données Pipedrive seront synchronisées quotidiennement vers BigQuery sans intervention manuelle.
