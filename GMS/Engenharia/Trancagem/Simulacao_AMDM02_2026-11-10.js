// Simulação do dia produtivo 10/11/2026 (05:20 a 05:20) na tela AM-DM-02: TH02, GH781-8 DD240801, 1ª trança.
// Rodar no console (F12) numa aba logada em https://danfoss.sharepoint.com/sites/OperationsGuaratingueta/
// Grava 1 AMDM02_Folha + 13 AMDM02_Janela + 1 AMDM02_Registro. Não grava se a folha já existir.
// Para desfazer: mandar à lixeira os IDs devolvidos no log (folha, janelas, registro).
(async()=>{
const site="https://danfoss.sharepoint.com/sites/OperationsGuaratingueta/_api/web/";
const h={Accept:'application/json;odata=nometadata'};
const dg=(await fetch(site.replace('web/','')+"contextinfo",{method:'POST',headers:h}).then(r=>r.json())).FormDigestValue;
const hp={...h,'Content-Type':'application/json;odata=nometadata','X-RequestDigest':dg};
const add=(l,b)=>fetch(site+`lists/getbytitle('${l}')/items`,{method:'POST',headers:hp,body:JSON.stringify(b)}).then(async r=>{const j=await r.json();if(!r.ok)throw new Error(l+': '+JSON.stringify(j));return j;});
const CH="2026-11-10|TH02|1", RESP="WILLIAM NATHAN RIBEIRO DE AMORIM";
const ex=await fetch(site+`lists/getbytitle('AMDM02_Folha')/items?$filter=Title eq '${CH}'`,{headers:h}).then(r=>r.json());
if(ex.value.length) return {pulado:"folha já existe",ID:ex.value[0].ID};
// Hora local (Brasília, UTC-3) -> ISO UTC
const utc=(d,hm)=>{const[H,M]=hm.split(':').map(Number);return new Date(Date.UTC(2026,10,d,H+3,M,0)).toISOString();};
const turno=hm=>{const[H,M]=hm.split(':').map(Number),m=H*60+M;return m>=320&&m<837?1:m>=837&&m<1340?2:3;};
const r3=v=>Math.round(v*1000)/1000, r4=v=>Math.round(v*10000)/10000;
const col=[
 [10,"05:42",[.663,.665,.664,.666,.664]],[10,"07:38",[.665,.666,.664,.667,.665]],
 [10,"09:35",[.666,.668,.667,.665,.667]],[10,"11:31",[.668,.669,.667,.670,.668]],
 [10,"13:25",[.667,.666,.668,.667,.666]],[10,"15:20",[.669,.671,.670,.672,.670]],
 [10,"17:14",[.672,.674,.671,.675,.673]],[10,"19:10",[.676,.678,.677,.681,.676]],
 [10,"21:05",[.666,.665,.667,.664,.666]],[10,"22:58",[.664,.663,.665,.664,.662]],
 [11,"00:52",[.663,.665,.664,.663,.664]],[11,"02:47",[.665,.664,.666,.665,.663]],
 [11,"04:40",[.664,.666,.665,.664,.665]]];
const log={};
const f=await add('AMDM02_Folha',{Title:CH,Data:"2026-11-10T03:00:00Z",Maquina:"TH02",Tranca:1,PN:"GH781-8",BRDCode:"DD240801",
 Caracteristica:"Diâmetro",Responsavel:RESP,ODLie:.65,ODNom:.665,ODLse:.68,PickLie:39,PickLse:41,
 Tensao1:2.5,Tensao2:2.45,Tensao3:2.55,Tensao4:2.5,Tensao5:2.5,Fios1:8,Fios2:8,Fios3:8,Fios4:8,Fios5:8,
 ODTubo1:.562,ODTubo2:.563,ODTubo3:.561,ODTubo4:.562,ODTubo5:.563,FiosSobrepostos:0,
 Observacoes:"SIMULAÇÃO DE TESTE (Claude, 11/11) — não é dado real. X̄ subiu ao longo do 2º turno; coleta das 19:10 com amostra 4 em 0,681 (acima do LSE). Ajuste de tensão às 19:30; voltou ao nominal na coleta das 21:05."});
log.folha=f.ID; log.janelas=[];
for(let i=0;i<col.length;i++){const[d,hm,a]=col[i],s=a.reduce((x,y)=>x+y,0);
 const j=await add('AMDM02_Janela',{Title:f.ID+"|"+i,IdFolha:f.ID,Janela:i,HoraColeta:utc(d,hm),Turno:turno(hm),
  Amostra1:a[0],Amostra2:a[1],Amostra3:a[2],Amostra4:a[3],Amostra5:a[4],Soma:r3(s),Media:r4(s/a.length),
  Amplitude:r3(Math.max(...a)-Math.min(...a)),LancadoPor:RESP,LancadoEm:utc(d,hm)});
 log.janelas.push(j.ID);}
const g=await add('AMDM02_Registro',{Title:f.ID+"|1",IdFolha:f.ID,Tranca:1,NPicks:40,
 ODTranca1:.664,ODTranca2:.666,ODTranca3:.665,ODTranca4:.665,ODTranca5:.664,Operador:RESP,LancadoEm:utc(11,"04:45")});
log.registro=g.ID;
return log;
})();
