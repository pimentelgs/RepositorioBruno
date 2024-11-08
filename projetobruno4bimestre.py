from pymongo import MongoClient
from pymongo import collection
import hashlib

# ============================================================================================================================#

client = MongoClient(
    "mongodb+srv://guipim999:Gui070823@cluster1.dixgf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1")
db = client['banco_hospital']
collection = db['colecao1']
if client.admin.command('ping')['ok'] == 1:
    print("Conexão estabelecida com sucesso!")


# CRIPTOGRAFIA
def criptografar(x):
    stringhash = hashlib.sha256(x.encode()).hexdigest()
    return stringhash


# DESCRIPTOGRAFIA

# VERIFICAÇÃO DE SENHA
def verificar_senha(medico, password):
    documento = collection.find_one({"medico": f"{medico}"})
    if documento:
        senha_armazenada = documento.get('senha')
        if senha_armazenada == password:
            print("Senha correta!")
            return True
        else:
            print("Senha incorreta!")
            return False
    else:
        print("Médico não encontrado!")
        return False


# CREATE
def create(medico, senha, paciente, historico, tratamento):
    medico_criptografado = criptografar(medico)
    senha_criptografada = criptografar(senha)
    paciente_criptografado = criptografar(paciente)
    historico_criptografado = criptografar(historico)
    tratamento_criptografado = criptografar(tratamento)
    pessoa = {"medico": f"{medico_criptografado}", "senha": f"{senha_criptografada}", "paciente": f"{paciente_criptografado}",
              "historico": f"{historico_criptografado}", "tratamento": f"{tratamento_criptografado}"}
    c = collection.insert_one(pessoa)
    criptografar(paciente)
    criptografar(historico)
    criptografar(tratamento)


# READ
def ler(paciente):
    for itens in collection.find_one({"paciente": f"{criptografar(paciente)}"}):
        print(itens)

# DELETE
def delete(paciente):
    query = {"paciente": paciente}
    quantos = input(f"Deseja deletar todos os {paciente}? (S/N): ")
    if quantos == "S":
        collection.delete_many(query)
    else:
        collection.delete_one(query)


# ============================================================================================================================#

medico = input("Digite o nome do médico: ")
password = input("Digite a senha do médico: ")

continuar = "S"
while continuar == "S":
    print("=-"*25)

    resposta = input("Create, Read ou Delete? ")

    if resposta == "Create":
        if verificar_senha(medico, password) == True:
            medico = input("Digite o nome do médico para criar: ")
            senha = input("Digite a senha do médico para criar: ")
            paciente = input("Digite o nome do paciente para criar: ")
            historico = input("Digite o histórico do paciente para criar: ")
            tratamento = input("Digite o tratamento do paciente para criar: ")
            create(medico, senha, paciente, historico, tratamento)
            print("Documento gerado com sucesso!")

    if resposta == "Read":
        if verificar_senha(medico, password) == True:
            paciente = input("Digite o nome do paciente para ler: ")
            ler(paciente)

    if resposta == "Delete":
        if verificar_senha(medico, password) == True:
            paciente = input("Digite o nome do paciente que deseja deletar: ")
            delete(paciente)
            print("Documento deletado com sucesso!")

    print("=-" * 25)

    continuar = input("Deseja continuar? S/N")