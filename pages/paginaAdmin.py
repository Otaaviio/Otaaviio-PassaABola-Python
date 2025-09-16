import os
import app
import pages.paginaJogadora as paginaJogadora
import json

ARQUIVO_CAMPEONATOS = "json/campeonatos.json"
ARQUIVO_TIMES = "json/times.json"

# ----------------------------
# Utilitários
# ----------------------------
def carregarCampeonatos():
    with open(ARQUIVO_CAMPEONATOS, "r", encoding="utf-8") as f:
        return json.load(f)

def salvarCampeonatos(campeonatos):
    with open(ARQUIVO_CAMPEONATOS, "w", encoding="utf-8") as f:
        json.dump(campeonatos, f, indent=4, ensure_ascii=False)

def carregarTimes():
    with open(ARQUIVO_TIMES, "r", encoding="utf-8") as f:
        return json.load(f)

def salvarTimes(times):
    with open(ARQUIVO_TIMES, "w", encoding="utf-8") as f:
        json.dump(times, f, indent=4, ensure_ascii=False)

def opcaoInvalida(admin):
    input('Opção inválida\nTecle "Enter" para voltar')
    menuAdmin(admin)

# ----------------------------
# Menu Admin
# ----------------------------
def menuAdmin(admin):
    os.system("cls")
    app.mostraLetreiro()
    print('''\n--- Menu Admin ---          
1 - Listar jogadoras
2 - Enviar notificação global
3 - Criar campeonato
4 - Gerenciar campeonatos
5 - Sair\n''')

    opcao = int(input("Escolha uma opção: "))
    if opcao == 1:
        listarJogadoras(admin)
    elif opcao == 2:
        enviarNotificacaoGlobal(admin)
    elif opcao == 3:
        criaCampeonato(admin)
    elif opcao == 4:
        gerenciarCampeonatos(admin)
    elif opcao == 5:
        app.main()
    else:
        opcaoInvalida(admin)

# ----------------------------
# Listagem de jogadoras
# ----------------------------
def listarJogadoras(admin):
    os.system("cls")
    print("--- Lista de Jogadoras ---\n")
    lista = [j for j in app.jogadoras if j.get("tipoDeUsuario") == 1]
    if not lista:
        print("Nenhuma jogadora cadastrada.")
    else:
        for i, jog in enumerate(lista, start=1):
            print(f"{i} - {jog.get('nome','')} | {jog.get('email','')} | {jog.get('posicao','')}")

    input("\nPressione Enter para voltar.")
    menuAdmin(admin)

# ----------------------------
# Notificações
# ----------------------------
def enviarNotificacaoGlobal(admin):
    os.system("cls")
    print("--- Enviar Notificação Global ---\n")
    mensagem = input("Digite a mensagem para todas as jogadoras: ")
    if not mensagem:
        input("Mensagem vazia. Pressione Enter para voltar.")
        return menuAdmin(admin)

    for jog in app.jogadoras:
        if jog.get("tipoDeUsuario") == 1:
            paginaJogadora.adicionarNotificacao(
                jog.get("email",""),
                f"[Admin {admin.get('nome','')}] {mensagem}"
            )

    input("\nNotificação global enviada com sucesso!\nPressione Enter para voltar.")
    menuAdmin(admin)

# ----------------------------
# Campeonatos
# ----------------------------
def criaCampeonato(admin):
    os.system("cls")
    print("--- Criar Campeonato ---")

    nomeCampeonato = input("Nome do campeonato: ")
    local = input("Local do campeonato: ")
    dataHora = input("Data e hora do campeonato: ")
    requisitos = input("Requisitos para participar: ")
    regras = input("Regras do campeonato (link do documento): ")
    numeroTimes = int(input("Quantos times vão participar: "))
    numeroJogadorasPorTime = int(input("Quantas jogadoras por time: "))
    dataLimiteInscricao = input("Data limite para inscrição (YYYY-MM-DD): ")

    if not nomeCampeonato or not local or not dataHora:
        input("Informações obrigatórias faltando. Pressione Enter.")
        return criaCampeonato(admin)

    campeonato = {
        "nomeCampeonato": nomeCampeonato,
        "local": local,
        "dataHora": dataHora,
        "requisitos": requisitos,
        "regras": regras,
        "numTimes": numeroTimes,
        "numJogadorasPorTime": numeroJogadorasPorTime,
        "dataLimiteInscricao": dataLimiteInscricao,
        "timesInscritos": [],
        "timesAprovados": []
    }

    campeonatos = carregarCampeonatos()
    campeonatos.append(campeonato)
    salvarCampeonatos(campeonatos)

    input("\nCampeonato criado com sucesso!\nPressione Enter para voltar.")
    menuAdmin(admin)


def gerenciarCampeonatos(admin):
    os.system("cls")
    with open("campeonatos.json", "r", encoding="utf-8") as f:
        campeonatos = app.json.load(f)

    if not campeonatos:
        input("Nenhum campeonato encontrado. Pressione Enter.")
        return menuAdmin(admin)

    print("\n--- Campeonatos ---\n")
    for i, c in enumerate(campeonatos, start=1):
        print(f"{i} - {c['nomeCampeonato']} | Times aprovados: {len(c.get('timesAprovados', []))}")

    escolha = int(input("\nEscolha um campeonato (0 para voltar): "))
    if escolha == 0 or escolha > len(campeonatos):
        return menuAdmin(admin)

    campeonato = campeonatos[escolha-1]
    gerenciarTimesCampeonato(admin, campeonato, campeonatos)


def gerenciarTimesCampeonato(admin, campeonato, campeonatos):
    os.system("cls")
    with open("times.json", "r", encoding="utf-8") as f:
        times = app.json.load(f)

    print(f"\n--- {campeonato['nomeCampeonato']} ---")
    print("Times inscritos:\n")

    if not campeonato.get("timesInscritos"):
        input("Nenhum time inscrito ainda. Pressione Enter.")
        return gerenciarCampeonatos(admin)

    for i, t_nome in enumerate(campeonato["timesInscritos"], start=1):
        time = next((t for t in times if t["nome"] == t_nome), None)
        if not time:
            continue
        print(f"\n{i} - {time['nome']} (Criadora: {time['criadora']})")
        print("Jogadoras:")
        for email in time["jogadoras"]:
            jogadora = next((j for j in app.jogadoras if j["email"] == email), None)
            if jogadora:
                print(f" - {jogadora['nome']} | {jogadora.get('posicao','')} | {jogadora.get('idade',0)} anos")

    escolha = int(input("\nEscolha um time para aprovar/rejeitar (0 para voltar): "))
    if escolha == 0 or escolha > len(campeonato["timesInscritos"]):
        return gerenciarCampeonatos(admin)

    time_nome = campeonato["timesInscritos"][escolha-1]
    print(f"\n1 - Aprovar time '{time_nome}'\n2 - Rejeitar\n3 - Voltar")
    acao = int(input("Escolha: "))
    if acao == 1:
        campeonato.setdefault("timesAprovados", []).append(time_nome)
        input(f"Time '{time_nome}' aprovado! Pressione Enter.")
    elif acao == 2:
        campeonato["timesInscritos"].remove(time_nome)
        input(f"Time '{time_nome}' rejeitado! Pressione Enter.")

    with open("campeonatos.json", "w", encoding="utf-8") as f:
        app.json.dump(campeonatos, f, indent=4, ensure_ascii=False)

    gerenciarTimesCampeonato(admin, campeonato, campeonatos)

# ----------------------------
# Times
# ----------------------------
def listarTimes(admin):
    os.system("cls")
    print("--- Lista de Times ---\n")

    times = carregarTimes()
    if not times:
        print("Nenhum time cadastrado.")
    else:
        for i, t in enumerate(times, start=1):
            print(f"{i} - {t['nome']} | Criadora: {t['criadora']} | Jogadoras: {len(t['jogadoras'])}")

    input("\nPressione Enter para voltar.")
    menuAdmin(admin)
