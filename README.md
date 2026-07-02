# Metalúrgica Itaparica — Sistema de Acompanhamento de Serviços

Site institucional com dashboard de gerenciamento para uma metalúrgica.
Projeto de estudo desenvolvido com Django.

## Stack

- **Django 5.2** — framework web
- **Python 3.10+**
- **SQLite** — banco de dados
- **Pillow** — manipulação de imagens
- **python-dotenv** — carregamento de variáveis de ambiente
- **HTML/CSS/JS** — frontend com design responsivo

## Funcionalidades

- Página institucional com apresentação da empresa e serviços oferecidos
- Consulta pública de serviços por CPF ou telefone
- Dashboard privado (staff) com visão geral e métricas
- CRUD completo de clientes e serviços
- Controle de status: aguardando → em andamento → concluído
- Histórico de mudanças de status com data/hora
- Controle de pagamentos (pendente / parcial / pago)
- Previsão de entrega com detecção automática de atrasados
- Menu responsivo e design mobile-first
- Botão flutuante do WhatsApp

## Como rodar

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/metalurgica-itaparica.git
cd metalurgica-itaparica

# Crie e ative o ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite .env com sua SECRET_KEY e DEBUG

# Execute as migrações
python manage.py migrate

# Crie um superusuário para acessar o dashboard
python manage.py createsuperuser

# Inicie o servidor de desenvolvimento
python manage.py runserver
```

Acesse:
- **Site público:** http://127.0.0.1:8000/
- **Dashboard:** http://127.0.0.1:8000/dashboard/
- **Admin Django:** http://127.0.0.1:8000/admin/

## Estrutura do projeto

```
metalurgica-itaparica/
├── oficina/                  # Configuração do projeto Django
│   ├── settings.py
│   ├── urls.py
│   └── context_processors.py
├── servico/                  # App principal
│   ├── models.py             # Cliente, Servico, HistoricoStatus, ServicoOferta
│   ├── views.py              # Views públicas e do dashboard
│   ├── admin.py              # Configuração do admin
│   ├── templates/            # Templates HTML
│   └── static/               # CSS, JS, imagens
├── base_templates/           # Template base global
├── base_static/              # Assets estáticos globais
├── index.html                # Versão estática standalone
├── requirements.txt
└── manage.py
```

## Rotas principais

| Rota | Descrição | Acesso |
|---|---|---|
| `/` | Home institucional | Público |
| `/acompanhar/` | Consultar serviço por CPF/telefone | Público |
| `/dashboard/` | Painel com métricas | Staff |
| `/dashboard/servicos/` | Lista de serviços | Staff |
| `/dashboard/clientes/` | Lista de clientes | Staff |
| `/admin/` | Django admin | Superuser |

## Licença

Projeto de estudo — sinta-se à vontade para usar e modificar.
