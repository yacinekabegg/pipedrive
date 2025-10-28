#!/bin/bash
# Script de tâche automatisée pour le pipeline Pipedrive
# À utiliser avec cron pour des chargements réguliers

# Configuration
SCRIPT_DIR="/Users/yacinekabeche/Desktop/Vibe codings/Pipedrive"
LOG_DIR="$SCRIPT_DIR/logs"
LOG_FILE="$LOG_DIR/pipedrive_$(date +%Y%m%d_%H%M%S).log"

# Créer le répertoire de logs s'il n'existe pas
mkdir -p "$LOG_DIR"

# Fonction de logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Fonction de gestion d'erreur
handle_error() {
    log "❌ Erreur: $1"
    exit 1
}

# Début du script
log "🚀 Début du chargement Pipedrive"

# Aller dans le répertoire du script
cd "$SCRIPT_DIR" || handle_error "Impossible d'accéder au répertoire $SCRIPT_DIR"

# Vérifier que Python est disponible
if ! command -v python3 &> /dev/null; then
    handle_error "Python3 non trouvé"
fi

# Mode de chargement (peut être modifié selon les besoins)
MODE=${1:-"incremental"}  # Par défaut: chargement incrémental

case $MODE in
    "all")
        log "📊 Mode: Chargement complet"
        python3 pipedrive_main.py --mode all >> "$LOG_FILE" 2>&1
        ;;
    "incremental")
        log "📊 Mode: Chargement incrémental (7 derniers jours)"
        python3 pipedrive_main.py --mode incremental >> "$LOG_FILE" 2>&1
        ;;
    "selected")
        log "📊 Mode: Chargement sélectif (deals, persons, products)"
        python3 pipedrive_main.py --mode selected --resources deals persons products >> "$LOG_FILE" 2>&1
        ;;
    *)
        log "❌ Mode invalide: $MODE"
        log "Modes disponibles: all, incremental, selected"
        exit 1
        ;;
esac

# Vérifier le code de retour
if [ $? -eq 0 ]; then
    log "✅ Chargement terminé avec succès"
else
    log "❌ Erreur lors du chargement"
    exit 1
fi

# Nettoyer les anciens logs (garder seulement les 30 derniers jours)
find "$LOG_DIR" -name "pipedrive_*.log" -mtime +30 -delete 2>/dev/null

log "🏁 Script terminé"

