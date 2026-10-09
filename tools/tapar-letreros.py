from PIL import Image
import statistics
def _px(im,x,y): return im.getpixel((min(max(x,0),im.width-1),min(max(y,0),im.height-1)))
def _avg(im,pts):
    s=[0,0,0]
    for p in pts:
        c=_px(im,*p)
        for i in range(3): s[i]+=c[i]
    return tuple(v/len(pts) for v in s)
def hfill(im,box):
    x0,y0,x1,y1=box; src=im.copy()
    for y in range(y0,y1):
        a=_avg(src,[(x0-k,y+d) for k in (2,3,4) for d in (-1,0,1)])
        b=_avg(src,[(x1+k,y+d) for k in (1,2,3) for d in (-1,0,1)])
        for x in range(x0,x1):
            t=(x-x0)/max(1,x1-x0-1)
            im.putpixel((x,y),tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3)))
def vfill(im,box):
    x0,y0,x1,y1=box; src=im.copy()
    for x in range(x0,x1):
        a=_avg(src,[(x+d,y0-k) for k in (2,3,4) for d in (-1,0,1)])
        b=_avg(src,[(x+d,y1+k) for k in (1,2,3) for d in (-1,0,1)])
        for y in range(y0,y1):
            t=(y-y0)/max(1,y1-y0-1)
            im.putpixel((x,y),tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3)))
def coons(im,box):
    x0,y0,x1,y1=box; src=im.copy()
    L=[_avg(src,[(x0-k,y+d) for k in (2,3,4) for d in (-1,0,1)]) for y in range(y0,y1)]
    R=[_avg(src,[(x1+k,y+d) for k in (1,2,3) for d in (-1,0,1)]) for y in range(y0,y1)]
    T=[_avg(src,[(x+d,y0-k) for k in (2,3,4) for d in (-1,0,1)]) for x in range(x0,x1)]
    B=[_avg(src,[(x+d,y1+k) for k in (1,2,3) for d in (-1,0,1)]) for x in range(x0,x1)]
    w,h=x1-x0,y1-y0
    for j in range(h):
        for i in range(w):
            tx=i/max(1,w-1); ty=j/max(1,h-1)
            H=[L[j][c]*(1-tx)+R[j][c]*tx for c in range(3)]
            V=[T[i][c]*(1-ty)+B[i][c]*ty for c in range(3)]
            # peso: más cerca del borde horizontal -> más peso a V, y al revés
            dx=min(tx,1-tx); dy=min(ty,1-ty)
            wv=(dx+1e-3)/(dx+dy+2e-3)
            im.putpixel((x0+i,y0+j),tuple(int(V[c]*wv+H[c]*(1-wv)) for c in range(3)))
def medcols(im,box,ref):
    """Repite por columna el color mediano de las filas ref (y0,y1): para láminas y listones verticales."""
    x0,y0,x1,y1=box; r0,r1=ref
    for x in range(x0,x1):
        col=[im.getpixel((x,y)) for y in range(r0,r1)]
        m=tuple(int(statistics.median(c[i] for c in col)) for i in range(3))
        for y in range(y0,y1): im.putpixel((x,y),m)

from PIL import ImageFilter, ImageChops
def patchfit(im,box,dxr,dyr,ring=6,feather=5,step=2):
    """Tapa copiando de otra zona de la misma imagen el trozo que mejor encaja en el borde (para tramas repetidas)."""
    x0,y0,x1,y1=box
    g=im.convert('L'); W,H=g.size; d=list(g.getdata())
    G=lambda x,y:d[y*W+x]
    pts=[]
    for x in range(x0-ring,x1+ring,step):
        for y in list(range(y0-ring,y0))+list(range(y1,y1+ring)): pts.append((x,y))
    for y in range(y0,y1,step):
        for x in list(range(x0-ring,x0))+list(range(x1,x1+ring)): pts.append((x,y))
    best=None
    for dy in dyr:
        for dx in dxr:
            if x0-ring+dx<0 or x1+ring+dx>=W or y0-ring+dy<0 or y1+ring+dy>=H: continue
            # el origen del trozo no debe tocar el cuadro a tapar
            if not (x1+ring+dx<x0-ring or x0-ring+dx>x1+ring or y1+ring+dy<y0-ring or y0-ring+dy>y1+ring): continue
            s=0
            for (x,y) in pts:
                v=G(x,y)-G(x+dx,y+dy); s+=v*v
            if best is None or s<best[0]: best=(s,dx,dy)
    s,dx,dy=best
    src=im.crop((x0+dx,y0+dy,x1+dx,y1+dy))
    # corrige brillo por la diferencia media del anillo
    off=[0,0,0]; n=0
    for (x,y) in pts[::3]:
        a=im.getpixel((x,y)); b=im.getpixel((x+dx,y+dy)); n+=1
        for i in range(3): off[i]+=a[i]-b[i]
    off=[int(o/n) for o in off]
    src=src.point(lambda v,i=0:v)  # copia
    chans=[c.point(lambda v,o=off[i]:max(0,min(255,v+o))) for i,c in enumerate(src.split())]
    src=Image.merge('RGB',chans)
    m=Image.new('L',(x1-x0,y1-y0),0)
    inner=Image.new('L',(x1-x0-2*feather,y1-y0-2*feather),255)
    m.paste(inner,(feather,feather)); m=m.filter(ImageFilter.GaussianBlur(feather/1.5))
    im.paste(src,(x0,y0),m)
    return best

def parche_con_tono(im,box,dx,dy):
    """Pega el trozo (dx,dy) y le corrige el tono con un campo suave tomado de los cuatro bordes."""
    x0,y0,x1,y1=box; W,H=im.size
    D=Image.new('RGB',(W,H),(128,128,128))
    # diferencia solo en el anillo
    for x in range(x0-6,x1+6):
        for y in list(range(y0-6,y0))+list(range(y1,y1+6)):
            a=im.getpixel((x,y)); b=im.getpixel((x+dx,y+dy))
            D.putpixel((x,y),tuple(max(0,min(255,128+a[i]-b[i])) for i in range(3)))
    for y in range(y0,y1):
        for x in list(range(x0-6,x0))+list(range(x1,x1+6)):
            a=im.getpixel((x,y)); b=im.getpixel((x+dx,y+dy))
            D.putpixel((x,y),tuple(max(0,min(255,128+a[i]-b[i])) for i in range(3)))
    coons(D,box)
    for y in range(y0,y1):
        for x in range(x0,x1):
            b=im.getpixel((x+dx,y+dy)); d=D.getpixel((x,y))
            im.putpixel((x,y),tuple(max(0,min(255,b[i]+d[i]-128)) for i in range(3)))

def parche_tono_suave(im,box,dx,dy,ring=8):
    """Igual, pero el tono se corrige solo con la diferencia MEDIA de cada lado (sin arrastrar líneas de la trama)."""
    x0,y0,x1,y1=box
    def media(pts):
        s=[0,0,0]
        for (x,y) in pts:
            a=im.getpixel((x,y)); b=im.getpixel((x+dx,y+dy))
            for i in range(3): s[i]+=a[i]-b[i]
        return [v/len(pts) for v in s]
    T=media([(x,y) for x in range(x0,x1) for y in range(y0-ring,y0-1)])
    B=media([(x,y) for x in range(x0,x1) for y in range(y1+1,y1+ring)])
    L=media([(x,y) for y in range(y0,y1) for x in range(x0-ring,x0-1)])
    R=media([(x,y) for y in range(y0,y1) for x in range(x1+1,x1+ring)])
    out=[]
    for y in range(y0,y1):
        ty=(y-y0)/max(1,y1-y0-1)
        for x in range(x0,x1):
            tx=(x-x0)/max(1,x1-x0-1)
            b=im.getpixel((x+dx,y+dy))
            o=[((T[i]*(1-ty)+B[i]*ty)+(L[i]*(1-tx)+R[i]*tx))/2 for i in range(3)]
            out.append(((x,y),tuple(max(0,min(255,int(b[i]+o[i]))) for i in range(3))))
    for p,c in out: im.putpixel(p,c)

def dilatar(mask,n,W,H):
    for _ in range(n):
        nuevo=set(mask)
        for (x,y) in mask:
            for dx in (-1,0,1):
                for dy in (-1,0,1):
                    X,Y=x+dx,y+dy
                    if 0<=X<W and 0<=Y<H: nuevo.add((X,Y))
        mask=nuevo
    return mask
def rellenar(im,mask):
    """Rellena los píxeles de la máscara de afuera hacia adentro con el promedio de los vecinos ya conocidos."""
    W,H=im.size; mask=set(mask)
    while mask:
        capa=[]
        for (x,y) in mask:
            vs=[im.getpixel((x+dx,y+dy)) for dx in (-1,0,1) for dy in (-1,0,1)
                if (dx or dy) and 0<=x+dx<W and 0<=y+dy<H and (x+dx,y+dy) not in mask]
            if vs: capa.append(((x,y),tuple(sum(v[i] for v in vs)//len(vs) for i in range(3))))
        if not capa: break
        for p,c in capa: im.putpixel(p,c); mask.discard(p)

def en_poligono(p,poly):
    x,y=p; dentro=False; n=len(poly)
    for i in range(n):
        x1,y1=poly[i]; x2,y2=poly[(i+1)%n]
        if (y1>y)!=(y2>y) and x < (x2-x1)*(y-y1)/(y2-y1)+x1: dentro=not dentro
    return dentro
def rellenar_vert(im,mask,limite=None,maxrun=70):
    """Cada píxel enmascarado toma el color interpolado entre el primer píxel libre de arriba y el de abajo en su columna.
    Conserva láminas y listones verticales. Si no hay vecino libre abajo (dentro de 'limite'), copia el de arriba."""
    mask=set(mask); cols={}
    for (x,y) in mask: cols.setdefault(x,[]).append(y)
    W,H=im.size
    for x,ys in cols.items():
        ys.sort(); i=0
        while i<len(ys):
            j=i
            while j+1<len(ys) and ys[j+1]==ys[j]+1: j+=1
            a,b=ys[i],ys[j]
            ya,yb=a-1,b+1
            while (x,ya) in mask and ya>0: ya-=1
            while (x,yb) in mask and yb<H-1: yb+=1
            ok_b = yb<H and (limite is None or en_poligono((x,yb),limite))
            ca=im.getpixel((x,max(ya,0)))
            cb=im.getpixel((x,yb)) if ok_b else ca
            for y in range(a,b+1):
                t=(y-ya)/max(1,yb-ya)
                im.putpixel((x,y),tuple(int(ca[k]*(1-t)+cb[k]*t) for k in range(3)))
            i=j+1

import random, statistics as _st
def rellenar_ruido(im,mask,radio=14,intentos=14,semilla=7):
    """Relleno con textura: cada píxel enmascarado copia un píxel libre cercano, el que más se parece al relleno suave de guía.
    Sirve para follaje y superficies con grano, donde un relleno liso se nota."""
    rnd=random.Random(semilla); W,H=im.size; mask=set(mask)
    guia=im.copy(); rellenar(guia,mask)
    libres=lambda x,y:(0<=x<W and 0<=y<H and (x,y) not in mask)
    out={}
    for (x,y) in mask:
        g=guia.getpixel((x,y)); mejor=None
        for _ in range(intentos):
            q=(x+rnd.randint(-radio,radio),y+rnd.randint(-radio,radio))
            if not libres(*q): continue
            c=im.getpixel(q); d=sum((c[i]-g[i])**2 for i in range(3))
            if mejor is None or d<mejor[0]: mejor=(d,c)
        out[(x,y)]=mejor[1] if mejor else g
    for p,c in out.items(): im.putpixel(p,c)
def rellenar_col_mediana(im,mask,alto=45,filtro=None):
    """Cada píxel enmascarado toma la mediana de los píxeles libres de su columna (vale para listones o tablas con veta vertical)."""
    mask=set(mask); W,H=im.size; out={}
    for (x,y) in mask:
        vs=[im.getpixel((x,yy)) for yy in range(max(0,y-alto),min(H,y+alto+1)) if (x,yy) not in mask
            and (filtro is None or filtro(im.getpixel((x,yy))))]
        out[(x,y)]=tuple(int(_st.median(v[i] for v in vs)) for i in range(3)) if vs else im.getpixel((x,y))
    for p,c in out.items(): im.putpixel(p,c)
