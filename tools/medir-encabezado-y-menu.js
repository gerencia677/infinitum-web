(async()=>{
 const r=e=>e.getBoundingClientRect();
 const W=innerWidth,H=innerHeight;
 const out={W,H,desborde_h:document.documentElement.scrollWidth>W+1};
 const hdr=document.querySelector('.hdr'),logo=document.querySelector('.hdr__logo img'),cot=document.querySelector('.pill--cot'),bur=document.querySelector('.burger');
 out.encabezado={alto:Math.round(r(hdr).height),logo_ancho:Math.round(r(logo).width),logo_alto:Math.round(r(logo).height),choque_logo_cotizar:r(logo).right>r(cot).left-6,burger_dentro:r(bur).right<=W};
 document.querySelector('.burger').click(); await new Promise(x=>setTimeout(x,700));
 const m=document.querySelector('#menu'),nav=document.querySelectorAll('.menu__nav a'),ult=nav[nav.length-1],foot=document.querySelector('.menu__foot'),mlogo=document.querySelector('.menu__top img');
 const fs=parseFloat(getComputedStyle(nav[0]).fontSize);
 out.menu={abierto:m.classList.contains('open'),items:nav.length,fuente_item:fs,logo_alto:Math.round(r(mlogo).height),logo_mayor_que_texto:r(mlogo).height>fs,ultimo_item_bottom:Math.round(r(ult).bottom),foot_bottom:Math.round(r(foot).bottom),cabe_sin_scroll:m.scrollHeight<=m.clientHeight+1&&r(foot).bottom<=H+1&&r(ult).bottom<=r(foot).top+2};
 return JSON.stringify(out);
})()
