#!/usr/bin/env python3
"""Genera pages/estudio-de-arquitectura.html (borrador paralelo, noindex, sin enlace en el menu).
Se corre: python3 tools/generar-estudio.py && python3 build.py
Para publicarla de verdad: quitar la linea `` y sumarla al menu en templates/base.html."""
from html import escape
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def a(es, en):
    return f'data-es="{escape(es)}" data-en="{escape(en)}"'


def p(es, en, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<p{c} {a(es, en)}>{es}</p>'


def h(n, es, en, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<h{n}{c} {a(es, en)}>{es}</h{n}>'


def eyebrow(es, en):
    return f'<p class="eyebrow" {a(es, en)}>{es}</p>'


def cab(eb, titulo, texto, chips=()):
    ch = "".join(f'<span {a(*c)}>{c[0]}</span>' for c in chips)
    ch = f'<div class="pv__chips">{ch}</div>' if ch else ""
    return f'''    <div class="pv__cab rise">
      <div>
        {eyebrow(*eb)}
        {h(2, *titulo)}
      </div>
      <div>
        {p(*texto)}
        {ch}
      </div>
    </div>'''


CONT = [0]


def cards(items, numerar=False):
    o = ""
    for k, tt, d in items:
        n = ""
        if numerar:
            CONT[0] += 1
            n = f'<span class="ar-n">{CONT[0]:02d}</span>'
        o += f'<div><b {a(*k)}>{n}{k[0]}</b><h3 {a(*tt)}>{tt[0]}</h3><p {a(*d)}>{d[0]}</p></div>\n      '
    return f'<div class="fx__obras rise">\n      {o}</div>'


def puerta(href, img, k, tt, d, ir):
    return f'''    <a class="puerta" href="{href}">
      <img src="{img}" alt="" aria-hidden="true">
      <div class="puerta__in">
        <b {a(*k)}>{k[0]}</b>
        <h3 {a(*tt)}>{tt[0]}</h3>
        <p {a(*d)}>{d[0]}</p>
        <span class="puerta__ir" {a(*ir)}>{ir[0]} &rarr;</span>
      </div>
    </a>'''


def svc(n, tt, d):
    return f'''      <div class="svc__row">
        <div class="svc__n">.{n:02d}</div>
        <div>
          <h3 {a(*tt)}>{tt[0]}</h3>
          <p {a(*d)}>{d[0]}</p>
        </div>
      </div>
'''


def galeria(imgs, cols=3):
    o = "".join(f'<a href="{i}" data-lb><img src="{i}" alt="{escape(al)}" loading="lazy"></a>' for i, al in imgs)
    return f'<div class="gal-ed gal-ed--3 rise">{o}</div>'


def faq(items):
    o = ""
    for q, r in items:
        o += f'<details class="fx__q"><summary {a(*q)}>{q[0]}</summary><p {a(*r)}>{r[0]}</p></details>'
    return f'<div class="fx__faq rise">{o}</div>'


def seccion(id_, fondo, eb, titulo, texto, chips, items, imgs, cta, numerar=True):
    s = f'<section id="{id_}" class="pv__proy"{fondo}>\n  <div class="wrap">\n'
    s += cab(eb, titulo, texto, chips) + "\n    " + cards(items, numerar) + "\n"
    if imgs:
        s += "    " + galeria(imgs) + "\n"
    if cta:
        s += (f'    <p class="rise" style="text-align:center;margin-top:28px"><a class="pill pill--gold" '
              f'href="{cta[0]}" {a(cta[1], cta[2])}>{cta[1]}</a></p>\n')
    return s + "  </div>\n</section>\n"


P = ['''<!--
title: Arquitectura — Infinitum Estudio de Arquitectura
desc: Arquitectura para vivir, trabajar y vender. Estudio con [[ANIOS]] años de trayectoria: espacios residenciales, corporativos y puntos de venta, con un solo equipo del primer trazo a la obra terminada.
slug: estudio-de-arquitectura.html
-->
''']

# 1. Portada
P.append(f'''<section class="phero" style="min-height:clamp(520px,88vh,880px)">
  <img src="assets/img/estudio/res-sala.jpg" alt="" aria-hidden="true">
  <div class="phero__in">
    {eyebrow("ESTUDIO DE ARQUITECTURA", "ARCHITECTURE STUDIO")}
    {h(1, "Arquitectura para vivir, trabajar y vender.", "Architecture to live, work and sell.")}
    {p("La arquitectura cambia cómo vive una familia, cómo trabaja un equipo y cómo vende una marca. [[ANIOS]] años construyéndola en Colombia y Estados Unidos.", "Architecture changes how a family lives, how a team works and how a brand sells. [[ANIOS]] years building it in Colombia and the United States.")}
  </div>
</section>
''')

# 2. Tres puertas
P.append('<section style="padding:0">\n  <div class="puertas puertas--fx">')
P.append(puerta("estudio-de-arquitectura.html#corporativo", "assets/img/estudio/cor-pasillo.jpg",
                ("CORPORATIVO", "CORPORATE"),
                ("Arquitectura de oficinas y sedes", "Architecture for offices and headquarters"),
                ("Espacios de trabajo diseñados para el equipo y para los clientes que los visitan, entregados llave en mano.", "Workspaces designed for the team and for the clients who visit them, delivered turnkey."),
                ("Ver productos corporativos", "See corporate products")))
P.append(puerta("estudio-de-arquitectura.html#residencial", "assets/img/estudio/res-sala.jpg",
                ("RESIDENCIAL", "RESIDENTIAL"),
                ("Arquitectura residencial contemporánea", "Contemporary residential architecture"),
                ("Casas y apartamentos con arquitectura, interiorismo y mobiliario a la medida, desde el primer trazo.", "Houses and apartments with architecture, interior design and made-to-measure furniture, from the first line."),
                ("Ver productos residenciales", "See residential products")))
P.append(puerta("estudio-de-arquitectura.html#puntos-de-venta", "assets/img/paseo-junin/pj-01.jpg",
                ("PUNTOS DE VENTA", "RETAIL"),
                ("Arquitectura comercial que se recuerda", "Retail architecture that is remembered"),
                ("Tiendas, joyerías y restaurantes con fachada, exhibición y mobiliario resueltos como una sola pieza.", "Stores, jewelers and restaurants with façade, display and furniture resolved as a single piece."),
                ("Ver productos comerciales", "See retail products")))
P.append('  </div>\n</section>\n')


# 2b. Franja de datos verificables (referente: ZHA)
P.append(f'''<div class="wrap rise" style="margin-top:clamp(28px,4vw,52px)">
  <div class="stats">
    <div class="stat"><b>2005</b><span {a("Inicio de la experiencia", "Experience begins")}>Inicio de la experiencia</span></div>
    <div class="stat"><b data-anios>[[ANIOS]]</b><span {a("Años de trayectoria", "Years of practice")}>Años de trayectoria</span></div>
    <div class="stat"><b>2019</b><span {a("Operación en Estados Unidos", "Operating in the United States")}>Operación en Estados Unidos</span></div>
    <div class="stat"><b>3</b><span {a("Tipologías: residencial, corporativo y comercial", "Typologies: residential, corporate and retail")}>Tipologías: residencial, corporativo y comercial</span></div>
    <div class="stat"><b>1</b><span {a("Equipo responsable del trazo a la obra", "Team accountable from drawing to site")}>Equipo responsable del trazo a la obra</span></div>
  </div>
</div>
''')

# 3. Curaduría
P.append(f'''<section class="on-dark empresas" id="curaduria">
  <div class="wrap">
    <div class="rise">
      {eyebrow("ARQUITECTURA INTEGRADA", "INTEGRATED ARCHITECTURE")}
      {h(2, "Lo que se dibuja es lo que se construye.", "What is drawn is what gets built.", "big")}
      {p("Todo espacio empieza con una pregunta: ¿cómo quiere vivir, trabajar o vender? El equipo que la escucha es el mismo que traza, fabrica y construye. Por eso la respuesta llega completa: proporción, material, luz y detalle.", "Every space starts with a question: how do you want to live, work or sell? The team that listens is the same one that draws, makes and builds. So the answer arrives whole: proportion, material, light and detail.", "lead")}
    </div>
    <div class="ar4 rise">
      <div><b>01</b><h3 {a("Trazo", "Drawing")}>Trazo</h3><p {a("Concepto, planos y vistas realistas con el equipo que luego construye.", "Concept, plans and realistic views by the team that will build.")}>Concepto, planos y vistas realistas con el equipo que luego construye.</p></div>
      <div><b>02</b><h3 {a("Taller", "Workshop")}>Taller</h3><p {a("Carpintería y fachadas fabricadas en nuestra planta con CNC, con el detalle intacto.", "Joinery and façades made in our CNC plant, with the detail intact.")}>Carpintería y fachadas fabricadas en nuestra planta con CNC, con el detalle intacto.</p></div>
      <div><b>03</b><h3 {a("Obra", "Site")}>Obra</h3><p {a("Estructura, acabados e instalación dirigidos por una sola persona responsable.", "Structure, finishes and installation directed by one accountable person.")}>Estructura, acabados e instalación dirigidos por una sola persona responsable.</p></div>
      <div><b>04</b><h3 {a("Entrega", "Handover")}>Entrega</h3><p {a("Revisión final, documentación y garantía por escrito.", "Final review, documentation and a written warranty.")}>Revisión final, documentación y garantía por escrito.</p></div>
    </div>
  </div>
</section>
''')


# 3b. Principios (manifiesto)
P.append(seccion("principios", ' style="background:var(--paper)"',
    ("NUESTROS PRINCIPIOS", "OUR PRINCIPLES"), ("Tres ideas que guían cada proyecto.", "Three ideas that guide every project."),
    ("Un espacio bien pensado se nota en la vida de quien lo usa. Estas tres ideas guían cada plano y cada obra.",
     "A well-thought space shows in the life of the person who uses it. These three ideas guide every drawing and every project."),
    [],
    [(("PRINCIPIO 1", "PRINCIPLE 1"), ("La arquitectura se prueba en la vida diaria", "Architecture is tested in daily life"),
      ("Una casa se mide en la mañana de una familia. Una oficina, en lo que su equipo logra junto. Un local, en quien entra y vuelve.",
       "A house is measured by a family's morning. An office, by what its team achieves together. A store, by who comes in and returns.")),
     (("PRINCIPIO 2", "PRINCIPLE 2"), ("Lo dibujado se construye", "What is drawn gets built"),
      ("Fabricamos la carpintería, calculamos la estructura y dirigimos la obra. La idea llega al espacio con el mismo cuidado con que nació en el plano.",
       "We make the joinery, calculate the structure and direct the site. The idea reaches the space with the same care it had on the drawing.")),
     (("PRINCIPIO 3", "PRINCIPLE 3"), ("El detalle sostiene la emoción", "Detail carries the emotion"),
      ("Una junta limpia, una luz cálida y un encuentro justo de materiales hacen que un espacio se sienta bien antes de entenderse.",
       "A clean joint, a warm light and a precise meeting of materials make a space feel right before it is understood."))],
    [], None, False))

# 4. Corporativo
P.append(seccion("corporativo", "",
    ("CORPORATIVO", "CORPORATE"), ("Productos para empresas.", "Products for companies."),
    ("Una oficina bien pensada se siente cada mañana: en la energía del equipo, en la claridad de las ideas y en la impresión del cliente que llega. Estos son los productos que entregamos todos los días, con arquitectura, obra y mobiliario bajo un solo responsable.",
     "A well-thought office is felt every morning: in the energy of the team, the clarity of ideas and the impression on the client who arrives. These are the products we deliver every day, with architecture, construction and furniture under one party."),
    [("Arquitectura y obra", "Architecture and build"), ("Mobiliario propio", "Own furniture"), ("Llave en mano", "Turnkey")],
    [(("ARQUITECTURA Y OBRA", "ARCHITECTURE AND BUILD"), ("Oficinas y sedes llave en mano", "Turnkey offices and headquarters"),
      ("Del primer boceto a la primera mañana de trabajo en su nueva sede, con una sola propuesta y una sola fecha de entrega.",
       "From the first sketch to the first working morning in your new headquarters, with one proposal and one delivery date.")),
     (("REFORMA", "RENOVATION"), ("Oficinas que siguen funcionando", "Offices that keep working"),
      ("Transformamos su oficina por etapas mientras el equipo sigue trabajando, con cronograma de obra y una persona responsable en sitio.",
       "We transform your office in phases while the team keeps working, with a construction schedule and a person responsible on site.")),
     (("IMAGEN", "IMAGE"), ("Recepción, salas de juntas y áreas de marca", "Reception, meeting rooms and brand areas"),
      ("Los espacios que el cliente recuerda. Los pensamos con la marca: materiales, luz y carpintería que cuentan quién es usted.",
       "The spaces clients remember. We think them with the brand: materials, light and joinery that tell who you are.")),
     (("MOBILIARIO", "FURNITURE"), ("Puestos de trabajo y almacenamiento a la medida", "Workstations and made-to-measure storage"),
      ("Mobiliario fabricado en nuestra planta o abastecido internacionalmente, con ficha técnica y garantía.",
       "Furniture made in our plant or sourced internationally, with spec sheet and warranty."))],
    [("assets/img/estudio/cor-pasillo.jpg", "Pasillo de oficina con vidrio, madera y muro verde"),
     ("assets/img/estudio/cor-sala.jpg", "Sala de juntas con mesa blanca a la medida"),
     ("assets/img/estudio/cor-mesa.jpg", "Mesa de reuniones y carpintería en madera")],
    ("arquitectura-corporativa.html", "Ver la galería corporativa", "See the corporate gallery")))

# 5. Residencial
P.append(seccion("residencial", ' style="background:var(--paper)"',
    ("RESIDENCIAL", "RESIDENTIAL"), ("Productos para hogares.", "Products for homes."),
    ("Un hogar bien pensado cambia las mañanas, ordena las tardes y reúne a la familia. Trabajamos la arquitectura, el interior y el mobiliario como una sola historia, con la luz y los materiales elegidos desde el primer trazo.",
     "A well-thought home changes the mornings, orders the afternoons and brings the family together. We work the architecture, the interior and the furniture as one story, with light and materials chosen from the first line."),
    [("Arquitectura", "Architecture"), ("Interiorismo", "Interior design"), ("Mobiliario a la medida", "Custom furniture")],
    [(("CASA NUEVA", "NEW HOUSE"), ("Arquitectura y construcción", "Architecture and construction"),
      ("Del lote a la primera cena en familia: diseño, licencias, obra y acabados con un solo equipo y un cronograma claro.",
       "From the plot to the first family dinner: design, permits, construction and finishes with one team and a clear schedule.")),
     (("APARTAMENTO", "APARTMENT"), ("Remodelación e interiorismo", "Remodeling and interior design"),
      ("Distribución, cocinas, baños y carpintería para un apartamento que se siente nuevo desde el primer día.",
       "Layout, kitchens, bathrooms and joinery for an apartment that feels new from the first day.")),
     (("FACHADA Y EXTERIOR", "FAÇADE AND EXTERIOR"), ("Fachadas, pérgolas y puertas", "Façades, pergolas and doors"),
      ("El primer saludo de su casa. La diseñamos y fabricamos nosotros, en materiales que resisten el sol y la lluvia con poco mantenimiento.",
       "Your home's first greeting. We design and make it, in materials that withstand sun and rain with low maintenance.")),
     (("MOBILIARIO", "FURNITURE"), ("Cocinas, clósets y piezas a la medida", "Kitchens, closets and made-to-measure pieces"),
      ("Carpintería fabricada en nuestra planta, con medidas exactas y acabados a elegir.",
       "Joinery made in our plant, with exact measurements and finishes of your choice."))],
    [("assets/img/estudio/res-fachada.jpg", "Fachada de casa residencial con piedra, madera y vidrio"),
     ("assets/img/estudio/res-sala.jpg", "Sala de doble altura con vista a la montaña"),
     ("assets/img/estudio/res-cocina.jpg", "Cocina y comedor con isla en piedra y madera"),],
    ("arquitectura-residencial.html", "Ver la galería residencial", "See the residential gallery")))

# 6. Puntos de venta
P.append(seccion("puntos-de-venta", "",
    ("PUNTOS DE VENTA", "RETAIL"), ("Productos para el comercio.", "Products for retail."),
    ("En un local, la arquitectura recibe al cliente antes que el vendedor. Atrae desde el pasillo, guía el recorrido y pone el producto en su mejor luz. Resolvemos la fachada, la exhibición y el mobiliario como una sola pieza.",
     "In a store, architecture greets the customer before the salesperson does. It draws people in from the corridor, guides the route and shows the product in its best light. We resolve the façade, the display and the furniture as one piece."),
    [("Fachada del local", "Storefront"), ("Exhibición", "Display"), ("Mobiliario a la medida", "Custom furniture")],
    [(("TIENDAS Y ALMACENES", "STORES"), ("Del acceso a la caja", "From entrance to checkout"),
      ("Góndolas, islas, mostradores y cielos pensados como un solo sistema para que el cliente recorra el local con gusto.",
       "Shelving, islands, counters and ceilings thought as a single system so customers move through the store with pleasure.")),
     (("JOYERÍAS Y BOUTIQUES", "JEWELERS AND BOUTIQUES"), ("Vitrinas que cuidan lo que exhiben", "Display cases that care for what they show"),
      ("Cristal, luz y detalle a escala íntima, donde cada pieza ocupa su lugar y brilla.",
       "Glass, light and detail at an intimate scale, where each piece has its place and shines.")),
     (("RESTAURANTES", "RESTAURANTS"), ("Locales que se reconocen desde lejos", "Venues recognized from afar"),
      ("Barras, mesas, luz y fachada con la identidad de la marca, listos para recibir a sus comensales.",
       "Bars, tables, light and façade with the identity of the brand, ready to welcome your guests.")),
     (("FACHADA DEL LOCAL", "STOREFRONT"), ("La fachada vende antes de que el cliente entre", "The storefront sells before the customer walks in"),
      ("Vidrio, acero, mural y luz de marca, con la estructura calculada desde el primer plano.",
       "Glass, steel, mural and brand lighting, with the structure calculated from the first drawing."))],
    [("assets/img/paseo-junin/pj-01.jpg", "Paseo Junín, paseo comercial en El Santuario, Antioquia"),
     ("assets/img/paseo-junin/pj-05.jpg", "Arcos de ladrillo con jardineras iluminadas en Paseo Junín"),
     ("assets/img/ventas/fachada-local-1.jpg", "Fachada de un local de calzado con vidrio, acero y mural gráfico")],
    ("puntos-de-venta.html", "Ver puntos de venta", "See retail projects")))


# 7b. Obra seleccionada: ficha estandar (referentes: Studio Gang, Olson Kundig)
def ficha(img, alt, titulo, filas):
    f = "".join(f'<div><dt {a(*k)}>{k[0]}</dt><dd {a(*v)}>{v[0]}</dd></div>' for k, v in filas)
    return f'<a class="ar-ficha" href="{img}" data-lb><figure><img src="{img}" alt="{escape(alt)}" loading="lazy"></figure><h3 {a(*titulo)}>{titulo[0]}</h3><dl>{f}</dl></a>'

FILAS = lambda tip, mat, lin: [(("Tipología", "Typology"), tip), (("Materiales", "Materials"), mat), (("Línea", "Line"), lin)]
P.append(f'''<section id="obra" class="pv__proy" style="background:var(--paper)">
  <div class="wrap">
    <div class="rise">
      {eyebrow("OBRA SELECCIONADA", "SELECTED WORK")}
      {h(2, "Seis espacios, una misma manera de construir.", "Six spaces, one way of building.")}
    </div>
    <div class="ar-fichas rise">
      {ficha("assets/img/estudio/res-fachada.jpg", "Casa residencial con piedra, madera y vidrio", ("Una casa que abre sus brazos al paisaje", "A house that opens its arms to the landscape"),
        FILAS(("Casa residencial", "Residential house"), ("Piedra, madera y vidrio", "Stone, wood and glass"), ("Residencial", "Residential")))}
      {ficha("assets/img/estudio/cor-sala.jpg", "Sala de juntas con mesa blanca a la medida", ("Una sala donde las decisiones se toman con claridad", "A room where decisions are made with clarity"),
        FILAS(("Oficina corporativa", "Corporate office"), ("Superficie sólida, madera y alfombra modular", "Solid surface, wood and modular carpet"), ("Corporativo", "Corporate")))}
      {ficha("assets/img/paseo-junin/pj-01.jpg", "Paseo Junín, paseo comercial con rotulación luminosa", ("Un paseo comercial que se reconoce desde la calle", "A shopping promenade recognized from the street"),
        FILAS(("Paseo comercial", "Shopping promenade"), ("Ladrillo, aluminio compuesto, madera, vidrio y luz", "Brick, aluminum composite, timber, glass and light"), ("Puntos de venta", "Retail")))}
      {ficha("assets/img/estudio/res-pasillo.jpg", "Pasillo de casa con cielo de madera y muro de piedra", ("Un recorrido de madera y luz que invita a entrar", "A path of wood and light that invites you in"),
        FILAS(("Casa residencial", "Residential house"), ("Madera, piedra y vidrio a piso", "Wood, stone and floor-to-ceiling glass"), ("Residencial", "Residential")))}
      {ficha("assets/img/estudio/cor-pasillo.jpg", "Pasillo de oficina con vidrio, madera y muro verde", ("Una oficina con luz, madera y verde", "An office with light, wood and greenery"),
        FILAS(("Oficina corporativa", "Corporate office"), ("Vidrio, madera y muro vegetal", "Glass, wood and a green wall"), ("Corporativo", "Corporate")))}
      {ficha("assets/img/ventas/zona-calzado-2.jpg", "Tienda con columnas metálicas y exhibición con neón", ("Un local donde cada pieza tiene su escena", "A store where every piece has its stage"),
        FILAS(("Local comercial", "Retail store"), ("Acero, madera a la medida y neón", "Steel, made-to-measure wood and neon"), ("Puntos de venta", "Retail")))}
    </div>
  </div>
</section>
''')

# 7. Método
P.append(f'''<section id="metodo" class="pv__proy" style="background:var(--paper)">
  <div class="wrap">
    <div class="rise">
      {eyebrow("CÓMO TRABAJAMOS", "HOW WE WORK")}
      {h(2, "Seis etapas, un solo responsable.", "Six stages, one party accountable.")}
    </div>
    <div class="svc rise">
{svc(1, ("Escucha y programa", "Listening and brief"), ("Conversamos sobre la marca, el equipo, el uso y la inversión. Usted recibe un programa claro del espacio.", "We talk about the brand, the team, the use and the investment. You receive a clear program for the space."))}{svc(2, ("Concepto", "Concept"), ("Una idea de diseño con imágenes, materiales y una primera distribución, para decidir la dirección antes de dibujar más.", "A design idea with images, materials and a first layout, to decide the direction before drawing further."))}{svc(3, ("Anteproyecto", "Preliminary design"), ("Planos, vistas realistas y presupuesto estimado. Aquí se aprueba la forma del proyecto.", "Plans, realistic views and an estimated budget. This is where the shape of the project is approved."))}{svc(4, ("Proyecto ejecutivo", "Construction documents"), ("Planos técnicos, detalles de carpintería, especificación de materiales y presupuesto cerrado.", "Technical drawings, joinery details, material specifications and a closed budget."))}{svc(5, ("Obra y fabricación", "Construction and manufacturing"), ("Obra, carpintería de nuestra planta, abastecimiento internacional e instalación, con cronograma y seguimiento semanal.", "Construction, joinery from our plant, international sourcing and installation, with a schedule and weekly follow-up."))}{svc(6, ("Entrega y garantía", "Handover and warranty"), ("Revisión final, entrega con documentación y garantía por escrito.", "Final review, handover with documentation and a written warranty."))}    </div>
  </div>
</section>
''')

# 8. Por qué Infinitum
P.append(seccion("por-que", "",
    ("LO QUE NOS DIFERENCIA", "WHAT SETS US APART"), ("Un estudio de arquitectura que también construye.", "An architecture studio that also builds."),
    ("Muchos estudios entregan un plano. Nosotros entregamos el espacio terminado, y por eso lo que usted imagina es lo que usted habita.",
     "Many studios deliver a drawing. We deliver the finished space, so what you imagine is what you inhabit."),
    [],
    [(("UN SOLO RESPONSABLE", "ONE PARTY ACCOUNTABLE"), ("Del concepto a la entrega", "From concept to handover"),
      ("Una propuesta, un equipo y una persona que responde por todo el alcance.",
       "One proposal, one team and one person answerable for the whole scope.")),
     (("FABRICACIÓN PROPIA", "OWN MANUFACTURING"), ("Carpintería y fachadas hechas por nosotros", "Joinery and façades made by us"),
      ("Planta con CNC en Medellín: el detalle diseñado se fabrica con toda su precisión.",
       "A CNC plant in Medellín: the detail we design is made with all its precision.")),
     (("ABASTECIMIENTO", "SOURCING"), ("Materiales de todo el mundo", "Materials from around the world"),
      ("Piedra, madera, vidrio y mobiliario abastecidos y traídos con nuestro proceso de importación.",
       "Stone, wood, glass and furniture sourced and brought in through our own import process.")),
     (("TRAYECTORIA", "TRACK RECORD"), ("[[ANIOS]] años de obra", "[[ANIOS]] years of projects"),
      ("Desde 2005 en Colombia, con operación en Estados Unidos desde 2019.",
       "In Colombia since 2005, with operations in the United States since 2019."))],
    [], None, False))

# 9. Preguntas
P.append(f'''<section id="preguntas" class="pv__proy" style="background:var(--paper)">
  <div class="wrap">
    <div class="rise">
      {eyebrow("PREGUNTAS FRECUENTES", "FREQUENTLY ASKED QUESTIONS")}
      {h(2, "Lo que nos preguntan antes de empezar.", "What we are asked before we start.")}
    </div>
    {faq([
        (("¿Cómo se define el valor de un proyecto?", "How is the value of a project defined?"),
         ("Con la propuesta de anteproyecto usted recibe un presupuesto estimado, y con el proyecto ejecutivo un presupuesto cerrado, con cantidades, materiales y fecha de entrega.", "With the preliminary design you receive an estimated budget, and with the construction documents a closed budget, with quantities, materials and a delivery date.")),
        (("¿Pueden diseñar y también construir?", "Can you design and also build?"),
         ("Sí. Es lo que nos distingue: diseñamos, fabricamos la carpintería, abastecemos e instalamos, con un solo responsable.", "Yes. It is what sets us apart: we design, make the joinery, source and install, with one party accountable.")),
        (("¿Trabajan solo en Medellín?", "Do you only work in Medellín?"),
         ("Trabajamos en Colombia y en Latinoamérica, con operación en Estados Unidos. Cada proyecto tiene un responsable en sitio.", "We work in Colombia and Latin America, with operations in the United States. Each project has a person responsible on site.")),
        (("¿Pueden remodelar un espacio que ya funciona?", "Can you renovate a space that is already in use?"),
         ("Sí. Planeamos la obra por etapas para que su equipo o su local sigan operando.", "Yes. We plan the work in phases so your team or your store keeps operating.")),
    ])}
  </div>
</section>
''')

# 9b. Manifiesto de cierre
P.append(f'''<section class="on-dark empresas" id="manifiesto">
  <div class="wrap center rise">
    {eyebrow("LO QUE CREEMOS", "WHAT WE BELIEVE")}
    {h(2, "La arquitectura transforma la vida de quien la habita.", "Architecture transforms the life of the person who inhabits it.", "big")}
    {p("Un espacio bien hecho da calma a una familia, foco a un equipo y confianza a un cliente. Por eso cada proyecto se trata como una promesa: pensado con cuidado, construido con precisión y entregado para durar.", "A well-made space gives calm to a family, focus to a team and confidence to a client. That is why every project is treated as a promise: thought with care, built with precision and delivered to last.", "lead")}
  </div>
</section>
''')

# 10. Cierre
P.append(f'''<section class="on-dark">
  <div class="wrap center">
    {h(2, "Conversemos sobre el espacio que usted imagina.", "Let us talk about the space you imagine.", "big")}
    <p><a class="pill pill--gold" href="contacto.html" {a("Agendar una conversación", "Book a conversation")}>Agendar una conversación</a></p>
  </div>
</section>

<div class="lb" id="lb" hidden aria-hidden="true"><button class="lb__x" type="button" aria-label="Cerrar">&times;</button><img class="lb__img" alt=""></div>
''')

(RAIZ / "pages" / "estudio-de-arquitectura.html").write_text("\n".join(P), encoding="utf-8")
print("ok")
