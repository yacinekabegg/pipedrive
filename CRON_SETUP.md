# Configuration des tâches automatisées (Cron Jobs)

Ce document explique comment configurer des tâches automatisées pour exécuter le pipeline Pipedrive de manière régulière.

## Configuration Cron

### 1. Ouvrir l'éditeur cron

```bash
crontab -e
```

### 2. Ajouter des tâches

Voici quelques exemples de configurations cron :

#### Chargement quotidien (incrémental) à 6h du matin
```bash
0 6 * * * /Users/yacinekabeche/Desktop/Vibe\ codings/Pipedrive/run_pipeline.sh incremental
```

#### Chargement complet hebdomadaire (dimanche à 2h du matin)
```bash
0 2 * * 0 /Users/yacinekabeche/Desktop/Vibe\ codings/Pipedrive/run_pipeline.sh all
```

#### Chargement sélectif toutes les 4 heures
```bash
0 */4 * * * /Users/yacinekabeche/Desktop/Vibe\ codings/Pipedrive/run_pipeline.sh selected
```

#### Chargement incrémental toutes les 2 heures en semaine
```bash
0 */2 * * 1-5 /Users/yacinekabeche/Desktop/Vibe\ codings/Pipedrive/run_pipeline.sh incremental
```

### 3. Format Cron

```
* * * * * command
│ │ │ │ │
│ │ │ │ └─── Jour de la semaine (0-7, 0 et 7 = dimanche)
│ │ │ └───── Mois (1-12)
│ │ └─────── Jour du mois (1-31)
│ └───────── Heure (0-23)
└─────────── Minute (0-59)
```

### 4. Exemples de fréquences

- `0 6 * * *` - Tous les jours à 6h00
- `0 */2 * * *` - Toutes les 2 heures
- `30 2 * * 1` - Tous les lundis à 2h30
- `0 0 1 * *` - Le 1er de chaque mois à minuit
- `0 6 * * 1-5` - Du lundi au vendredi à 6h00

## Monitoring et Logs

### Vérifier les logs

```bash
# Voir les logs récents
ls -la /Users/yacinekabeche/Desktop/Vibe\ codings/Pipedrive/logs/

# Suivre les logs en temps réel
tail -f /Users/yacinekabeche/Desktop/Vibe\ codings/Pipedrive/logs/pipedrive_*.log
```

### Vérifier les tâches cron

```bash
# Lister les tâches cron actuelles
crontab -l

# Vérifier les logs système cron
grep CRON /var/log/syslog
```

## Gestion des erreurs

### Notifications par email

Ajoutez cette ligne au début de votre crontab pour recevoir les erreurs par email :

```bash
MAILTO=votre-email@example.com
```

### Script de monitoring

Créez un script pour vérifier l'état du pipeline :

```bash
#!/bin/bash
# check_pipeline.sh

LOG_DIR="/Users/yacinekabeche/Desktop/Vibe codings/Pipedrive/logs"
LAST_LOG=$(ls -t $LOG_DIR/pipedrive_*.log | head -1)

if [ -f "$LAST_LOG" ]; then
    if grep -q "✅ Chargement terminé avec succès" "$LAST_LOG"; then
        echo "✅ Pipeline OK - $(date)"
    else
        echo "❌ Pipeline en erreur - $(date)"
        # Ici vous pouvez ajouter une notification (email, Slack, etc.)
    fi
else
    echo "⚠️  Aucun log trouvé - $(date)"
fi
```

## Bonnes pratiques

1. **Testez d'abord manuellement** : Vérifiez que le script fonctionne avant de l'automatiser
2. **Utilisez des chemins absolus** : Évitez les chemins relatifs dans les tâches cron
3. **Gérez les logs** : Configurez la rotation des logs pour éviter qu'ils deviennent trop volumineux
4. **Surveillez les erreurs** : Configurez des alertes pour les échecs
5. **Planifiez les chargements** : Évitez les heures de pointe pour les chargements complets

## Exemple de configuration complète

```bash
# Configuration complète pour un environnement de production
MAILTO=admin@company.com

# Chargement incrémental quotidien à 6h
0 6 * * * /Users/yacinekabeche/Desktop/Vibe\ codings/Pipedrive/run_pipeline.sh incremental

# Chargement complet hebdomadaire le dimanche à 2h
0 2 * * 0 /Users/yacinekabeche/Desktop/Vibe\ codings/Pipedrive/run_pipeline.sh all

# Vérification de l'état toutes les heures
0 * * * * /Users/yacinekabeche/Desktop/Vibe\ codings/Pipedrive/check_pipeline.sh
```

