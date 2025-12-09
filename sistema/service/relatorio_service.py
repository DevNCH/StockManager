from sistema.dao.pedido_dao import PedidoDAO
from sistema.dao.nota_fiscal_dao import NotaFiscalDAO
from sistema.dao.ficha_tecnica_pedido_dao import FichaTecnicaPedidoDAO
from sistema.dao.ficha_tecnica_insumo_dao import FichaTecnicaInsumoDAO
from sistema.dao.ficha_tecnica_dao import FichaTecnicaDAO
from sistema.dao.insumo_dao import InsumoDAO
from sistema.utils.helpers import Helpers

class RelatorioService:

    @staticmethod
    def gerar_dados_dashboard(data_inicio_br, data_fim_br):
        # Converte datas para MySQL (YYYY-MM-DD)
        dt_ini = Helpers.data_para_mysql(data_inicio_br)
        dt_fim = Helpers.data_para_mysql(data_fim_br)

        # 1. Financeiro Geral
        pedidos = PedidoDAO.buscar_por_periodo(dt_ini, dt_fim)
        notas = NotaFiscalDAO.buscar_por_periodo(dt_ini, dt_fim)

        faturamento = sum([p.valor for p in pedidos])
        custos = sum([n.valor for n in notas])
        lucro = faturamento - custos

        # 2. Ranking de Produtos Vendidos
        ids_pedidos = [p.id for p in pedidos]
        ranking_produtos = {} # {id_ficha: {'nome': str, 'qtd': float, 'total': float}}

        if ids_pedidos:
            # Busca todos os itens vendidos nesses pedidos
            # Nota: O DAO precisa de um método 'listar_por_pedidos' (plural) ou fazemos loop.
            # Vamos fazer loop para ser seguro com o DAO atual, embora menos performático.
            # Se tiver muitos pedidos, o ideal é criar um método SQL 'WHERE id_pedido IN (...)' no DAO.
            
            # Otimização: Vamos usar o método que busca por ID do pedido
            todos_itens = []
            for id_ped in ids_pedidos:
                itens = FichaTecnicaPedidoDAO.listar_por_pedido(id_ped)
                todos_itens.extend(itens)

            for item in todos_itens:
                idf = item.id_ficha_tecnica
                qtd = float(item.quantidade)
                val = float(item.valor_unitario)
                
                if idf not in ranking_produtos:
                    ficha = FichaTecnicaDAO.buscar_por_id(idf)
                    nome_prod = ficha.nome if ficha else "Desconhecido"
                    ranking_produtos[idf] = {'nome': nome_prod, 'qtd': 0.0, 'total': 0.0}
                
                ranking_produtos[idf]['qtd'] += qtd
                ranking_produtos[idf]['total'] += (qtd * val)

        # Transforma dicionário em lista ordenada (Mais vendidos primeiro)
        lista_produtos = sorted(ranking_produtos.values(), key=lambda x: x['qtd'], reverse=True)

        # 3. Consumo de Insumos (Teórico)
        consumo_insumos = {} # {id_insumo: {'nome': str, 'qtd': float}}
        
        # Para cada produto vendido, soma sua receita
        for item_venda in todos_itens if ids_pedidos else []:
            idf = item_venda.id_ficha_tecnica
            qtd_venda = float(item_venda.quantidade)
            
            # Pega a receita
            receita = FichaTecnicaInsumoDAO.listar_por_ficha(idf)
            
            for ing in receita:
                idi = ing.id_insumo
                qtd_receita = float(ing.quantidade)
                total_consumido = qtd_receita * qtd_venda
                
                if idi not in consumo_insumos:
                    obj_insumo = InsumoDAO.buscar_por_id(idi)
                    nome_ins = obj_insumo.nome if obj_insumo else "Desconhecido"
                    unidade = obj_insumo.unidade_medida if obj_insumo else ""
                    consumo_insumos[idi] = {'nome': nome_ins, 'qtd': 0.0, 'unidade': unidade}
                
                consumo_insumos[idi]['qtd'] += total_consumido

        lista_consumo = sorted(consumo_insumos.values(), key=lambda x: x['qtd'], reverse=True)

        return {
            "financeiro": {"faturamento": faturamento, "custos": custos, "lucro": lucro},
            "produtos": lista_produtos,
            "insumos": lista_consumo
        }