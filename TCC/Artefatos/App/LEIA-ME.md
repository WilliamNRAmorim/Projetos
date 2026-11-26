# GMS_App_TCC.msapp

Versão do app GMS (Power Apps Canvas) preparada para o TCC.

- Sem kill switch (MEL-274): sem `Flow_Composto`, sem `varCompostoPermitida`, `App.OnError` removido.
- Sem a marca Danfoss: logo da Splash e das telas Hora-Hora trocados pelo logo GMS; "DANFOSS DRT" virou "GMS"; e-mails de gestão fictícios (`supervisor@gms.exemplo`, `gestor@gms.exemplo`).
- Resto igual ao app original (telas, fórmulas, regras de negócio).
- As fontes de dados continuam apontando para as listas SharePoint originais; sem login com acesso a elas, o app abre vazio (nenhum dado é exibido).

## Importar no Power Apps Studio
1. make.powerapps.com > Apps > Import canvas app (ou Studio > Abrir > Procurar) e escolher `GMS_App_TCC.msapp`.
2. As conexões (SharePoint, Excel, fluxo GMS_PackListParaFicha) ficarão pendentes; autorize ou remova as que não precisar.
3. `src/` traz os fontes desempacotados (`pac canvas pack --msapp GMS_App_TCC.msapp --sources src`).
