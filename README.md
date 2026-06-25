# EduTrack IA

Plataforma acadêmica para organizar disciplinas, tarefas, notas e rotina de estudos, com painel visual e backend gerenciado no Xano.

## O que é

O **EduTrack IA** é uma aplicação web construída em **Streamlit** que centraliza a vida acadêmica do estudante em um único painel. O frontend em Python consome APIs REST do **Xano**, onde ficam autenticação, persistência de dados e regras de negócio definidas em XanoScript.

A interface adota identidade visual em tons de azul e galáxia na autenticação, com temas configuráveis no painel interno.

## Objetivo

Oferecer ao estudante uma visão clara do semestre: acompanhar entregas, notas, professores e desempenho, com apoio de relatórios e de um assistente de estudos, reduzindo a fragmentação entre planilhas, calendários e anotações soltas.

## Público-alvo

- Estudantes universitários e de ensino técnico que precisam organizar múltiplas disciplinas
- Quem busca um painel único para tarefas, notas e calendário acadêmico
- Desenvolvedores que trabalham com o ecossistema Xano e desejam um frontend Streamlit integrado

## Principais funcionalidades

| Módulo | Descrição |
|--------|-----------|
| **Autenticação** | Login e cadastro via Xano (`/auth/login`, `/auth/signup`), sessão JWT no Streamlit |
| **Dashboard** | Resumo de disciplinas, tarefas, média geral, recomendações e exportação de PDF |
| **Disciplinas** | CRUD completo de matérias vinculadas ao usuário |
| **Tarefas** | CRUD de atividades com status, datas e vínculo com disciplinas |
| **Notas** | Registro e edição de avaliações por disciplina |
| **Calendário** | Visão mensal agregando tarefas e notas; fallback local quando `/calendario` não existe no Xano |
| **Professores** | Cadastro e listagem de contatos docentes |
| **Perfil** | Dados acadêmicos estendidos (nome, curso, semestre etc.) |
| **Assistente IA (Luna)** | Interface de chat com respostas locais de demonstração |
| **Configurações** | Conta, temas de cores e placeholders para integrações Google |

### Backend Xano (XanoScript)

O repositório inclui definições sincronizadas com o workspace Xano:

- **APIs:** grupo `authentication` (auth, CRUD de entidades) e `event_logs`
- **Tabelas:** `user`, `disciplinas`, `tarefas`, `notas`, `professores`, `perfil`, `event_log`
- **Funções:** `log_event`, `generate_magic_link`, `enforce_role`
- **Reset de senha:** endpoints de magic link no backend (sem fluxo completo na UI Streamlit)

## Tecnologias utilizadas

| Camada | Tecnologia |
|--------|------------|
| Frontend | Python 3, Streamlit |
| Backend | Xano (BaaS) + XanoScript (`.xs`) |
| HTTP | `requests` |
| Dados / gráficos | `pandas`, `plotly` |
| Relatórios | `reportlab` |
| Sincronização Xano | extensão `.xano/` (workspace `v1`) |

## Estrutura do projeto

```
EduTrack-IA/
├── app.py                 # Entrada Streamlit e roteamento de páginas
├── requirements.txt
├── pages/                 # Telas: dashboard, disciplinas, tarefas, etc.
├── components/            # Login, sidebar, cards e formulários
├── services/              # Cliente Xano, PDF, stubs Google
├── utils/                 # Sessão, estilos, temas, erros, desempenho
├── assets/images/         # Imagens da interface (ex.: login-cosmos.png)
├── apis/                  # Endpoints XanoScript
├── tables/                # Schemas XanoScript
├── functions/             # Funções XanoScript
├── docs/                  # Guias de desenvolvimento XanoScript
└── .xano/                 # Configuração de sync com o workspace Xano
```

## Requisitos

- Python 3.10 ou superior
- Conta e workspace Xano configurados (instância já referenciada no projeto)
- Conexão com a internet para comunicação com a API Xano

## Como executar localmente

```powershell
# 1. Clonar o repositório
git clone https://github.com/feitosaM4/EduTrack-IA.git
cd EduTrack-IA

# 2. Criar e ativar ambiente virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Instalar dependências
pip install -r requirements.txt

# 4. (Opcional) Configurar variáveis de ambiente
copy .env.example .env

# 5. Iniciar a aplicação
streamlit run app.py
```

A aplicação abre no navegador (porta padrão `8501`). Na primeira execução, use **Criar minha conta** ou faça login com credenciais já cadastradas no Xano.

## Como configurar

### API Xano

A URL base da API pode ser definida pela variável de ambiente `XANO_API_URL`. O valor padrão está em `services/xano_api.py` e no arquivo `.env.example`:

```
XANO_API_URL=https://x8ki-letl-twmt.n7.xano.io/api:HRRA97nd
```

### Sincronização do backend

As definições em `apis/`, `tables/` e `functions/` são sincronizadas com o workspace Xano via extensão Xano (config em `.xano/config.json`). Após alterar XanoScript localmente, publique as mudanças no workspace antes de testar no frontend.

### Imagem de login

O arquivo `assets/images/login-cosmos.png` compõe o planeta decorativo da tela de autenticação. Sem ele, o fundo em gradiente galáxia continua funcionando normalmente.

### Streamlit

Configurações em `.streamlit/config.toml` (navegação lateral automática desabilitada — o app usa roteamento próprio).

## Status atual do projeto

**Em desenvolvimento ativo.** O núcleo acadêmico (auth, disciplinas, tarefas, notas, professores, perfil e dashboard) está integrado ao Xano e operacional no Streamlit. Integrações externas (Google Calendar, Google Drive, OAuth Google), assistente IA real e calendário dedicado no backend ainda estão parciais ou em stub.

---

## Melhorias em andamento

Com base no código e na estrutura atual do repositório:

1. **Endpoint `/calendario` no Xano** — `services/xano_api.py` contém TODOs explícitos; hoje o calendário agrega tarefas e notas e usa fallback quando a API retorna 404.

2. **Endpoint `/estudo-semanal`** — função `listar_estudo_semanal()` existe no cliente Xano, mas não há endpoint correspondente nem uso nas páginas.

3. **Assistente IA (Luna)** — `pages/assistente.py` responde com texto fixo; o agente de exemplo em `agents/` não está conectado ao Streamlit.

4. **Login com Google** — botão presente na tela de login sem fluxo OAuth implementado.

5. **Integrações Google** — `services/google_calendar.py` e `services/google_drive.py` são stubs; a página Configurações exibe mensagem "em breve".

6. **Recuperação de senha na UI** — backend com magic link (`reset/request-reset-link`) existe no Xano; o Streamlit ainda não oferece fluxo completo de redefinição.

7. **Checkbox "Lembrar de mim"** — exibido na tela de login sem persistência de sessão.

8. **Tabela `subjects`** — definida em `tables/839564_subjects.xs` sem API ou uso no app (o CRUD ativo usa `disciplinas`).

9. **Tarefas agendadas Xano** — pasta `tasks/` contém apenas documentação; nenhuma automação `.xs` implementada.

10. **Configuração por ambiente** — suporte inicial a `XANO_API_URL` via `.env`; demais segredos e URLs ainda podem ser centralizados conforme o projeto crescer.

11. **Asset `login-cosmos.png`** — presente em `assets/images/`; ajustes finos de posicionamento podem ser feitos conforme resolução.

## Licença

Consulte o proprietário do repositório para termos de uso e distribuição.
