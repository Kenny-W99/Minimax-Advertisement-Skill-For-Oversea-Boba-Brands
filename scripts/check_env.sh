#!/usr/bin/env bash
# Quick preflight for API mode. Never prints the key itself.
ok=1
for b in ffmpeg ffprobe python3; do
  if command -v "$b" >/dev/null 2>&1; then echo "ok   $b"; else echo "MISS $b"; ok=0; fi
done
PY="${PYTHON:-${1:-python3}}"   # the interpreter that will run the scripts: PYTHON=/path/to/python bash check_env.sh
echo "python $PY"
"$PY" -c "import PIL" 2>/dev/null && echo "ok   pillow" || { echo "MISS pillow (pip install pillow)"; ok=0; }
MPY="${MUSIC_PYTHON:-$PY}"      # music3.py may run on a different interpreter: MUSIC_PYTHON=/path/to/venv/python
"$MPY" -c "import gradio_client" 2>/dev/null && echo "ok   gradio_client ($MPY)" || echo "warn gradio_client missing in $MPY (pip install gradio_client) — needed only for scripts/music3.py"
if [ -n "${MINIMAX_API_KEY:-}" ]; then echo "ok   MINIMAX_API_KEY is set (${#MINIMAX_API_KEY} chars)"; else echo "MISS MINIMAX_API_KEY (pay-as-you-go key from platform.minimax.io)"; ok=0; fi
echo "host ${MINIMAX_API_HOST:-https://api.minimax.io}"
[ "$ok" = 1 ] && echo "READY" || echo "NOT READY"
