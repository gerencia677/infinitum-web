#!/bin/bash
# ============================================================
# Publica la web de Infinitum en GitHub Pages.
# Se corre una sola vez. Despues, para actualizar, basta con
# `python3 build.py && git add docs && git commit -m "..." && git push`
#
#   bash ~/dev/infinitum-web/publicar.sh
# ============================================================
set -euo pipefail

cd "$(dirname "$0")"
REPO="infinitum-web"

echo "→ 1 de 5. Armando el sitio"
python3 build.py > /dev/null
touch docs/.nojekyll
echo "   $(ls docs/*.html | wc -l | tr -d ' ') paginas, $(du -sh docs | cut -f1)"

echo "→ 2 de 5. Guardando los cambios"
git add build.py .gitignore docs pages templates assets README.md publicar.sh
git -c user.name="Juan David Gomez" -c user.email="gerencia@mg.com.co" \
    commit -q -m "Sitio listo para publicar" || echo "   nada nuevo que guardar"

USUARIO="$(gh api user --jq .login)"
echo "   cuenta de GitHub: $USUARIO"

echo "→ 3 de 5. Creando el repositorio"
if gh repo view "$USUARIO/$REPO" > /dev/null 2>&1; then
  echo "   ya existia, se reutiliza"
  git remote get-url origin > /dev/null 2>&1 || git remote add origin "https://github.com/$USUARIO/$REPO.git"
else
  gh repo create "$REPO" --public --source=. \
     --description "Sitio web de Infinitum Arquitectura + Mobiliario"
fi

echo "→ 4 de 5. Subiendo"
git push -u origin HEAD --quiet

echo "→ 5 de 5. Prendiendo GitHub Pages sobre la carpeta docs"
gh api -X POST "repos/$USUARIO/$REPO/pages" \
   -f "source[branch]=main" -f "source[path]=/docs" > /dev/null 2>&1 \
|| gh api -X PUT "repos/$USUARIO/$REPO/pages" \
   -f "source[branch]=main" -f "source[path]=/docs" > /dev/null 2>&1 \
|| echo "   ojo: revise Settings > Pages en el repositorio"

echo
echo "============================================================"
echo "  LISTO. La direccion es:"
echo "  https://$USUARIO.github.io/$REPO/"
echo
echo "  GitHub tarda entre 1 y 3 minutos la primera vez."
echo "  Si sale 404 al principio, espere y recargue."
echo "============================================================"
