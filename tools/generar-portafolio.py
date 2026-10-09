#!/usr/bin/env python3
"""Genera borradores/portafolio.html desde la lista de proyectos de abajo."""
import html
D="Diseño arquitectónico";PL="Planeación";LI="Licenciamiento";CO="Construcción";MO="Mobiliario";IN="Interiorismo";FA="Fachadas";PR="Procurement"
P="assets/img/portafolio/";Q="assets/img/proyectos/"
def c(img,est,tit,meta,desc,chips):
    return dict(img=img,est=est,tit=tit,meta=meta,desc=desc,chips=chips)
LINEAS=[
("comercial","Puntos de venta y comercio","Locales, stands y fachadas diseñados para vender. Del concepto a la instalación, con el mobiliario fabricado por nosotros.",False,[
 c(P+"carino.jpg","Construido","Tienda de moda en centro comercial","Medellín","Probadores curvos, cortinas, mobiliario tapizado y circulación pensada para el recorrido de compra.",[D,IN,MO,CO]),
 c(P+"expo.jpg","Construido","Stand de cuidado natural","Cadena de grandes superficies","Módulo de exhibición con muro verde y mobiliario en madera, replicable por sede.",[D,MO,CO]),
 c(P+"verona.jpg","Construido","Local de calzado urbano","Centro comercial · Medellín","Estantería metálica y madera, vitrina completa y mural gráfico a escala.",[D,MO,CO]),
 c(P+"perfume.jpg","Diseñado","Perfumería de lujo con mezzanine","Medellín · Local de 2 niveles","Vitrinas con herrajes dorados, cielo gráfico y circulación pensada para el recorrido del cliente.",[D,IN,MO]),
 c(P+"fiara.jpg","Construido","Cadena de tiendas de jeans","Montería, Valledupar, Bello y Barranquilla","Un mismo sistema de exhibición adaptado a cada local, con vitrina en rojo y madera.",[D,MO,CO]),
 c(P+"annchery.jpg","Construido","Tienda en centro comercial","Ciudad de México","Isla central, vitrinas retroiluminadas y mostrador de atención.",[D,MO,CO]),
 c(P+"fachada-esquina.jpg","Diseñado","Fachada de moda en esquina","Propuesta diurna y nocturna","Panel metálico facetado, iluminación lineal y acceso a nivel de calle.",[D,FA]),
 c(P+"grillo.jpg","Diseñado","Edificio comercial","Rionegro, Antioquia","Fachada en vidrio y marco metálico oscuro, con locales sobre la calle.",[D,PL,FA]),
 c(P+"dulce.jpg","Diseñado","Bodega comercial de cuatro niveles","Caldas, Antioquia","Fachada en lamas de madera y vidrio, con la marca como remate del volumen.",[D,PL,FA]),
 c("assets/img/hero/hero-comercial-1.jpg","Construido","Barbería de lujo","Tres sedes","Tres locales desarrollados en simultáneo con un mismo lenguaje de materiales.",[D,IN,MO,CO]),
]),
("oficinas","Oficinas y espacios corporativos","Puestos de trabajo, salas y áreas comunes. Diseño, fabricación e instalación con un solo responsable.",True,[
 c(P+"tresvias.jpg","En ejecución","Remodelación de centro comercial","Medellín · Circulaciones y locales","Pasillos con vegetación, iluminación continua y módulos para locales.",[D,PL,CO]),
 c(P+"avgroup.jpg","Construido","Oficinas corporativas","Planta abierta y salas de reunión","Zona de descanso, salas con vidrio y mobiliario de oficina.",[D,IN,MO,CO]),
 c(P+"of-muro.jpg","Construido","Oficinas con muro verde","Medellín","Divisiones en vidrio, mobiliario fabricado y zonas de reunión.",[D,MO,CO]),
 c(P+"of-planta.jpg","Construido","Oficinas de planta abierta","Medellín","Losa aligerada a la vista y vista a la ciudad.",[D,MO,CO]),
 c(Q+"oficina-biofilica.jpg","Construido","Oficina biofílica","Medellín","Vegetación integrada al puesto de trabajo y luz natural.",[D,IN,MO]),
 c(Q+"oficina-corporativa.jpg","Construido","Oficinas corporativas","Medellín","Sala de juntas y puestos con acabados en madera.",[D,MO,CO]),
]),
("gastronomia","Gastronomía y hotelería","Cafés, restaurantes y barras. Cocina, sala y fachada resueltas como una sola pieza.",False,[
 c(P+"roof.jpg","Diseñado","Café en terraza de centro comercial","Barra, cubierta y mobiliario","Cubierta oscura, mesas en madera y barra en U con taburetes.",[D,MO]),
]),
("residencial","Residencial","Casas, apartamentos y fincas de alto patrimonio. Diseño, licencia, obra y mobiliario.",True,[
 c("assets/img/proyectos/casa-cr-banda.jpg","En ejecución","Casa CR","Medellín · 1.527,74 m²","Residencia contemporánea desarrollada de principio a fin: diseño, planos, construcción, mobiliario y acabados.",[D,PL,CO,MO]),
 c(P+"gomezgil.jpg","Diseñado","Casa con piscina","Llanogrande, Rionegro","Volumen en dos niveles con piscina, terraza y sala con chimenea lineal.",[D,IN]),
 c(P+"essenza1.jpg","Diseñado","Casa en parcelación campestre","Oriente antioqueño","Interiores con piedra, madera y vegetación hacia el jardín.",[D,IN,LI]),
 c(P+"sernaduque.jpg","Construido","Casa en concreto y madera","Antioquia","Volúmenes bajos en concreto a la vista, con celosía de madera y jardín.",[D,CO]),
 c(P+"nutibara.jpg","Diseñado","Edificio residencial con fachada verde","Medellín · Avenida Nutibara","Torre esbelta en ladrillo con terrazas jardín y vidrio de piso a techo.",[D,PL]),
 c(P+"finca.jpg","Construido","Finca con casa, terraza y piscina","Llanogrande, Rionegro","Cubierta de teja de barro, corredores y piscina al paisaje.",[D,CO,MO]),
 c(P+"andalucia.jpg","Diseñado","Casa campestre","Andalucía · Parcelación","Casa de dos niveles con jardín y acceso vehicular.",[D,PL]),
 c(P+"arango.jpg","Diseñado","Casa de campo","Puerto Berrío, Antioquia","Cubiertas inclinadas, corredor cubierto y estructura metálica.",[D]),
 c(P+"quintero.jpg","Diseñado","Baño principal y vestier","Llanogrande, Rionegro","Bañera exenta, vestier en madera oscura y espejo con luz integrada.",[D,IN,MO]),
 c(Q+"open-sky.jpg","Construido","Open Sky","Residencial","Vivienda con grandes aperturas hacia el exterior.",[D,CO]),
 c(Q+"horse-house.jpg","Diseñado","Luxury Horse House","Residencial","Casa de lujo con espacios para caballos.",[D]),
 c(Q+"forest-house.jpg","Diseñado","Luxury Forest House","Residencial","Casa integrada al bosque.",[D]),
 c(Q+"garden-living.jpg","Construido","Garden Living","Interiorismo","Sala con relación directa al jardín.",[IN,MO]),
 c(Q+"casa-q.jpg","Construido","Casa Q","Llanogrande","Residencia con fachada en vidrio y madera.",[D,CO]),
 c(Q+"casa-sd.jpg","Construido","Casa SD","Residencial","Terraza y piscina como espacio principal.",[D,CO]),
 c(Q+"casa-sg.jpg","Construido","Casa SG","Residencial","Doble altura con fachada en vidrio y madera.",[D,CO]),
]),
("parcelaciones","Parcelaciones y desarrollo de suelo","Del lote al plano de implantación: loteo, cuadro de áreas, redes y ubicación de las casas.",True,[
 c(P+"capiro.jpg","Diseñado","Agroparcelación","Oriente antioqueño","Plano general de loteo con cuadro de áreas y propuesta de ubicación de las casas.",[PL,"Loteo",LI]),
 c(P+"santuario.jpg","Construido","Equipamiento comercial en contenedores","Santuario, Antioquia","Módulos construidos con administración delegada.",[D,CO]),
]),
("mobiliario","Mobiliario y carpintería","Fabricamos en nuestra planta. Cada pieza sale de un plano de taller con despiece y cuadro de cortes.",False,[
 c(P+"santana.jpg","Fabricado","Closets, cajoneras y vanities","Proyecto residencial","Plano de taller con lista de corte y enchape por pieza.",[MO,"Fabricación"]),
 c(P+"auteco.jpg","Construido","Counter y escritorio de atención","Espacio comercial","Plantas, alzados y despiece del mueble antes de fabricarlo.",[MO,"Fabricación"]),
]),
]
MIAMI=[
 ("Construido","1067 · Motion","Hialeah, Florida","Cocinas, vanities y closets fabricados en Colombia e instalados en Estados Unidos.",[MO,PR,"Instalación"]),
 ("En desarrollo","House of Wellness","Florida","Cuarzo y mobiliario de amenidades en coordinación con el constructor.",[MO,PR]),
 ("Por confirmar","1025 · Hialeah","Hialeah, Florida","Ficha en preparación.",[]),
 ("Por confirmar","Los Domus","Miami, Florida","Ficha en preparación.",[]),
 ("Por confirmar","Domus 123","Miami, Florida","Ficha en preparación.",[]),
 ("Por confirmar","Namdar 222","Florida","Ficha en preparación.",[]),
]
def card(k,cls=""):
    ch="".join(f"<span>{html.escape(x)}</span>" for x in k["chips"])
    return f'<article class="pf {cls}"><div class="pf__img"><img src="{k["img"]}" alt="{html.escape(k["tit"])}, {html.escape(k["meta"])}" loading="lazy"><b class="pf__estado">{k["est"]}</b></div><div class="pf__txt"><h3>{html.escape(k["tit"])}</h3><div class="pf__meta">{html.escape(k["meta"])}</div><p>{html.escape(k["desc"])}</p><div class="pf__chips">{ch}</div></div></article>'
def clases(n):
    cl=["pf--w","" ]+[""]*(n-2) if n>=2 else ["pf--f"]
    if n>=2:
        r=(n-2)%3
        if r==1: cl[-1]="pf--f"
        if r==2: cl[-1]="pf--h"; cl[-2]="pf--h"
    return cl
B="borrador-x7k2/"
out=[]
for id,tit,txt,dark,L in LINEAS:
    cl=clases(len(L))
    out.append(f'<section id="{id}" class="pf-linea{" on-dark" if dark else ""}"><div class="wrap"><div class="pf-linea__cab"><h2>{tit}</h2><p>{txt}</p></div><div class="pf-grid">{"".join(card(k,cl[i]) for i,k in enumerate(L))}</div></div></section>')
def mcard(e,t,m,d,ch):
    chs="".join(f"<span>{x}</span>" for x in ch)
    return f'<article class="pf pf--pend"><div class="pf__img"><img class="pf__sim" src="assets/img/simbolo-dorado.png" alt=""><b class="pf__estado">{e}</b></div><div class="pf__txt"><h3>{t}</h3><div class="pf__meta">{m}</div><p>{d}</p><div class="pf__chips">{chs}</div></div></article>'
out.append('<section id="miami" class="pf-linea on-dark"><div class="wrap"><div class="pf-linea__cab"><h2>Desde Miami, para todo Estados Unidos</h2><p>Más de siete años en Miami, desde 2019. Desarrollamos proyectos desde allí para cualquier estado. Infinitum US LLC es la sociedad que contrata y factura en Estados Unidos. <a href="https://infinitumusa.com" style="color:var(--gold);box-shadow:inset 0 -1px 0 var(--gold)">Visite infinitumusa.com</a></p></div><div class="pf-grid">'+"".join(mcard(*m) for m in MIAMI)+'</div></div></section>')
out.append('<section id="aliados" class="pf-linea"><div class="wrap"><div class="pf-linea__cab"><h2>Aliados</h2><p>Empresas con las que producimos, abastecemos y exhibimos. Cada una abre una puerta distinta.</p></div><div class="aliados"><div><a href="verona-stone.html"><b>Verona Stone</b></a><span>Colombia · Piedra importada con existencias y precio. <a href="verona-stone.html">Ver catálogo</a></span></div><div><b>Huarcaya</b><span>Perú · Alianza de producción</span></div><div><b>Expo Miami</b><span>Estados Unidos · Exhibición y feria</span></div><div><b>Infinitum US · Oficina Miami</b><span>15959 NW 15th Ave, Miami · Operación en Estados Unidos</span></div></div></div></section>')
nav="".join(f'<a href="{B}#{i}">{n}</a>' for i,n in [("comercial","Puntos de venta"),("oficinas","Oficinas"),("gastronomia","Gastronomía"),("residencial","Residencial"),("parcelaciones","Parcelaciones"),("mobiliario","Mobiliario"),("miami","Miami"),("aliados","Aliados")])
head=f'''<!--
title: Portafolio — Infinitum
desc: Obra y diseño por línea de negocio, de Medellín a Miami.
slug: portafolio.html
-->
<section class="phero"><img src="{P}perfume.jpg" alt="" aria-hidden="true"><div class="phero__in"><p class="eyebrow">PORTAFOLIO</p><h1>Diseñado, construido, fabricado.</h1><p>Una selección de lo que hemos hecho, por línea de negocio. Cada proyecto dice en qué etapa está y qué hicimos en él.</p></div></section>
<section><div class="wrap"><nav class="pf-nav" aria-label="Líneas de negocio">{nav}</nav>
<div class="pf-leyenda"><span><i>Construido</i>obra entregada</span><span><i>En ejecución</i>obra en curso</span><span><i>Diseñado</i>proyecto entregado</span><span><i>Fabricado</i>mueble hecho en nuestra planta</span></div></div></section>
'''
tail='<section class="on-dark"><div class="wrap center"><h2 class="big">¿Tiene un proyecto parecido?</h2><p><a class="pill pill--gold" href="contacto.html">Cotizar</a></p></div></section>'
open("borradores/portafolio.html","w").write(head+"\n".join(out)+"\n"+tail)
print("proyectos:",sum(len(l[4]) for l in LINEAS)+len(MIAMI))
