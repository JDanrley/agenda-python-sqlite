import sqlite3

conexao = sqlite3.connect("contatos.db")
cursor = conexao.cursor()


class Agenda(object):
  def __init__(self):
    pass

  def view(self):
    view = cursor.execute('SELECT * FROM contatos').fetchall()
    if len(view) > 0:
      print('''
+---------------------------------+
|  Contatos existentes na tabela  |
+---------------------------------+ ''')
    else:
      print('\nA Agenda não possui nenhum contato')
      Agenda.pause(x)
      Agenda.main(x)
      
    view = cursor.execute('SELECT * FROM contatos').fetchall()
    for i in view:
      for j in i:
        if j == i[0]: print(f'\nContato ID: {j}\nNome: {i[1]}\nCelular: {i[2]}\nEmail: {i[3]}\n')
    
  def gera_contato(self):
    
    nome = input('Digite o nome do contato a ser adicionado: ')
    email = input('Digite o email do contato: ')
    ddd_celular_aceito = 0 #Flag que será validada para 'True' caso o valor informado para o DDD se mostre válido

    while not ddd_celular_aceito:
      try:
        celular_ddd = int(input('Digite o DDD do celular: '))
        
      except ValueError: #Evitando o erro de inserção de caracteres não numéricos 
        print('ERRO: O valor inserido não contém apenas números, favor informar novamente o DDD.')
        continue
      
      celular_ddd = str(celular_ddd)
      
      if len(celular_ddd) > 3:
        teste = input(('ERRO: O valor inserido possui mais de 3 caracteres. Deseja salvar mesmo assim? (S/N): ')).lower()
        if teste == 's':
          print('Valor armazenado com sucesso')
          ddd_celular_aceito = 1
          break

        else:
          continue
        
      if len(celular_ddd) == 3:
        
        if str(celular_ddd)[0] != '0': #Confirmando que caso o DDD tenha 3 dígitos, o primeiro foi de fato zero
          teste_ddd = input('O valor inserido do DDD inserido não é de um DDD válido no Brasil, deseja continuar? (S/N): ').lower()
          if teste_ddd == 'n':
            continue
          
          
      elif len(celular_ddd) == 2 and '0' not in str(celular_ddd):
        print('DDD armazenado com sucesso')
        ddd_celular_aceito = 1 #Alterando flag para True
        
      else:
        print('ERRO: Favor inserir DDD válido')
  
    celular_aceito = 0 #Flag que será validada para 'True' caso o valor informado para o número de celular se mostre válido

    while not celular_aceito:
      num_celular = input('Digite o número do celular, sem o DDD: ')

      copia_num_celular = num_celular
      num_celular = str()
      
      for digito in copia_num_celular: #Removendo valores não númericos, como '-' (traços) e espaços
        if digito.isdecimal(): #Aplicando o filtro de valor numérico
          num_celular += digito

      if len(num_celular) not in (8,9):
        
        teste = input('O valor inserido não possui o tamanho padrão para números no Brasil, deseja continuar? (S/N): ').lower()
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
    contato = Agenda.gera_contato(x)
    cursor.execute('INSERT INTO contatos (id, nome, celular, email) VALUES(NULL, ?, ?, ?)', (contato[0], contato[1], contato[2]))
    conexao.commit()
    print(f'Contato {contato[0]} armazenado com sucesso')
    Agenda.pause(x)
    

  def remove_contato(self):

    print('''
+-------------------------+
|   Remoção de contatos   |
+-------------------------+
''')
    get = cursor.execute("SELECT id column from contatos").fetchall() #obtendo lista com ID's
    
    IDs = list()
    
    for i in get: #for loop que irá armazenar apenas os ID's existentes, como inteiros
      IDs.append(int(i[0]))

    Agenda.view(x)
    
    try:
      
      removido = int(input('Digite o ID do contato que deseja remover: '))
      
      if removido not in IDs:
        raise ValueError

    except ValueError:
      
      teste = input("ERRO: O valor inserido não se refere a nenhum dos ID's. Digite 'Sim' para tentar novamente: ").strip().lower()
      if teste[0] == 's':
        Agenda.remove_contato(x)

      else:
        Agenda.pause(x)

    #Remoção do contato selecionado:
        
    cursor.execute(f'DELETE from contatos WHERE id = {removido}')
    conexao.commit()
    print(f'Contato {removido} removido com sucesso!')
    
    Agenda.main(x)
    
  def pause(self):

    input('\nTecle ENTER para continuar...')
    return

  def main(self):
        
    op = input(f'''
  Menu de ações da agenda
  Escolha sua ação dentre as opções abaixo:
            
  1 - Exibir contatos
  2 - Adicionar novo contato
  3 - Deletar contatos
  4 - Restaurar último contato deletado
  Insira o número referente à ação para continuar: ''').lower()
        
    if op == '1':
      Agenda.view(x)
      Agenda.pause(x)
            
    if op == '2':
            
      Agenda.armazena_contato(x)

    if op == '3':
      Agenda.remove_contato(x)

    if op == '4':
      print('Vish. Essa funcionaldiade nem comecei ainda')
      Agenda.main(x)

    if input('\nVocê deseja realizar alguma outra ação?\nResponda com "Sim" para continuar a utilizar a agenda: ').lower()[0] == 's':
      Agenda.main(x)

    else:
      print('Obrigado por utilizar a agenda Pythônica.\nTchaaaau')
      __name__ = '__sair__'
      
if __name__ == '__main__':
  print('Bem-vindo à Agenda Telefênonica Pythônica.\nDesenvolvida por @darlinhows')
  cursor.execute('''
        CREATE TABLE IF NOT EXISTS contatos (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        celular INTEGER NOT NULL,
        email TEXT,
        UNIQUE(id)
)
''')
  conexao.commit()
  x = Agenda()
  x.pause()
  x.main()
