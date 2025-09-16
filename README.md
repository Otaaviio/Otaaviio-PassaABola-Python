# ⚽ PassaABola - Sistema de Gestão de Jogadoras de Futebol Feminino

![Python](https://img.shields.io/badge/python-3.x-blue?logo=python)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![License](https://img.shields.io/badge/license-MIT-green)
![Contributors](https://img.shields.io/badge/contributors-5-brightgreen)

## 📌 Sobre o Projeto

O **PassaABola** é uma aplicação desenvolvida pela equipe **GoalBreakers** 
em **Python** para gerenciar e conectar **jogadoras de
futebol feminino**, **olheiras** e **administradoras**.

O sistema facilita a organização de **times**, **campeonatos** e promove
o **desenvolvimento profissional** das atletas, oferecendo
**oportunidades de visibilidade e crescimento no esporte**.

------------------------------------------------------------------------

## 🚀 Funcionalidades

### 👤 Sistema de Usuários

-   **Cadastro e Login**: Jogadoras, olheiras e administradoras
-   **Autenticação**: Login seguro com validação de credenciais

### 🏃 Perfil da Jogadora

-   Edição de informações pessoais (posição, idade, highlights, redes
    sociais)
-   Biografia para apresentação pessoal
-   Sistema de pontos baseado em participações e conquistas

### 🏟️ Gerenciamento de Times

-   Criação de times por jogadoras
-   Sistema de convites para ingressar em times
-   Gestão de membros pelo(a) capitão(ã)
-   Limite de **12 jogadoras por time**

### 🏆 Campeonatos

-   Criação de campeonatos por administradoras
-   Inscrição de times em campeonatos
-   Aprovação de inscrições pelas administradoras
-   Definição de requisitos de participação

### 🔔 Notificações

-   Mensagens individuais entre usuários
-   Mensagens globais enviadas pelas administradoras
-   **Timeline**: registro cronológico de eventos importantes

### ⭐ Avaliações

-   Olheiras podem avaliar jogadoras com **notas e comentários**
-   Feedback construtivo para auxiliar no desenvolvimento das atletas

------------------------------------------------------------------------

## 🌟 Features Principais

-   **3 tipos de usuários**: Jogadoras, Olheiras e Administradoras\
-   **Persistência de dados** em arquivos JSON\
-   **Interface via console** com menus intuitivos\
-   **Timeline automática** de eventos importantes\
-   **Validação de dados** para manter integridade das informações\
-   **Sistema de pontos e recompensas**\
-   **Gestão de convites e aprovações** em times e campeonatos

------------------------------------------------------------------------

## 🛠️ Tecnologias Utilizadas

-   **Python 3.x** -- linguagem principal\
-   **JSON** -- armazenamento de dados\
-   **OS Module** -- interação com o sistema operacional\
-   **Datetime** -- manipulação de datas e horários

------------------------------------------------------------------------

## ▶️ Como Executar

1.  Certifique-se de ter **Python 3.x** instalado\

2.  Execute o arquivo principal:

    ``` bash
    python app.py
    ```

3.  Siga as instruções no menu para login ou cadastro

------------------------------------------------------------------------

## 📂 Estrutura do Projeto

    📦 PassaABola
     ┣ 📜 app.py                  # Arquivo principal da aplicação
     ┣ 📂 pages/                  # Módulos de cada tipo de usuário
     ┃ ┣ 📜 paginaJogadora.py     # Funcionalidades da jogadora
     ┃ ┣ 📜 paginaOlheiro.py      # Funcionalidades da olheira
     ┃ ┗ 📜 paginaAdmin.py        # Funcionalidades da administradora
     ┣ 📂 json/                   # Arquivos de dados
     ┃ ┣ 📜 jogadoras.json        # Dados das jogadoras
     ┃ ┣ 📜 times.json            # Dados dos times
     ┃ ┣ 📜 campeonatos.json      # Dados dos campeonatos
     ┃ ┣ 📜 notificacoes.json     # Notificações dos usuários
     ┃ ┗ 📜 timeline.json         # Timeline das jogadoras

------------------------------------------------------------------------

## 👥 Equipe Goal Breakers

-   **Laura Tigre**\
-   **Áurea Sardinha**\
-   **Eduardo Ulisses**\
-   **Henrique Guedes**\
-   **Otávio Inaba**

------------------------------------------------------------------------

💡 Projeto acadêmico desenvolvido com foco em **organização esportiva e
inclusão digital** no futebol feminino.
