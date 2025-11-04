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
    print('''\n=== MENU OLHEIRO ===
          
1 - Buscar/Filtrar jogadoras
2 - Sair\n''')

    try:
        opcao = int(input("Escolha uma opção: "))
        
        if opcao == 1:
            buscarJogadoras(olheiro)
        elif opcao == 2:
            app.main()
        else:
            print("Opção inválida!")
            input("Pressione Enter...")
            menuOlheiro(olheiro)
    except ValueError:
        print("Digite um número válido!")
        input("Pressione Enter...")
        menuOlheiro(olheiro)
    except Exception as e:
        print(f"Erro: {e}")
        input("Pressione Enter...")
        menuOlheiro(olheiro)

# ----------------------------
# Busca Avançada de Jogadoras
# ----------------------------
def buscarJogadoras(olheiro):
    os.system("cls")
    app.mostraLetreiro()
    print("\n=== BUSCAR JOGADORAS (Filtros) ===\n")

    jogadoras = [j for j in app.jogadoras if j.get("tipoDeUsuario") == 1]

    if not jogadoras:
        print("❌ Nenhuma jogadora cadastrada.")
        input("Pressione Enter para voltar...")
        return menuOlheiro(olheiro)

    try:
        # Filtros
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
            
            if idade_min:
                try:
                    if idade < int(idade_min):
                        idade_ok = False
                except ValueError:
                    print("Idade mínima inválida, ignorando filtro.")
            
            # Validação de idade máxima
            if idade_max:
                try:
                    if idade > int(idade_max):
                        idade_ok = False
                except ValueError:
                    print("Idade máxima inválida, ignorando filtro.")
            
            sub_ok = str(j.get("sub", "")) == sub_filtro if sub_filtro else True

            if nome_ok and posicao_ok and idade_ok and sub_ok:
                filtradas.append(j)

        if not filtradas:
            print("\nNenhuma jogadora encontrada com os filtros.")
            input("Pressione Enter para voltar...")
            return menuOlheiro(olheiro)

        print("\n=== JOGADORAS ENCONTRADAS ===\n")
        for i, j in enumerate(filtradas, start=1):
            print(f"{i}. {j.get('nome','')} | {j.get('posicao','')} | {j.get('idade',0)} anos | Sub-{j.get('sub','')}")

        while True:
            try:
                escolha = int(input("\nDigite o número da jogadora (0 para voltar): "))
                
                if escolha == 0:
                    return menuOlheiro(olheiro)
                
                if escolha < 1 or escolha > len(filtradas):
                    print(f"Escolha entre 1 e {len(filtradas)}!")
                    continue
                
                jogadora = filtradas[escolha - 1]
                mostrarPerfilParaOlheiro(olheiro, jogadora)
                break
            except ValueError:
                print("Digite um número válido!")
                
    except Exception as e:
        print(f"Erro ao buscar jogadoras: {e}")
        input("Pressione Enter...")
        menuOlheiro(olheiro)

# ----------------------------
# Perfil da Jogadora (já existente)
# ----------------------------
def mostrarPerfilParaOlheiro(olheiro, jogadora):
    os.system("cls")
    print(f"\n=== PERFIL: {jogadora.get('nome','')} ===\n")
    print(f"E-mail: {jogadora.get('email','')}")
    print(f"Idade: {jogadora.get('idade',0)} anos")
    print(f"Posição: {jogadora.get('posicao','')}")
    print(f"Sub: {jogadora.get('sub','')}")
    print(f"Highlights: {jogadora.get('highlights','')}")
    print(f"Pontos: {jogadora.get('pontos',0)}")
    print(f"Biografia: {jogadora.get('biografia','')}")

    # Avaliações
    avaliacoes = jogadora.get("avaliacoes", [])
    if avaliacoes:
        qtd = len(avaliacoes)
        media = sum(a.get("nota",0) for a in avaliacoes) / qtd
        print(f"\n📊 Avaliações recebidas: {qtd}")
        print(f"⭐ Média de notas: {media:.1f} / 5")
        print("\nÚltimas avaliações:")
        for a in avaliacoes[-3:]:
            print(f"  • {a.get('olheiro')} | Nota: {a.get('nota')} | {a.get('comentario')}")
    else:
        print("\nNenhuma avaliação recebida ainda.")

    print('''\n=== OPÇÕES ===
1 - Avaliar jogadora
2 - Enviar notificação
3 - Voltar\n''')

    try:
        opcao = int(input("Escolha: "))
        
        if opcao == 1:
            realizarAvaliacao(olheiro, jogadora)
        elif opcao == 2:
            enviarNotificacao(olheiro, jogadora)
        elif opcao == 3:
            return buscarJogadoras(olheiro)
        else:
            print("Opção inválida!")
            input("Pressione Enter...")
            mostrarPerfilParaOlheiro(olheiro, jogadora)
    except ValueError:
        print("Digite um número válido!")
        input("Pressione Enter...")
        mostrarPerfilParaOlheiro(olheiro, jogadora)



def realizarAvaliacao(olheiro, jogadora):
    print("\n=== AVALIAR JOGADORA ===\n")
    
    try:
        while True:
            try:
                nota = int(input("Digite a nota (1 a 5): "))
                if nota < 1 or nota > 5:
                    print("A nota deve estar entre 1 e 5!")
                    continue
                break
            except ValueError:
                print("Digite um número válido!")
        
        comentario = input("Digite um comentário (opcional): ")

        if "avaliacoes" not in jogadora:
            jogadora["avaliacoes"] = []

        avaliacao = {
            "olheiro": olheiro.get("nome",""),
            "nota": nota,
            "comentario": comentario,
            "data": ""
        }
        jogadora["avaliacoes"].append(avaliacao)
        salvarAlteracoes()

        paginaJogadora.adicionarEvento(
            jogadora.get("email",""), 
            f"Avaliação recebida de {olheiro.get('nome')} - Nota {nota}"
        )

        print("\nAvaliação registrada com sucesso!")
        input("Pressione Enter para voltar ao perfil...")
        mostrarPerfilParaOlheiro(olheiro, jogadora)
        
    except Exception as e:
        print(f"Erro ao avaliar: {e}")
        input("Pressione Enter...")
        mostrarPerfilParaOlheiro(olheiro, jogadora)



def enviarNotificacao(olheiro, jogadora):
    print("\n=== ENVIAR NOTIFICAÇÃO ===\n")
    
    try:
        mensagem = input("Digite a mensagem: ")
        
        if not mensagem:
            print("Mensagem não pode ser vazia!")
            input("Pressione Enter...")
            return mostrarPerfilParaOlheiro(olheiro, jogadora)
        
        paginaJogadora.adicionarNotificacao(
            jogadora.get("email",""), 
            f"[Olheiro {olheiro.get('nome','')}] {mensagem}"
        )
        
        print("\nNotificação enviada com sucesso!")
        input("Pressione Enter para voltar ao perfil...")
        mostrarPerfilParaOlheiro(olheiro, jogadora)
        
    except Exception as e:
        print(f"Erro ao enviar notificação: {e}")
        input("Pressione Enter...")
        mostrarPerfilParaOlheiro(olheiro, jogadora)