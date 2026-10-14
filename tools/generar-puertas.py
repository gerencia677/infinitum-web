#!/usr/bin/env python3
"""Genera pages/puertas.html y pages/puertas-catalogo.html con pesos calculados.
Se corre: python3 tools/generar-puertas.py && python3 build.py"""
import json, re
from pathlib import Path
RAIZ = Path(__file__).resolve().parent.parent

# ---------- Pesos de referencia (kg por m2 de hoja, con marco y estructura) ----------
# Supuestos: vidrio 2,5 kg/m2 por mm; aluminio compuesto 4 mm = 5,5 kg/m2 por cara;
# roble 750 kg/m3; acero 7.850 kg/m3; lama de madera plastica (WPC) hueca de 21 mm = 10 kg/m2 de frente.
MAT = {
 "mad_maciza": ("Madera maciza (roble, 60 mm)", "Solid wood (oak, 60 mm)", round(0.060*750)),            # 45
 "mad_chap":   ("Madera enchapada sobre estructura (60 mm)", "Veneered wood over structure (60 mm)", 35),
 "vidrio":     ("Vidrio laminado 8+8 con marco de aluminio", "Laminated 8+8 glass with aluminum frame", round(16*2.5+8)),   # 48
 "vidrio10":   ("Vidrio laminado 10+10 con marco de aluminio", "Laminated 10+10 glass with aluminum frame", round(20*2.5+8)), # 58
 "acm":        ("Aluminio compuesto 4 mm, dos caras, sobre estructura", "Aluminum composite 4 mm, both faces, over structure", round(2*5.5+5)),  # 16
 "acm_wpc":    ("Aluminio compuesto con lamas frontales de madera plástica", "Aluminum composite with wood-plastic front slats", round(2*5.5+5+10)), # 26
 "acero":      ("Acero 2 mm, dos caras, sobre estructura", "Steel 2 mm, both faces, over structure", round(2*2*7.85+12)),    # 43
 "acero_vid":  ("Marco de acero con vidrio laminado 8+8", "Steel frame with laminated 8+8 glass", 55),
}
TAM = [("2 × 5 m", 2*5), ("3 × 4 m", 3*4), ("3 × 5 m", 3*5)]
def r5(x): return int(5*round(x/5))
def herraje(kg):
    if kg <= 250: return ("Herraje oculto de catálogo", "Concealed catalog hardware")
    if kg <= 500: return ("Herraje oculto de alta capacidad", "High-capacity concealed hardware")
    return ("Herraje a medida e ingeniería especial", "Custom hardware and special engineering")

# ---------- Catálogo ----------
MODELOS = [
 ("1","Vidrio corporativo","Corporate glass","Oficinas, vestíbulos y sedes","Offices, lobbies and headquarters","vidrio",3,4,1,"Hoja de vidrio de piso a techo con perfilería de aluminio negro o bronce. Entrada que deja ver el vestíbulo desde la calle.","Floor-to-ceiling glass leaf with black or bronze aluminum framing. An entrance that shows the lobby from the street.","Aluminio y vidrio laminado 8+8","Aluminum and laminated 8+8 glass"),
 ("2","Vidrio comercial de dos hojas","Two-leaf retail glass","Grandes locales y puntos de venta","Large stores and retail points","vidrio",1.8,3.2,2,"Dos hojas pivotantes, cada una de una sola pieza de vidrio de 3,20 m de altura, la medida comercial más común en Colombia. Vitrina y puerta en un solo gesto.","Two pivoting leaves, each a single piece of glass 3.20 m tall, the most common commercial size in Colombia. Storefront and door in a single gesture.","Aluminio bronce y vidrio laminado 8+8","Bronze aluminum and laminated 8+8 glass"),
 ("3","Madera noble","Fine wood","Residencias y casas de lujo","Residences and luxury homes","mad_chap",3,5,1,"Hoja de nogal enchapada sobre estructura, veta vertical y manija de acero de gran longitud. La puerta como monumento de la casa.","Walnut leaf veneered over structure, vertical grain and an extra-long steel handle. The door as the home's monument.","Nogal sobre estructura, acero","Walnut over structure, steel"),
 ("4","Madera con lamas frontales","Wood with front slats","Casas, restaurantes y hoteles","Homes, restaurants and hotels","mad_chap_wpc",2,5,1,"Hoja de roble con lamas verticales de madera plástica al frente, en continuidad con el muro. La puerta se confunde con la fachada.","Oak leaf with vertical wood-plastic slats on the front, continuous with the wall. The door blends into the façade.","Roble y lamas de madera plástica (WPC)","Oak and wood-plastic (WPC) slats"),
 ("5","Aluminio compuesto liso","Smooth aluminum composite","Sedes corporativas y edificios","Corporate headquarters and buildings","acm",3,4,1,"Hoja a ras de la fachada en aluminio compuesto, del mismo panel del edificio. Liviana, de bajo mantenimiento y casi invisible hasta que se abre.","Leaf flush with the façade in aluminum composite, the same panel as the building. Light, low maintenance and almost invisible until it opens.","Aluminio compuesto 4 mm","Aluminum composite 4 mm"),
 ("6","Aluminio compuesto con lamas","Aluminum composite with slats","Restaurantes y puntos de venta","Restaurants and retail points","acm_wpc",3,5,1,"Panel de aluminio compuesto con lamas frontales de madera plástica. Calidez de madera con el peso y el mantenimiento de un panel.","Aluminum composite panel with wood-plastic front slats. The warmth of wood with the weight and maintenance of a panel.","Aluminio compuesto y madera plástica (WPC)","Aluminum composite and wood-plastic (WPC)"),
 ("7","Acero y vidrio","Steel and glass","Hoteles y accesos de gran altura","Hotels and tall entrances","acero_vid",3,4,1,"Marco de acero con vidrio de retícula fina, en tono bronce. Presencia de hotel y de edificio patrimonial.","Steel frame with fine-grid glass in a bronze tone. The presence of a hotel and of a heritage building.","Acero y vidrio laminado 8+8","Steel and laminated 8+8 glass"),
 ("8","Gran portal de dos hojas","Grand two-leaf portal","Galerías comerciales, hoteles y casas","Shopping galleries, hotels and homes","mad_vid",2,5,2,"Dos hojas de madera y vidrio, cada una de 2 × 5 m, que forman un portal de 4 × 5 m. Simetría y escala de edificio institucional.","Two wood and glass leaves, each 2 × 5 m, forming a 4 × 5 m portal. Symmetry and the scale of an institutional building.","Madera y vidrio laminado","Wood and laminated glass"),
 ("9","Vidrio con travesaño y bandera","Glass with transom and upper panel","Locales y fachadas comerciales de doble altura","Double-height stores and commercial façades","vidrio",2,3.2,2,"Las hojas llegan hasta 3,20 m, y sobre un travesaño horizontal continúa un segundo vidrio hasta cinco metros. El travesaño trabaja como estructura y como diseño, junto con las puertas.","The leaves reach 3.20 m, and above a horizontal transom a second glass continues up to five meters. The transom works as structure and as design, together with the doors.","Aluminio, travesaño estructural y vidrio laminado","Aluminum, structural transom and laminated glass"),

]
EXTRA = {"mad_chap_wpc": 35+10, "mad_vid": 45}
def peso_modelo(clave, w, h):
    kgm2 = EXTRA.get(clave) or MAT[clave][2]
    return kgm2, r5(kgm2*w*h)


CONSIDERACIONES = [
 ("Estructura del edificio","Building structure","El peso de la hoja viaja por los pivotes a la estructura. El proyecto estructural define el dintel o viga superior, la placa o el piso del pivote inferior y los apoyos laterales, antes de fundir.","The leaf's weight travels through the pivots into the structure. The structural project defines the lintel or head beam, the slab or floor for the bottom pivot and the side supports, before pouring."),
 ("Herraje pivotante","Pivot hardware","Se elige por el peso de la hoja y por la frecuencia de uso: de catálogo oculto hasta unos 250 kg, de alta capacidad hasta unos 500 kg, y a medida por encima. Se verifica con el fabricante del herraje.","It is chosen by leaf weight and frequency of use: concealed catalog hardware up to about 250 kg, high-capacity up to about 500 kg, and custom above. It is verified with the hardware manufacturer."),
 ("Vidrio de 3,20 m","3.20 m glass","La altura comercial más común del vidrio en Colombia es de 3,20 m en una sola pieza. Por encima se usa un segundo vidrio sobre un travesaño horizontal, que se diseña como estructura y como parte de la puerta.","The most common commercial glass height in Colombia is 3.20 m in a single piece. Above it, a second glass is used over a horizontal transom, designed as structure and as part of the door."),
 ("Seguridad del vidrio","Glass safety","Vidrio laminado, templado o ambos, con espesores definidos por la medida de la hoja, el uso y el viento. Los bordes y los herrajes de vidrio se calculan en conjunto.","Laminated glass, tempered glass or both, with thicknesses defined by the leaf size, use and wind. Edges and glass hardware are calculated together."),
 ("Viento, agua y aire","Wind, water and air","Perfiles, sellos, umbrales y drenajes diseñados para lluvia y viento. Una hoja pivotante grande trabaja como una vela: la carga de viento se incluye en el cálculo.","Profiles, seals, thresholds and drainage designed for rain and wind. A large pivot leaf acts like a sail: wind load is included in the calculation."),
 ("Dilatación y tolerancias","Expansion and tolerances","La madera, el aluminio, el vidrio y el acero se dilatan distinto con el sol. Se prevén holguras, sellos y juntas por material, y la hoja se fabrica con tolerancias de planitud.","Wood, aluminum, glass and steel expand differently in the sun. Clearances, seals and joints are planned per material, and the leaf is built with flatness tolerances."),
 ("Madera estable","Stable wood","Núcleo balanceado, enchapado por ambas caras, control de humedad y acabado de exterior en todas las caras, incluidos los cantos y la base.","Balanced core, veneer on both faces, moisture control and an exterior finish on every face, including edges and base."),
 ("Evacuación y accesibilidad","Egress and accessibility","Cuando la puerta es una salida de evacuación o un acceso público, se revisan la reglamentación colombiana aplicable, el ancho libre de paso, la fuerza de apertura y la apertura de emergencia con el ingeniero responsable.","When the door is an egress or a public access, the applicable Colombian regulations, clear opening width, opening force and emergency opening are reviewed with the responsible engineer."),
 ("Instalación","Installation","Izaje, ruta de ingreso, nivelación del piso y plomo del marco se planean antes de llegar a la obra. La instalación la hace una cuadrilla especializada, con un solo responsable.","Lifting, access route, floor leveling and frame plumb are planned before arriving on site. Installation is done by a specialized crew, with one accountable partner."),
 ("Garantía y mantenimiento","Warranty and maintenance","La puerta se entrega con garantía y con un plan de mantenimiento: revisión de herrajes, sellos y acabados. Los componentes de desgaste se reponen por piezas.","The door is delivered with a warranty and a maintenance plan: review of hardware, seals and finishes. Wear components are replaced piece by piece."),
]
def consideraciones():
    return "".join(f'<div><b>{i:02d}</b><h3 data-es="{a}" data-en="{b}">{a}</h3><p data-es="{c}" data-en="{d}">{c}</p></div>' for i,(a,b,c,d) in enumerate(CONSIDERACIONES,1))

def obra(c1,c2,t1,t2,p1,p2): return f'<div><b data-es="{c1}" data-en="{c2}">{c1}</b><h3 data-es="{t1}" data-en="{t2}">{t1}</h3><p data-es="{p1}" data-en="{p2}">{p1}</p></div>'
def card(es,en,pes,pen): return f'<div class="emp__card"><h3 data-es="{es}" data-en="{en}">{es}</h3><p data-es="{pes}" data-en="{pen}">{pes}</p></div>'
def fig(src,alt): return f'<a href="assets/img/fachadas/{src}" data-lb><img src="assets/img/fachadas/{src}" alt="{alt}" loading="lazy"></a>'
def bi(es,en,tag="span"): return f'<{tag} data-es="{es}" data-en="{en}">{es}</{tag}>'

def tabla_materiales():
    filas=""
    claves=["mad_maciza","mad_chap","vidrio","vidrio10","acm","acm_wpc","acero","acero_vid"]
    for k in claves:
        es,en,kgm2=MAT[k]
        celdas="".join(f"<td>{r5(kgm2*a)}</td>" for _,a in TAM)
        filas+=f'<tr><th scope="row" data-es="{es}" data-en="{en}">{es}</th><td>{kgm2}</td>{celdas}</tr>'
    cab="".join(f"<th>{t}</th>" for t,_ in TAM)
    return f'''<div class="fx__tabla rise"><table>
<thead><tr><th data-es="Material de la hoja" data-en="Leaf material">Material de la hoja</th><th data-es="kg por m²" data-en="kg per m²">kg por m²</th>{cab}</tr></thead>
<tbody>{filas}</tbody></table></div>
<p class="fx__nota rise" data-es="Pesos de referencia por hoja, en kilogramos, redondeados a 5 kg y con una variación de ±15 %. Supuestos: vidrio 2,5 kg/m² por milímetro, aluminio compuesto de 4 mm a 5,5 kg/m² por cara, roble a 750 kg/m³, acero a 7.850 kg/m³ y lamas huecas de madera plástica a 10 kg/m². El cálculo definitivo se hace con el proyecto." data-en="Reference weights per leaf, in kilograms, rounded to 5 kg with a ±15 % variation. Assumptions: glass 2.5 kg/m² per millimeter, 4 mm aluminum composite at 5.5 kg/m² per face, oak at 750 kg/m³, steel at 7,850 kg/m³ and hollow wood-plastic slats at 10 kg/m². The final calculation is made with the project.">Pesos de referencia por hoja, en kilogramos, redondeados a 5 kg y con una variación de ±15 %. Supuestos: vidrio 2,5 kg/m² por milímetro, aluminio compuesto de 4 mm a 5,5 kg/m² por cara, roble a 750 kg/m³, acero a 7.850 kg/m³ y lamas huecas de madera plástica a 10 kg/m². El cálculo definitivo se hace con el proyecto.</p>'''

def ficha(m):
    n,es,en,usoes,usoen,clave,w,h,hojas,pes,pen,mates,maten=m
    kgm2,kg=peso_modelo(clave,w,h)
    hes,hen=herraje(kg)
    fw=str(w).replace(".",","); fh=str(h).replace(".",",")
    tam=f"{fw} × {fh} m" if hojas==1 else f"{hojas} hojas de {fw} × {fh} m"
    tame=f"{w} × {h} m" if hojas==1 else f"{hojas} leaves of {w} × {h} m"
    return f'''<article class="fx__mod rise">
  <a href="assets/img/fachadas/cat-puerta-{n}.jpg" data-lb class="fx__mod__img"><img src="assets/img/fachadas/cat-puerta-{n}.jpg" alt="Modelo de referencia {es}: puerta pivotante {tam}" loading="lazy"></a>
  <div class="fx__mod__txt">
    <p class="eyebrow">{bi(f"MODELO {n}",f"MODEL {n}")}</p>
    <h3 data-es="{es}" data-en="{en}">{es}</h3>
    <p data-es="{pes}" data-en="{pen}">{pes}</p>
    <dl>
      <div><dt data-es="Medida" data-en="Size">Medida</dt><dd data-es="{tam}" data-en="{tame}">{tam}</dd></div>
      <div><dt data-es="Materiales" data-en="Materials">Materiales</dt><dd data-es="{mates}" data-en="{maten}">{mates}</dd></div>
      <div><dt data-es="Peso por hoja" data-en="Weight per leaf">Peso por hoja</dt><dd>{kg} kg</dd></div>
      <div><dt data-es="Herraje" data-en="Hardware">Herraje</dt><dd data-es="{hes}" data-en="{hen}">{hes}</dd></div>
      <div><dt data-es="Ideal para" data-en="Ideal for">Ideal para</dt><dd data-es="{usoes}" data-en="{usoen}">{usoes}</dd></div>
    </dl>
  </div>
</article>'''

# ---------- Página del catálogo ----------
fichas="".join(ficha(m) for m in MODELOS)
cat_html=f'''<!--
title: Catálogo de puertas arquitectónicas — Infinitum
desc: Catálogo de puertas arquitectónicas de gran formato de Infinitum: ocho modelos de referencia en vidrio, madera, aluminio compuesto y acero, con medidas, materiales, pesos y herrajes. Disponible en Colombia y Latinoamérica.
slug: puertas-catalogo.html
-->

<section class="phero">
  <img src="assets/img/fachadas/cat-puerta-8.jpg" alt="" aria-hidden="true" style="object-position:50% 50%">
  <div class="phero__in">
    <p class="eyebrow" data-es="CATÁLOGO · PUERTAS ARQUITECTÓNICAS" data-en="CATALOGUE · ARCHITECTURAL DOORS">CATÁLOGO · PUERTAS ARQUITECTÓNICAS</p>
    <h1 data-es="Nueve modelos para entradas que se recuerdan." data-en="Nine models for entrances that are remembered.">Nueve modelos para entradas que se recuerdan.</h1>
    <p data-es="Modelos de referencia en vidrio, madera, aluminio compuesto y acero, para oficinas, puntos de venta, hoteles y residencias. Cada puerta se diseña, se calcula y se construye a la medida de su obra." data-en="Reference models in glass, wood, aluminum composite and steel, for offices, retail points, hotels and residences. Every door is designed, calculated and built to the measure of its project.">Modelos de referencia en vidrio, madera, aluminio compuesto y acero, para oficinas, puntos de venta, hoteles y residencias. Cada puerta se diseña, se calcula y se construye a la medida de su obra.</p>
  </div>
</section>

<section class="pv__indice">
  <div class="wrap">
    <nav class="pf-nav" aria-label="Catálogo de puertas">
      <a href="puertas.html" data-es="La línea" data-en="The line">La línea</a>
      <a href="puertas-catalogo.html#modelos" data-es="Modelos" data-en="Models">Modelos</a>
      <a href="puertas-catalogo.html#pesos" data-es="Pesos" data-en="Weights">Pesos</a>
      <a href="puertas-catalogo.html#ingenieria" data-es="Ingeniería" data-en="Engineering">Ingeniería</a>
      <a href="contacto.html" data-es="Cotizar" data-en="Quote">Cotizar</a>
    </nav>
  </div>
</section>

<section id="modelos" class="pv__proy" style="background:var(--paper)">
  <div class="wrap">
    <div class="pv__cab rise">
      <div>
        <p class="eyebrow" data-es="MODELOS DE REFERENCIA" data-en="REFERENCE MODELS">MODELOS DE REFERENCIA</p>
        <h2 data-es="Del vestíbulo corporativo a la casa de lujo." data-en="From the corporate lobby to the luxury home.">Del vestíbulo corporativo a la casa de lujo.</h2>
      </div>
      <div>
        <p data-es="Nuestro foco son las empresas: sedes, oficinas, grandes locales, hoteles y centros comerciales. Las mismas puertas viven también en residencias de lujo. Las imágenes son ilustrativas de cada modelo." data-en="Our focus is business: headquarters, offices, large stores, hotels and shopping centers. The same doors also live in luxury residences. The images illustrate each model.">Nuestro foco son las empresas: sedes, oficinas, grandes locales, hoteles y centros comerciales. Las mismas puertas viven también en residencias de lujo. Las imágenes son ilustrativas de cada modelo.</p>
      </div>
    </div>
    <div class="fx__mods">{fichas}</div>
  </div>
</section>

<section id="pesos" class="pv__proy">
  <div class="wrap">
    <div class="pv__cab rise">
      <div>
        <p class="eyebrow" data-es="PESOS DE REFERENCIA" data-en="REFERENCE WEIGHTS">PESOS DE REFERENCIA</p>
        <h2 data-es="El peso decide el herraje y la estructura." data-en="Weight decides the hardware and the structure.">El peso decide el herraje y la estructura.</h2>
      </div>
      <div>
        <p data-es="Hasta unos 250 kg alcanza un herraje oculto de catálogo. Entre 250 y 500 kg se usa un herraje de alta capacidad. Por encima de 500 kg la puerta pide herraje a medida e ingeniería especial, y la estructura del edificio debe preverla desde el inicio." data-en="Up to about 250 kg a concealed catalog hardware is enough. Between 250 and 500 kg a high-capacity hardware is used. Above 500 kg the door calls for custom hardware and special engineering, and the building's structure must anticipate it from the start.">Hasta unos 250 kg alcanza un herraje oculto de catálogo. Entre 250 y 500 kg se usa un herraje de alta capacidad. Por encima de 500 kg la puerta pide herraje a medida e ingeniería especial, y la estructura del edificio debe preverla desde el inicio.</p>
      </div>
    </div>
    {tabla_materiales()}
  </div>
</section>

<section id="ingenieria" class="on-dark empresas">
  <div class="wrap">
    <div class="rise">
      <p class="eyebrow" data-es="CONSIDERACIONES DE INGENIERÍA Y ARQUITECTURA" data-en="ENGINEERING AND ARCHITECTURE CONSIDERATIONS">CONSIDERACIONES DE INGENIERÍA Y ARQUITECTURA</p>
      <h2 class="big" data-es="Lo que revisamos en cada proyecto." data-en="What we review in every project.">Lo que revisamos en cada proyecto.</h2>
      <p class="lead" data-es="Una puerta de este tamaño es una pieza de ingeniería. Estas diez consideraciones se revisan con el arquitecto y el ingeniero estructural desde el inicio, y quedan escritas en la propuesta." data-en="A door of this size is a piece of engineering. These ten considerations are reviewed with the architect and the structural engineer from the start, and are written into the proposal.">Una puerta de este tamaño es una pieza de ingeniería. Estas diez consideraciones se revisan con el arquitecto y el ingeniero estructural desde el inicio, y quedan escritas en la propuesta.</p>
    </div>
    <div class="fx__obras fx__obras--dark rise">{consideraciones()}</div>
  </div>
</section>

<section class="on-dark">
  <div class="wrap center">
    <h2 class="big" data-es="Su puerta, diseñada a su medida." data-en="Your door, designed to your measure.">Su puerta, diseñada a su medida.</h2>
    <p><a class="pill pill--gold" href="contacto.html" data-es="Cotizar mi puerta" data-en="Get a door quote">Cotizar mi puerta</a></p>
    <p class="fx__disp" data-es="Disponible en Colombia y Latinoamérica." data-en="Available in Colombia and Latin America.">Disponible en Colombia y Latinoamérica.</p>
  </div>
</section>

<div class="lb" id="lb" hidden aria-hidden="true"><button class="lb__x" type="button" aria-label="Cerrar">&times;</button><img class="lb__img" alt=""></div>
'''
(RAIZ/"pages"/"puertas-catalogo.html").write_text(cat_html,encoding="utf-8")

# ---------- Página de la línea (B2B primero) ----------
espacios_b2b="".join([
 card("Oficinas y sedes corporativas","Offices and corporate headquarters","La primera puerta que cruzan clientes y equipo. Una entrada con presencia dice cómo trabaja la empresa.","The first door clients and staff cross. An entrance with presence says how the company works."),
 card("Grandes locales y puntos de venta","Large stores and retail points","Puertas de vidrio de piso a techo que abren el local a la calle y hacen de la vitrina un solo gesto.","Floor-to-ceiling glass doors that open the store to the street and make the storefront a single gesture."),
 card("Hoteles y centros comerciales","Hotels and shopping centers","Accesos de doble altura con puertas de gran escala, para recibir con la imponencia de un edificio.","Double-height entrances with large-scale doors, to welcome with the imposing presence of a building."),
 card("Restaurantes y concesionarios","Restaurants and dealerships","Una puerta que se vuelve imagen de marca: madera, panel o vidrio, con iluminación integrada.","A door that becomes brand image: wood, panel or glass, with integrated lighting."),
 card("Clínicas y edificios institucionales","Clinics and institutional buildings","Puertas amplias, claras y de fácil operación, resueltas con la misma ingeniería.","Wide, clear, easy-to-operate doors resolved with the same engineering."),
 card("Residencias de lujo","Luxury residences","El acceso principal que anuncia la casa antes de entrar. Madera, vidrio o panel, a la medida del diseño.","The main entrance that announces the home before you step in. Wood, glass or panel, made to the measure of the design."),
])
medidas="".join([
 obra("2 × 5 M","2 × 5 M","Esbelta y alta","Slender and tall","Entradas estrechas con la proporción de una columna.","Narrow entrances with the proportion of a column."),
 obra("3 × 4 M","3 × 4 M","Ancha y serena","Wide and serene","Una hoja que abre como una pared, para vestíbulos y accesos principales.","A leaf that opens like a wall, for lobbies and main entrances."),
 obra("3 × 5 M","3 × 5 M","La medida de referencia","The reference size","Una hoja de quince metros cuadrados, diseñada y calculada a la medida de la obra.","A fifteen-square-meter leaf, designed and calculated to the measure of the work."),
])
estr="".join([
 obra("1","1","El peso de la hoja","The weight of the leaf","Se calcula con el tamaño y el material: madera maciza, vidrio, aluminio, panel o metal pesan distinto.","It is calculated from the size and the material: solid wood, glass, aluminum, panel or metal weigh differently."),
 obra("2","2","El dintel y la viga superior","The lintel and head beam","Reciben el pivote superior y la carga horizontal. Se dimensionan antes de fundir.","They receive the top pivot and the horizontal load. They are sized before pouring."),
 obra("3","3","El piso y la placa","The floor and slab","Soportan el pivote inferior y todo el peso de la hoja. Se dejan reforzados y nivelados.","They carry the bottom pivot and the full weight of the leaf. They are left reinforced and level."),
 obra("4","4","Los apoyos laterales","The side supports","Columnas o muros rígidos que mantienen el marco a escuadra y limitan la deformación.","Rigid columns or walls that keep the frame square and limit deformation."),
 obra("5","5","Las tolerancias y la dilatación","Tolerances and expansion","La madera, el aluminio y el vidrio se dilatan distinto. Se prevén holguras y sellos para cada material.","Wood, aluminum and glass expand differently. Clearances and seals are planned for each material."),
 obra("6","6","El ingreso a obra","Access to the site","Una hoja de este tamaño entra con grúa o con ruta definida. Se planea el izaje y la instalación.","A leaf of this size arrives by crane or along a defined route. Lifting and installation are planned."),
])
mat="".join([
 obra("MADERA","WOOD","Madera noble","Fine wood","Nogal, roble y otras maderas, macizas o enchapadas, con núcleo balanceado y acabados para exterior.","Walnut, oak and other woods, solid or veneered, with a balanced core and exterior finishes."),
 obra("VIDRIO","GLASS","Vidrio y aluminio","Glass and aluminum","Hojas de vidrio de piso a techo con perfilería de aluminio negro o bronce.","Floor-to-ceiling glass leaves with black or bronze aluminum framing."),
 obra("PANEL","PANEL","Aluminio compuesto y HPL","Aluminum composite and HPL","Hojas lisas en paneles de bajo mantenimiento, del mismo material de la fachada.","Smooth leaves in low-maintenance panels, in the same material as the façade."),
 obra("LAMAS","SLATS","Madera plástica al frente","Wood-plastic fronts","Lamas de madera plástica (WPC) sobre la hoja y el muro, para que la puerta continúe la fachada.","Wood-plastic (WPC) slats over the leaf and the wall, so the door continues the façade."),
 obra("METAL","METAL","Acero y lámina metálica","Steel and sheet metal","Hojas en acero con acabado de pintura o de óxido controlado, y en lámina lisa o perforada.","Steel leaves with painted or controlled-patina finishes, and in smooth or perforated sheet."),
 obra("HERRAJES","HARDWARE","Herrajes e iluminación","Hardware and lighting","Manijas de gran longitud, cerraduras de alta seguridad e iluminación integrada al marco.","Extra-long handles, high-security locks and lighting integrated into the frame."),
])
ing="".join([
 card("Peso y carga","Weight and load","Cada hoja se calcula por peso y por carga antes de fabricar, para que gire con la suavidad de una puerta común.","Each leaf is calculated by weight and load before fabrication, so it turns as smoothly as an ordinary door."),
 card("Pivote superior e inferior","Top and bottom pivot","Herrajes pivotantes de alta capacidad, ocultos en el marco y en el piso, dimensionados para la hoja.","High-capacity pivot hardware, concealed in the frame and floor, sized for the leaf."),
 card("Marco y refuerzos","Frame and reinforcement","Marco y refuerzos internos que mantienen la hoja plana y firme a lo largo del tiempo.","Frame and internal reinforcements that keep the leaf flat and firm over time."),
 card("Agua, aire y viento","Water, air and wind","Perfiles, sellos y umbrales pensados para el exterior: lluvia, viento y clima agresivo.","Profiles, seals and thresholds designed for the outdoors: rain, wind and harsh climates."),
 card("Madera estable","Stable wood","Control de humedad y núcleo balanceado para que la madera se mantenga estable con los cambios de clima.","Moisture control and a balanced core so the wood stays stable through climate changes."),
 card("Instalación y garantía","Installation and warranty","Instalación por cuadrilla especializada y garantía de la puerta, con un solo responsable de principio a fin.","Installation by a specialized crew and a door warranty, with one accountable partner from start to finish."),
])
tiles="".join(f'<figure class="fx__t"><a href="puertas-catalogo.html#modelos"><img src="assets/img/fachadas/cat-puerta-{m[0]}.jpg" alt="Modelo {m[1]}" loading="lazy"></a><figcaption>{bi(m[1],m[2],"b")}{bi(m[3],m[4])}</figcaption></figure>' for m in MODELOS)
qa=[("¿Qué medidas hacen?","What sizes do you make?","Nuestra medida de referencia es 3 × 5 metros, y una puerta puede ser mayor o menor. El tamaño se define con el proyecto estructural, según el peso, el material y la obra.","Our reference size is 3 × 5 meters, and a door can be larger or smaller. The size is defined with the structural project, according to weight, material and the work."),
("¿Cuándo hay que pensar en la puerta?","When should the door be planned?","Desde el inicio de la obra. El peso de la hoja se calcula con el proyecto estructural, para dejar listos el dintel, los apoyos laterales y el piso donde se anclan los herrajes.","From the start of the work. The leaf's weight is calculated with the structural project, so the lintel, side supports and the floor where the hardware anchors are ready."),
("¿Cuánto pesa una puerta de gran formato?","How much does a large-format door weigh?","Depende del material. Como referencia, una hoja de 3 × 4 metros pesa unos 190 kg en aluminio compuesto, unos 420 kg en madera enchapada y unos 575 kg en vidrio laminado. La tabla de pesos muestra cada material.","It depends on the material. As a reference, a 3 × 4 meter leaf weighs about 190 kg in aluminum composite, about 420 kg in veneered wood and about 575 kg in laminated glass. The weight table shows each material."),
("¿Solo se hacen en madera?","Are they only made in wood?","La madera es una opción. También hacemos hojas en vidrio y aluminio, aluminio compuesto, HPL, madera plástica al frente y acero o lámina metálica, solos o combinados.","Wood is one option. We also make leaves in glass and aluminum, aluminum composite, HPL, wood-plastic fronts and steel or sheet metal, alone or combined."),
("¿Sirven para exterior?","Are they suitable for the outdoors?","Sí. Se diseñan para sol, lluvia y viento, con sellos, umbrales y acabados de exterior.","Yes. They are designed for sun, rain and wind, with seals, thresholds and exterior finishes."),
("¿Dónde está disponible?","Where is it available?","Esta línea está disponible en Colombia y en Latinoamérica.","This line is available in Colombia and Latin America.")]
items="".join(f'<details class="fx__q"><summary data-es="{a}" data-en="{b}">{a}</summary><p data-es="{c}" data-en="{d}">{c}</p></details>' for a,b,c,d in qa)
ld={"@context":"https://schema.org","@graph":[{"@type":"Service","name":"Puertas arquitectónicas de gran formato","serviceType":"Cálculo, diseño, fabricación e instalación de puertas pivotantes de gran formato en madera, vidrio, aluminio, aluminio compuesto, HPL, madera plástica y acero, para empresas y residencias; medida de referencia 3 x 5 metros","provider":{"@type":"Organization","name":"Infinitum","url":"https://infinitum.archi"},"areaServed":[{"@type":"Country","name":"Colombia"},{"@type":"Place","name":"Latinoamérica"}]},{"@type":"FAQPage","mainEntity":[{"@type":"Question","name":a,"acceptedAnswer":{"@type":"Answer","text":c}} for a,b,c,d in qa]}]}
galeria="".join(fig(f"cat-puerta-{i}.jpg",f"Imagen de referencia, modelo {i} de puertas arquitectónicas") for i in (1,2,5,7))
com_block=f'''<section id="comercial" class="pv__proy" style="background:var(--paper)">
  <div class="wrap">
    <div class="pv__cab rise">
      <div>
        <p class="eyebrow" data-es="LOCALES COMERCIALES" data-en="RETAIL STORES">LOCALES COMERCIALES</p>
        <h2 data-es="Puertas de vidrio que abren el local a la calle." data-en="Glass doors that open the store to the street.">Puertas de vidrio que abren el local a la calle.</h2>
      </div>
      <div>
        <p data-es="El vidrio comercial más común en Colombia mide hasta 3,20 m de altura en una sola pieza, y con esa medida se diseña la puerta. Si el local pide más altura, se sube con un segundo vidrio sobre un travesaño horizontal. Ese travesaño deja de ser un detalle: se convierte en estructura y en diseño, y trabaja en conjunto con las puertas." data-en="The most common commercial glass in Colombia is up to 3.20 m tall in a single piece, and the door is designed to that size. If the store calls for more height, it rises with a second glass over a horizontal transom. That transom stops being a detail: it becomes structure and design, working together with the doors.">El vidrio comercial más común en Colombia mide hasta 3,20 m de altura en una sola pieza, y con esa medida se diseña la puerta. Si el local pide más altura, se sube con un segundo vidrio sobre un travesaño horizontal. Ese travesaño deja de ser un detalle: se convierte en estructura y en diseño, y trabaja en conjunto con las puertas.</p>
        <div class="pv__chips"><span data-es="Vidrio de 3,20 m" data-en="3.20 m glass">Vidrio de 3,20 m</span><span data-es="Travesaño estructural" data-en="Structural transom">Travesaño estructural</span><span data-es="Doble altura" data-en="Double height">Doble altura</span></div>
      </div>
    </div>
    <div class="fx__rej rise" style="--c:3">{"".join(fig(f"com-{i}.jpg",a) for i,a in ((1,"Imagen de referencia: boutique con puerta pivotante de vidrio de 3,20 m"),(2,"Imagen de referencia: farmacia o clínica con puertas de vidrio de 3,20 m y banda fija superior"),(3,"Imagen de referencia: restaurante con puerta de vidrio pivotante de 3,20 m")))}</div>
    <p class="fx__nota rise" data-es="Imágenes ilustrativas de referencia. No son obras de Infinitum." data-en="Illustrative reference images. They are not Infinitum projects.">Imágenes ilustrativas de referencia. No son obras de Infinitum.</p>
  </div>
</section>

<section id="residencial" class="pv__proy">
  <div class="wrap">
    <div class="pv__cab rise">
      <div>
        <p class="eyebrow" data-es="RESIDENCIAL" data-en="RESIDENTIAL">RESIDENCIAL</p>
        <h2 data-es="La puerta como monumento de la casa." data-en="The door as the home's monument.">La puerta como monumento de la casa.</h2>
      </div>
      <div>
        <p data-es="En una casa de lujo la puerta es la primera pieza de arquitectura que se toca. Madera noble, vidrio o panel, con lamas al frente o a ras del muro, y una escala que anuncia el diseño antes de entrar." data-en="In a luxury home the door is the first piece of architecture you touch. Fine wood, glass or panel, with slats on the front or flush with the wall, and a scale that announces the design before you step in.">En una casa de lujo la puerta es la primera pieza de arquitectura que se toca. Madera noble, vidrio o panel, con lamas al frente o a ras del muro, y una escala que anuncia el diseño antes de entrar.</p>
      </div>
    </div>
    <div class="fx__rej rise" style="--c:3">{"".join(fig(s_,a) for s_,a in (("puertas-madera.jpg","Imagen de referencia: puerta pivotante de roble en muro de piedra"),("cat-puerta-3.jpg","Imagen de referencia: puerta de nogal de cinco metros en villa de lujo"),("cat-puerta-4.jpg","Imagen de referencia: puerta de roble con lamas de madera plástica al frente"),("puertas-noche.jpg","Imagen de referencia: puerta de madera con pérgola de noche"),("puertas-vidrio.jpg","Imagen de referencia: puerta de vidrio y aluminio negro en residencia"),("puertas-hero.jpg","Imagen de referencia: puerta monumental de nogal en villa contemporánea")))}</div>
    <p class="fx__nota rise" data-es="Imágenes ilustrativas de referencia. No son obras de Infinitum." data-en="Illustrative reference images. They are not Infinitum projects.">Imágenes ilustrativas de referencia. No son obras de Infinitum.</p>
  </div>
</section>

'''
puertas_html=f'''<!--
title: Puertas arquitectónicas de gran formato — Infinitum
desc: Puertas arquitectónicas pivotantes de gran formato para oficinas, puntos de venta, hoteles y residencias de lujo. Ingeniería, diseño, fabricación, instalación y garantía. Disponible en Colombia y Latinoamérica.
slug: puertas.html
-->

<section class="phero">
  <img src="assets/img/fachadas/puertas-hero.jpg" alt="" aria-hidden="true" style="object-position:50% 50%">
  <div class="phero__in">
    <p class="md-marca" data-es="PUERTAS ARQUITECTÓNICAS" data-en="ARCHITECTURAL DOORS">PUERTAS ARQUITECTÓNICAS</p>
    <p class="eyebrow" data-es="LÍNEA DE EXTERIOR · INFINITUM" data-en="EXTERIOR LINE · INFINITUM">LÍNEA DE EXTERIOR · INFINITUM</p>
    <h1 data-es="La puerta que se convierte en arquitectura." data-en="The door that becomes architecture.">La puerta que se convierte en arquitectura.</h1>
    <p data-es="Un monumento a la belleza y a la imponencia, para oficinas, puntos de venta, hoteles y casas de lujo. Con 3 × 5 metros como medida de referencia, primero las calculamos, después las diseñamos, las fabricamos, las instalamos y las garantizamos." data-en="A monument to beauty and presence, for offices, retail points, hotels and luxury homes. With 3 × 5 meters as a reference size, we calculate them first, then design, build, install and warranty them.">Un monumento a la belleza y a la imponencia, para oficinas, puntos de venta, hoteles y casas de lujo. Con 3 × 5 metros como medida de referencia, primero las calculamos, después las diseñamos, las fabricamos, las instalamos y las garantizamos.</p>
  </div>
</section>

<section class="pv__indice">
  <div class="wrap">
    <nav class="pf-nav" aria-label="Secciones de puertas arquitectónicas">
      <a href="puertas.html#espacios" data-es="Espacios" data-en="Spaces">Espacios</a>
      <a href="puertas.html#estructura" data-es="Estructura" data-en="Structure">Estructura</a>
      <a href="puertas.html#medidas" data-es="Medidas" data-en="Sizes">Medidas</a>
      <a href="puertas.html#materiales" data-es="Materiales" data-en="Materials">Materiales</a>
      <a href="puertas.html#comercial" data-es="Locales" data-en="Stores">Locales</a>
      <a href="puertas.html#residencial" data-es="Residencial" data-en="Residential">Residencial</a>
      <a href="puertas.html#catalogo" data-es="Catálogo" data-en="Catalogue">Catálogo</a>
      <a href="puertas.html#exterior" data-es="Con la fachada" data-en="With the façade">Con la fachada</a>
      <a href="puertas.html#preguntas" data-es="Preguntas" data-en="Questions">Preguntas</a>
    </nav>
  </div>
</section>

<section class="on-dark empresas" id="espacios">
  <div class="wrap">
    <div class="rise">
      <p class="eyebrow" data-es="PARA EMPRESAS Y PARA CASAS" data-en="FOR BUSINESS AND FOR HOMES">PARA EMPRESAS Y PARA CASAS</p>
      <h2 class="big" data-es="Donde una gran puerta marca la diferencia." data-en="Where a grand door makes the difference.">Donde una gran puerta marca la diferencia.</h2>
      <p class="lead" data-es="Nuestro foco son las empresas: una entrada imponente es lo primero que ven el cliente y el equipo. Las casas de lujo, donde más se aprecia, completan la línea. Hemos instalado puertas de gran formato en residencias, algunas con más de cinco años de uso continuo, y cientos de puertas para oficinas y puntos de venta." data-en="Our focus is business: an imposing entrance is the first thing clients and staff see. Luxury homes, where it is most appreciated, complete the line. We have installed large-format doors in residences, some with more than five years of continuous use, and hundreds of doors for offices and retail points.">Nuestro foco son las empresas: una entrada imponente es lo primero que ven el cliente y el equipo. Las casas de lujo, donde más se aprecia, completan la línea. Hemos instalado puertas de gran formato en residencias, algunas con más de cinco años de uso continuo, y cientos de puertas para oficinas y puntos de venta.</p>
    </div>
    <div class="emp__grid rise">{espacios_b2b}</div>
  </div>
</section>

<section class="on-dark empresas" id="nucleo" style="padding-top:0">
  <div class="wrap">
    <div class="rise">
      <p class="eyebrow" data-es="NUESTRO NÚCLEO" data-en="OUR CORE">NUESTRO NÚCLEO</p>
      <h2 class="big" data-es="Una gran puerta es ingeniería y diseño." data-en="A grand door is engineering and design.">Una gran puerta es ingeniería y diseño.</h2>
      <p class="lead" data-es="Para que una obra sea arquitectónica necesita ingeniería. Una puerta de gran formato no tiene un tamaño fijo: 3 × 5 metros es nuestra referencia, y cada proyecto puede pedir más o menos. Lo que sí se mantiene es la lógica. Cuanto más grande la hoja, más pesa, y ese peso viaja por los pivotes hasta la estructura del edificio. Por eso la puerta se piensa desde el inicio de la obra, junto con el proyecto estructural: se define el tamaño, el material y el peso, y se dejan calculados el dintel, los apoyos laterales y el piso donde se anclan los herrajes. Así la hoja gira con suavidad, permanece plana y estable con los años, y el diseño se construye tal como se dibujó." data-en="For a work to be architectural it needs engineering. A large-format door has no fixed size: 3 × 5 meters is our reference, and each project may call for more or less. The logic stays the same. The larger the leaf, the more it weighs, and that weight travels through the pivots into the building's structure. That is why the door is planned from the start of the work, together with the structural project: size, material and weight are defined, and the lintel, side supports and the floor where the hardware anchors are calculated. This way the leaf turns smoothly, stays flat and stable over the years, and the design is built just as it was drawn.">Para que una obra sea arquitectónica necesita ingeniería. Una puerta de gran formato no tiene un tamaño fijo: 3 × 5 metros es nuestra referencia, y cada proyecto puede pedir más o menos. Lo que sí se mantiene es la lógica. Cuanto más grande la hoja, más pesa, y ese peso viaja por los pivotes hasta la estructura del edificio. Por eso la puerta se piensa desde el inicio de la obra, junto con el proyecto estructural: se define el tamaño, el material y el peso, y se dejan calculados el dintel, los apoyos laterales y el piso donde se anclan los herrajes. Así la hoja gira con suavidad, permanece plana y estable con los años, y el diseño se construye tal como se dibujó.</p>
    </div>
  </div>
</section>

<section id="estructura" class="pv__proy" style="background:var(--paper)">
  <div class="wrap">
    <div class="pv__cab rise">
      <div>
        <p class="eyebrow" data-es="DESDE EL INICIO DE LA OBRA" data-en="FROM THE START OF THE WORK">DESDE EL INICIO DE LA OBRA</p>
        <h2 data-es="Lo que el proyecto estructural debe prever." data-en="What the structural project must anticipate.">Lo que el proyecto estructural debe prever.</h2>
      </div>
      <div>
        <p data-es="Estas son las recomendaciones que damos al arquitecto y al ingeniero estructural cuando el diseño incluye una puerta de gran formato." data-en="These are the recommendations we give the architect and the structural engineer when the design includes a large-format door.">Estas son las recomendaciones que damos al arquitecto y al ingeniero estructural cuando el diseño incluye una puerta de gran formato.</p>
      </div>
    </div>
    <div class="fx__obras rise">{estr}</div>
  </div>
</section>

<section id="medidas" class="pv__proy">
  <div class="wrap">
    <div class="pv__cab rise">
      <div>
        <p class="eyebrow" data-es="MEDIDAS Y PESOS" data-en="SIZES AND WEIGHTS">MEDIDAS Y PESOS</p>
        <h2 data-es="El tamaño lo define el proyecto." data-en="The project defines the size.">El tamaño lo define el proyecto.</h2>
      </div>
      <div>
        <p data-es="3 × 5 metros es nuestra medida de referencia. Una puerta puede ser mayor o menor, siempre que el peso, el material y la estructura del edificio se calculen juntos. El peso depende del material, y el herraje depende del peso." data-en="3 × 5 meters is our reference size. A door can be larger or smaller, as long as the weight, the material and the building's structure are calculated together. Weight depends on the material, and the hardware depends on the weight.">3 × 5 metros es nuestra medida de referencia. Una puerta puede ser mayor o menor, siempre que el peso, el material y la estructura del edificio se calculen juntos. El peso depende del material, y el herraje depende del peso.</p>
      </div>
    </div>
    <div class="fx__obras rise">{medidas}</div>
    {tabla_materiales()}
  </div>
</section>

<section id="ingenieria" class="on-dark empresas">
  <div class="wrap">
    <div class="rise">
      <p class="eyebrow" data-es="INGENIERÍA" data-en="ENGINEERING">INGENIERÍA</p>
      <h2 class="big" data-es="Lo que calculamos y construimos." data-en="What we calculate and build.">Lo que calculamos y construimos.</h2>
    </div>
    <div class="emp__grid rise">{ing}</div>
  </div>
</section>

<section id="materiales" class="pv__proy">
  <div class="wrap">
    <div class="pv__cab rise">
      <div>
        <p class="eyebrow" data-es="MATERIALES" data-en="MATERIALS">MATERIALES</p>
        <h2 data-es="Cada material cambia el peso y la ingeniería." data-en="Each material changes the weight and the engineering.">Cada material cambia el peso y la ingeniería.</h2>
      </div>
      <div>
        <p data-es="La madera no es la única opción. Elegimos el material por su comportamiento al sol, al agua y al paso del tiempo, y por el peso que la estructura puede recibir. La puerta puede acompañar la fachada o convertirse en su gesto principal." data-en="Wood is not the only option. We choose the material for how it behaves in sun, water and time, and for the weight the structure can receive. The door can accompany the façade or become its main gesture.">La madera no es la única opción. Elegimos el material por su comportamiento al sol, al agua y al paso del tiempo, y por el peso que la estructura puede recibir. La puerta puede acompañar la fachada o convertirse en su gesto principal.</p>
      </div>
    </div>
    <div class="fx__obras rise">{mat}</div>
  </div>
</section>

{com_block}<section id="catalogo" class="pv__proy" style="background:var(--paper)">
  <div class="wrap">
    <div class="pv__cab rise">
      <div>
        <p class="eyebrow" data-es="CATÁLOGO" data-en="CATALOGUE">CATÁLOGO</p>
        <h2 data-es="Nueve modelos de referencia." data-en="Nine reference models.">Nueve modelos de referencia.</h2>
      </div>
      <div>
        <p data-es="De la sede corporativa a la casa de lujo, en vidrio, madera, aluminio compuesto y acero. Cada modelo trae su medida, su peso y su herraje." data-en="From the corporate headquarters to the luxury home, in glass, wood, aluminum composite and steel. Each model carries its size, weight and hardware.">De la sede corporativa a la casa de lujo, en vidrio, madera, aluminio compuesto y acero. Cada modelo trae su medida, su peso y su herraje.</p>
        <div class="pv__chips"><a class="pill pill--gold" href="puertas-catalogo.html" data-es="Ver el catálogo completo" data-en="See the full catalogue">Ver el catálogo completo</a></div>
      </div>
    </div>
    <div class="fx__rej fx__rej--t rise" style="--c:4">{tiles}</div>
    <p class="fx__nota rise" data-es="Imágenes ilustrativas de referencia de cada modelo. Las fotografías de obra de Infinitum se suman a medida que las producimos." data-en="Illustrative reference images of each model. Infinitum project photographs are added as we produce them.">Imágenes ilustrativas de referencia de cada modelo. Las fotografías de obra de Infinitum se suman a medida que las producimos.</p>
  </div>
</section>

<section id="exterior" class="on-dark empresas">
  <div class="wrap">
    <div class="rise">
      <p class="eyebrow" data-es="LÍNEA DE EXTERIOR" data-en="EXTERIOR LINE">LÍNEA DE EXTERIOR</p>
      <h2 class="big" data-es="Una fachada con una gran puerta lo dice todo." data-en="A façade with a grand door says it all.">Una fachada con una gran puerta lo dice todo.</h2>
      <p class="lead" data-es="La puerta, la fachada y la pérgola se diseñan juntas, con los mismos materiales y el mismo estándar de obra, para que el exterior se lea como una sola pieza y con bajo costo de mantenimiento." data-en="The door, the façade and the pergola are designed together, with the same materials and the same standard of work, so the exterior reads as a single piece with low maintenance cost.">La puerta, la fachada y la pérgola se diseñan juntas, con los mismos materiales y el mismo estándar de obra, para que el exterior se lea como una sola pieza y con bajo costo de mantenimiento.</p>
    </div>
    <div class="emp__grid rise">
      <div class="emp__card"><h3 data-es="Fachadas" data-en="Façades">Fachadas</h3><p data-es="Aluminio compuesto, HPL, vidrio y madera tecnológica para exteriores." data-en="Aluminum composite, HPL, glass and engineered wood for exteriors.">Aluminio compuesto, HPL, vidrio y madera tecnológica para exteriores.</p><p><a class="pill pill--line" href="fachadas.html" data-es="Ver fachadas" data-en="See façades">Ver fachadas</a></p></div>
      <div class="emp__card"><h3 data-es="Pérgolas arquitectónicas" data-en="Architectural pergolas">Pérgolas arquitectónicas</h3><p data-es="Sombra, protección de la lluvia y luz integrada para terrazas, restaurantes y accesos." data-en="Shade, rain protection and integrated light for terraces, restaurants and entrances.">Sombra, protección de la lluvia y luz integrada para terrazas, restaurantes y accesos.</p><p><a class="pill pill--line" href="fachadas.html#pergolas" data-es="Ver pérgolas" data-en="See pergolas">Ver pérgolas</a></p></div>
      <div class="emp__card"><h3 data-es="Puertas arquitectónicas" data-en="Architectural doors">Puertas arquitectónicas</h3><p data-es="Hojas pivotantes de gran formato, calculadas desde el inicio de la obra." data-en="Large-format pivot leaves, calculated from the start of the work.">Hojas pivotantes de gran formato, calculadas desde el inicio de la obra.</p><p><a class="pill pill--line" href="puertas-catalogo.html" data-es="Ver el catálogo" data-en="See the catalogue">Ver el catálogo</a></p></div>
    </div>
  </div>
</section>

<section id="preguntas" class="pv__proy">
  <div class="wrap">
    <div class="rise">
      <p class="eyebrow" data-es="PREGUNTAS FRECUENTES" data-en="FREQUENTLY ASKED QUESTIONS">PREGUNTAS FRECUENTES</p>
      <h2 data-es="Lo que preguntan arquitectos y propietarios." data-en="What architects and owners ask.">Lo que preguntan arquitectos y propietarios.</h2>
    </div>
    <div class="fx__faq rise">{items}</div>
  </div>
</section>

<section class="on-dark">
  <div class="wrap center">
    <h2 class="big" data-es="Su puerta, la próxima." data-en="Your door, next.">Su puerta, la próxima.</h2>
    <p><a class="pill pill--gold" href="contacto.html" data-es="Cotizar mi puerta" data-en="Get a door quote">Cotizar mi puerta</a></p>
    <p class="fx__disp" data-es="Esta línea está disponible en Colombia y Latinoamérica." data-en="This line is available in Colombia and Latin America.">Esta línea está disponible en Colombia y Latinoamérica.</p>
  </div>
</section>

<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>

<div class="lb" id="lb" hidden aria-hidden="true"><button class="lb__x" type="button" aria-label="Cerrar">&times;</button><img class="lb__img" alt=""></div>
'''
(RAIZ/"pages"/"puertas.html").write_text(puertas_html,encoding="utf-8")
# resumen de pesos para revisión
for m in MODELOS:
    n,es,_,_,_,clave,w,h,hojas,*_=m
    k,kg=peso_modelo(clave,w,h); print(n,es,f"{w}x{h}",f"{k} kg/m2",f"{kg} kg por hoja",herraje(kg)[0])
for k,(es,en,v) in MAT.items(): print(k,v,[r5(v*a) for _,a in TAM])
