from sistema.dao.insumo_dao import InsumoDAO
from sistema.models.insumo import Insumo


def print_title(title):
    print("\n" + "="*50)
    print(title)
    print("="*50)


if __name__ == "__main__":
    print_title("TESTE INSUMOS — LISTAR TODOS")
    insumos = InsumoDAO.listar_todos()
    for i in insumos:
        print(i)

    print_title("INSERIR NOVO INSUMO")
    novo = Insumo(nome="Teste_Insumo", quantidade=10.5, unidade_medida="kg")
    novo = InsumoDAO.inserir(novo)
    print("Inserido:", novo)

    print_title("BUSCAR POR ID")
    buscado = InsumoDAO.buscar_por_id(novo.id)
    print("Buscado:", buscado)

    print_title("ATUALIZAR")
    buscado.nome = "Teste_Modificado"
    InsumoDAO.atualizar(buscado)
    print("Atualizado:", InsumoDAO.buscar_por_id(buscado.id))

    print_title("DELETAR")
    InsumoDAO.deletar(buscado.id)
    print("Depois de deletar:", InsumoDAO.buscar_por_id(buscado.id))
