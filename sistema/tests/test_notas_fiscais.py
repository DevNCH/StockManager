from sistema.dao.nota_fiscal_dao import NotaFiscalDAO
from sistema.models.nota_fiscal import NotaFiscal
import datetime


def print_title(title):
    print("\n" + "="*60)
    print(title)
    print("="*60)


if __name__ == "__main__":
    print_title("LISTAR NOTAS FISCAIS")
    notas = NotaFiscalDAO.listar_todas()
    for n in notas:
        print(n)

    print_title("INSERIR NOVA NOTA")
    nova = NotaFiscal(
        nfce="123456789",
        serie="001",
        data_emissao=datetime.date.today(),
        cnpj_fornecedor="00.000.000/0000-00",
        nome_fornecedor="Fornecedor Teste",
        valor=199.90
    )
    nova = NotaFiscalDAO.inserir(nova)
    print("Inserida:", nova)

    print_title("BUSCAR POR ID")
    print(NotaFiscalDAO.buscar_por_id(nova.id))

    print_title("ATUALIZAR")
    nova.valor = 555.55
    NotaFiscalDAO.atualizar(nova)
    print("Atualizado:", NotaFiscalDAO.buscar_por_id(nova.id))

    print_title("DELETAR")
    NotaFiscalDAO.deletar(nova.id)
    print("Após deletar:", NotaFiscalDAO.buscar_por_id(nova.id))
