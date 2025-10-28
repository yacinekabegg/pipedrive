# 🚀 Pipeline Pipedrive vers BigQuery - Guide Complet

## 📋 Vue d'ensemble

Ce projet utilise **dlt** (data load tool) pour ingérer automatiquement les données de Pipedrive dans BigQuery. Il inclut des scripts de configuration, de déploiement et d'automatisation.

## 📁 Structure du projet

```
Pipedrive/
├── pipedrive/                    # Source dlt Pipedrive
│   ├── __init__.py
│   ├── settings.py
│   ├── typing.py
│   └── helpers/
├── .dlt/                         # Configuration dlt
│   ├── config.toml
│   └── secrets.toml              # ⚠️ À configurer
├── pipedrive_pipeline.py         # Script de base
├── pipedrive_main.py             # Script principal avec options
├── configure.py                  # Script de configuration
├── deploy.py                     # Script de déploiement
├── run_pipeline.sh              # Script pour cron jobs
├── requirements.txt              # Dépendances Python
├── README.md                    # Documentation principale
├── CRON_SETUP.md               # Guide des tâches automatisées
└── env.example                 # Exemple de configuration
```

## 🎯 Ressources disponibles (18 au total)

1. **custom_fields_mapping** - Mapping des champs personnalisés
2. **activities** - Activités et tâches
3. **activity_types** - Types d'activités
4. **deals** - Opportunités de vente
5. **files** - Fichiers attachés
6. **filters** - Filtres personnalisés
7. **notes** - Notes
8. **persons** - Contacts individuels
9. **organizations** - Organisations/entreprises
10. **pipelines** - Processus de vente
11. **products** - Produits/services
12. **projects** - Projets
13. **stages** - Étapes du processus
14. **tasks** - Tâches
15. **users** - Utilisateurs de la plateforme
16. **deals_participants** - Participants aux deals
17. **deals_flow** - Flux des deals
18. **leads** - Prospects

## ⚙️ Configuration rapide

### 1. Installation des dépendances

```bash
pip3 install -r requirements.txt
```

### 2. Configuration des credentials

**Option A : Script interactif**
```bash
python3 configure.py
```

**Option B : Configuration manuelle**
Éditez `.dlt/secrets.toml` :

```toml
[sources.pipedrive]
pipedrive_api_key = "votre_token_pipedrive"

[destination.bigquery]
location = "US"

[destination.bigquery.credentials]
project_id = "votre-project-id"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "service-account@project.iam.gserviceaccount.com"
```

### 3. Test de configuration

```bash
python3 pipedrive_main.py --mode resources
```

## 🚀 Utilisation

### Chargement complet
```bash
python3 pipedrive_main.py --mode all
```

### Chargement sélectif
```bash
python3 pipedrive_main.py --mode selected --resources deals persons products
```

### Chargement incrémental (7 derniers jours)
```bash
python3 pipedrive_main.py --mode incremental
```

### Chargement incrémental depuis une date
```bash
python3 pipedrive_main.py --mode incremental --since 2023-03-01
```

## 🔄 Automatisation

### Tâches cron

**Chargement quotidien à 6h :**
```bash
0 6 * * * /Users/yacinekabeche/Desktop/Vibe\ codings/Pipedrive/run_pipeline.sh incremental
```

**Chargement complet hebdomadaire :**
```bash
0 2 * * 0 /Users/yacinekabeche/Desktop/Vibe\ codings/Pipedrive/run_pipeline.sh all
```

### Script de déploiement
```bash
python3 deploy.py
```

## 📊 Monitoring

### Vérifier les logs
```bash
# Logs récents
ls -la logs/

# Suivre les logs en temps réel
tail -f logs/pipedrive_*.log
```

### Vérifier les données dans BigQuery
```sql
-- Voir les tables créées
SELECT table_name 
FROM `votre-project.pipedrive_data.INFORMATION_SCHEMA.TABLES`

-- Exemple de requête sur les deals
SELECT * 
FROM `votre-project.pipedrive_data.deals` 
LIMIT 10
```

## 🛠️ Dépannage

### Erreurs courantes

1. **"Placeholder value encountered"**
   - Solution : Configurez vos credentials dans `.dlt/secrets.toml`

2. **"Authentication failed"**
   - Solution : Vérifiez votre token Pipedrive et vos credentials BigQuery

3. **"Permission denied"**
   - Solution : Vérifiez les permissions du service account BigQuery

### Commandes de diagnostic

```bash
# Tester la connexion Pipedrive
python3 -c "from pipedrive import pipedrive_source; print('OK')"

# Tester la connexion BigQuery
python3 -c "import dlt; dlt.pipeline('test', 'bigquery', 'test')"

# Voir les informations du pipeline
python3 pipedrive_main.py --mode info
```

## 📈 Optimisations

### Chargement incrémental
- Utilisez le mode `incremental` pour les chargements réguliers
- Le chargement complet est recommandé seulement pour l'initialisation

### Sélection de ressources
- Chargez seulement les ressources nécessaires avec `--resources`
- Toujours inclure `custom_fields_mapping` pour la traduction des champs

### Performance BigQuery
- Configurez la localisation appropriée dans `secrets.toml`
- Utilisez des datasets séparés pour différents environnements

## 🔐 Sécurité

- ⚠️ **Ne jamais commiter** le fichier `.dlt/secrets.toml`
- Utilisez des service accounts avec des permissions minimales
- Configurez la rotation des tokens régulièrement
- Surveillez les accès aux données sensibles

## 📞 Support

- Documentation dlt : https://dlthub.com/docs
- Source Pipedrive : https://dlthub.com/docs/dlt-ecosystem/verified-sources/pipedrive
- Communauté Slack : https://dlthub.com/slack

---

**🎉 Votre pipeline Pipedrive vers BigQuery est prêt !**

Commencez par configurer vos credentials, puis exécutez votre premier chargement.

