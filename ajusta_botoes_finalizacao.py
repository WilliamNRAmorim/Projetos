"""Reestiliza btn_PackingManualExt e btn_DividirPalletExt em Telas/scr_Finalização_1.txt (mesmo padrão dos botões
Editar Plano / Imprimir Ficha / Finalizar Ordem) e cria os ícones. Preserva OnSelect e DisplayMode de cada botão."""
import re, os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Telas', 'scr_Finalização_1.txt')
raw = open(P, 'rb').read()
crlf = b'\r\n' in raw
s = raw.decode('utf-8').replace('\r\n', '\n')
FILL = '\u3164\u3164'          # mesmo "espaço invisível" que Editar Plano / Imprimir Ficha usam para abrir espaço pro ícone


def bloco(nome, proximo):
    i = s.index('      - %s:\n' % nome)
    j = s.index('      - %s:\n' % proximo, i)
    return i, j


def pega(blk, prop):
    """texto completo (1+ linhas) de uma propriedade no bloco"""
    m = re.search(r'^            %s: (.*?)(?=^            [A-Za-z.]+: |\Z)' % re.escape(prop), blk, re.S | re.M)
    return m.group(0).rstrip('\n')


# --- Pack manual -----------------------------------------------------------------------------
i, j = bloco('btn_PackingManualExt', 'btn_DividirPalletExt')
old = s[i:j]
onselect = pega(old, 'OnSelect')
disp = pega(old, 'DisplayMode')
novo_pack = f"""      - btn_PackingManualExt:
          Control: Classic/Button@2.2.0
          Properties:
            BorderColor: =fx_CorBorda
            BorderThickness: =1
            Color: =fx_CorTexto
{disp}
            Fill: =fx_CorSuperficie
            Font: =fx_FonteFamilia
            Height: =44
            HoverFill: =fx_CorInfoSuave
{onselect}
            PressedFill: =fx_CorInfoSuave
            RadiusBottomLeft: =fx_Raio
            RadiusBottomRight: =fx_Raio
            RadiusTopLeft: =fx_Raio
            RadiusTopRight: =fx_Raio
            Size: =fx_FonteCorpo
            Text: ="{FILL}Packing manual"
            Width: =183
            X: =1168
            Y: =690
      - ico_PackingManualExt:
          Control: ModernIcon@1.1.1
          Properties:
            DisplayMode: =btn_PackingManualExt.DisplayMode
            Height: =24
            Icon: ="Add"
            IconColor: =fx_CorInfo
            OnSelect: =Select(btn_PackingManualExt)
            Width: =24
            X: =1186
            Y: =700
"""
s = s[:i] + novo_pack + s[j:]

# --- Dividir pallet ----------------------------------------------------------------------------
i, j = bloco('btn_DividirPalletExt', 'cntr_PalletExt')
old = s[i:j]
onselect = pega(old, 'OnSelect')
disp = pega(old, 'DisplayMode')
novo_div = f"""      - btn_DividirPalletExt:
          Control: Classic/Button@2.2.0
          Properties:
            BorderColor: =If(Self.DisplayMode = DisplayMode.Edit, fx_CorInfo, fx_CorBorda)
            BorderThickness: =1
            Color: =If(Self.DisplayMode = DisplayMode.Edit, fx_CorInfo, fx_CorRotulo)
{disp}
            Fill: =fx_CorSuperficie
            Font: =fx_FonteFamilia
            FontWeight: =FontWeight.Semibold
            Height: =fx_AlturaAcao
            HoverFill: =fx_CorInfoSuave
{onselect}
            PressedFill: =fx_CorInfoSuave
            RadiusBottomLeft: =fx_RaioS
            RadiusBottomRight: =fx_RaioS
            RadiusTopLeft: =fx_RaioS
            RadiusTopRight: =fx_RaioS
            Size: =fx_FonteCorpo
            Text: ="{FILL}Dividir pallet"
            Width: =165
            X: =961
            Y: =700
      - ico_DividirPalletExt:
          Control: ModernIcon@1.1.1
          Properties:
            DisplayMode: =btn_DividirPalletExt.DisplayMode
            Height: =24
            Icon: ="Cut"
            IconColor: =If(btn_DividirPalletExt.DisplayMode = DisplayMode.Edit, fx_CorInfo, fx_CorRotulo)
            OnSelect: =Select(btn_DividirPalletExt)
            Width: =24
            X: =977
            Y: =716
"""
s = s[:i] + novo_div + s[j:]
s = s.replace('Text: ="Versão 0.4.2"', 'Text: ="Versão 0.4.3"')
open(P, 'wb').write((s.replace('\n', '\r\n') if crlf else s).encode('utf-8'))
print('ok')
