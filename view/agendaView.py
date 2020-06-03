from infrastructure.contatoRepository import ContatoRepository
from service.agendaService import AgendaService
from domain.contato import Contato
from domain.helper import validateInput


class AgendaView():
    def __init__(self, contatoRepository):
        self.pagina = 0
        self.tamanho = 10
        self.contatoRepository = contatoRepository
        self.service = AgendaService(contatoRepository, self)
        pass

    def inputContato(self):
        nome = input('Digite o nome do contato a ser adicionado: ')
        email = input('Digite o email do contato: ')
        ddd_celular = None
        while not ddd_celular != None:
            try:
                ddd_celular = int(input('Digite o DDD do celular: '))
            except ValueError:
                ddd_celular = None
                print(
                    'ERRO: O valor inserido não contém apenas números, favor informar novamente o DDD.')
                continue
        numero_celular = input('Digite o número do celular, sem o DDD: ')
        return Contato(None, nome, email, ddd_celular, numero_celular)

    def pause(self):

        input('\nTecle ENTER para continuar...')
        self.opcoes()

    def view(self):
        queryContatos = self.contatoRepository.query()
        if len(queryContatos) < 0:
            print('\nA Agenda ainda não possui nenhum contato')
            self.pause()
            self.opcoes()

        print('''
+-----------------------+
|  Contatos existentes  |
+-----------------------+ ''')

        contatos = [Contato(*prop) for prop in queryContatos]
        for contato in contatos:
            print(f'\nContato ID: {contato.id}\nNome: {contato.nome}\nCelular: {contato.celular}\nEmail: {contato.email}\n')

    def opcoes(self):
        op = input(f'''Menu de ações da agenda
Escolha sua ação dentre as opções abaixo:

1 - Exibir contatos
2 - Adicionar novo contato
3 - Deletar contatos
4 - Restaurar contato deletado
5 - Sair
Insira o número referente à ação para continuar: ''').lower()

        if op == '1':
            self.view()
            self.pause()

        elif op == '2':
            contato = self.inputContato()

            self.service.criar(contato)

        elif op == '3':
            self.service.remover()

        elif op == '4':
            self.service.restaurar()
        elif op == '5':
            self.sair()

        opcaoEscolhida = input(
            '\nVocê deseja realizar alguma outra ação?\nResponda com "Sim" para continuar a utilizar a agenda: ')

        if validateInput(opcaoEscolhida):
            self.opcoes()

        self.sair()

    def sair(self):
        print('Obrigado por utilizar a agenda Pythônica.\nTchaaaau')
        exit(0)
