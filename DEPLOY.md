# 🚀 Guia de Deploy - NutriAI Científico

## 📋 Pré-requisitos

### **1. Conta Neon (Banco de Dados)**
1. Acesse: https://neon.tech
2. Crie conta gratuita
3. Crie novo projeto: "nutriai-database"
4. Copie a connection string

### **2. Chave Gemini AI**
1. Acesse: https://makersuite.google.com/app/apikey
2. Crie nova API key
3. Copie a chave

### **3. Conta Vercel**
1. Acesse: https://vercel.com
2. Conecte com GitHub

## 🎯 Deploy Backend

### **Passo 1: Preparar Repositório**

```bash
# 1. Criar repositório no GitHub
# Vá em github.com → New repository
# Nome: nutriai-backend

# 2. Subir código
git init
git add .
git commit -m "NutriAI Sistema Científico Completo"
git remote add origin https://github.com/SEU-USUARIO/nutriai-backend.git
git push -u origin main
```

### **Passo 2: Deploy no Vercel**

1. **Conectar Repositório**
   - Acesse vercel.com/dashboard
   - "Add New" → "Project"
   - "Import Git Repository"
   - Selecione seu repositório

2. **Configurar Projeto**
   - **Framework Preset:** Other
   - **Root Directory:** ./
   - **Build Command:** (deixe vazio)
   - **Output Directory:** (deixe vazio)

3. **Variáveis de Ambiente**
   - Clique em "Environment Variables"
   - Adicione as seguintes:

```env
GEMINI_API_KEY=sua_chave_gemini_aqui
NEON_DATABASE_URL=postgresql://user:pass@host/db
JWT_SECRET_KEY=nutriai_jwt_secret_2025_change_this
SECRET_KEY=nutriai_flask_secret_2025_change_this
CORS_ORIGINS=*
FLASK_ENV=production
```

4. **Deploy**
   - Clique "Deploy"
   - Aguarde conclusão (2-3 minutos)

### **Passo 3: Verificar Deploy**

1. **Acessar URL**
   ```
   https://seu-projeto.vercel.app/api/status
   ```

2. **Resposta Esperada**
   ```json
   {
     "status": "online",
     "message": "NutriAI API Científica funcionando",
     "version": "2.0.0",
     "database": "Neon",
     "gemini_configured": true,
     "features": {
       "scientific_fields": 50,
       "metabolic_calculations": true,
       "ai_personalization": true,
       "nutritionist_validation": true
     }
   }
   ```

## 🎨 Deploy Frontend (Opcional)

### **Se quiser frontend separado:**

```bash
# 1. Criar novo repositório
# Nome: nutriai-frontend

# 2. Subir apenas a pasta frontend
cd frontend
git init
git add .
git commit -m "NutriAI Frontend React"
git remote add origin https://github.com/SEU-USUARIO/nutriai-frontend.git
git push -u origin main

# 3. Deploy no Vercel
# Framework: React
# Build Command: npm run build
# Output Directory: dist
```

### **Configurar API URL no Frontend:**

```javascript
// Em App.jsx, linha ~30
const API_BASE = 'https://seu-backend.vercel.app'
```

## 🔧 Configurações Avançadas

### **Domínio Personalizado**

1. **No Vercel:**
   - Settings → Domains
   - Add Domain: "nutriai.com.br"
   - Configure DNS conforme instruções

### **Monitoramento**

1. **Logs do Vercel:**
   - Functions → View Function Logs
   - Monitore erros e performance

2. **Banco Neon:**
   - Dashboard → Monitoring
   - Acompanhe conexões e queries

## 🐛 Troubleshooting

### **Erro 404 NOT_FOUND**

**Causa:** Vercel não encontra arquivo principal

**Solução:**
```bash
# Verificar se existe app.py na raiz
ls -la app.py

# Se não existir, criar:
echo "from src.main import app
application = app" > app.py
```

### **Erro de Banco de Dados**

**Causa:** NEON_DATABASE_URL incorreta

**Solução:**
1. Verificar string no Neon Dashboard
2. Formato correto: `postgresql://user:pass@host:5432/db?sslmode=require`
3. Redeployar no Vercel

### **Erro Gemini API**

**Causa:** GEMINI_API_KEY inválida

**Solução:**
1. Gerar nova chave em makersuite.google.com
2. Verificar se não tem espaços extras
3. Atualizar no Vercel

### **Erro CORS**

**Causa:** Frontend não consegue acessar backend

**Solução:**
```env
# No Vercel, adicionar:
CORS_ORIGINS=https://seu-frontend.vercel.app,http://localhost:3000
```

## ✅ Checklist de Deploy

### **Backend**
- [ ] Repositório criado no GitHub
- [ ] Código commitado e pushed
- [ ] Projeto criado no Vercel
- [ ] Variáveis de ambiente configuradas
- [ ] Deploy realizado com sucesso
- [ ] `/api/status` retorna 200 OK
- [ ] `database: "Neon"` no status
- [ ] `gemini_configured: true` no status

### **Banco de Dados**
- [ ] Projeto criado no Neon
- [ ] Connection string copiada
- [ ] Variável NEON_DATABASE_URL configurada
- [ ] Tabelas criadas automaticamente
- [ ] Usuários de teste funcionando

### **IA Gemini**
- [ ] API Key gerada no Google
- [ ] Variável GEMINI_API_KEY configurada
- [ ] Teste de geração de plano funcionando

### **Frontend (se separado)**
- [ ] Repositório frontend criado
- [ ] API_BASE apontando para backend
- [ ] Deploy frontend realizado
- [ ] Login funcionando
- [ ] Comunicação com backend OK

## 🎯 URLs Finais

### **Backend**
```
https://seu-backend.vercel.app/api/status
https://seu-backend.vercel.app/api/auth/login
https://seu-backend.vercel.app/api/diet-plans/generate
```

### **Frontend (se separado)**
```
https://seu-frontend.vercel.app
```

### **Usuários de Teste**
```
Usuário: ana@email.com / 123456
Nutricionista: maria@nutricionista.com / 123456
```

## 🚀 Resultado Final

**Sistema NutriAI Científico funcionando em produção:**

- ✅ **Backend** rodando no Vercel
- ✅ **Banco Neon** conectado e funcionando
- ✅ **IA Gemini** gerando planos personalizados
- ✅ **50+ campos** científicos coletando dados
- ✅ **Cálculos metabólicos** precisos
- ✅ **Interface** usuário/nutricionista completa
- ✅ **Sistema** de validação profissional

**🎉 Pronto para uso real e comercialização!**

