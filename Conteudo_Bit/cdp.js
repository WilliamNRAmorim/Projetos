const {spawn}=require('child_process');
const url=process.argv[2];
const e=spawn('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',['--headless=new','--disable-extensions','--user-data-dir=C:\Users\willi\Downloads\Projetos\Conteudo_Bit\Producao\serie\preview\edgeprof-ep04fix','--remote-debugging-port=9333','--window-size=1080,1920',url],{stdio:'ignore'});
(async()=>{
 await new Promise(r=>setTimeout(r,4000));
 const list=await (await fetch('http://127.0.0.1:9333/json')).json();
 const pg=list.find(x=>x.type==='page'); const ws=new WebSocket(pg.webSocketDebuggerUrl);
 await new Promise(r=>ws.onopen=r);
 let id=0; const call=(expr)=>new Promise(res=>{const i=++id; const h=m=>{const d=JSON.parse(m.data); if(d.id===i){ws.removeEventListener('message',h);res(d.result)}}; ws.addEventListener('message',h); ws.send(JSON.stringify({id:i,method:'Runtime.evaluate',params:{expression:expr,returnByValue:true}}))});
 for(let k=0;k<60;k++){ const r=await call('JSON.stringify(window.MIX_INFO||null)'); if(r.result.value&&r.result.value!=='null'){console.log(r.result.value);break;} await new Promise(r=>setTimeout(r,2000)); }
 ws.close(); e.kill();
})();
