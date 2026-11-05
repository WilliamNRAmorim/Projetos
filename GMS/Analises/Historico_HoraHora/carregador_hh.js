// Colar inteiro no executor de JavaScript do navegador, numa pagina de danfoss.sharepoint.com (logado).
// Define window.__carregarHH(linhas) e window.__conferirHH(tituloIni, tituloFim). Ver PLANO_HORAHORA.md.
// Cada linha: [titulo, data|null, turno, celula, hora, mangueira, meta, metaAcum, realHora, realAcum, diferenca, tempoParado, motivo, motivo2, comentario, origem, alerta]
(async()=>{
const site="https://danfoss.sharepoint.com/sites/OperationsGuaratingueta";
const LB=site+"/_api/web/lists/getbytitle('HoraHora_Historico')";
const vh={Accept:'application/json;odata=verbose'},nm={headers:{Accept:'application/json;odata=nometadata'}};
window.__tipoHH=(await (await fetch(LB+"?$select=ListItemEntityTypeFullName",nm)).json()).ListItemEntityTypeFullName;
window.__itemHH=(a)=>{const o={__metadata:{type:window.__tipoHH},Title:String(a[0])};
 if(a[1])o.Data=a[1]+'T03:00:00Z';
 const t={2:'Turno',3:'Celula',4:'Hora',5:'Mangueira',12:'Motivo',13:'Motivo2',14:'Comentario',15:'Origem',16:'Alerta'};
 for(const [i,k] of Object.entries(t)) if(a[i]!==null&&a[i]!==undefined&&a[i]!=='') o[k]=a[i];
 const n={6:'Meta',7:'MetaAcum',8:'RealHora',9:'RealAcum',10:'Diferenca',11:'TempoParado'};
 for(const [i,k] of Object.entries(n)) if(a[i]!==null&&a[i]!==undefined) o[k]=a[i];
 return o;};
window.__titulosHH=async()=>{const S=new Set();let url=LB+"/items?$select=Title&$top=5000";
 while(url){const j=await (await fetch(url,nm)).json();j.value.forEach(x=>S.add(Number(x.Title)));url=j['odata.nextLink']||null;}return S;};
// Grava so o que ainda nao existe (pode repetir o mesmo bloco sem duplicar). 8 requisicoes em paralelo.
window.__carregarHH=async(linhas)=>{const S=await window.__titulosHH();const fila=linhas.filter(a=>!S.has(Number(a[0])));const pulados=linhas.length-fila.length;
 const dig=(await (await fetch(site+'/_api/contextinfo',{method:'POST',headers:vh})).text()).match(/"FormDigestValue":"([^"]+)"/)[1];
 const H={...vh,'Content-Type':'application/json;odata=verbose','X-RequestDigest':dig};let ok=0,err=[];
 const w=async()=>{while(fila.length){const a=fila.shift();try{const r=await fetch(LB+'/items',{method:'POST',headers:H,body:JSON.stringify(window.__itemHH(a))});if(r.status==201)ok++;else err.push(a[0]+':'+r.status);}catch(e){err.push(a[0]+':x');}}};
 await Promise.all(Array.from({length:8},w));return {ok,pulados,err:err.slice(0,10),nerr:err.length};};
// Conferencia por faixa de Title: n, duplicados, somas de RealHora, Meta e TempoParado
window.__conferirHH=async(a,b)=>{let all=[],url=LB+"/items?$select=Title,RealHora,Meta,TempoParado&$top=5000";
 while(url){const j=await (await fetch(url,nm)).json();all=all.concat(j.value);url=j['odata.nextLink']||null;}
 let n=0,r=0,m=0,p=0;const V=new Set(),D=new Set();
 for(const x of all){const t=Number(x.Title);if(t>=a&&t<=b){n++;if(V.has(t))D.add(t);V.add(t);r+=x.RealHora||0;m+=x.Meta||0;p+=x.TempoParado||0;}}
 const f=v=>Math.round(v*100)/100;return {n,dup:D.size,real:f(r),meta:f(m),parado:f(p),totalLista:all.length};};
return 'carregador_hh pronto: '+window.__tipoHH;})()
