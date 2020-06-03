from infrastructure.contatoRepository import ContatoRepository
from view.agendaView import AgendaView

if __name__ == '__main__':
    print('Bem-vindo à Agendas Telefênonica Pythônica.\nDesenvolvida por @darlinhows')
    repository = ContatoRepository()
    repository.connect()
    agenda = AgendaView(repository)
    agenda.pause()
