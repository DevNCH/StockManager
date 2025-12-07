from sistema.service.relatorio_service import RelatorioService

print("=== TESTE RELATORIOS ===")

inicio = "2025-01-01"
fim = "2025-12-31"

print("\nFaturamento:")
print(RelatorioService.faturamento(inicio, fim))

print("\nProdutos vendidos:")
print(RelatorioService.produtos_vendidos(inicio, fim))

print("\nConsumo de insumos:")
print(RelatorioService.consumo_insumos(inicio, fim))

print("\nGastos com insumos:")
print(RelatorioService.gastos_insumos(inicio, fim))

print("\nLucro:")
print(RelatorioService.lucro(inicio, fim))

print("\nRelatório completo:")
print(RelatorioService.relatorio_completo(inicio, fim))
