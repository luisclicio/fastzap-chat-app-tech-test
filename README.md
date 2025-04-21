# FastChat

Aplicação de chat em tempo real com Django, Django Channels, Celery, Docker e Vue.js/Nuxt.js. Resolvido como parte do desafio técnico para a vaga de desenvolvedor backend pleno na FastZap.

## Funcionalidades/Requisitos

### Autenticação

- Login com username e senha (padrão do Django)
- Autenticação via JWT (JSON Web Token) para a API e WebSocket

### Permissões

- Usuários administradores são indicados a partir do atributo booleano `is_staff`
- Apenas usuários administradores podem criar salas e vincular usuários a elas
- Usuários comuns só podem acessar salas em que forem membros
- Usuários administradores podem acessar todas as salas

### Salas

- Usuários podem ver as mensagens anteriormente enviadas na sala que são membros
- Usuários podem enviar mensagens para a sala que são membros
- Usuários de uma sala podem ver quem está online no momento, em tempo real

### Mensagens

- Mensagens são enviadas em tempo real via WebSocket
- Mensagens são persistidas no banco de dados com status pendente e enviadas para a tarefa de moderação no Celery
- Mensagens enviadas para a tarefa de moderação são verificadas por modelos de IA e, se aprovadas, são aprovadas e enviadas para os usuários conectados na sala via WebSocket

### WebSocket

- Comunicação em tempo real entre os usuários
- Verificação de permissão para acesso a salas
- Recebimento de mensagens aprovadas em tempo real
- Visualização de quem está online na sala em tempo real

### Tech Stack

- [x] Django + Django REST Framework
- [x] Django Channels
- [x] Celery + Redis
- [x] WebSocket com autenticação
- [x] Docker + Docker Compose (para desenvolvimento e produção)

### Extras

- [x] Painel administrativo do Django com customizações:
  - Salas
  - Membros da salas
  - Mensagens
- [x] Celery:
  - Definição padrão de retries em caso de erros (`CELERY_TASK_ANNOTATIONS`)
- [x] API documentada com Swagger/Redoc:
  - Swagger acessível em http://localhost:8000/api/schema/swagger/
  - Redoc acessível em http://localhost:8000/api/schema/redoc/
- [x] Logs:
  - Logs no principais eventos da aplicação
- [x] Testes automatizados:
  - Testes unitários para a API
  - Testes de integração para o WebSocket
  - Testes nas tarefas do Celery

## Executando o projeto

### Pré-requisitos

- Docker
- Docker Compose

### Clonando o repositório

```bash
git clone git@github.com:luisclicio/fastzap-chat-app-tech-test.git
```

```bash
cd fastzap-chat-app-tech-test
```

### Configurando o ambiente

```bash
cp .env.example .env
```

### Executar com ambiente de desenvolvimento

- Atualizar, se necessário, as seguintes variáveis no arquivo `.env`:

```env
DATABASE_HOST=database-dev
REDIS_HOST=redis-dev
```

- Iniciar os serviços com o Docker Compose:

```bash
docker compose -f docker-compose.dev.yaml up --build
```

- Acessar o container do Django:

```bash
docker compose -f docker-compose.dev.yaml exec api-dev bash
```

### Executar com ambiente de produção

- Atualizar, se necessário, as seguintes variáveis no arquivo `.env`:

```env
DATABASE_HOST=database
REDIS_HOST=redis
```

- Iniciar os serviços com o Docker Compose:

```bash
docker compose up --build
```

- Acessar o container do Django:

```bash
docker compose exec api bash
```

### Etapas comuns para ambos os ambientes

- Executar as migrações:

```bash
python manage.py migrate
```

- Criar um superusuário para acessar o painel admin:

```bash
python manage.py createsuperuser
```

- Acessar a aplicação web (http://localhost:3000/room/new) com o usuário admin e criar uma sala

- Acessar o painel admin (http://localhost:8000/admin/auth/user/add/) e cadastrar um usuário comum

- Acessar "Room members" no painel administrativo (http://localhost:8000/admin/core/roommember/add/) e vincular o usuário comum criado com a sala desejada

- Em outro navegador, acessar a aplicação web (http://localhost:3000/) com o usuário comum e entrar na sala criada

## Testes automatizados

- Iniciar os serviços com o Docker Compose em ambiente de desenvolvimento e acessar o container do Django

- Executar os testes:

```bash
python manage.py test
```
