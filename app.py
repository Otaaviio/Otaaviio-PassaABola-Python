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
# Funções menu
# ----------------------------
def menuDeOpcoes():
    print("\nDIGITE:\n")
    print("   1 - Login")
    print("   2 - Cadastre-se")
    print("   3 - Finalizar programa\n")

def escolheOpcaoDeMenu():
    try:
        opcao = int(input('Escolha uma opção: '))
        if opcao == 1:
            loginUsuario()
        elif opcao == 2:
            criaUsuario()
        elif opcao == 3:
            finalizaPrograma()
        else:
            opcaoInvalida()
    except:
        opcaoInvalida()

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
# Cadastro (BÁSICO)
# ----------------------------
def perguntasParaCadastro():
    nomeCompleto = input("Nome completo: ")
    email = input("E-mail: ")
    senha = input("Senha: ")
    cpf = input("CPF (apenas números): ")
    tipoDeUsuario = int(input("Você é:\n  1 - Jogadora\n  2 - Olheiro(a)\n"))

    verificaSeJaExiste(cpf)

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
    