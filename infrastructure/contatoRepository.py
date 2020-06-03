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
        self.createIfNotExists()

    def createIfNotExists(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contatos (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT,
            ddd TEXT NOT NULL,
            celular TEXT NOT NULL,
            isDeleted BOOLEAN DEFAULT 0,
            UNIQUE(id))''')
        self.conexao.commit()

    def create(self, contato):
        nome = 0
        celular = 1
        email = 2
        self.cursor.execute('INSERT INTO contatos (id, nome, ddd, celular, email) VALUES(NULL, ?, ?, ?, ?)',
                            (contato.nome, contato.ddd, contato.celular, contato.email))
        self.conexao.commit()

    def findById(self, id):
        return self.cursor.execute(f'SELECT * FROM contatos WHERE id = ? AND isDeleted = 0', (id,))

    def exists(self, id):
        return self.cursor.execute(f'SELECT EXISTS(SELECT 1 FROM contatos WHERE id = ?)', (id,)).fetchone()[0]

    def findContatosExcluidos(self, pagina=0, tamanho=10):
        skipItems = self.skip(pagina, tamanho)
        return self.cursor.execute(f'''SELECT * FROM contatos
                                    WHERE IsDeleted = 1
                                    ORDER BY id
                                    LIMIT {tamanho}
                                    OFFSET {skipItems}''').fetchall()

    def query(self):
        return self.cursor.execute(f'''SELECT * FROM contatos
                                    WHERE IsDeleted = 0
                                    ORDER BY id''').fetchall()

    def findIds(self):
        return self.cursor.execute("SELECT id column from contatos WHERE IsDeleted = 0").fetchall()

    def deleteById(self, id):
        """
         Apaga contato por id
         :param id: Id do contato
         :return:
         """
        self.cursor.execute(
            'UPDATE contatos SET IsDeleted = 1 WHERE id = ?', (id,))
        self.conexao.commit()

    def restaurar(self, id):
        """
        Restaura contato por id
        :param id: Id do contato
        :return:
        """
        self.cursor.execute(
            'UPDATE contatos SET IsDeleted = 0 WHERE id = ?', (id,))
        self.conexao.commit()

    def skip(self, pagina, tamanho):
        return pagina * tamanho
