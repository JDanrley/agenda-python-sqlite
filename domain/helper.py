from domain.contato import Contato

def validateEmpty(inputValue):
    return inputValue != ""

def validateInput(inputValue):
    return validateEmpty(inputValue) and inputValue.lower()[0] == 's'

def toContatoList(cursor):
    return [Contato(*prop) for prop in cursor]