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
  <img src="assets/img/estudio/res-fachada.jpg" alt="" aria-hidden="true">
  <div class="phero__in">
    {eyebrow("ESTUDIO DE ARQUITECTURA", "ARCHITECTURE STUDIO")}
    {h(1, "Arquitectura para vivir, trabajar y vender.", "Architecture to live, work and sell.")}
    {p("[[ANIOS]] años de arquitectura construida en Colombia y Estados Unidos. Un solo equipo, del primer trazo a la obra terminada.", "[[ANIOS]] years of built architecture in Colombia and the United States. One team, from the first line to the finished project.")}
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
P.append(puerta("estudio-de-arquitectura.html#puntos-de-venta", "assets/img/ventas/fachada-local-1.jpg",
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
      {p("Arquitectura, estructura, taller y obra trabajan bajo un mismo techo. El equipo que traza el primer concepto es el que entrega la obra, y por eso la idea llega completa: proporción, material, luz y detalle. Con [[ANIOS]] años de trayectoria, esa continuidad es nuestra manera de hacer arquitectura.", "Architecture, structure, workshop and site work under one roof. The team that draws the first concept is the one that delivers the project, so the idea arrives whole: proportion, material, light and detail. With [[ANIOS]] years behind us, that continuity is how we practice architecture.", "lead")}
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
    ("La arquitectura se juzga por cómo se vive, se trabaja y se vende en ella. Estos principios orientan cada plano y cada obra.",
     "Architecture is judged by how people live, work and sell in it. These principles guide every drawing and every site."),
    [],
    [(("PRINCIPIO 1", "PRINCIPLE 1"), ("La arquitectura se prueba en uso", "Architecture is tested in use"),
      ("Un hogar, una oficina o un local se miden por el día a día de quienes los usan. Proyectamos desde esa experiencia.",
       "A home, an office or a store is measured by the daily life of the people who use it. We design from that experience.")),
     (("PRINCIPIO 2", "PRINCIPLE 2"), ("Lo dibujado se construye", "What is drawn gets built"),
      ("Fabricamos la carpintería, calculamos la estructura y dirigimos la obra. Nada se pierde entre el plano y el espacio.",
       "We make the joinery, calculate the structure and direct the site. Nothing is lost between the drawing and the space.")),
     (("PRINCIPIO 3", "PRINCIPLE 3"), ("El detalle es parte del concepto", "Detail is part of the concept"),
      ("Una junta, una luz o un encuentro de materiales deciden la calidad de un espacio. Los resolvemos desde el primer trazo.",
       "A joint, a light or a meeting of materials decides the quality of a space. We resolve them from the first line."))],
    [], None, False))

# 4. Corporativo
P.append(seccion("corporativo", "",
    ("CORPORATIVO", "CORPORATE"), ("Productos para empresas.", "Products for companies."),
    ("Una oficina bien diseñada ordena el trabajo y comunica quién es la empresa. Estos son los productos que vendemos todos los días, cada uno con diseño, obra y mobiliario bajo un solo responsable.",
     "A well-designed office organizes the work and communicates who the company is. These are the products we sell every day, each with design, construction and furniture under one party."),
    [("Arquitectura y obra", "Architecture and build"), ("Mobiliario propio", "Own furniture"), ("Llave en mano", "Turnkey")],
    [(("ARQUITECTURA Y OBRA", "ARCHITECTURE AND BUILD"), ("Oficinas y sedes llave en mano", "Turnkey offices and headquarters"),
      ("Programa, distribución, interiorismo, obra, mobiliario e instalación para sedes nuevas, con una sola propuesta y una sola fecha de entrega.",
       "Program, layout, interior design, construction, furniture and installation for new headquarters, with one proposal and one delivery date.")),
     (("REFORMA", "RENOVATION"), ("Oficinas que siguen funcionando", "Offices that keep working"),
      ("Reformas por etapas para que el equipo siga trabajando, con cronograma de obra y una persona responsable en sitio.",
       "Phased renovations so the team keeps working, with a construction schedule and a person responsible on site.")),
     (("IMAGEN", "IMAGE"), ("Recepción, salas de juntas y áreas de marca", "Reception, meeting rooms and brand areas"),
      ("Los espacios que el cliente ve primero, diseñados con la marca: materiales, iluminación y detalles de carpintería.",
       "The spaces clients see first, designed with the brand: materials, lighting and joinery details.")),
     (("MOBILIARIO", "FURNITURE"), ("Puestos de trabajo y almacenamiento a la medida", "Workstations and made-to-measure storage"),
      ("Mobiliario fabricado en nuestra planta o abastecido internacionalmente, con ficha técnica y garantía.",
       "Furniture made in our plant or sourced internationally, with spec sheet and warranty."))],
    [("assets/img/estudio/cor-pasillo.jpg", "Pasillo de oficina con vidrio, madera y muro verde"),
     ("assets/img/estudio/cor-sala.jpg", "Sala de juntas con mesa blanca a la medida"),
     ("assets/img/estudio/cor-mesa.jpg", "Mesa de reuniones y carpintería en madera")],
    ("contacto.html", "Hablar de mi oficina", "Talk about my office")))

# 5. Residencial
P.append(seccion("residencial", ' style="background:var(--paper)"',
    ("RESIDENCIAL", "RESIDENTIAL"), ("Productos para hogares.", "Products for homes."),
    ("Una casa se diseña para la manera en que su familia vive. Trabajamos la arquitectura, el interior y el mobiliario como un solo proyecto, con la luz y los materiales elegidos desde el primer trazo.",
     "A home is designed for the way its family lives. We work the architecture, the interior and the furniture as a single project, with light and materials chosen from the first line."),
    [("Arquitectura", "Architecture"), ("Interiorismo", "Interior design"), ("Mobiliario a la medida", "Custom furniture")],
    [(("CASA NUEVA", "NEW HOUSE"), ("Arquitectura y construcción", "Architecture and construction"),
      ("Del lote a la entrega: diseño, licencias, obra y acabados, con un solo equipo y un cronograma claro.",
       "From the plot to handover: design, permits, construction and finishes, with one team and a clear schedule.")),
     (("APARTAMENTO", "APARTMENT"), ("Remodelación e interiorismo", "Remodeling and interior design"),
      ("Distribución, cocinas, baños, carpintería y mobiliario para apartamentos que se estrenan de nuevo.",
       "Layout, kitchens, bathrooms, joinery and furniture for apartments that feel new again.")),
     (("FACHADA Y EXTERIOR", "FAÇADE AND EXTERIOR"), ("Fachadas, pérgolas y puertas", "Façades, pergolas and doors"),
      ("El exterior de la casa, diseñado y fabricado por nosotros, con materiales de bajo mantenimiento.",
       "The exterior of the house, designed and made by us, in low-maintenance materials.")),
     (("MOBILIARIO", "FURNITURE"), ("Cocinas, clósets y piezas a la medida", "Kitchens, closets and made-to-measure pieces"),
      ("Carpintería fabricada en nuestra planta, con medidas exactas y acabados a elegir.",
       "Joinery made in our plant, with exact measurements and finishes of your choice."))],
    [("assets/img/estudio/res-fachada.jpg", "Fachada de casa residencial con piedra, madera y vidrio"),
     ("assets/img/estudio/res-sala.jpg", "Sala de doble altura con vista a la montaña"),
     ("assets/img/estudio/res-cocina.jpg", "Cocina y comedor con isla en piedra y madera"),],
    ("fachadas.html#residencial", "Ver fachadas residenciales", "See residential façades")))

# 6. Puntos de venta
P.append(seccion("puntos-de-venta", "",
    ("PUNTOS DE VENTA", "RETAIL"), ("Productos para el comercio.", "Products for retail."),
    ("En un local, el diseño trabaja como vendedor: atrae desde el pasillo, ordena el recorrido y pone el producto en su mejor luz. Resolvemos la fachada, la exhibición y el mobiliario como una sola pieza.",
     "In a store, design works as a salesperson: it draws people in from the corridor, organizes the route and shows the product in its best light. We resolve the façade, the display and the furniture as one piece."),
    [("Fachada del local", "Storefront"), ("Exhibición", "Display"), ("Mobiliario a la medida", "Custom furniture")],
    [(("TIENDAS Y ALMACENES", "STORES"), ("Del acceso a la caja", "From entrance to checkout"),
      ("Góndolas, islas, mostradores y cielos diseñados como un solo sistema para que el cliente recorra el local sin perderse.",
       "Shelving, islands, counters and ceilings designed as a single system so customers move through the store without getting lost.")),
     (("JOYERÍAS Y BOUTIQUES", "JEWELERS AND BOUTIQUES"), ("Vitrinas que cuidan lo que exhiben", "Display cases that care for what they show"),
      ("Cristal, iluminación y detalle en una escala íntima, donde cada pieza ocupa su lugar.",
       "Glass, lighting and detail at an intimate scale, where each piece has its place.")),
     (("RESTAURANTES", "RESTAURANTS"), ("Locales que se reconocen desde lejos", "Venues recognized from afar"),
      ("Barras, mesas, iluminación y fachada con la identidad de la marca, listos para operar.",
       "Bars, tables, lighting and façade with the identity of the brand, ready to operate.")),
     (("FACHADA DEL LOCAL", "STOREFRONT"), ("La fachada vende antes de que el cliente entre", "The storefront sells before the customer walks in"),
      ("Vidrio, acero, mural y luz de marca, con la estructura calculada desde el primer plano.",
       "Glass, steel, mural and brand lighting, with the structure calculated from the first drawing."))],
    [("assets/img/ventas/fachada-local-1.jpg", "Fachada de un local de calzado con vidrio, acero y mural gráfico"),
     ("assets/img/ventas/fachada-local-2.jpg", "Fachada de esquina de un local comercial"),
     ("assets/img/ventas/hogar-1.jpg", "Tienda de hogar y decoración en centro comercial")],
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
      {h(2, "Tres espacios, una misma manera de construir.", "Three spaces, one way of building.")}
    </div>
    <div class="ar-fichas rise">
      {ficha("assets/img/estudio/res-fachada.jpg", "Casa residencial con piedra, madera y vidrio", ("Una casa que abre hacia el paisaje", "A house that opens to the landscape"),
        FILAS(("Casa residencial", "Residential house"), ("Piedra, madera y vidrio", "Stone, wood and glass"), ("Residencial", "Residential")))}
      {ficha("assets/img/estudio/cor-sala.jpg", "Sala de juntas con mesa blanca a la medida", ("Una sala de juntas hecha a la medida", "A made-to-measure boardroom"),
        FILAS(("Oficina corporativa", "Corporate office"), ("Superficie sólida, madera y alfombra modular", "Solid surface, wood and modular carpet"), ("Corporativo", "Corporate")))}
      {ficha("assets/img/ventas/fachada-local-1.jpg", "Fachada de local comercial de vidrio y acero con mural", ("Una fachada que se ve desde el pasillo", "A storefront seen from the corridor"),
        FILAS(("Local comercial", "Retail store"), ("Vidrio, acero negro, mural y luz de marca", "Glass, black steel, mural and brand lighting"), ("Puntos de venta", "Retail")))}
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
    ("Muchos estudios dibujan y entregan el plano a un tercero. Nosotros llevamos la arquitectura hasta la obra terminada, y por eso lo dibujado es lo que se ve.",
     "Many studios draw and hand the plans to a third party. We carry the design through to the finished project, so what is drawn is what you see."),
    [],
    [(("UN SOLO RESPONSABLE", "ONE PARTY ACCOUNTABLE"), ("Del concepto a la entrega", "From concept to handover"),
      ("Una propuesta, un equipo y una persona que responde por todo el alcance.",
       "One proposal, one team and one person answerable for the whole scope.")),
     (("FABRICACIÓN PROPIA", "OWN MANUFACTURING"), ("Carpintería y fachadas hechas por nosotros", "Joinery and façades made by us"),
      ("Planta con CNC en Medellín: el detalle diseñado se fabrica sin perder precisión.",
       "A CNC plant in Medellín: the detail we design is made without losing precision.")),
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

# 10. Cierre
P.append(f'''<section class="on-dark">
  <div class="wrap center">
    {h(2, "Conversemos sobre su espacio.", "Let us talk about your space.", "big")}
    <p><a class="pill pill--gold" href="contacto.html" {a("Agendar una conversación de diseño", "Book a design conversation")}>Agendar una conversación de diseño</a></p>
  </div>
</section>

<div class="lb" id="lb" hidden aria-hidden="true"><button class="lb__x" type="button" aria-label="Cerrar">&times;</button><img class="lb__img" alt=""></div>
''')

(RAIZ / "pages" / "estudio-de-arquitectura.html").write_text("\n".join(P), encoding="utf-8")
print("ok")
