#!/bin/bash
# Monta el borrador del portafolio en una URL no listada: /borrador-x7k2/  (sin publicarlo en el sitio)
set -e
cd "$(dirname "$0")/.."
python3 tools/generar-portafolio.py
cp borradores/portafolio.html pages/portafolio.html
python3 build.py >/dev/null
rm pages/portafolio.html
mkdir -p docs/borrador-x7k2
python3 - <<'P'
s=open("docs/portafolio.html").read()
s=s.replace("<head>",'<head><base href="/"><meta name="robots" content="noindex,nofollow">',1)
open("docs/borrador-x7k2/index.html","w").write(s)
P
rm docs/portafolio.html
echo infinitum.archi > docs/CNAME; touch docs/.nojekyll
echo "robots: borrador-x7k2 no indexado"
