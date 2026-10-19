<!--
===============================================================
Título: README - Seravitta
Descrição: Visão geral, instalação, configuração, testes, fluxo de
           trabalho e deploy da plataforma Seravitta
Autor: Will
Data: 19/10/2026
===============================================================
-->

<div align="center">
  <img src="backend/static/images/logo/seravitta-horizontal.svg" alt="Seravitta" width="320"/>

  <p><strong>Conexões para o seu bem-estar</strong></p>

  [![CI](https://github.com/willdev34/seravitta/actions/workflows/ci.yml/badge.svg?branch=develop)](https://github.com/willdev34/seravitta/actions/workflows/ci.yml)
  ![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
  ![Django](https://img.shields.io/badge/Django-4.2_LTS-green.svg)
  ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)
  ![Cobertura](https://img.shields.io/badge/cobertura_minima-80%25-brightgreen.svg)
</div>

---

## Índice

- [Sobre o projeto](#sobre-o-projeto)
- [O que já funciona](#o-que-já-funciona)
- [Perfis de usuário e planos](#perfis-de-usuário-e-planos)
- [Tecnologias](#tecnologias)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Rodando localmente](#rodando-localmente)
- [Variáveis de ambiente](#variáveis-de-ambiente)
- [Comandos úteis](#comandos-úteis)
- [Testes e qualidade](#testes-e-qualidade)
- [Fluxo de trabalho](#fluxo-de-trabalho)
- [Ambientes e deploy](#ambientes-e-deploy)
- [Identidade visual e layout](#identidade-visual-e-layout)
- [Roadmap](#roadmap)
- [Contato e licença](#contato-e-licença)

---

## Sobre o projeto

A Seravitta (antes chamada Espaço Vital) é uma plataforma web que conecta pessoas a terapeutas holísticos e a espaços terapêuticos verificados. Quem busca encontra profissionais e locais com filtros e perfis detalhados. Quem atende divulga o seu trabalho e, no caso dos espaços, aluga salas para outros terapeutas.

O código é um monólito Django com templates renderizados no servidor, pensado para ser leve e fácil de manter. O nome do pacote Python continua `espacovital` por enquanto, só a marca mudou.

Quem usa a plataforma:

- **Visitantes**: buscam terapeutas, espaços e terapias, leem perfis e entram em contato.
- **Terapeutas**: mantêm o perfil, recebem contatos e avaliações, reservam salas em espaços.
- **Donos de espaço**: cadastram o espaço, as salas e os horários, e vinculam terapeutas.
- **Equipe da plataforma**: modera cadastros, planos e vouchers pelo admin do Django.

---

## O que já funciona

**Busca e listagens**
- Busca de terapeutas com filtros de tipo de sessão, público atendido, especialidade, localização e acessibilidade.
- Busca de espaços com filtros de localização, terapia, acessibilidade, locação e disponibilidade (manhã, tarde, noite e finais de semana). A ordenação inclui a média de avaliações.
- Listagens simples de terapeutas e de espaços, listagem por região e página de terapias.
- Perfis públicos de terapeuta e de espaço, com galeria de fotos, avaliações e formulário de contato.

**Cadastro e conta**
- Cadastro e login com django-allauth, confirmação obrigatória de e-mail e recuperação de senha.
- Onboarding por perfil (terapeuta, espaço ou ambos), com escolha de plano e código de voucher opcional.

**Painéis**
- Painel do terapeuta: perfil, estatísticas, espaços vinculados, agendamentos e assinatura.
- Painel do espaço: dados do espaço, salas, disponibilidade, terapeutas vinculados, pagamentos e assinatura.
- Admin do Django com ações em massa, exportação em CSV e painel de estatísticas.

**Agendamento de salas**
- Cadastro de salas com valor, capacidade e horários.
- Reserva de sala por terapeuta vinculado, com edição e cancelamento.
- Previsão de multa no cancelamento, registro de multas por descumprimento de regras e configuração de PIX por espaço.
- Convite de terapeutas por e-mail para se vincularem a um espaço.

**Interface**
- Layout responsivo revisado em 375, 768, 1024 e 1280 px, baseado nas telas da pasta `design/`.

---

## Perfis de usuário e planos

Existem sete planos, criados por migration (`core/migrations/0013_criar_planos_iniciais.py`), então um banco recém-migrado já os contém.

| Plano | Para quem |
|---|---|
| Gratuito Filiado | Terapeuta vinculado a um espaço, sem divulgação pública |
| Basic | Terapeuta com perfil público essencial |
| Premium A | Terapeuta com destaque nas buscas e estatísticas |
| Premium S | Espaço com destaque e estatísticas |
| Premium S+ | Espaço com gestão completa de salas e agendamentos |
| Combo A + S | Terapeuta e espaço juntos |
| Combo A + S+ | Terapeuta e espaço com gestão de salas |

Os limites de cada plano ficam no model `Plano` e podem ser ajustados pelo admin.

---

## Tecnologias

**Backend**
- Python 3.12 e Django 4.2 LTS
- PostgreSQL 16
- django-allauth (autenticação), django-filter, django-ckeditor 4, Pillow
- Gunicorn e WhiteNoise para servir a aplicação e os arquivos estáticos

**Frontend**
- Templates do Django, sem etapa de build
- Tailwind CSS via CDN, com as cores e fontes da marca configuradas em `templates/base.html`
- Font Awesome e fonte Roboto
- HTMX 1.9 carregado no `base.html`; as telas atuais usam formulários e JavaScript simples

**Qualidade e infraestrutura**
- pytest, pytest-django e pytest-cov, com cobertura mínima de 80%
- GitHub Actions para os testes
- Vercel (aplicação), Neon (PostgreSQL) e Cloudinary (uploads de mídia)

---

## Estrutura do repositório

```
seravitta/
├── .github/workflows/ci.yml     # Pipeline de testes
├── backend/                     # Aplicação Django
│   ├── manage.py
│   ├── pytest.ini               # Configuração dos testes e gate de 80%
│   ├── requirements.txt
│   ├── runtime.txt              # Versão do Python usada no deploy
│   ├── Procfile                 # Comando de subida com gunicorn
│   ├── espacovital/             # settings, urls, wsgi e asgi
│   ├── core/                    # Home, páginas institucionais, localização,
│   │                            # planos, vouchers, assinaturas e onboarding
│   ├── terapeutas/              # Terapeutas, avaliações, contatos e painel
│   ├── espacos/                 # Espaços, comodidades, avaliações e painel
│   ├── agendamentos/            # Salas, agendamentos, multas, PIX e vínculos
│   ├── terapias/                # Páginas de terapias
│   ├── blog/                    # Reservado, ainda sem telas
│   ├── templates/               # base.html e templates por app
│   ├── static/                  # CSS, JS, imagens e logos
│   └── fixtures/                # Países, estados, cidades e especialidades
├── design/                      # Telas de referência (PNG e PDF)
├── docs/                        # Mapa funcional do projeto
├── Wireframe/                   # Protótipo HTML inicial
└── docker-compose.yml           # PostgreSQL local
```

---

## Rodando localmente

### Pré-requisitos

- Python 3.12
- Docker (para o PostgreSQL) ou um PostgreSQL 16 já instalado
- Git
- No Windows, use o WSL2 com Ubuntu

### Passo a passo

```bash
# 1. Clonar e entrar no projeto
git clone https://github.com/willdev34/seravitta.git
cd seravitta

# 2. Subir o PostgreSQL (porta local 5433)
docker compose up -d

# 3. Criar e ativar o ambiente virtual
cd backend
python3 -m venv venv-wsl
source venv-wsl/bin/activate

# 4. Instalar as dependências
pip install --upgrade pip
pip install -r requirements.txt

# 5. Criar o arquivo .env (veja a próxima seção) e ajustar DB_PORT=5433
cp .env.example .env

# 6. Criar as tabelas, planos e grupos de permissão
python manage.py migrate

# 7. Carregar localização, terapias e comodidades
python manage.py popular_localizacoes
python manage.py popular_terapias
python manage.py popular_comodidades

# 8. Criar um superusuário e subir o servidor
python manage.py createsuperuser
python manage.py runserver
```

O site abre em `http://localhost:8000` e o admin em `http://localhost:8000/admin/`.

Em desenvolvimento os e-mails vão para o terminal (`EMAIL_BACKEND` de console). A confirmação de e-mail é obrigatória no cadastro, então o link de confirmação aparece no log do `runserver`.

---

## Variáveis de ambiente

As variáveis são lidas com `python-decouple`, do arquivo `backend/.env` ou do ambiente do servidor. O arquivo `.env` não vai para o Git.

| Variável | Para que serve | Padrão |
|---|---|---|
| `ENVIRONMENT` | `development`, `qa` ou `production` | `development` |
| `SECRET_KEY` | Chave do Django. Em produção é obrigatória, o sistema não sobe com a chave de desenvolvimento | chave de desenvolvimento |
| `DEBUG` | Modo de depuração | `True` |
| `ALLOWED_HOSTS` | Hosts permitidos, separados por vírgula | `localhost,127.0.0.1` |
| `CSRF_TRUSTED_ORIGINS` | Origens confiáveis para formulários | `http://localhost:8000` |
| `DATABASE_URL` | URL completa do banco (Neon). Quando existe, tem prioridade sobre as variáveis `DB_*` | vazio |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | Conexão com o banco local | `espacovital`, `postgres`, `postgres`, `localhost`, `5432` |
| `USE_CLOUDINARY` | Envia uploads para o Cloudinary | `false` |
| `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET` | Credenciais do Cloudinary | vazio |
| `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`, `DEFAULT_FROM_EMAIL` | Envio de e-mail | backend de console |
| `ENABLE_DEBUG_TOOLBAR` | Liga o Django Debug Toolbar em desenvolvimento | `False` |

Exemplo de `.env` para o banco do `docker-compose.yml`:

```env
ENVIRONMENT=development
SECRET_KEY=troque-por-uma-chave-sua
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000

DB_NAME=espacovital
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5433
```

Na Vercel, os domínios `VERCEL_URL`, `VERCEL_BRANCH_URL` e `VERCEL_PROJECT_PRODUCTION_URL` são adicionados sozinhos aos hosts e origens permitidos.

---

## Comandos úteis

Todos rodam dentro de `backend/`.

| Comando | O que faz |
|---|---|
| `python manage.py popular_localizacoes` | Carrega países, estados e cidades |
| `python manage.py popular_terapias` | Carrega as especialidades e terapias |
| `python manage.py popular_comodidades` | Carrega as comodidades dos espaços (`--clear` limpa antes) |
| `python manage.py popular_tipos_espacos` | Carrega os tipos de espaço |
| `python manage.py criar_planos` | Recria ou atualiza os sete planos (a migration já os cria) |
| `python manage.py setup_permissions` | Cria os grupos e permissões do sistema |
| `python manage.py upgrade_plano <usuario>` | Dá um plano a um usuário, útil para testes |
| `python manage.py load_fixtures` | Carrega os arquivos da pasta `fixtures/` |
| `python manage.py fix_sequences` | Corrige as sequences do PostgreSQL depois de importar dados |

---

## Testes e qualidade

```bash
cd backend

# Suíte completa, com cobertura (falha se ficar abaixo de 80%)
python -m pytest -q -p no:cacheprovider

# Um arquivo ou pasta, sem cobertura
python -m pytest -q -p no:cacheprovider --no-cov espacos/tests/unit/test_forms.py
```

- Os testes ficam em `tests/unit` e `tests/integration` dentro de cada app. O `conftest.py` aplica os markers `unit` e `integration` conforme a pasta.
- Precisam de um PostgreSQL acessível com as variáveis `DB_*`.
- A suíte completa leva alguns minutos. Hoje são mais de mil testes e a cobertura fica perto de 88%.
- O `pytest.ini` usa `-p no:capture`, então o `capsys` não funciona. Para testar saída no terminal, use `contextlib.redirect_stdout`.
- Existe um teste de fumaça do admin que abre lista, busca, cadastro, edição e exclusão de todos os modelos registrados.

### Integração contínua

O workflow `.github/workflows/ci.yml` roda a cada push e pull request para `develop` e `main`. O job `testes` faz, nesta ordem:

1. instala Python 3.12 e as dependências;
2. `python manage.py check`;
3. `python manage.py makemigrations --check --dry-run`, que falha se faltar uma migration;
4. `pytest` com PostgreSQL 16 e o gate de 80% de cobertura;
5. salva o `coverage.xml` como artefato.

---

## Fluxo de trabalho

- `develop`: branch de trabalho. Todo o desenvolvimento entra aqui.
- `main`: branch de produção. Recebe código só por pull request vindo da `develop`, com o job `testes` verde.
- Commits seguem o padrão Conventional Commits em português: `feat:`, `fix:`, `test:`, `docs:`, `refactor:`, `chore:`.
- Antes de abrir o pull request: testes passando, nenhuma migration pendente e layout conferido no celular.

Convenções de código:

- Todo arquivo começa com um comentário com título, descrição, autor e data.
- Cada bloco de código tem um comentário curto dizendo o que faz.
- Em templates, o `{% extends %}` deve ser a primeira tag do arquivo. Para o cabeçalho de comentário use `<!-- -->`.
- Os arquivos usam final de linha CRLF. Preserve o padrão ao editar.

---

## Ambientes e deploy

| Ambiente | Hospedagem | Banco | Observação |
|---|---|---|---|
| Local | WSL2 e Docker | PostgreSQL 16 em container | Mídia salva em `backend/media/` |
| Prévia | Vercel, branch `develop` | Neon, região São Paulo | Domínio de prévia da Vercel |
| Produção | Vercel, branch `main` | Neon | Troca da Production Branch para `main` ainda pendente |

- Arquivos estáticos são servidos pelo WhiteNoise. Antes de subir, rode `python manage.py collectstatic --noinput`.
- Uploads em produção vão para o Cloudinary (`USE_CLOUDINARY=true`).
- Com `ENVIRONMENT=production` o sistema liga HTTPS obrigatório, cookies seguros e `X_FRAME_OPTIONS=DENY`.
- O `Procfile` e o `railway.json` em `backend/` são do ambiente anterior e seguem como referência de comando de subida (`migrate`, `collectstatic` e `gunicorn espacovital.wsgi:application`).

---

## Identidade visual e layout

- Logos em `backend/static/images/logo/`: horizontal, vertical, símbolo, avatar redondo, uma cor, com assinatura e branca sobre petróleo.
- Cores da marca (configuradas no Tailwind do `base.html`):

| Nome | Cor |
|---|---|
| `primary` (petróleo) | `#1E5C5C` |
| `primary-dark` | `#123F40` |
| `coral` | `#EE8B73` |
| `mint` | `#9BD8C0` |
| `bege` | `#F1E8DA` |
| `light-bg` | `#FBF9F5` |

- Fonte: Roboto.
- As telas de referência estão em `design/` (home, terapeutas, espaços e terapias, com e sem filtro, em desktop e mobile). Novas telas seguem o padrão visual dessas.

---

## Roadmap

**Em andamento**
- Fase 7: proteção da `main` exigindo o job `testes`, troca da Production Branch da Vercel e remoção da branch `deploy/vercel`.
- Subir a cobertura dos arquivos de admin e de `core/views.py`.

**Próximos passos**
- Domínio próprio (`seravitta.com.br`), com e-mails e links de redes sociais atualizados.
- Telas de multa no agendamento e duração variável de sessão.
- Blog educativo (o app existe, as telas ainda não).
- Login social (a base do allauth está instalada, os provedores ainda não estão configurados).
- Migrar o CKEditor 4 para a versão 5.
- Criar um arquivo `.gitattributes` para fixar o final de linha dos arquivos.

**Ideias para depois**
- Integração com Google Agenda.
- Geração de QR Code PIX.
- Avisos por e-mail e WhatsApp.
- Relatórios para donos de espaço.

---

## Contato e licença

**Will**, desenvolvedor full stack

- E-mail: [willdevp@icloud.com](mailto:willdevp@icloud.com)
- LinkedIn: [linkedin.com/in/willdevfull](https://linkedin.com/in/willdevfull)

Licença: ainda não definida. O repositório não tem arquivo `LICENSE`.
