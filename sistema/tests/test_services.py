from sistema.service.insumo_service import InsumoService
from sistema.service.ficha_tecnica_service import FichaTecnicaService
from sistema.service.pedido_service import PedidoService
from sistema.service.relatorio_service import RelatorioService
from sistema.models.pedido import Pedido

print("="*80)
print("TESTE 1 — Registrar compra")
registro = InsumoService.registrar_compra(15, 1.5, 10.00, 2)
print(registro)

print("="*80)
print("TESTE 2 — Ajuste manual de estoque")
InsumoService.ajuste_manual(15, quantidade=555)
print(InsumoService.listar_estoque())

print("="*80)
print("TESTE 3 — Editar ficha técnica completa")
FichaTecnicaService.atualizar_ficha_completa(
    1,
    "Produto Teste Alterado",
    [
        {"id_insumo": 15, "quantidade": 0.5},
    ]
)
print("OK")

print("="*80)
print("TESTE 4 — Criar pedido com baixa automática")
pedido = Pedido(nome="Cliente Teste", data="2025-12-31", telefone="48999999999", valor=50)
novo_pedido = PedidoService.criar_pedido(pedido, [1], insumos_removidos=None)
print(novo_pedido)

print("="*80)
print("TESTE 5 — Relatórios")
print("Faturamento:", RelatorioService.faturamento("2025-01-01", "2025-12-31"))
