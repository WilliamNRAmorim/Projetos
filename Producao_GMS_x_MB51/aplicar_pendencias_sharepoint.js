// Termina o lote 3 no SharePoint. Rodar no console do navegador (F12) numa aba ja logada em
// https://danfoss.sharepoint.com/sites/OperationsGuaratingueta/  (cole tudo e de Enter).
// 1) troca a OP dos 11 lances que faltaram (so troca se a OP atual ainda for a de origem)
// 2) manda para a lixeira: refugo 4377 (27002870, 1 m) e fichas 654 e 2775 (so se nao tiverem lances)
// 3) acerta quantidade_extracao das fichas das OPs mexidas (so se a ficha estava igual a soma de antes)
(async()=>{
const site="https://danfoss.sharepoint.com/sites/OperationsGuaratingueta/_api/";
const h={Accept:'application/json;odata=nometadata'};
const W=site+"web/lists/getbytitle(";
const dg=(await fetch(site+"contextinfo",{method:'POST',headers:h}).then(r=>r.json())).FormDigestValue;
const hm={...h,'Content-Type':'application/json;odata=nometadata','X-RequestDigest':dg,'IF-MATCH':'*','X-HTTP-Method':'MERGE'};
const log=[];
const L=W+"'RegistrosInspeção')/items";
// 1) lances
const M=[[14984,29963522,30063656,82.7],[14986,29963522,30063656,72.7],[14352,29963533,29994196,31.2],[14355,29963533,29994196,22.2],[14357,29963533,29994196,19.7],[14401,29994196,29963533,71.3],[14406,29994196,29963533,52],[14408,29994196,29963533,18.5],[14760,30007593,30007587,69.9],[15186,30063656,30063654,88.9],[14924,30063851,30063852,134.1]];
for(const [id,de,para,q] of M){
 const c=await fetch(L+"("+id+")?$select=OP_ID,Quantidade_Inspe_x00e7__x00e3_o",{headers:h}).then(r=>r.json());
 if(c.OP_ID===para){log.push(['lance',id,'ja estava']);continue;}
 if(c.OP_ID!==de||Math.abs(c.Quantidade_Inspe_x00e7__x00e3_o-q)>0.005){log.push(['lance',id,'pulado',c.OP_ID]);continue;}
 const r=await fetch(L+"("+id+")",{method:'POST',headers:hm,body:JSON.stringify({OP_ID:para})});log.push(['lance',id,r.status]);
}
// 2) lixeira
const te=await fetch(W+"'TiposErros')/items(4377)?$select=OP_ID,OData__x0043_",{headers:h}).then(r=>r.json());
if(te.OP_ID===27002870&&te.OData__x0043_===1){const r=await fetch(W+"'TiposErros')/items(4377)/recycle()",{method:'POST',headers:{...h,'X-RequestDigest':dg}});log.push(['refugo4377',r.status]);}
for(const [fid,op] of [[654,27002870],[2775,29200475]]){
 const f=await fetch(W+"'ficha_producao')/items("+fid+")?$select=OP",{headers:h}).then(r=>r.json());
 const li=await fetch(L+"?$select=Id&$filter=OP_ID eq "+op,{headers:h}).then(r=>r.json());
 if(f.OP!==op||li.value.length){log.push(['ficha',fid,'nao apagada']);continue;}
 const r=await fetch(W+"'ficha_producao')/items("+fid+")/recycle()",{method:'POST',headers:{...h,'X-RequestDigest':dg}});log.push(['ficha',fid,r.status]);
}
// 3) fichas
const ANTES={"20185934":157.5,"28757194":676.5,"28913921":225.5,"28913924":246.7,"29049022":775.1,"29058297":956.5,"29086343":229.2,"29086344":215.3,"29102460":969.6,"29102521":493.6,"29112843":459,"29118857":441,"29161730":436.8,"29162476":581.8,"29162477":499.9,"29162766":652.6,"29185934":221.7,"29185936":872.5,"29204406":404,"29234477":482.8,"29234478":698.7,"29234481":682.8,"29234582":681.5,"29234583":833.2,"29247852":368.2,"29260325":519,"29276153":442.6,"29280230":221.9,"29291810":497.7,"29291811":1057.8,"29305868":669,"29395274":637.1,"29395275":572.9,"29467554":384.7,"29717694":545.5,"29733447":405.9,"29763284":452.4,"29787147":393.9,"29787149":379.1,"29788689":480.9,"29805458":507.4,"29820548":702.1,"29820549":662.3,"29832954":1009.1,"29832955":632,"29847619":475.1,"29847701":524.1,"29949228":672.5,"29949591":505.4,"29963522":405,"29963533":207.3,"29991373":401.1,"29994196":228.7,"30007587":492.7,"30007593":688.6,"30063654":406.5,"30063656":377.9,"30063851":689.7,"30063852":475.6};
for(const [op,antes] of Object.entries(ANTES)){
 const li=await fetch(L+"?$top=500&$select=Quantidade_Inspe_x00e7__x00e3_o&$filter=OP_ID eq "+op,{headers:h}).then(r=>r.json());
 const novo=Math.round(li.value.reduce((s,x)=>s+(x.Quantidade_Inspe_x00e7__x00e3_o||0),0)*10)/10;
 const fi=await fetch(W+"'ficha_producao')/items?$select=ID,field_46&$filter=OP eq "+op,{headers:h}).then(r=>r.json());
 if(fi.value.length!==1){log.push(['ficha',op,'fichas:'+fi.value.length]);continue;}
 const f=fi.value[0];
 if(f.field_46==null||Math.abs(f.field_46-novo)<0.05){continue;}
 if(Math.abs(f.field_46-antes)>0.6){log.push(['ficha',f.ID,op,'quantidade '+f.field_46+' nao bate com a soma de antes '+antes+'; novo seria '+novo+' (decidir)']);continue;}
 const r=await fetch(W+"'ficha_producao')/items("+f.ID+")",{method:'POST',headers:hm,body:JSON.stringify({field_46:novo})});log.push(['ficha',f.ID,op,f.field_46+' -> '+novo,r.status]);
}
console.table(log);return log;
})();
