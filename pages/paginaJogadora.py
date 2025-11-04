import os
import json
import app
from datetime import datetime

ARQUIVO_JOGADORAS = "json/jogadoras.json"
ARQUIVO_NOTIFICACOES = "json/notificacoes.json"
ARQUIVO_TIMELINE = "json/timeline.json"
ARQUIVO_TIMES = "json/times.json"
ARQUIVO_CAMPEONATOS = "json/campeonatos.json"

# ----------------------------
# Utilitários
# ----------------------------

def salvarAlteracoes(jogadoras):
    with open(ARQUIVO_JOGADORAS, "w", encoding="utf-8") as f:
        json.dump(jogadoras, f, indent=4, ensure_ascii=False)

def carregarNotificacoes():
    if not os.path.exists(ARQUIVO_NOTIFICACOES):
        with open(ARQUIVO_NOTIFICACOES, "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open(ARQUIVO_NOTIFICACOES, "r", encoding="utf-8") as f:
        return json.load(f)

def salvarNotificacoes(notificacoes):
    with open(ARQUIVO_NOTIFICACOES, "w", encoding="utf-8") as f:
        json.dump(notificacoes, f, indent=4, ensure_ascii=False)
        
def carregarTimeline():
    if not os.path.exists(ARQUIVO_TIMELINE):
        with open(ARQUIVO_TIMELINE, "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open(ARQUIVO_TIMELINE, "r", encoding="utf-8") as f:
        return json.load(f)

def salvarTimeline(timeline):
    with open(ARQUIVO_TIMELINE, "w", encoding="utf-8") as f:
        json.dump(timeline, f, indent=4, ensure_ascii=False)

def carregarTimes():
    if not os.path.exists(ARQUIVO_TIMES):
        with open(ARQUIVO_TIMES, "w", encoding="utf-8") as f:
            json.dump([], f)
    with open(ARQUIVO_TIMES, "r", encoding="utf-8") as f:
        return json.load(f)

def salvarTimes(times):
    with open(ARQUIVO_TIMES, "w", encoding="utf-8") as f:
        json.dump(times, f, indent=4, ensure_ascii=False)

def carregarCampeonatos():
    if not os.path.exists(ARQUIVO_CAMPEONATOS):
        with open(ARQUIVO_CAMPEONATOS, "w", encoding="utf-8") as f:
            json.dump([], f)
    with open(ARQUIVO_CAMPEONATOS, "r", encoding="utf-8") as f:
        return json.load(f)

def salvarCampeonatos(campeonatos):
    with open(ARQUIVO_CAMPEONATOS, "w", encoding="utf-8") as f:
        json.dump(campeonatos, f, indent=4, ensure_ascii=False)

def adicionarEvento(email, mensagem):
    timeline = carregarTimeline()
    if email not in timeline:
        timeline[email] = []
    evento = {
        "data": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "mensagem": mensagem
    }
    timeline[email].append(evento)
    salvarTimeline(timeline)

def adicionarNotificacao(email, mensagem):
    notificacoes = carregarNotificacoes()
    if not email:
        return
    if email not in notificacoes:
        notificacoes[email] = []
    notificacoes[email].append(mensagem)
    salvarNotificacoes(notificacoes)
    adicionarEvento(email, f"Notificação recebida: {mensagem}")

def opcaoInvalida(jogadora):
    input('Opção inválida\nTecle "Enter" para voltar')
    mainJogadora(jogadora)

# ----------------------------
# Menu principal da jogadora
# ----------------------------
def menuJogadora():
    print('''\n--- Menu Jogadora ---
          
1 - Ver perfil
2 - Notificações
3 - Ver Timeline
4 - Gerenciar Time
5 - Sair\n''')

def escolhaMenuJogadora(jogadora):

    try:
        menuJogadora()

        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            verPerfil(jogadora)
        elif opcao == "2":
            notificacoes(jogadora)
        elif opcao == "3":
            verTimeline(jogadora)
        elif opcao == "4":
            gerenciarTime(jogadora)
        elif opcao == "5":
            app.main()
        else:
            print(" Opção inválida!")
            input("Pressione Enter para voltar...")
            mainJogadora(jogadora)
    except Exception as e:
        print(f" Erro: {e}")
        input("Pressione Enter para voltar...")
        mainJogadora(jogadora)


def verPerfil(jogadora):
    os.system("cls")
    print("=== SEU PERFIL ===\n")
    print(f"Nome: {jogadora.get('nome','')}")
    print(f"E-mail: {jogadora.get('email','')}")
    print(f"Idade: {jogadora.get('idade',0)}")
    print(f"Posição: {jogadora.get('posicao','')}")
    print(f"Sub: {jogadora.get('sub',0)}")
    print(f"Highlights: {jogadora.get('highlights','')}")
    print(f"Rede social: {jogadora.get('redeSocial','')}")
    print(f"Biografia: {jogadora.get('biografia','')}")
    print(f"Pontos: {jogadora.get('pontos', 0)}")

    try:
        opcao = int(input('\nDigite:\n 1 - Editar Perfil\n 2 - Voltar\n\nEscolha: '))
        
        if opcao == 1:
            editaJogadora(jogadora)
        elif opcao == 2:
            mainJogadora(jogadora)
        else:
            print(" Opção inválida!")
            input("Pressione Enter...")
            verPerfil(jogadora)
    except ValueError:
        print(" Digite um número válido!")
        input("Pressione Enter...")
        verPerfil(jogadora)
    
def editaJogadora(jogadora):
    os.system("cls")
    print("\n=== EDITANDO PERFIL ===\n")
    
    try:
        jogadora["nome"] = input("Nome completo: ")
        
        email = None
        while email is None:
            email_input = input("E-mail: ")
            email = app.valida_email(email_input)
            if email is None:
                print("Tente novamente.\n")
        jogadora["email"] = email
        
        jogadora["senha"] = input("Senha: ")
        
        while True:
            try:
                idade = int(input("Idade (apenas números): "))
                if idade < 0 or idade > 120:
                    print(" Idade inválida! Digite um valor entre 0 e 120.")
                    continue
                jogadora["idade"] = idade
                break
            except ValueError:
                print(" Digite um número válido!")
        
        jogadora["posicao"] = input("Posição que joga: ")
        
        while True:
            try:
                sub = int(input("Sub que joga (exemplo: 17, 20): "))
                jogadora["sub"] = sub
                break
            except ValueError:
                print(" Digite um número válido!")
        
        jogadora["highlights"] = input("Highlights (link do vídeo no YouTube): ")
        jogadora["redeSocial"] = input("Rede social (link): ")
        jogadora["biografia"] = input("Sobre você (conte-nos quem você é): ")

        salvarAlteracoes(app.jogadoras)

        print("\n Perfil atualizado com sucesso!")
        input("Pressione Enter para voltar...")
        mainJogadora(jogadora)
        
    except Exception as e:
        print(f" Erro ao atualizar perfil: {e}")
        input("Pressione Enter para tentar novamente...")
        editaJogadora(jogadora)

def verTimeline(jogadora):
    os.system("cls")
    app.mostraLetreiro()
    timeline = carregarTimeline()
    eventos = timeline.get(jogadora.get("email",""), [])

    print("\n--- Timeline da Carreira ---\n")
    if eventos:
        for ev in eventos:
            print(f"[{ev['data']}] {ev['mensagem']}")
    else:
        print("Nenhum evento registrado ainda.")

    input("\nPressione Enter para voltar.")
    mainJogadora(jogadora)

# ----------------------------
# Notificações
# ----------------------------
def notificacoes(jogadora):
    os.system("cls")
    app.mostraLetreiro()

    notificacoes = carregarNotificacoes()
    mensagens = notificacoes.get(jogadora.get("email",""), [])

    print("\n--- Notificações ---")
    if mensagens:
        for i, msg in enumerate(mensagens, start=1):
            print(f"{i}. {msg}")
    else:
        print("Nenhuma notificação no momento.")

    input("\nPressione Enter para voltar.")
    mainJogadora(jogadora)

# ----------------------------
# Gerenciamento de Times
# ----------------------------

def gerenciarTime(jogadora):
    os.system("cls")
    app.mostraLetreiro()
    
    times = carregarTimes()
    email = jogadora.get("email")

    meu_time = next((t for t in times if email in t.get("jogadoras", [])), None)

    if meu_time:
        print(f"\n=== MEU TIME: {meu_time['nome']} ===")
        print("\nIntegrantes:")
        for j in meu_time.get("jogadoras"):
            print(f"  • {j}")
        
        convites = meu_time.get("convites")
        if convites:
            print("\nConvites pendentes:")
            for c in convites:
                print(f"  • {c}")
        else:
            print("\n✓ Nenhum convite pendente.")

        if jogadora["email"] == meu_time.get("criadora"):
            print("\nVOCÊ É O(A) CAPITÃO(Ã) DESTE TIME")
            print("\nOpções:")
            print("1 - Convidar jogadora")
            print("2 - Sair do time")
            print("3 - Inscrever em campeonato")
            print("4 - Voltar")
            
            try:
                opcao = int(input("\nEscolha: "))
                if opcao == 1:
                    convidarJogadora(jogadora, meu_time)
                elif opcao == 2:
                    sairDoTime(jogadora, meu_time)
                elif opcao == 3:
                    inscreverEmCampeonato(jogadora, meu_time)
                elif opcao == 4:
                    mainJogadora(jogadora)
                else:
                    print(" Opção inválida!")
                    input("Pressione Enter...")
                    gerenciarTime(jogadora)
            except ValueError:
                print(" Digite um número válido!")
                input("Pressione Enter...")
                gerenciarTime(jogadora)
        else:
            print("\nOpções:")
            print("1 - Sair do time")
            print("2 - Voltar")
            
            try:
                opcao = int(input("\nEscolha: "))
                if opcao == 1:
                    sairDoTime(jogadora, meu_time)
                elif opcao == 2:
                    mainJogadora(jogadora)
                else:
                    print(" Opção inválida!")
                    input("Pressione Enter...")
                    gerenciarTime(jogadora)
            except ValueError:
                print(" Digite um número válido!")
                input("Pressione Enter...")
                gerenciarTime(jogadora)
    else:
        print("\n Você não participa de nenhum time.")
        print("\nOpções:")
        print("1 - Criar time")
        print("2 - Ver convites recebidos")
        print("3 - Voltar")
        
        try:
            opcao = int(input("\nEscolha: "))
            if opcao == 1:
                criarTime(jogadora)
            elif opcao == 2:
                verConvites(jogadora)
            elif opcao == 3:
                mainJogadora(jogadora)
            else:
                print(" Opção inválida!")
                input("Pressione Enter...")
                gerenciarTime(jogadora)
        except ValueError:
            print(" Digite um número válido!")
            input("Pressione Enter...")
            gerenciarTime(jogadora)

def criarTime(jogadora):
    os.system("cls")
    print("--- Criar Novo Time ---\n")
    
    times = carregarTimes()
    nome = input("Nome do time: ")
    
    novo_time = {
        "nome": nome,
        "criadora": jogadora["email"],
        "jogadoras": [jogadora["email"]],
        "convites": []
    }
    
    times.append(novo_time)
    salvarTimes(times)
    
    adicionarEvento(jogadora["email"], f"Criou o time '{nome}'")
    
    input(f"\nTime '{nome}' criado com sucesso!\nVocê é o(a) capitão(ã) do time.\nPressione Enter.")
    gerenciarTime(jogadora)

def convidarJogadora(jogadora, time):
    os.system("cls")
    print(f"--- Convidar Jogadora para {time['nome']} ---\n")
    
    if len(time.get("jogadoras", [])) >= 12:
        input("Time já tem 12 jogadoras (limite máximo)! Pressione Enter.")
        return gerenciarTime(jogadora)

    email = input("Digite o email da jogadora a convidar: ")
    
    if not email:
        print('Aperte\n1 - Tentar novamente\n2 - Voltar ao menu\n')
        opcao = app.validaEntrada("Opção: ", int, [1,2])
        return convidarJogadora(jogadora, time) if opcao == 1 else gerenciarTime(jogadora)
    
    jogadora_existe = any(j.get("email") == email and j.get("tipoDeUsuario") == 1 
                         for j in app.jogadoras)
    
    if not jogadora_existe:
        input("Jogadora não encontrada no sistema! Pressione Enter.")
        return convidarJogadora(jogadora, time)
    
    if email in time.get("jogadoras", []):
        input("Esta jogadora já faz parte do time! Pressione Enter.")
        return convidarJogadora(jogadora, time)
    
    if email in time.get("convites", []):
        input("Esta jogadora já foi convidada! Pressione Enter.")
        return convidarJogadora(jogadora, time)
    
    times = carregarTimes()
    ja_tem_time = any(email in t.get("jogadoras", []) for t in times)
    
    if ja_tem_time:
        input("Esta jogadora já participa de outro time! Pressione Enter.")
        return convidarJogadora(jogadora, time)
    
    if "convites" not in time:
        time["convites"] = []
    
    time["convites"].append(email)
    
    for i, t in enumerate(times):
        if t["nome"] == time["nome"]:
            times[i] = time
            break
    
    salvarTimes(times)
    
    adicionarNotificacao(email, f"Você recebeu um convite para entrar no time '{time['nome']}'")
    adicionarEvento(jogadora["email"], f"Convidou jogadora para o time {time['nome']}")
    
    input(f"Convite enviado para {email}! Pressione Enter.")
    gerenciarTime(jogadora)

def sairDoTime(jogadora, time):
    os.system("cls")
    print(f"--- Sair do Time: {time['nome']} ---\n")
    
    confirmacao = app.validaEntrada(
        "Tem certeza que deseja sair do time?\n1 - Sim\n2 - Não\n", 
        int, [1, 2]
    )
    
    if confirmacao == 1:
        times = carregarTimes()
        
        for i, t in enumerate(times):
            if t["nome"] == time["nome"]:
                if jogadora["email"] in t["jogadoras"]:
                    t["jogadoras"].remove(jogadora["email"])
                
                if t["criadora"] == jogadora["email"] and t["jogadoras"]:
                    nova_criadora = t["jogadoras"][0]
                    t["criadora"] = nova_criadora
                    adicionarNotificacao(nova_criadora, 
                        f"Você agora é o(a) capitão(ã) do time '{t['nome']}'")
                    print(f"Liderança transferida para: {nova_criadora}")
                    adicionarEvento(jogadora["email"], f"Transferiu a liderança do time {time['nome']}")
                
                elif not t["jogadoras"]:
                    times.pop(i)
                    print(f"Time '{time['nome']}' foi dissolvido (sem membros).")
                
                break
        
        salvarTimes(times)
        adicionarEvento(jogadora["email"], f"Saiu do time {time['nome']}")
        input("Você saiu do time. Pressione Enter.")
    else:
        input("Operação cancelada. Pressione Enter.")
    
    mainJogadora(jogadora)

def verConvites(jogadora):
    os.system("cls")
    print("--- Convites Recebidos ---\n")
    
    times = carregarTimes()
    convites = [t for t in times if jogadora["email"] in t.get("convites", [])]
    
    if not convites:
        input("Nenhum convite recebido. Pressione Enter.")
        return gerenciarTime(jogadora)

    for i, t in enumerate(convites, start=1):
        criadora = t.get("criadora", "N/A")
        qtd_jogadoras = len(t.get("jogadoras", []))
        print(f"{i} - {t['nome']} (Capitã: {criadora}) - {qtd_jogadoras}/12 jogadoras")

    escolha = int(input("\nEscolha um convite para responder (0 para voltar): "))
    
    if escolha == 0:
        return gerenciarTime(jogadora)
    
    time_escolhido = convites[escolha-1]
    responderConvite(jogadora, time_escolhido)

def responderConvite(jogadora, time):
    os.system("cls")
    print(f"--- Convite do Time: {time['nome']} ---")
    print(f"Capitã: {time.get('criadora', 'N/A')}")
    print(f"Jogadoras: {len(time.get('jogadoras', []))}/12")
    print("\n1 - Aceitar convite\n2 - Recusar convite\n3 - Voltar")
    
    resp = int(input("Escolha: "))
    
    if resp == 3:
        return verConvites(jogadora)

    times = carregarTimes()
    
    for i, t in enumerate(times):
        if t["nome"] == time["nome"]:
            if resp == 1:
                if len(t.get("jogadoras", [])) >= 12:
                    input("Time já está completo (12/12)! Pressione Enter.")
                    return verConvites(jogadora)
                
                t["jogadoras"].append(jogadora["email"])
                t["convites"].remove(jogadora["email"])
                
                adicionarNotificacao(t["criadora"], 
                    f"{jogadora['nome']} aceitou o convite do time '{t['nome']}'")
                
                adicionarEvento(jogadora["email"], f"Entrou no time {t['nome']}")
                
                input(f"Você entrou no time '{t['nome']}'! Pressione Enter.")
                
            elif resp == 2:
                t["convites"].remove(jogadora["email"])
                
                adicionarNotificacao(t["criadora"], 
                    f"{jogadora['nome']} recusou o convite do time '{t['nome']}'")
                
                input("Convite recusado. Pressione Enter.")
            
            times[i] = t
            break
    
    salvarTimes(times)
    gerenciarTime(jogadora)

def inscreverEmCampeonato(jogadora, time):
    os.system("cls")
    app.mostraLetreiro()
    
    try:
        campeonatos = carregarCampeonatos()
        
        time_ja_inscrito = [
            c["nomeCampeonato"] 
            for c in campeonatos 
            if time["nome"] in c.get("timesInscritos", []) or time["nome"] in c.get("timesAprovados", [])
        ]
        if time_ja_inscrito:
            print(f"\nSeu time '{time['nome']}' já está inscrito no campeonato: {time_ja_inscrito[0]}.")
            input("Pressione Enter para voltar...")
            return gerenciarTime(jogadora)
            
        campeonatos_disponiveis = [
            camp for camp in campeonatos 
            if (
                len(camp.get("timesInscritos", [])) < camp.get("numTimes", 0) and
                time["nome"] not in camp.get("timesInscritos", []) and
                time["nome"] not in camp.get("timesAprovados", [])
            )
        ]
        
        if not campeonatos_disponiveis:
            print("\n Não há campeonatos disponíveis para inscrição no momento.")
            input("Pressione Enter para voltar...")
            return gerenciarTime(jogadora)

        print(" === CAMPEONATOS DISPONÍVEIS ===\n")
        for i, camp in enumerate(campeonatos_disponiveis, start=1):
            vagas_restantes = camp.get("numTimes", 0) - len(camp.get("timesInscritos", []))
            print(f"{i}. {camp['nomeCampeonato']}")
            print(f"   📍 Local: {camp['local']}")
            print(f"   📅 Data: {camp['dataHora']}")
            print(f"   👥 Vagas: {vagas_restantes}/{camp.get('numTimes',0)}")
            print(f"   ⚽ Jogadoras por time: {camp.get('numJogadorasPorTime',0)}")
            print(f"   📋 Requisitos: {camp['requisitos']}")
            print("-" * 60)
        
        while True:
            try:
                escolha = int(input("\nEscolha um campeonato (0 para voltar): "))
                
                if escolha == 0:
                    return gerenciarTime(jogadora)
                
                if escolha < 1 or escolha > len(campeonatos_disponiveis):
                    print(f" Escolha um número entre 1 e {len(campeonatos_disponiveis)}!")
                    continue
                
                break
            except ValueError:
                print(" Digite um número válido!")
        
        campeonato_escolhido = campeonatos_disponiveis[escolha-1]
        
        if len(time.get("jogadoras", [])) < campeonato_escolhido.get("numJogadorasPorTime", 0):
            print(f"\n Seu time precisa de no mínimo {campeonato_escolhido['numJogadorasPorTime']} jogadoras!")
            print(f"   Você tem apenas {len(time.get('jogadoras', []))} jogadora(s).")
            input("Pressione Enter para voltar...")
            return gerenciarTime(jogadora)

        for camp in campeonatos:
            if camp["nomeCampeonato"] == campeonato_escolhido["nomeCampeonato"]:
                camp["timesInscritos"].append(time["nome"])
                salvarCampeonatos(campeonatos)
                
                adicionarEvento(
                    jogadora["email"], 
                    f"Time '{time['nome']}' inscrito no '{camp['nomeCampeonato']}'"
                )
                
                jogadora["pontos"] = jogadora.get("pontos", 0) + 10
                salvarAlteracoes(app.jogadoras)
                
                print(f"\ Time '{time['nome']}' inscrito com sucesso!")
                print(f"   Campeonato: {campeonato_escolhido['nomeCampeonato']}")
                print(f"   +10 pontos para você!")
                input("\nAguarde a aprovação pelo admin.\nPressione Enter...")
                return gerenciarTime(jogadora)
                
    except Exception as e:
        print(f" Erro ao inscrever time: {e}")
        input("Pressione Enter para voltar...")
        gerenciarTime(jogadora)
# ----------------------------
# Fluxo do menu
# ----------------------------

def mainJogadora(jogadora):
    os.system("cls")
    app.mostraLetreiro()
    escolhaMenuJogadora(jogadora)