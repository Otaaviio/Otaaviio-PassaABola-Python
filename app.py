import os
import json
import pages.paginaAdmin as paginaAdmin
import pages.paginaJogadora as paginaJogadora
import pages.paginaOlheiro as paginaOlheiro

# ----------------------------
# Configurações de persistência
# ----------------------------
ARQUIVO_JOGADORAS = "Json/jogadoras.json"

def carregar_jogadoras():
    if not os.path.exists(ARQUIVO_JOGADORAS):
        with open(ARQUIVO_JOGADORAS, "w", encoding="utf-8") as f:
            json.dump([], f)
    with open(ARQUIVO_JOGADORAS, "r", encoding="utf-8") as f:
        dados = json.load(f)
        if isinstance(dados, list):
            return dados
        elif isinstance(dados, dict):
            return [dados]
        else:
            return []

def salvar_jogadoras(jogadoras):
    with open(ARQUIVO_JOGADORAS, "w", encoding="utf-8") as f:
        json.dump(jogadoras, f, indent=4, ensure_ascii=False)

jogadoras = carregar_jogadoras()


# ----------------------------
# Funções utilitárias
# ----------------------------
def mostraLetreiro():
    print('''
░█▀▀█ ░█▀▀▀█ ─█▀▀█ ░█─── 　 ░█▀▀█ ░█▀▀█ ░█▀▀▀ ─█▀▀█ ░█─▄▀ ░█▀▀▀ ░█▀▀█ ░█▀▀▀█ 
░█─▄▄ ░█──░█ ░█▄▄█ ░█─── 　 ░█▀▀▄ ░█▄▄▀ ░█▀▀▀ ░█▄▄█ ░█▀▄─ ░█▀▀▀ ░█▄▄▀ ─▀▀▀▄▄ 
░█▄▄█ ░█▄▄▄█ ░█─░█ ░█▄▄█ 　 ░█▄▄█ ░█─░█ ░█▄▄▄ ░█─░█ ░█─░█ ░█▄▄▄ ░█─░█ ░█▄▄▄█
''')

def opcaoInvalida():
    input("\nOpção inválida\nPressione 'Enter' para voltar")
    main()

def finalizaPrograma():
    os.system("cls")
    print('''\n
█▀█ █▀█ █▀█ █▀▀ █▀█ ▄▀█ █▀▄▀█ ▄▀█   █▀▀ █ █▄░█ ▄▀█ █░░ █ ▀█ ▄▀█ █▀▄ █▀█ ░   █▀█ █▄▄ █▀█ █ █▀▀ ▄▀█ █▀▄ █▀█ █
█▀▀ █▀▄ █▄█ █▄█ █▀▄ █▀█ █░▀░█ █▀█   █▀░ █ █░▀█ █▀█ █▄▄ █ █▄ █▀█ █▄▀ █▄█ ▄   █▄█ █▄█ █▀▄ █ █▄█ █▀█ █▄▀ █▄█ ▄''')
    
# ----------------------------
# Funções de validação
# ----------------------------

def validaEntrada(mensagem, tipo=str, opcoes_validas=None, permite_vazio=False):
    while True:
        try:
            entrada = input(mensagem)
            
            if permite_vazio and entrada == "":
                return entrada
            
            if tipo == int:
                valor = int(entrada)
            elif tipo == float:
                valor = float(entrada)
            else:
                valor = entrada
            
            if opcoes_validas is not None and valor not in opcoes_validas:
                print(f"Opção inválida! Escolha entre: {opcoes_validas}")
                continue
            
            return valor
            
        except ValueError:
            if tipo == int:
                print("Erro: Digite um número inteiro válido!")
            elif tipo == float:
                print("Erro: Digite um número decimal válido!")
            else:
                print("Entrada inválida!")

def valida_cpf(cpf):
    try:
        cpf = cpf.strip()
        
        if not cpf.isdigit():
            raise ValueError("CPF deve conter apenas números")
        
        if len(cpf) != 11:
            raise ValueError("CPF deve ter exatamente 11 dígitos")
        
        return cpf
        
    except ValueError as e:
        print(f" Erro: {e}")
        return None


def valida_email(email):
    try:
        email = email.strip()
        
        if "@" not in email and "." not in email:
            raise ValueError("Formatação de Email inválida")
        
        if email.count("@") != 1:
            raise ValueError("Email deve conter apenas um '@'")
        
        return email
        
    except ValueError as e:
        print(f" Erro: {e}")
        return None

# ----------------------------
# Funções menu
# ----------------------------
def menuDeOpcoes():
    print("\nDIGITE:\n")
    print("   1 - Login")
    print("   2 - Cadastre-se")
    print("   3 - Finalizar programa\n")

def escolheOpcaoDeMenu():
    opcao = validaEntrada('Escolha uma opção: ', int, [1, 2, 3])
    
    if opcao == 1:
        loginUsuario()
    elif opcao == 2:
        criaUsuario()
    elif opcao == 3:
        finalizaPrograma()

# ----------------------------
# Login e autenticação
# ----------------------------
def loginUsuario():
    os.system("cls")
    mostraLetreiro()
    print("\nLOGIN DE USUÁRIO\n")

    email = input("E-mail: ")
    senha = input("Senha: ")

    for usuario in jogadoras:
        if usuario.get("email") == email and usuario.get("senha") == senha:
            print(f"\nLogin realizado com sucesso!\nSeja bem-vindo(a), {usuario.get('nome')}!")
            tipoDeUsuario(usuario)
            return

    input("\nE-mail ou senha incorretos.\nTecle 'Enter' para tentar novamente")
    loginUsuario()

def tipoDeUsuario(usuario):
    if usuario.get("tipoDeUsuario") == 1:
        paginaJogadora.mainJogadora(usuario)
    elif usuario.get("tipoDeUsuario") == 2:
        paginaOlheiro.menuOlheiro(usuario)
    elif usuario.get("tipoDeUsuario") == 3:
        paginaAdmin.menuAdmin(usuario)
    else:
        input("\nTipo de usuário inválido. Tecle 'Enter' para voltar ao menu")
        loginUsuario()

# ----------------------------
# Cadastro
# ----------------------------
def perguntasParaCadastro():
    print("=== CADASTRO DE NOVO USUÁRIO ===\n")
    
    nomeCompleto = validaEntrada("Nome completo: ", str)

    email = None
    while email is None:
        email_input = input("E-mail: ")
        email = valida_email(email_input)
        if email is None:
            print("Tente novamente.\n")

    senha = validaEntrada("Senha: ", str)

    cpf = None
    while cpf is None:
        cpf_input = input("CPF (apenas números, 11 dígitos): ")
        cpf = valida_cpf(cpf_input)
        if cpf is None:
            print("Tente novamente.\n")

    verificaSeJaExiste(cpf)

    print("\nVocê é:")
    print("  1 - Jogadora")
    print("  2 - Olheiro(a)")
    tipoDeUsuario = validaEntrada("Escolha: ", int, [1, 2])

    if tipoDeUsuario == 1:
        return {
            "nome": nomeCompleto,
            "email": email,
            "senha": senha,
            "cpf": cpf,
            "tipoDeUsuario": tipoDeUsuario,
            "idade": 0,
            "posicao": "",
            "sub": 0,
            "highlights": "",
            "redeSocial": "",
            "pontos": 0,
            "avaliacoes": []
        }
    else:
        return {
            "nome": nomeCompleto,
            "email": email,
            "senha": senha,
            "cpf": cpf,
            "tipoDeUsuario": tipoDeUsuario
        }

def verificaSeJaExiste(cpf):
    for usuario in jogadoras:
        if usuario.get("cpf") == cpf:
            input("\nEsse CPF já está cadastrado.\nTecle 'Enter' para voltar ao menu")
            main()

def criaUsuario():
    os.system("cls")
    mostraLetreiro()
    print("\nCADASTRO DE USUÁRIO\n")

    usuario = perguntasParaCadastro()
    jogadoras.append(usuario)
    salvar_jogadoras(jogadoras)

    input("\nCadastro realizado com sucesso!\nTecle 'Enter' para voltar ao menu")
    main()

# ----------------------------
# Ponto de entrada
# ----------------------------
def main():
    os.system("cls")
    mostraLetreiro()
    menuDeOpcoes()
    escolheOpcaoDeMenu()
# ----------------------------
# Início do programa
# ----------------------------
if __name__ == "__main__":
    main()
    