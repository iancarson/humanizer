#!/usr/bin/env bash
# Install Humanizer as a Claude Code skill.
#
# Usage:
#   ./install.sh                   # install to ~/.claude/skills/humanizer (user-wide)
#   ./install.sh --project         # install to ./.claude/skills/humanizer (current project)
#   ./install.sh --target /path    # install to /path/.claude/skills/humanizer

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE="${SCRIPT_DIR}/SKILL.md"

if [[ ! -f "${SOURCE}" ]]; then
    echo "Error: SKILL.md not found at ${SOURCE}" >&2
    exit 1
fi

TARGET_BASE="${HOME}"
case "${1:-}" in
    --project)
        TARGET_BASE="$(pwd)"
        ;;
    --target)
        if [[ -z "${2:-}" ]]; then
            echo "Error: --target requires a path" >&2
            exit 1
        fi
        TARGET_BASE="$2"
        ;;
    "")
        ;;
    *)
        echo "Unknown argument: $1" >&2
        echo "Usage: $0 [--project | --target /path]" >&2
        exit 1
        ;;
esac

DEST_DIR="${TARGET_BASE}/.claude/skills/humanizer"
DEST_FILE="${DEST_DIR}/SKILL.md"

mkdir -p "${DEST_DIR}"

if [[ -f "${DEST_FILE}" ]]; then
    BACKUP="${DEST_FILE}.backup.$(date +%Y%m%d-%H%M%S)"
    cp "${DEST_FILE}" "${BACKUP}"
    echo "Existing skill backed up to ${BACKUP}"
fi

cp "${SOURCE}" "${DEST_FILE}"

echo ""
echo "Humanizer installed to ${DEST_FILE}"
echo ""
echo "Try it:"
echo "  In Claude Code, type:  /humanizer"
echo "  Or:                    humanize this draft"
echo ""
echo "First-run setup (optional):"
echo "  humanizer setup"
echo ""
