#!/bin/bash
# ============================================================
# Amarra infinitum.archi al sitio de GitHub Pages.
#
# SE CORRE DESPUES de cambiar los registros en GoDaddy, no antes.
# Si se corre antes, GitHub marca error y tumba la direccion
# gerencia677.github.io mientras tanto.
#
#   bash ~/dev/infinitum-web/apuntar-dominio.sh
# ============================================================
set -euo pipefail
cd "$(dirname "$0")"

DOMINIO="infinitum.archi"
USUARIO="$(gh api user --jq .login)"
REPO="infinitum-web"

echo "→ 1 de 4. Revisando a donde apunta $DOMINIO"
IPS="$(dig +short $DOMINIO A | sort | tr '\n' ' ')"
echo "   hoy: $IPS"
case "$IPS" in
  *185.199.10*|*185.199.11*) echo "   bien, ya apunta a GitHub" ;;
  *) echo
     echo "   ALTO. Todavia no apunta a GitHub."
     echo "   Primero hay que cambiar los registros en GoDaddy. Sin eso esto no sigue."
     exit 1 ;;
esac

echo "→ 2 de 4. Dejando el nombre del dominio dentro del sitio"
echo "$DOMINIO" > docs/CNAME
python3 build.py > /dev/null
echo "$DOMINIO" > docs/CNAME     # build.py limpia docs, se vuelve a escribir
git add docs build.py apuntar-dominio.sh
git -c user.name="Juan David Gomez" -c user.email="gerencia@mg.com.co" \
    commit -q -m "El sitio responde por $DOMINIO" || echo "   nada nuevo"
git push -q origin main

echo "→ 3 de 4. Avisandole a GitHub"
gh api -X PUT "repos/$USUARIO/$REPO/pages" -f "cname=$DOMINIO" > /dev/null 2>&1 || true

echo "→ 4 de 4. Prendiendo el candado de seguridad"
sleep 20
gh api -X PUT "repos/$USUARIO/$REPO/pages" -F "https_enforced=true" > /dev/null 2>&1 \
  || echo "   el certificado todavia se esta emitiendo, puede tardar hasta 1 hora"

echo
echo "============================================================"
echo "  LISTO. https://$DOMINIO"
echo "  El certificado de seguridad puede tardar hasta una hora."
echo "============================================================"
