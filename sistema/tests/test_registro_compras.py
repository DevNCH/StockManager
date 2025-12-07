from sistema.dao.registro_compra_dao import RegistroCompraDAO
from sistema.models.registro_compra import RegistroCompra


def print_title(title):
    print("\n" + "="*60)
    print(title)
    print("="*60)


if __name__ == "__main__":
    print_title("LISTAR REGISTROS")
    registros = RegistroCompraDAO.listar_todos()
    for r in registros:
        print(r)

    print_title("INSERIR REGISTRO")
    
    registro = RegistroCompra(
        id_insumo=15,
        id_nota_fiscal=2,
        quantidade=3.5,
        valor=15.99
    )
    registro = RegistroCompraDAO.inserir(registro)
    print("Inserido:", registro)

    print_title("BUSCAR POR ID")
    print(RegistroCompraDAO.buscar_por_id(registro.id))

    print_title("ATUALIZAR")
    registro.quantidade = 10
    RegistroCompraDAO.atualizar(registro)
    print("Atualizado:", RegistroCompraDAO.buscar_por_id(registro.id))

    print_title("DELETAR")
    RegistroCompraDAO.deletar(registro.id)
    print("Após deletar:", RegistroCompraDAO.buscar_por_id(registro.id))
