# Auditoria de Segurança — Metalúrgica Itaparica

**Data:** 13/06/2026  
**Status:** Pendente — tratar antes do deploy em produção

---

## 🔴 Crítico

### 1. SECRET_KEY fraca
- **Arquivo:** `oficina/settings.py:27`
- **Problema:** Chave gerada automaticamente pelo `startproject` com prefixo `django-insecure-`
- **Risco:** Força bruta da chave → falsificação de sessões, CSRF tokens e assinaturas
- **Correção:** Gerar nova chave com `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` e colocar no `.env`

### 2. ALLOWED_HOSTS = ['*']
- **Arquivo:** `oficina/settings.py:32`
- **Problema:** Aceita qualquer host HTTP
- **Risco:** Host Header Injection — atacante forja header `Host`, gerando links maliciosos para reset de senha e cache poisoning
- **Correção:** Listar domínios reais: `['metalurgicaitaparica.com.br', 'www.metalurgicaitaparica.com.br']`

---

## 🟠 Alto

### 3. DEBUG=True em produção
- **Arquivo:** `oficina/settings.py:30` + `.env:2`
- **Problema:** Debug ativo
- **Risco:** Vazamento de informações sensíveis — stack traces expõem caminhos do sistema, configurações e queries SQL
- **Correção:** Em produção, `DEBUG=False` no `.env`

### 4. Sem HTTPS/SSL
- **Arquivo:** `oficina/settings.py`
- **Problema:** `SECURE_SSL_REDIRECT` não configurado
- **Risco:** Dados trafegam em texto puro — senha do admin, CPF de clientes e tokens CSRF podem ser interceptados
- **Correção:** Configurar certificado SSL + `SECURE_SSL_REDIRECT = True`

### 5. Session cookie não secure
- **Arquivo:** `oficina/settings.py`
- **Problema:** `SESSION_COOKIE_SECURE` não configurado
- **Risco:** Cookie de sessão enviado em HTTP — sequestro de sessão em rede não criptografada
- **Correção:** `SESSION_COOKIE_SECURE = True` (requer HTTPS)

### 6. CSRF cookie não secure
- **Arquivo:** `oficina/settings.py`
- **Problema:** `CSRF_COOKIE_SECURE` não configurado
- **Risco:** Token CSRF via HTTP — vulnerável a sniffing
- **Correção:** `CSRF_COOKIE_SECURE = True` (requer HTTPS)

### 7. HSTS não configurado
- **Arquivo:** `oficina/settings.py`
- **Problema:** `SECURE_HSTS_SECONDS` não definido
- **Risco:** Navegador não força HTTPS em futuras visitas — vulnerável a downgrade attack
- **Correção:** `SECURE_HSTS_SECONDS = 31536000` (requer HTTPS)

---

## 🟡 Médio

### 8. static() e media() servidos pelo Django
- **Arquivo:** `oficina/urls.py:42-43`
- **Problema:** Django serve arquivos estáticos e de mídia
- **Risco:** Ineficiente em produção; pode expor arquivos não intencionais
- **Correção:** Envolver em `if settings.DEBUG:` ou remover e usar nginx/apache

### 9. CPF sem validação no backend
- **Arquivo:** `servico/views.py:174`
- **Problema:** A validação de CPF é apenas frontend (JavaScript)
- **Risco:** Backend aceita CPF inválido — JS validation é contornável
- **Correção:** Adicionar validação no backend (biblioteca `cpf-cnpj` ou função custom)

---

## 🟢 Baixo

### 10. valor_pago sem validação de negativo
- **Arquivo:** `servico/views.py:142`
- **Problema:** `servico.valor_pago += valor` sem verificar se `valor > 0`
- **Risco:** Frontend pode enviar valor negativo e **diminuir** o valor pago
- **Correção:** Já existe `if valor > 0` — confirmar que cobre edge cases

### 11. cliente_id sem verificação de existência
- **Arquivo:** `servico/views.py:196`
- **Problema:** `cliente_id` do POST é usado diretamente, sem verificar se o cliente existe
- **Risco:** Se o cliente foi deletado entre o GET e o POST, o `ForeignKey` levanta `IntegrityError`
- **Correção:** Usar `get_object_or_404(Cliente, id=cliente_id)` antes de criar o serviço

### 12. Upload de imagem sem validação de tipo/tamanho
- **Arquivo:** `servico/models.py:45`
- **Problema:** `ImageField` sem restrições adicionais
- **Risco:** Upload de arquivos arbitrários disfarçados de imagem
- **Correção:** Adicionar `validate_image_file_extension` e limitar tamanho

### 13. requirements.txt sem versão fixa
- **Arquivo:** `requirements.txt`
- **Problema:** `django>=5.2` permite atualização automática
- **Risco:** Atualização inesperada pode quebrar a aplicação
- **Correção:** Fixar versões exatas: `django==5.2.14`

---

## ✅ Já corrigido / OK

| Item | Status |
|---|---|
| CSRF tokens | ✅ Em todos os formulários (`{% csrf_token %}`) |
| XSS (template escaping) | ✅ Django auto-escapa `{{ }}` — sem `|safe` ou `autoescape off` |
| SQL Injection | ✅ Django ORM parametriza queries automaticamente |
| Clickjacking | ✅ `XFrameOptionsMiddleware` ativo |
| Autenticação dashboard | ✅ `@login_required` + `@user_passes_test(_staff_check)` em todas as rotas |
| Senhas | ✅ Validadores ativos (mínimo, complexidade, etc.) |
| `.env` no `.gitignore` | ✅ SECRET_KEY não vaza para o repositório |
