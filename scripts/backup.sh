#!/bin/bash

# AgentLogger Database Backup Script
# Usage: ./backup.sh [backup_name]

set -e

# Configuration
POSTGRES_USER=${POSTGRES_USER:-postgres}
POSTGRES_DB=${POSTGRES_DB:-agentlogger}
BACKUP_DIR="/var/lib/postgresql/backups"
DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME=${1:-"agentlogger_backup_${DATE}"}

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

echo "🗄️  Starting database backup..."
echo "Database: $POSTGRES_DB"
echo "User: $POSTGRES_USER"
echo "Backup file: ${BACKUP_NAME}.sql"

# Create the backup
pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" --clean --if-exists --create > "$BACKUP_DIR/${BACKUP_NAME}.sql"

# Compress the backup
gzip "$BACKUP_DIR/${BACKUP_NAME}.sql"

echo "✅ Backup completed: $BACKUP_DIR/${BACKUP_NAME}.sql.gz"

# Clean up old backups (keep last 7 days)
find "$BACKUP_DIR" -name "agentlogger_backup_*.sql.gz" -mtime +7 -delete

echo "🧹 Old backups cleaned up (kept last 7 days)"
echo "📊 Current backups:"
ls -lah "$BACKUP_DIR"/agentlogger_backup_*.sql.gz 2>/dev/null || echo "No backups found" 