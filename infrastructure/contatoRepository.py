import sqlite3


class ContatoRepository:
    """
    Repository de contato, as operações relacionadas a esta entidade são centralizadas aqui
    """

    def __init__(self):
        pass

    def connect(self):
        self.conexao = sqlite3.connect("contatos.db")
        self.cursor = self.conexao.cursor()

    def createIfNotExists(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contatos (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            celular INTEGER NOT NULL,
            email TEXT,
            UNIQUE(id))''')
        self.conexao.commit()

    def create(self, contato):
        nome = 0
        celular = 1
        email = 2
        self.cursor.execute('INSERT INTO contatos (id, nome, celular, email) VALUES(NULL, ?, ?, ?)',
                            (contato[nome], contato[celular], contato[email]))
        self.conexao.commit()

    def query(self):
        return self.cursor.execute('SELECT * FROM contatos ORDER BY nome DESC LIMIT 1 OFFSET 1').fetchall()

    def findIds(self):
        return self.cursor.execute("SELECT id column from contatos").fetchall()

    def deleteById(self, id):
        """
         Apaga contato por id
         :param id: Id do contato
         :return:
         """
        print(id)
        self.cursor.execute('DELETE from contatos WHERE id = ?', (id,))
        self.conexao.commit()
