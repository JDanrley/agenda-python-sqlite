import re
EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"
CELULAR_REGEX = r"^\s*(\d{2}|\d{0})[-. ]?(\d{5}|\d{4})[-. ]?(\d{4})[-. ]?\s*$"


class Contato:
    def __init__(self, id, nome, email, ddd, celular, isDeleted=0):
        self.id = id
        self.email = email
        self.nome = nome
        self.isDeleted = isDeleted
        self.ddd = ddd
        self.celular = celular
        self.emailRegex = re.compile(EMAIL_REGEX)
        self.celularRegex = re.compile(CELULAR_REGEX)
        pass

    def isValid(self):
        try:
            self.validateEmail()
            self.validateDdd()
            self.validateCelular()
            return True
        except Exception as e:
            print(f'\n Erro na validação dos dados do contato {self.nome}: {e}')
            return False

    def validateEmail(self, email=None):
        match = self.emailRegex.match(email if email != None else self.email)
        if (match == None):
            raise Exception("Email inválido")

    def validateDdd(self, ddd=None):
        ddd = ddd if ddd != None else self.ddd
        parsed_ddd = str(ddd)
        if (len(parsed_ddd) > 3):
            raise Exception("O valor inserido possui mais de 3 caracteres.")

        elif ((len(parsed_ddd) == 3 and not parsed_ddd.startswith('0')) or (len(parsed_ddd) == 2 and '0' in parsed_ddd)):
            raise Exception(
                'O valor inserido do DDD inserido não é de um DDD válido no Brasil')

    def validateCelular(self, celular=None):
        celular = celular if celular != None else self.celular
        match = self.celularRegex.match(celular)
        if(match == None or len(str(celular)) not in (8, 9)):
            raise Exception('celular inválido')
