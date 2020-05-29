import re
EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"


class Contato:
    def __init__(self, nome, email, ddd, telefone):
        self.email = email
        self.nome = nome
        self.ddd = ddd
        self.telefone = telefone
        self.emailRegex = re.compile(EMAIL_REGEX)
        pass

    def validate(self):
        self.validateEmail()

    def validateEmail(self, email=None):
        match = self.emailRegex.match(email if email != None else self.email)
        if (match != None):
            raise Exception("Email inválido")
