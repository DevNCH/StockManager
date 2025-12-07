from sistema.dao.ficha_tecnica_dao import FichaTecnicaDAO
from sistema.dao.ficha_tecnica_insumo_dao import FichaTecnicaInsumoDAO
from sistema.models.ficha_tecnica import FichaTecnica
from sistema.models.ficha_tecnica_insumo import FichaTecnicaInsumo


def print_title(msg):
    print("\n" + "="*60)
    print(msg)
    print("="*60)


if __name__ == "__main__":
    print_title("CRIAR FICHA TECNICA")
    ft = FichaTecnica(nome="Produto Teste", valor=0)
    ft = FichaTecnicaDAO.inserir(ft)
    print("Criada:", ft)

    print_title("ADICIONAR INSUMO NA FICHA")
    fti = FichaTecnicaInsumo(
        id_ficha_tecnica=ft.id,
        id_insumo=15,
        quantidade=0.250
    )
    fti = FichaTecnicaInsumoDAO.inserir(fti)
    print("Adicionado:", fti)

    print_title("LISTAR ITENS DA FICHA")
    itens = FichaTecnicaInsumoDAO.listar_por_ficha(ft.id)
    for item in itens:
        print(item)

    print_title("ATUALIZAR ITEM")
    fti.quantidade = 0.500
    FichaTecnicaInsumoDAO.atualizar(fti)
    print("Atualizado:", FichaTecnicaInsumoDAO.listar_por_ficha(ft.id))

    print_title("DELETAR ITEM")
    FichaTecnicaInsumoDAO.deletar(fti.id)
    print("Após deletar:", FichaTecnicaInsumoDAO.listar_por_ficha(ft.id))

    print_title("DELETAR FICHA")
    FichaTecnicaDAO.deletar(ft.id)
