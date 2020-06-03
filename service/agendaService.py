from infrastructure.contatoRepository import ContatoRepository
from domain.contato import Contato
from domain.helper import *

class AgendaService:
    def __init__(self, contatoRepository, view):
        self.contatoRepository = contatoRepository
        self.view = view
        self.paginaExcluidos = 0
        pass

    def criar(self, contato):
        if(contato == None):
            print(
                'O contato não pode ser salvo. Algum problema ocorreu durante o cadastro')

        if not contato.isValid():
            self.view.opcoes()

        self.contatoRepository.create(contato)
        print(f'Contato {contato.nome} armazenado com sucesso')

        return

    def restaurar(self):
        print('''
+-------------------------+
|   Contatos excluidos    |
+-------------------------+
''')
        self.visualizarContatosExcluidos(0)

    def visualizarContatosExcluidos(self, pagina=1):
        if(self.paginaExcluidos + pagina >= 0):
            self.paginaExcluidos += pagina
        contatosExcluidosQuery = self.contatoRepository.findContatosExcluidos(
            self.paginaExcluidos)
        contatosExcluidos = toContatoList(contatosExcluidosQuery)

        for contato in contatosExcluidos:
            print(f'Id: {contato.id} - Nome: {contato.nome}')

        self.opcoesRestauracao()

    def restaurarContato(self):
        contatoId = 0

        try:
            contatoId = int(
                input('Digite o Id do contato que deseja restaurar: '))

            if not self.contatoRepository.exists(contatoId):
                raise Exception('Contato não existe')

        except ValueError:
            print("ERRO: Id inválido")
            self.view.pause()
        except Exception as e:
            print(f'\n\n{e}\n')
            self.view.pause()

        if(contatoId == 0):
            self.view.pause()

        self.contatoRepository.restaurar(contatoId)
        print('Contato restaurado com sucesso')

    def opcoesRestauracao(self):
        opcaoEscolhida = input('''
1 - Visualizar proximos
2 - Visualizar anteriores
3 - Restaurar contato
Insira o número referente à ação para continuar: ''')
        if not validateEmpty(opcaoEscolhida):
            return
        elif opcaoEscolhida == '1':
            self.visualizarContatosExcluidos()
        elif opcaoEscolhida == '2':
            self.visualizarContatosExcluidos(-1)
        elif opcaoEscolhida == '3':
            self.paginaExcluidos = 0
            self.restaurarContato()

    def remover(self):
        print('''
+-------------------------+
|   Remoção de contatos   |
+-------------------------+

Contatos existentes
''')
        contatosQuery = self.contatoRepository.query()

        contatos = toContatoList(contatosQuery)
        for contato in contatos:
            print(f'Id: {contato.id} - Nome: {contato.nome}')

        try:
            contatoId = int(
                input('Digite o ID do contato que deseja remover: '))

            if not self.contatoRepository.exists(contatoId):
                raise ValueError

        except ValueError:

            opcaoEscolhida = input(
                "ERRO: O contato não existe. Digite 'Sim' para tentar novamente: ")

            if validateInput(opcaoEscolhida):
                self.remover()
            else:
                return

        queryContato = self.contatoRepository.findById(contatoId)

        try:
            contato = toContatoList(queryContato)[0]

        except IndexError:
            print("\n\nUsuário não encontrado, tente novamente :c\n\n")
            self.remover()

        self.contatoRepository.deleteById(contato.id)

        print(f'\nContato {contato.nome} removido com sucesso!')

        return
