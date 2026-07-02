# PRD — Metalúrgica Itaparica

## Visão Geral

Site institucional para uma metalúrgica com sistema de acompanhamento de serviços. Clientes cadastram serviços e acompanham o status em tempo real.

## Funcionalidades

### 1. Cadastro de Serviços
- Cliente solicita um serviço com descrição, fotos e dados de contato
- Cada serviço pertence a um cliente
- Um cliente pode ter múltiplos serviços

### 2. Estados do Serviço
- `por fazer` — serviço recebido, aguardando início
- `em andamento` — execução em progresso
- `feito` — serviço concluído

### 3. Acompanhamento pelo Cliente
- Cliente consulta o status do serviço (sem necessidade de login)
- Página pública com token/identificador único por serviço
- Visualização do histórico de mudanças de status

### 4. Admin (funcionário da metalúrgica)
- Lista de todos os serviços com filtro por status
- Alterar status do serviço
- Adicionar observações/atualizações visíveis ao cliente

## Modelo de Dados (propostas)

### Cliente
- nome, telefone, email, data_cadastro

### Serviço
- cliente (FK)
- descricao, observacoes
- status (choices: por_fazer, em_andamento, feito)
- token_acompanhamento (UUID único para link público)
- criado_em, atualizado_em

### HistoricoStatus
- servico (FK)
- status_anterior, status_novo
- criado_em

## Frontend

### Requisitos de Design
- Design moderno e limpo
- Mobile first (responsivo)
- Tema claro (cores atuais mantidas como base: azul marinho + azul claro)
- Tipografia legível
- Transições suaves e micro-interações

### Páginas
| Rota | Página |
|---|---|
| `/` | Home institucional (já existe) |
| `/servicos/` | Lista de serviços públicos |
| `/servico/<token>/` | Página de acompanhamento de um serviço |
| `/admin/` | Painel Django admin (já existe) |

### Melhorias no Frontend Atual
- Substituir `display: none` do menu mobile por um hamburguer funcional
- Remover o `index.html` standalone e unificar tudo no Django
- Formulário de contato funcional com backend real
- Adicionar seção "Acompanhe seu serviço" com input de token

## Planejamento de Implementação

### Fase 1 — Modelos e Admin
- Criar modelos Cliente, Serviço, HistoricoStatus
- Configurar admin com listagem, filtros, busca
- Gerar migration e migrar

### Fase 2 — Acompanhamento
- View pública de serviço por token
- Página com detalhes e status atual

### Fase 3 — Formulário de Solicitação
- Formulário público para cadastrar novo serviço
- Retorna token para o cliente acompanhar

### Fase 4 — Frontend
- Unificar templates (remover `index.html` standalone)
- Menu mobile funcional
- Design refinado mobile first

## Não-Escopo (v1)
- Autenticação de cliente (login/senha)
- Notificações (email/WhatsApp)
- Dashboard com gráficos
- API REST
