// Colar inteiro no javascript_tool, com o navegador do app numa pagina de danfoss.sharepoint.com (logado).
// Define window.__M, __item e __carregar(tituloInicial, arrayDeLinhasCodificadas). Ver PLANO_CARGA.md.
window.__M=["","2556-10","2556-12","2556-16","2556-3","2556-4","2556-5","2556-6","2556-8","2583-12","2807-10-BRA","2807-12-BRA","2807-8-BRA","EC115-10L","EC115-10LRL","EC115-12","EC115-12L","EC115-12LRL","EC115-16L","EC115-16LRL","EC115-4L","EC115-4LRL","EC115-6L","EC115-6LRL","EC115-8LRL","EC118-04L","EC118-04LRL","EC118-04LRL-01","EC118-06","EC118-06L","EC118-06LRL","EC118-06LRL-01","EC118-08","EC118-08L","EC118-08LRL","EC118-08LRL-01","EC118-10L","EC118-10LRL","EC118-12LRL","EC118-16L","EC118-16LRL","EC215-04L","EC215-04L-BRA","EC215-06","EC215-06L","EC215-06LRL","EC215-08","EC215-08L","EC215-08LRL","EC215-10L","EC215-10LRL","EC215-10LRL-01","EC215-12","EC215-12L","EC215-12LRL","EC215-16L","EC215-16LRL","EC215-16LRL-01","EC415-08LRL","EC415-10LRL","EC415-12LRL","FC310-04","FC310-06","FC310-08","FC310-10","FC310-12","FC310-16","FC598-08","FC598-10","FC598-12-BRA","FC598-8-PROT","FC639-16","FC735-04-BRA","FC735-10","FC735-10-BRA","FC735-12","FC735-12-BRA","FC735-6","FC735-8","FC839B-04","FC839B-04-BRA","FC839B-04-bra","FC839B-06","FC839B-06-01","FC839B-06-BRA","FC839B-6","FC839B-8","FC849-08","GH493-10","GH493-12","GH493-16","GH493-6","GH493-8","GH493-8-BRA","GH506-16","GH663-10","GH663-12","GH663-16","GH663-4","GH663-6","GH663-8","GH681-04-01","GH681-08-01","GH681-10","GH681-12","GH681-16","GH681-4","GH681-6","GH681-8","GH781-06-01","GH781-10","GH781-10-01","GH781-12","GH781-12-01","GH781-12R250BZ","GH781-16","GH781-4","GH781-4-BRA","GH781-6","GH781-8","H28004-250R","H28006-250R","HC101-06-01","HC101-4","HC101-6","HC101-8","HC139-07-01","HC139-7","HC139-7(S/G)","HC3000-4","HC3000-6","HC3000-8","Hc3000-6","Hc3000-8","ec118-04lrl","ec118-06lrl","ec215-16lrl","fc735-10-bra","fc735-12-bra","fc839b-6","gh493-12","gh493-16","gh663-16","gh681-4","gh681-6","gh681-8","gh781-10","gh781-12","gh781-16","gh781-6","gh781-8","hc101-4","hc101-6","hc101-8","hc3000-4","hc3000-6","hc3000-8"];
(async()=>{
const site="https://danfoss.sharepoint.com/sites/OperationsGuaratingueta";
const LB=site+"/_api/web/lists/getbytitle('Historico_Apontamento')";
const vh={Accept:'application/json;odata=verbose'};
window.__tipo=(await (await fetch(LB+"?$select=ListItemEntityTypeFullName",{headers:{Accept:'application/json;odata=nometadata'}})).json()).ListItemEntityTypeFullName;
window.__item=(n,line)=>{const p=line.split(','),d=new Date(Date.UTC(2018,0,1)+Number(p[0])*864e5).toISOString().slice(0,10);
 const o={__metadata:{type:window.__tipo},Title:String(n),Data:d+'T03:00:00Z',Turno:Number(p[1])};
 if(p[2]!=='')o.Mangueira=window.__M[Number(p[2])]; if(p[3]!=='')o.OP=p[3]; if(p[4]!=='')o.QtdAprovada=Number(p[4]);
 for(const m of (p[5]||'').matchAll(/([A-P])(\d*\.?\d+)/g))o['Defeito_'+m[1]]=Number(m[2]);
 if(p[6]!=='')o.QtdReprovada=Number(p[6]);
 if(p[7]){const e=p[7].split('~');if(e[0])o.OData__x0043_O15=e[0];if(e[1])o.MIGO=e[1];if(e[2])o.Delivery=e[2];}
 return o;};
window.__carregar=async(ini,linhas)=>{const dig=(await (await fetch(site+'/_api/contextinfo',{method:'POST',headers:vh})).text()).match(/"FormDigestValue":"([^"]+)"/)[1];
 const H={...vh,'Content-Type':'application/json;odata=verbose','X-RequestDigest':dig};let ok=0,err=[];
 const fila=linhas.map((l,i)=>[ini+i,l]);
 const w=async()=>{while(fila.length){const [n,l]=fila.shift();try{const r=await fetch(LB+'/items',{method:'POST',headers:H,body:JSON.stringify(window.__item(n,l))});if(r.status==201)ok++;else err.push(n+':'+r.status);}catch(e){err.push(n+':x');}}};
 await Promise.all(Array.from({length:8},w));return {ok,err:err.slice(0,10),nerr:err.length};};
// conferencia: contagem e soma por faixa de Title
// percorre odata.nextLink (a lista tem mais de 5.000 itens); devolve tambem duplicatas de Title na faixa
window.__conferir=async(a,b)=>{let n=0,sa=0,sr=0,tot=0,seen=new Set(),dup=0,url=LB+`/items?$select=Id,Title,QtdAprovada,QtdReprovada&$top=5000`;
 while(url){const r=await (await fetch(url,{headers:{Accept:'application/json;odata=nometadata'}})).json();
  for(const x of r.value){tot++;const t=Number(x.Title);if(t>=a&&t<=b){n++;if(seen.has(t))dup++;seen.add(t);sa+=x.QtdAprovada||0;sr+=x.QtdReprovada||0;}}
  url=r['odata.nextLink']||null;}
 return {n,dup,totalLista:tot,aprov:Math.round(sa*10)/10,rep:Math.round(sr*10)/10};};
return 'carregador pronto: '+window.__tipo;})()
