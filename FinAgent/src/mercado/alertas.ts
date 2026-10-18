export type Alerta = { id: string; ativoId: string; direcao: 'acima' | 'abaixo'; nivel: number };

export function alertaDisparado(a: Alerta, preco: number): boolean {
  return a.direcao === 'acima' ? preco >= a.nivel : preco <= a.nivel;
}

export function alertasDisparados(alertas: Alerta[], precos: Record<string, number | undefined>): Alerta[] {
  return alertas.filter((a) => {
    const p = precos[a.ativoId];
    return p != null && alertaDisparado(a, p);
  });
}
