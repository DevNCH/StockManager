from sistema.dao.pedido_dao import PedidoDAO
from sistema.dao.ficha_tecnica_pedido_dao import FichaTecnicaPedidoDAO
from sistema.models.pedido import Pedido
from sistema.models.ficha_tecnica_pedido import FichaTecnicaPedido
import datetime


def print_title(t):
    print("\n" + "="*60)
    print(t)
    print("="*60)


if __name__ == "__main__":
    print_title("CRIAR PEDIDO")
    p = Pedido(
        nome="Cliente Teste",
        data=datetime.date.today(),
        telefone="48999999999",
        valor=50.0,
        observacoes="Teste",
        cpf_cnpj=None,
        cep=None,
        unidade_federal=None,
        cidade=None,
        bairro=None,
        rua=None,
        numero=None,
        complemento=None
    )
    p = PedidoDAO.inserir(p)
    print("Criado:", p)

    print_title("VINCULAR FICHA TÉCNICA")
    ftp = FichaTecnicaPedido(
        id_ficha_tecnica=1,  # ajustar conforme seu banco
        id_pedido=p.id
    )
    ftp = FichaTecnicaPedidoDAO.inserir(ftp)
    print("Vinculado:", ftp)

    print_title("LISTAR FICHAS DO PEDIDO")
    lista = FichaTecnicaPedidoDAO.listar_por_pedido(p.id)
    for item in lista:
        print(item)

    print_title("DELETAR VÍNCULO")
    FichaTecnicaPedidoDAO.deletar(ftp.id)
    print(FichaTecnicaPedidoDAO.listar_por_pedido(p.id))

    print_title("DELETAR PEDIDO")
    PedidoDAO.deletar(p.id)
    print(PedidoDAO.buscar_por_id(p.id))
