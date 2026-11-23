// Gabarito do Uiu v4. Rodar em uma aba do site OperationsGuaratingueta (console ou javascript_tool). Só leitura.
const B='https://danfoss.sharepoint.com/sites/OperationsGuaratingueta/_api/web/';
const L=async(l,sel,f)=>{let o=[],n=B+"lists/getbytitle('"+encodeURIComponent(l)+"')/items?$select=ID,"+sel+"&$filter="+encodeURIComponent(f)+"&$orderby=ID&$top=5000";
 while(n){const r=await fetch(n,{headers:{Accept:'application/json;odata=nometadata'}});if(!r.ok)throw new Error(l+' '+r.status);const j=await r.json();o=o.concat(j.value);n=j['odata.nextLink']}return o};
const by=(v,k,s)=>{const o={};let t=0;v.forEach(r=>{const a=k.map(c=>r[c]??'(vazio)').join(' | '),x=s?(+r[s]||0):1;o[a]=+((o[a]||0)+x).toFixed(2);t+=x});
 return{n:v.length,total:+t.toFixed(2),g:Object.entries(o).sort((x,y)=>y[1]-x[1]).slice(0,20)}};
const faixa=(c,a,b,h)=>`${c} ge datetime'${a}T${h}:00Z' and ${c} lt datetime'${b}T${h}:00Z'`;
const soData=(c,a,b)=>faixa(c,a,b,'00:00'),civil=(c,a,b)=>faixa(c,a,b,'03:00'),prod=(c,a,b)=>faixa(c,a,b,'08:20');
const Q='Quantidade_Inspe_x00e7__x00e3_o',X='OData__x0043_',a='2026-11-13',b='2026-11-14';
// Refugo com dia e mês trocados: data muito longe da criação do item.
const trocada=r=>Math.abs(new Date(r.DataHoraRefugo)-new Date(r.Created))>60*864e5;
// Turno pela hora da inspeção (05:20 Brasília = 08:20Z = 500 min).
const turno=r=>{const d=new Date(r.DataHoraInspecao),m=(d.getUTCHours()*60+d.getUTCMinutes()+1440-500)%1440;return m<517?'1':m<1020?'2':'3'};
const I=await L('RegistrosInspeção',Q+',Mangueira,cabine_teste',civil('DataHoraInspecao',a,b));
const P=await L('RegistrosInspeção',Q+',DataHoraInspecao',prod('DataHoraInspecao',a,b));P.forEach(r=>r.t=turno(r));
const S=await L('RegistrosInspeção',Q,prod('DataHoraInspecao','2026-11-09',b));
const O=await L('RegistrosInspeção',Q+',Mangueira',civil('DataHoraInspecao','2026-10-01','2026-11-01'));
const D=await L('RegistrosInspeção',Q,prod('DataHoraInspecao','2026-11-15','2026-11-16'));
const R=await L('TiposErros','A,'+X,soData('DataHoraRefugo',a,b));
const RO=await L('TiposErros','A,OP_ID,Tran_x00e7_adeira,DataHoraRefugo,Created,'+X,soData('DataHoraRefugo','2026-10-01','2026-11-01'));
const RK=RO.filter(r=>!trocada(r));
const E=await L('Eventos_Producao','etapa,tipo,turno,metros,origem_ID,origem',soData('data_ref',a,b)+" and origem eq 'ficha_producao'");
// Cancelada: desconta só a mesma ficha e etapa, com ID menor que o do evento Cancelado (busca sem limite de período).
const C=(await L('Eventos_Producao','origem_ID,etapa,origem',"tipo eq 'Cancelado'")).filter(c=>c.origem=='ficha_producao');
const cancelada=r=>r.tipo!='Cancelado'&&C.some(c=>c.origem_ID==r.origem_ID&&c.etapa==r.etapa&&r.ID<c.ID);
const ok=E.filter(r=>!cancelada(r)),fp=ok.filter(r=>r.tipo=='Fim'||r.tipo=='Parcial');
// Hora-Hora: só trançadeiras e a última linha (maior ID) de cada janela.
const CEL=['TH01','TH02','TH03','TH04','TH05','TH06','TH07','TO04','TM01','TM04','Spiral'];
const ultima=v=>{const m={};v.filter(r=>CEL.includes(r.field_2)).forEach(r=>{const k=[r.field_0,r.field_2,r.TurnoH,r.field_3].join('|');if(!m[k]||m[k].ID<r.ID)m[k]=r});return Object.values(m)};
const HC='field_0,field_2,field_3,field_7,field_11,field_12,TurnoH';
const H=ultima(await L('Hora-Hora',HC,soData('field_0',a,b))),HS=ultima(await L('Hora-Hora',HC,soData('field_0','2026-11-09',b)));
// Motivo normalizado e em três blocos (nunca somados). Programada = Tipo do dMotivoParada.
const PROG=['Almoço','Manutenção Preventiva','Manutenção Preventiva (Fora do Prazo)','Manut. Prod. Total (MPT)','Reunião','Reunião/Treinamento','Amostra','TESTE ENGENHARIA','Execução Check List Lean','Set-up','Inventário'];
const norm=m=>{const t=(m||'').replace(/^\d+\s*-\s*/,'').trim();return t=='Refeição'?'Almoço':t=='Problema no tubo'?'Análise/Problema no tubo':t};
H.forEach(r=>{r.mot=norm(r.field_12)||'(vazio)';r.bloco=r.mot=='(vazio)'?'sem motivo':PROG.includes(r.mot)?'programada':r.mot=='Divergência do Tempo Padrão'?'divergência':'demais'});
const M=await L('Producao_Montagem','field_3,field_9',soData('field_1',a,b));
const MP=await L('Paradas_Montagem','field_5,field_6',soData('field_1',a,b));
MP.forEach(r=>r.bloco=r.field_5=='TE - Tempo Excedido'?'TE':r.field_5=='RF - Refeição'?'RF':'parada real');
const OI=await L('RegistrosInspeção',Q+',Mangueira','OP_ID eq 30803591'),OR=await L('TiposErros','A,'+X,'OP_ID eq 30803591');
({q1:by(I,['Mangueira'],Q),q4:by(I,['cabine_teste'],Q),q3:by(P,['t'],Q),q6:by(S,[],Q),q7:by(O,['Mangueira'],Q),q8:D.length,q10:by(R,['A'],X),
 q12:by(RK,['A'],X),q12fora:by(RO.filter(trocada),['A'],X),q14:by(RK,['Tran_x00e7_adeira'],X),q15:by(RK,['OP_ID'],X).g.slice(0,5),
 q16:by(fp,['etapa'],'metros').g,q16desc:E.filter(cancelada).map(r=>[r.origem_ID,r.etapa,r.tipo,r.metros]),
 q16v:by(ok.filter(r=>r.etapa=='Vulcanização'&&r.tipo=='Início'),['etapa'],'metros'),
 q17:by(fp.filter(r=>r.etapa=='Cobertura'),['turno'],'metros'),q18:E.filter(r=>r.tipo=='Cancelado').map(r=>[r.origem_ID,r.etapa]),
 q19:by(H,['field_2'],'field_7'),q20:by(H,['TurnoH'],'field_7'),q21:H.filter(r=>r.field_2=='TH05').length,q22:by(HS,['field_2'],'field_7'),
 q23:by(H,['bloco','mot'],'field_11').g,q24:by(M,['field_3'],'field_9'),q25:by(MP,['bloco'],'field_6').g,q26:[by(OI,['Mangueira'],Q),by(OR,['A'],X)]})
