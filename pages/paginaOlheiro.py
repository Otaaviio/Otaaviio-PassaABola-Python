import os
import app
import pages.paginaJogadora as paginaJogadora

# ----------------------------
# Utilitários
# ----------------------------
def salvarAlteracoes():
    app.salvar_jogadoras(app.jogadoras)

def opcaoInvalida(olheiro):
    input("Opção inválida\nPressione 'Enter' para voltar\n")
    menuOlheiro(olheiro)

# ----------------------------
# Menu Olheiro
# ----------------------------
def menuOlheiro(olheiro):
    os.system("cls")
    app.mostraLetreiro()
    print('''\n--- Menu Olheiro ---
          
1 - Buscar/Filtrar jogadoras
2 - Sair\n''')

    opcao = int(input("Escolha uma opção: "))
    if opcao == 1:
        buscarJogadoras(olheiro)
    elif opcao == 2:
        app.main()

# ----------------------------
# Busca Avançada de Jogadoras
# ----------------------------
def buscarJogadoras(olheiro):
    os.system("cls")
    app.mostraLetreiro()
    print("\n--- Buscar Jogadoras (Filtros Avançados) ---\n")

    jogadoras = [j for j in app.jogadoras if j.get("tipoDeUsuario") == 1]

    if not jogadoras:
        input("Nenhuma jogadora cadastrada.\nPressione Enter para voltar.")
        return menuOlheiro(olheiro)

    nome_filtro = input("Filtrar por nome (Enter para ignorar): ").lower()
    posicao_filtro = input("Filtrar por posição (Enter para ignorar): ").lower()
    idade_min = input("Idade mínima (Enter para ignorar): ")
    idade_max = input("Idade máxima (Enter para ignorar): ")
    sub_filtro = input("Filtrar por Sub (Enter para ignorar): ")

    filtradas = []
    for j in jogadoras:
        nome_ok = nome_filtro in j.get("nome", "").lower() if nome_filtro else True
        posicao_ok = posicao_filtro in j.get("posicao", "").lower() if posicao_filtro else True
        idade = j.get("idade", 0)
        idade_ok = True
        if idade_min.isdigit() and idade < int(idade_min):
            idade_ok = False
        if idade_max.isdigit() and idade > int(idade_max):
            idade_ok = False
        sub_ok = str(j.get("sub", "")) == sub_filtro if sub_filtro else True

        if nome_ok and posicao_ok and idade_ok and sub_ok:
            filtradas.append(j)

    if not filtradas:
        input("\nNenhuma jogadora encontrada com os filtros.\nPressione Enter para voltar.")
        return menuOlheiro(olheiro)

    print("\n--- Jogadoras Encontradas ---\n")
    for i, j in enumerate(filtradas, start=1):
        print(f"{i} - {j.get('nome','')} | {j.get('posicao','')} | {j.get('idade',0)} anos | Sub-{j.get('sub','')}")

    escolha = int(input("\nDigite o número da jogadora para abrir (0 para voltar): "))
    if escolha == 0:
        return menuOlheiro(olheiro)
    if escolha < 1 or escolha > len(filtradas):
        input("Escolha inválida. Pressione Enter para voltar.")
        return buscarJogadoras(olheiro)

    jogadora = filtradas[escolha - 1]
    mostrarPerfilParaOlheiro(olheiro, jogadora)

# ----------------------------
# Perfil da Jogadora (já existente)
# ----------------------------
def mostrarPerfilParaOlheiro(olheiro, jogadora):
    os.system("cls")
    print(f"\n--- Perfil: {jogadora.get('nome','')} ---")
    print(f"E-mail: {jogadora.get('email','')}")
    print(f"Idade: {jogadora.get('idade',0)}")
    print(f"Posição: {jogadora.get('posicao','')}")
    print(f"Sub: {jogadora.get('sub','')}")
    print(f"Highlights: {jogadora.get('highlights','')}")
    print(f"Pontos: {jogadora.get('pontos',0)}")

    avaliacoes = jogadora.get("avaliacoes", [])
    if avaliacoes:
        qtd = len(avaliacoes)
        media = sum(a.get("nota",0) for a in avaliacoes) / qtd
        print(f"\n📊 Avaliações recebidas: {qtd}")
        print(f"⭐ Média de notas: {media:.1f} / 5")
        print("\nÚltimas avaliações:")
        for a in avaliacoes[-3:]:
            print(f"- {a.get('olheiro')} | Nota: {a.get('nota')} | {a.get('comentario')}")
    else:
        print("\nNenhuma avaliação recebida ainda.")

    print('''\nOpções:
1 - Avaliar jogadora
2 - Enviar notificação
3 - Voltar\n''')

    opcao = int(input("Escolha uma opção: "))
    if opcao == 1:
        realizarAvaliacao(olheiro, jogadora)
    elif opcao == 2:
        enviarNotificacao(olheiro, jogadora)
    elif opcao == 3:
        return buscarJogadoras(olheiro)


def realizarAvaliacao(olheiro, jogadora):
    print("\n--- Avaliar Jogadora ---")
    nota = int(input("Digite a nota (1 a 5): "))
    comentario = input("Digite um comentário (opcional): ")

    if "avaliacoes" not in jogadora:
        jogadora["avaliacoes"] = []

    avaliacao = {
        "olheiro": olheiro.get("nome",""),
        "nota": nota,
        "comentario": comentario
    }
    jogadora["avaliacoes"].append(avaliacao)
    salvarAlteracoes()

    app.adicionarEvento(jogadora.get("email",""), f"⭐ Avaliação recebida do Olheiro {olheiro.get('nome')} - Nota {nota}")

    input("\nAvaliação registrada com sucesso! Pressione Enter para voltar ao perfil.")
    mostrarPerfilParaOlheiro(olheiro, jogadora)


def enviarNotificacao(olheiro, jogadora):
    print("\n--- Enviar Notificação ---")
    mensagem = input("Digite a mensagem da notificação: ")
    paginaJogadora.adicionarNotificacao(jogadora.get("email",""), f"[Olheiro {olheiro.get('nome','')} {olheiro.get('email','')}] {mensagem}")
    input("\nNotificação enviada com sucesso! Pressione Enter para voltar ao perfil.")
    mostrarPerfilParaOlheiro(olheiro, jogadora)