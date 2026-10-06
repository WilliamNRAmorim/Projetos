// gerador de PDF A4 paisagem do packing list (sem biblioteca) - roda na pagina do SharePoint
window.PL={};
(function(PL){
const PAT="212222|222122|222221|121223|121322|131222|122213|122312|132212|221213|221312|231212|112232|122132|122231|113222|123122|123221|223211|221132|221231|213212|223112|312131|311222|321122|321221|312212|322112|322211|212123|212321|232121|111323|131123|131321|112313|132113|132311|211313|231113|231311|112133|112331|132131|113123|113321|133121|313121|211331|231131|213113|213311|213131|311123|311321|331121|312113|312311|332111|314111|221411|431111|111224|111422|121124|121421|141122|141221|112214|112412|122114|122411|142112|142211|241211|221114|413111|241112|134111|111242|121142|121241|114212|124112|124211|411212|421112|421211|212141|214121|412121|111143|111341|131141|114113|114311|411113|411311|113141|114131|311141|411131|211412|211214|211232|2331112".split("|");
const MM=72/25.4;
function c128(txt){const v=[104];for(const ch of txt)v.push(ch.charCodeAt(0)-32);let s=104;for(let i=1;i<v.length;i++)s+=v[i]*i;v.push(s%103);v.push(106);return v.map(x=>PAT[x]).join("");}
function br(n){const [i,d]=n.toFixed(2).split(".");return i.replace(/\B(?=(\d{3})+(?!\d))/g,".")+","+d;}
function esc(t){return t.replace(/\/g,"\\\\").replace(/\(/g,"\(").replace(/\)/g,"\)");}
PL.pdf=function(o){ // o:{op,pn,date,slices,total,pid}
const W=841.89,H=595.28,k=MM,lm=12*k,top=H-12*k;let c="";
const R=(x,y,w,h,fill)=>{c+=(fill?`${fill} rg `:"1 1 1 rg ")+`1.4 w ${x.toFixed(2)} ${y.toFixed(2)} ${w.toFixed(2)} ${h.toFixed(2)} re B\n`;};
const T=(t,x,y,sz,bold,center,w)=>{const tw=t.length*sz*0.52;const px=center?x+w/2-tw/2:x;c+=`0 g BT /${bold?"F2":"F1"} ${sz} Tf ${px.toFixed(2)} ${y.toFixed(2)} Td (${esc(t)}) Tj ET\n`;};
const box=(x,y,w,h,t,sz,bold,fill,center)=>{R(x,y,w,h,fill);T(t,x+3*k,y+h/2-sz*0.35,sz,bold,center,w);};
const bars=(txt,cx,y0,bw,bh)=>{const p=c128(txt);let tw=0;for(const d of p)tw+=+d;tw*=bw;let x=cx-tw/2;c+="0 g\n";for(let i=0;i<p.length;i++){const w=+p[i]*bw;if(i%2==0)c+=`${x.toFixed(2)} ${y0.toFixed(2)} ${w.toFixed(2)} ${bh.toFixed(2)} re f\n`;x+=w;}};
const lw=125*k,rh=11*k;let y=top-rh;
for(const [lab,val,sz] of [["DATE",o.date,15],["LOCAL","DANFOSS DRT",15],["ID PALLET",String(o.op),15],["PART-NUMBER",o.pn,17]]){box(lm,y,38*k,rh,lab,12,true);box(lm+38*k,y,lw-38*k,rh,val,sz,true);y-=rh;}
bars(o.pn,lm+lw/2,y-26*k,(o.pn.length>8?0.5:0.6)*k,22*k);T(o.pn,lm,y-31*k,9,false,true,lw);y-=34*k;
box(lm,y-rh,lw,rh,"TOTAL (m)",13,true,".82 .82 .82",true);y-=rh;
box(lm,y-18*k,lw,18*k,br(o.total),34,true,"1 1 0",true);y-=18*k;
bars(String(Math.round(o.total)),lm+lw/2,y-27*k,0.7*k,22*k);T(br(o.total),lm,y-32*k,9,false,true,lw);
const rx=lm+lw+8*k,rw=W-12*k-rx;
box(rx,top-rh,rw,rh,"PACKING LIST",14,true,".82 .82 .82",true);
const th=(top-rh-14*k-12*k)/14;y=top-rh;const cw=[rw*.12,rw*.38,rw*.12,rw*.38];
let x=rx;["N\272","QTY (m)","N\272","QTY (m)"].forEach((h,i)=>{R(x,y-th,cw[i],th,".82 .82 .82");c+=`0 g BT /F2 10 Tf ${(x+cw[i]/2-(h.startsWith("N")?6:18)).toFixed(2)} ${(y-th/2-3).toFixed(2)} Td (${h}) Tj ET\n`;x+=cw[i];});
y-=th;
for(let i=0;i<13;i++){x=rx;for(let j=0;j<2;j++){const idx=i+1+j*13;const q=idx<=o.slices.length?o.slices[idx-1]:null;
 [String(idx),q===null?"0,00":br(q)].forEach((t,kx)=>{const wd=cw[j*2+kx];R(x,y-th,wd,th,null);T(t,x,y-th/2-3.5,11,false,true,wd);x+=wd;});}y-=th;}
if(o.slices.length>26)c+=`0 g BT /F3 8 Tf ${rx.toFixed(2)} ${(y-4*k).toFixed(2)} Td (* ${o.slices.length} lances; a folha mostra os 26 primeiros. O total acima e o real.) Tj ET\n`;
c+=`.4 g BT /F1 7 Tf ${lm.toFixed(2)} ${(8*k).toFixed(2)} Td (Reimpressao do BD Packing List antigo - packing #${o.pid} - importado em lote \(MEL-237\)) Tj ET\n`;
const objs=["<</Type/Catalog/Pages 2 0 R>>","<</Type/Pages/Kids[3 0 R]/Count 1>>",`<</Type/Page/Parent 2 0 R/MediaBox[0 0 ${W} ${H}]/Contents 7 0 R/Resources<</Font<</F1 4 0 R/F2 5 0 R/F3 6 0 R>>>>>>`,
"<</Type/Font/Subtype/Type1/BaseFont/Helvetica/Encoding/WinAnsiEncoding>>","<</Type/Font/Subtype/Type1/BaseFont/Helvetica-Bold/Encoding/WinAnsiEncoding>>","<</Type/Font/Subtype/Type1/BaseFont/Helvetica-Oblique/Encoding/WinAnsiEncoding>>",`<</Length ${c.length}>>\nstream\n${c}endstream`];
let out="%PDF-1.4\n";const off=[];objs.forEach((b,i)=>{off.push(out.length);out+=`${i+1} 0 obj\n${b}\nendobj\n`;});
const xr=out.length;out+=`xref\n0 ${objs.length+1}\n0000000000 65535 f \n`+off.map(n=>String(n).padStart(10,"0")+" 00000 n \n").join("")+`trailer\n<</Size ${objs.length+1}/Root 1 0 R>>\nstartxref\n${xr}\n%%EOF`;
const u=new Uint8Array(out.length);for(let i=0;i<out.length;i++)u[i]=out.charCodeAt(i)&255;return u;};
})(window.PL);
