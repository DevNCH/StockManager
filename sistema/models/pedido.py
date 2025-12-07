class Pedido:
    def __init__(self, id=None, nome=None, data=None, telefone=None, valor=0.0, observacoes=None,
                 cpf_cnpj=None, cep=None, unidade_federal=None, cidade=None, bairro=None, rua=None, numero=None, complemento=None):
        self.id = id
        self.nome = nome
        self.data = data
        self.telefone = telefone
        self.valor = float(valor)
        self.observacoes = observacoes
        self.cpf_cnpj = cpf_cnpj
        self.cep = cep
        self.unidade_federal = unidade_federal
        self.cidade = cidade
        self.bairro = bairro
        self.rua = rua
        self.numero = numero
        self.complemento = complemento

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "data": self.data,
            "telefone": self.telefone,
            "valor": self.valor,
            "observacoes": self.observacoes,
            "cpf_cnpj": self.cpf_cnpj,
            "cep": self.cep,
            "unidade_federal": self.unidade_federal,
            "cidade": self.cidade,
            "bairro": self.bairro,
            "rua": self.rua,
            "numero": self.numero,
            "complemento": self.complemento
        }