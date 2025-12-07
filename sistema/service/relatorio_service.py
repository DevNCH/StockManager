from sistema.dao.pedido_dao import PedidoDAO
from sistema.dao.ficha_tecnica_pedido_dao import FichaTecnicaPedidoDAO
from sistema.dao.ficha_tecnica_insumo_dao import FichaTecnicaInsumoDAO
from sistema.dao.nota_fiscal_dao import NotaFiscalDAO


class RelatorioService:

    # -----------------------------------
    # 1 — Faturamento no período
    # -----------------------------------
    @staticmethod
    def faturamento(data_inicio, data_fim):
        pedidos = PedidoDAO.buscar_por_periodo(data_inicio, data_fim)
        return sum(p.valor for p in pedidos)

    @staticmethod
    def produtos_vendidos(data_inicio, data_fim):
        pedidos = PedidoDAO.buscar_por_periodo(data_inicio, data_fim)
        ids = [p.id for p in pedidos]
        
        # Se não tiver pedidos, retorna vazio para não quebrar o SQL
        if not ids:
            return {}

        vinculos = FichaTecnicaPedidoDAO.listar_por_pedidos(ids)

        contagem = {}
        for v in vinculos:
            # ANTES: contagem[...] + 1
            # AGORA: Soma a quantidade que foi vendida (ex: 2 pastéis)
            qtd = float(v.quantidade) if v.quantidade else 1.0
            contagem[v.id_ficha_tecnica] = contagem.get(v.id_ficha_tecnica, 0) + qtd

        return contagem

    @staticmethod
    def consumo_insumos(data_inicio, data_fim):
        """
        Calcula o consumo teórico baseado nas vendas.
        Nota: Para ser 100% exato com as customizações (ingredientes retirados),
        seria necessário uma query SQL complexa. Para o prazo de 1 semana,
        usar o consumo padrão (baseado na ficha técnica) é aceitável.
        """
        pedidos = PedidoDAO.buscar_por_periodo(data_inicio, data_fim)
        ids_pedidos = [p.id for p in pedidos]
        
        if not ids_pedidos:
            return {}

        # Busca todos os itens vendidos nesses pedidos
        itens_vendidos = FichaTecnicaPedidoDAO.listar_por_pedidos(ids_pedidos)
        
        consumo_total = {}

        for item_venda in itens_vendidos:
            # Para cada pastel vendido, busca sua receita
            receita = FichaTecnicaInsumoDAO.listar_por_ficha(item_venda.id_ficha_tecnica)
            
            qtd_vendida = float(item_venda.quantidade)

            for ingrediente in receita:
                total_item = float(ingrediente.quantidade) * qtd_vendida
                consumo_total[ingrediente.id_insumo] = consumo_total.get(ingrediente.id_insumo, 0) + total_item

        return consumo_total


    # -----------------------------------
    # 4 — Gasto com insumos (via notas fiscais)
    # -----------------------------------
    @staticmethod
    def gastos_insumos(data_inicio, data_fim):
        notas = NotaFiscalDAO.buscar_por_periodo(data_inicio, data_fim)
        return sum(n.valor for n in notas)

    # -----------------------------------
    # 5 — Lucro total
    # -----------------------------------
    @staticmethod
    def lucro(data_inicio, data_fim):
        return RelatorioService.faturamento(data_inicio, data_fim) - \
               RelatorioService.gastos_insumos(data_inicio, data_fim)

    # -----------------------------------
    # 6 — Relatório consolidado
    # -----------------------------------
    @staticmethod
    def relatorio_completo(data_inicio, data_fim):
        return {
            "faturamento": RelatorioService.faturamento(data_inicio, data_fim),
            "gasto_insumos": RelatorioService.gastos_insumos(data_inicio, data_fim),
            "lucro": RelatorioService.lucro(data_inicio, data_fim),
            "produtos_vendidos": RelatorioService.produtos_vendidos(data_inicio, data_fim),
            "consumo_insumos": RelatorioService.consumo_insumos(data_inicio, data_fim)
        }
