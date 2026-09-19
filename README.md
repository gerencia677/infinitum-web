# Web de INFINITUM

Sitio nuevo. Toma el **diseño** de `infinitum.archi` y el **contenido real** de
`infi.com.co`, corregido contra el manual de marca y contra la bóveda.

Versión **2026-09-18 1800 v1**.

## Cómo se cambia algo

No hay que instalar nada. Node no se usa, npm no se usa.

```bash
cd ~/dev/infinitum-web
python3 build.py
```

Eso arma las ocho páginas en `dist/`. Para verlo en el navegador:

```bash
python3 -m http.server 4173 --directory ~/dev/infinitum-web/dist
```

Y se abre `http://127.0.0.1:4173`.

## Dónde vive cada cosa

| Carpeta | Qué hay |
|---|---|
| `templates/base.html` | La cabecera, el menú y el pie. **Se cambian aquí una vez** y quedan en las ocho páginas |
| `pages/*.html` | El contenido de cada página, solo el cuerpo |
| `assets/css/site.css` | Todo el diseño. Colores, tipografía, tarjetas, rejillas |
| `assets/js/site.js` | Carrusel, menú, filtros, español/inglés. Sin librerías |
| `assets/img/` | Fotos. `hero/` para la portada, `proyectos/` para las tarjetas |
| `dist/` | Lo que se publica. **Se genera solo, no se edita a mano** |

Cada página empieza con un bloque de datos entre `<!-- -->`: título, descripción
y dirección. Eso alimenta el buscador y las redes.

## Lo que se corrigió frente a los dos sitios viejos

| | Decía | Dice ahora |
|---|---|---|
| Fundación | 2001, 24 años | **2005, 21 años.** Verificado el 17-sep-2026 |
| Correo | `studio@infinitum.archi`, que rebota porque el dominio no tiene MX | `gerencia@mg.com.co` |
| WhatsApp | 315 832 2406 en uno, 311 265 3727 en el otro | **318 409 6572**, el del manual |
| Proyectos | HOME ONE, HOME TWO, HOME TREE en Viena y Reikiavik | Casa CR, Celebrity 2.0, Be Live y seis más, todos reales |
| Colores | blanco y negro, sin marca | Navy `#14213D` y dorado `#C9A85C` |
| Idioma | menú en español, contenido en inglés | Español de base, inglés con el botón del menú |

## Lo que falta y solo él puede dar

1. **Fotos** de Casa Q, Casa GZ, Casa SD, Casa SG, Sportage Unicentro, Celebrity
   Arkadia, Cariño Santo, Oficinas La Media Naranja, Oficina MN y Oficina P. Hoy
   están nombradas en texto porque no hay imagen limpia.
2. **Los PDF de los catálogos**, para que el botón descargue en vez de llevar a
   contacto.
3. **Decidir un solo número de WhatsApp** entre los tres que circulan.
4. **Confirmar la fecha de Estados Unidos.** La bóveda dice operación desde 2019,
   los dos sitios dicen Miami 2020 y proyectos 2024. Quedó la versión de los sitios.
5. **Dónde se publica**, y el DNS de `infinitum.archi` en GoDaddy.

## Publicar

`dist/` es una carpeta de archivos estáticos. Sirve en Cloudflare Pages, Netlify,
GitHub Pages o cualquier hosting. No necesita servidor de aplicaciones, no necesita
base de datos, y no depende de ninguna suscripción.
