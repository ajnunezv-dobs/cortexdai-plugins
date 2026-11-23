#!/usr/bin/env bash
# Publica los plugins: marca la versión en cada skill, valida, sube a GitHub y le dice a la conexión única qué versión
# está vigente (PLUGINS_VIGENTES), para que las skills viejas avisen a la persona que hay una nueva.
#
#   bash scripts/publicar.sh            (antes: subir "version" en el plugin.json de lo que cambió)
set -euo pipefail
cd "$(dirname "$0")/.."
python scripts/marcar-version.py
python scripts/validar.py
VIGENTES=$(python - <<'PY'
import json, os
v = []
for p in sorted(os.listdir("plugins")):
    if os.path.exists(f"plugins/{p}/.mcp.json"):
        pj = json.load(open(f"plugins/{p}/.claude-plugin/plugin.json", encoding="utf-8"))
        v.append(f"{pj['name']}={pj['version']}")
print(",".join(v))
PY
)
git add -A
git diff --cached --quiet || git commit -q -m "Publicación de plugins: $VIGENTES"
git push -q origin main
gcloud run services update mcp --update-env-vars="^|^PLUGINS_VIGENTES=$VIGENTES" --project=dobs-cortexdai-central --region=us-central1 --quiet >/dev/null
echo "Publicado: $VIGENTES (commit $(git rev-parse --short HEAD))"
echo "Quien ya tiene los plugins lo verá al pulsar Check for updates; mientras tanto, las skills viejas le avisan."
