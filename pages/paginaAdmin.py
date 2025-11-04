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
    print('''\n=== MENU ADMIN ===          
1 - Listar jogadoras
2 - Enviar notificação global
3 - Criar campeonato
4 - Gerenciar campeonatos
5 - Sair\n''')

    try:
        opcao = int(input("Escolha uma opção: "))
        match opcao:
            case 1:
                listarJogadoras(admin)
            case 2:
                enviarNotificacaoGlobal(admin)
            case 3:
                criaCampeonato(admin)
            case 4:
                gerenciarCampeonatos(admin)
            case 5:
                app.main()
            case _:
                print("Opção inválida!")
                input("Pressione Enter...")
                menuAdmin(admin)
    except ValueError:
        print("Digite um número válido!")
        input("Pressione Enter...")
        menuAdmin(admin)

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
    print("=== CRIAR CAMPEONATO ===\n")

    try:
        nomeCampeonato = input("Nome do campeonato: ")
        if not nomeCampeonato:
            print("Nome não pode ser vazio!")
            input("Pressione Enter...")
            return criaCampeonato(admin)
        
        local = input("Local do campeonato: ")
        if not local:
            print("Local não pode ser vazio!")
            input("Pressione Enter...")
            return criaCampeonato(admin)
        
        dataHora = input("Data e hora (ex: 2025-12-31 15:00): ")
        if not dataHora:
            print("Data/hora não pode ser vazia!")
            input("Pressione Enter...")
            return criaCampeonato(admin)
        
        requisitos = input("Requisitos para participar: ")
        regras = input("Regras do campeonato (link): ")
        
        while True:
            try:
                numeroTimes = int(input("Quantos times vão participar: "))
                if numeroTimes <= 0:
                    print("Número deve ser maior que 0!")
                    continue
                break
            except ValueError:
                print("Digite um número válido!")
        
        while True:
            try:
                numeroJogadorasPorTime = int(input("Quantas jogadoras por time: "))
                if numeroJogadorasPorTime <= 0:
                    print("Número deve ser maior que 0!")
                    continue
                break
            except ValueError:
                print("Digite um número válido!")
        
        dataLimiteInscricao = input("Data limite para inscrição (YYYY-MM-DD): ")

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

        print("\nCampeonato criado com sucesso!")
        input("Pressione Enter para voltar...")
        menuAdmin(admin)
        
    except Exception as e:
        print(f"Erro ao criar campeonato: {e}")
        input("Pressione Enter...")
        criaCampeonato(admin)


def gerenciarCampeonatos(admin):
    os.system("cls")

    try:
        campeonatos = carregarCampeonatos()

        if not campeonatos:
            print("Nenhum campeonato encontrado.")
            input("Pressione Enter...")
            return menuAdmin(admin)

        print("\n=== CAMPEONATOS ===\n")
        for i, c in enumerate(campeonatos, start=1):
            print(f"{i}. {c['nomeCampeonato']}")
            print(f"   Times aprovados: {len(c.get('timesAprovados', []))}")
            print(f"   Times inscritos: {len(c.get('timesInscritos', []))}")
            print("-" * 50)

        while True:
            try:
                escolha = int(input("\nEscolha um campeonato (0 para voltar): "))
                
                if escolha == 0:
                    return menuAdmin(admin)
                
                if escolha < 1 or escolha > len(campeonatos):
                    print(f"Escolha entre 1 e {len(campeonatos)}!")
                    continue
                
                break
            except ValueError:
                print("Digite um número válido!")

        campeonato = campeonatos[escolha-1]
        gerenciarTimesCampeonato(admin, campeonato, campeonatos)

    except Exception as e:
        print(f"Erro: {e}")
        input("Pressione Enter...")
        menuAdmin(admin)


def gerenciarTimesCampeonato(admin, campeonato, campeonatos):
    os.system("cls")
    
    try:
        times = carregarTimes()

        print(f"\n=== {campeonato['nomeCampeonato']} ===")
        print("Times inscritos aguardando aprovação:\n")

        if not campeonato.get("timesInscritos"):
            print("Nenhum time inscrito ainda.")
            input("Pressione Enter...")
            return gerenciarCampeonatos(admin)

        for i, t_nome in enumerate(campeonato["timesInscritos"], start=1):
            time = next((t for t in times if t["nome"] == t_nome), None)
            if not time:
                continue
            print(f"\n{i}. {time['nome']} (Capitã: {time['criadora']})")
            print("   Jogadoras:")
            for email in time["jogadoras"]:
                jogadora = next((j for j in app.jogadoras if j["email"] == email), None)
                if jogadora:
                    nome = jogadora.get('nome', 'N/A')
                    posicao = jogadora.get('posicao', 'N/A')
                    idade = jogadora.get('idade', 0)
                    print(f"     • {nome} | {posicao} | {idade} anos")

        while True:
            try:
                escolha = int(input("\nEscolha um time (0 para voltar): "))
                
                if escolha == 0:
                    return gerenciarCampeonatos(admin)
                
                if escolha < 1 or escolha > len(campeonato["timesInscritos"]):
                    print(f"Escolha entre 1 e {len(campeonato['timesInscritos'])}!")
                    continue
                
                break
            except ValueError:
                print("Digite um número válido!")

        time_nome = campeonato["timesInscritos"][escolha-1]
        print(f"\n=== Time: {time_nome} ===")
        print("1 - Aprovar time")
        print("2 - Rejeitar time")
        print("3 - Voltar")
        
        while True:
            try:
                acao = int(input("\nEscolha: "))
                
                if acao == 1:
                    campeonato.setdefault("timesAprovados", []).append(time_nome)
                    campeonato["timesInscritos"].remove(time_nome)
                    salvarCampeonatos(campeonatos)
                    print(f"\nTime '{time_nome}' aprovado!")
                    input("Pressione Enter...")
                    break
                elif acao == 2:
                    campeonato["timesInscritos"].remove(time_nome)
                    salvarCampeonatos(campeonatos)
                    print(f"\nTime '{time_nome}' rejeitado!")
                    input("Pressione Enter...")
                    break
                elif acao == 3:
                    break
                else:
                    print("Opção inválida!")
                    
            except ValueError:
                print("Digite um número válido!")

        gerenciarTimesCampeonato(admin, campeonato, campeonatos)
    
    except Exception as e:
        print(f"Erro: {e}")
        input("Pressione Enter...")
        gerenciarCampeonatos(admin)

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
