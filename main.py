from infrastructure.contatoRepository import ContatoRepository


class Agenda(object):
    def __init__(self, contatoRepository):
        self.contatoRepository = contatoRepository
        pass

    def view(self):
        view = self.contatoRepository.query()
        if len(view) > 0:
            print('''
+---------------------------------+
|  Contatos existentes na tabela  |
+---------------------------------+ ''')
        else:
            print('\nA Agenda não possui nenhum contato')
            Agenda.pause(agenda)
            Agenda.main(agenda)

        view = self.contatoRepository.query()
        for i in view:
            for j in i:
                if j == i[0]:
                    print(f'\nContato ID: {j}\nNome: {i[1]}\nCelular: {i[2]}\nEmail: {i[3]}\n')

    def gera_contato(self):

        nome = input('Digite o nome do contato a ser adicionado: ')
        email = input('Digite o email do contato: ')
        # Flag que será validada para 'True' caso o valor informado para o DDD se mostre válido
        ddd_celular_aceito = 0

        while not ddd_celular_aceito:
            try:
                celular_ddd = int(input('Digite o DDD do celular: '))

            except ValueError:  # Evitando o erro de inserção de caracteres não numéricos
                print(
                    'ERRO: O valor inserido não contém apenas números, favor informar novamente o DDD.')
                continue

            celular_ddd = str(celular_ddd)

            if len(celular_ddd) > 3:
                teste = input(
                    ('ERRO: O valor inserido possui mais de 3 caracteres. Deseja salvar mesmo assim? (S/N): ')).lower()
                if teste == 's':
                    print('Valor armazenado com sucesso')
                    ddd_celular_aceito = 1
                    break

                else:
                    continue

            if len(celular_ddd) == 3:

                # Confirmando que caso o DDD tenha 3 dígitos, o primeiro foi de fato zero
                if str(celular_ddd)[0] != '0':
                    teste_ddd = input(
                        'O valor inserido do DDD inserido não é de um DDD válido no Brasil, deseja continuar? (S/N): ').lower()
                    if teste_ddd == 'n':
                        continue

            elif len(celular_ddd) == 2 and '0' not in str(celular_ddd):
                print('DDD armazenado com sucesso')
                ddd_celular_aceito = 1  # Alterando flag para True

            else:
                print('ERRO: Favor inserir DDD válido')

        celular_aceito = 0  # Flag que será validada para 'True' caso o valor informado para o número de celular se mostre válido

        while not celular_aceito:
            num_celular = input('Digite o número do celular, sem o DDD: ')

            copia_num_celular = num_celular
            num_celular = str()

            # Removendo valores não númericos, como '-' (traços) e espaços
            for digito in copia_num_celular:
                if digito.isdecimal():  # Aplicando o filtro de valor numérico
                    num_celular += digito

            if len(num_celular) not in (8, 9):

                teste = input(
                    'O valor inserido não possui o tamanho padrão para números no Brasil, deseja continuar? (S/N): ').lower()
                if teste[0] == 's':
                    print(f'Número ({celular_ddd}) {num_celular} armazenado com sucesso')
                    celular_aceito = 1
                else:
                    continue

            else:
                celular_aceito = 1

        celular = celular_ddd + num_celular
        celular = int(celular)

        return[nome, celular, email]

    def armazena_contato(self):
        contato = Agenda.gera_contato(agenda)
        self.contatoRepository.create(contato)
        print(f'Contato {contato[0]} armazenado com sucesso')
        Agenda.pause(agenda)

    def remove_contato(self):

        print('''
+-------------------------+
|   Remoção de contatos   |
+-------------------------+
''')
        contatosIds = self.contatoRepository.findIds()

        IDs = list()

        for id in contatosIds:  # for loop que irá armazenar apenas os ID's existentes, como inteiros
            IDs.append(int(id[0]))

        Agenda.view(agenda)

        try:

            removido = int(
                input('Digite o ID do contato que deseja remover: '))

            if removido not in IDs:
                raise ValueError

        except ValueError:

            teste = input(
                "ERRO: O valor inserido não se refere a nenhum dos ID's. Digite 'Sim' para tentar novamente: ").strip().lower()
            if teste[0] == 's':
                Agenda.remove_contato(agenda)

            else:
                Agenda.pause(agenda)

        # Remoção do contato selecionado:

        self.contatoRepository.deleteById(removido)

        print(f'Contato {removido} removido com sucesso!')

        Agenda.main(agenda)

    def pause(self):

        input('\nTecle ENTER para continuar...')
        return

    def opcoes(self):

        op = input(f'''
  Menu de ações da agenda
  Escolha sua ação dentre as opções abaixo:
            
  1 - Exibir contatos
  2 - Adicionar novo contato
  3 - Deletar contatos
  4 - Restaurar último contato deletado
  Insira o número referente à ação para continuar: ''').lower()

        if op == '1':
            Agenda.view(agenda)
            Agenda.pause(agenda)

        if op == '2':

            Agenda.armazena_contato(agenda)

        if op == '3':
            Agenda.remove_contato(agenda)

        if op == '4':
            print('Vish. Essa funcionaldiade nem comecei ainda')
            Agenda.main(agenda)

        if input('\nVocê deseja realizar alguma outra ação?\nResponda com "Sim" para continuar a utilizar a agenda: ').lower()[0] == 's':
            Agenda.main(agenda)

        else:
            print('Obrigado por utilizar a agenda Pythônica.\nTchaaaau')
            __name__ = '__sair__'


if __name__ == '__main__':
    print('Bem-vindo à Agenda Telefênonica Pythônica.\nDesenvolvida por @darlinhows')
    repository = ContatoRepository()
    repository.connect()
    agenda = Agenda(repository)
    agenda.pause()
    agenda.opcoes()
