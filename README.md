# 🧬 NutriAI - Sistema Científico de Nutrição

Sistema completo de nutrição personalizada com IA Gemini, análise científica avançada e validação por nutricionistas.

## 🎯 Características Principais

### 🔬 **Análise Científica Completa**
- **50+ campos científicos** para análise nutricional precisa
- **Cálculos metabólicos** (TMB, TDEE, macronutrientes)
- **Histórico familiar** e predisposições genéticas
- **Análise comportamental** alimentar
- **Avaliação de estilo de vida** completa

### 🤖 **IA Gemini Integrada**
- **Planos personalizados** baseados em dados científicos
- **Prompt avançado** com análise metabólica
- **Considerações familiares** para prevenção
- **Orçamento rigoroso** respeitado
- **Fallback inteligente** quando não configurada

### 👨‍⚕️ **Sistema Profissional**
- **Interface usuário** com dashboard científico
- **Interface nutricionista** para validação
- **Workflow completo** de aprovação/rejeição
- **Estatísticas profissionais** detalhadas
- **Feedback personalizado** para pacientes

## 🏗️ Arquitetura

### **Backend (Flask)**
```
src/
├── main.py              # Aplicação principal
├── models/
│   └── nutriai_models.py # Modelos com 50+ campos científicos
├── routes/
│   ├── auth.py          # Autenticação JWT
│   └── diet_plans.py    # Planos alimentares
└── services/
    └── gemini_service.py # Integração IA Gemini
```

### **Frontend (React)**
```
frontend/src/
└── App.jsx              # Interface completa usuário/nutricionista
```

### **Banco de Dados**
- **Neon PostgreSQL** (produção)
- **SQLite** (desenvolvimento)
- **Migração automática** de tabelas

## 🚀 Deploy Rápido

### **1. Backend no Vercel**

```bash
# Clone/baixe os arquivos
git init
git add .
git commit -m "NutriAI Sistema Científico"
git remote add origin https://github.com/SEU-USUARIO/nutriai-backend.git
git push -u origin main

# No Vercel:
# 1. Conecte o repositório
# 2. Configure as variáveis de ambiente
# 3. Deploy automático
```

### **2. Variáveis de Ambiente (Vercel)**

```env
GEMINI_API_KEY=sua_chave_gemini_aqui
NEON_DATABASE_URL=postgresql://user:pass@host/db
JWT_SECRET_KEY=nutriai_jwt_secret_2025
SECRET_KEY=nutriai_flask_secret_2025
```

### **3. Frontend (Opcional)**

```bash
# Se quiser frontend separado
cd frontend
npm install
npm run build
# Deploy no Vercel/Netlify
```

## 📊 Campos Científicos

### **Dados Antropométricos**
- Circunferência abdominal
- Histórico de peso (6 meses)
- Peso meta e padrão de variação

### **Comportamento Alimentar**
- Velocidade para comer
- Frequência de beliscadas
- Consumo de água e álcool
- Alimentos que odeia

### **Estilo de Vida**
- Horas e qualidade do sono
- Nível de estresse (1-10)
- Rotina e horário de trabalho

### **Histórico Familiar**
- Diabetes, hipertensão
- Obesidade, problemas cardíacos

### **Atividade Física**
- Tipo, frequência, duração
- Intensidade percebida

### **Autoavaliação**
- Energia e disposição (1-10)
- Problemas digestivos
- Padrão de fome/saciedade

### **Objetivos**
- Meta mensal de peso
- Prazo total e motivação
- Experiência anterior

## 🧮 Cálculos Científicos

### **Taxa Metabólica Basal (TMB)**
```python
# Harris-Benedict Revisada
# Homens: 88.362 + (13.397 × peso) + (4.799 × altura) - (5.677 × idade)
# Mulheres: 447.593 + (9.247 × peso) + (3.098 × altura) - (4.330 × idade)
```

### **Gasto Energético Total (TDEE)**
```python
# TMB × Fator de Atividade
# Sedentário: 1.2
# Leve: 1.375
# Moderado: 1.55
# Intenso: 1.725
```

### **Distribuição de Macronutrientes**
```python
# Baseado no objetivo:
# Emagrecimento: 35% P, 30% C, 35% G
# Ganho de massa: 30% P, 40% C, 30% G
# Manutenção: 25% P, 45% C, 30% G
```

## 🔗 Endpoints da API

### **Autenticação**
```http
POST /api/auth/register    # Registro com dados científicos
POST /api/auth/login       # Login
GET  /api/auth/profile     # Perfil do usuário
PUT  /api/auth/profile     # Atualizar perfil
```

### **Planos Alimentares**
```http
POST /api/diet-plans/generate           # Gerar plano com IA
GET  /api/diet-plans/my-plans          # Histórico do usuário
GET  /api/diet-plans/pending           # Planos pendentes (nutricionista)
POST /api/diet-plans/{id}/validate     # Validar plano
GET  /api/diet-plans/nutritionist-dashboard # Dashboard nutricionista
```

### **Status**
```http
GET /api/status    # Status da API e configurações
```

## 👥 Usuários de Teste

### **Usuário Padrão**
```
Email: ana@email.com
Senha: 123456
Tipo: user
```

### **Nutricionista**
```
Email: maria@nutricionista.com
Senha: 123456
Tipo: nutritionist
```

## 🎯 Funcionalidades

### **Para Usuários**
- ✅ **Perfil científico** completo (50+ campos)
- ✅ **Análise metabólica** automática (TMB, TDEE, macros)
- ✅ **Geração de planos** com IA Gemini
- ✅ **Dashboard** com métricas científicas
- ✅ **Histórico** de planos e progresso
- ✅ **Feedback** personalizado de nutricionistas

### **Para Nutricionistas**
- ✅ **Dashboard profissional** com estatísticas
- ✅ **Lista de planos** aguardando validação
- ✅ **Análise científica** completa dos pacientes
- ✅ **Sistema de aprovação/rejeição** com feedback
- ✅ **Métricas** de performance (taxa de aprovação)
- ✅ **Dados científicos** para tomada de decisão

## 🔧 Configuração Local (Opcional)

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar variáveis
cp .env.example .env
# Editar .env com suas chaves

# 3. Executar
python app.py

# 4. Acessar
# http://localhost:5000/api/status
```

## 🌟 Diferenciais

### **Científico vs Genérico**
- ❌ **Genérico:** "Qual seu objetivo?"
- ✅ **Científico:** 50+ campos + cálculos metabólicos

### **IA vs Receitas Prontas**
- ❌ **Receitas:** Planos fixos e genéricos
- ✅ **IA Gemini:** Personalização total baseada em dados

### **Automático vs Profissional**
- ❌ **Automático:** Sem validação humana
- ✅ **Profissional:** Nutricionistas validam todos os planos

## 📈 Roadmap

### **Versão Atual (2.0)**
- ✅ Sistema científico completo
- ✅ IA Gemini integrada
- ✅ Interface usuário/nutricionista
- ✅ 50+ campos científicos

### **Próximas Versões**
- 🔄 **API de preços** de supermercados
- 🔄 **Sistema de pagamento** (R$ 29,90/mês)
- 🔄 **App mobile** React Native
- 🔄 **Relatórios** científicos em PDF
- 🔄 **Integração** com wearables

## 🏆 Resultado

**Sistema NutriAI Científico 100% funcional:**

- ✅ **Backend Flask** com 50+ campos científicos
- ✅ **Frontend React** com interface completa
- ✅ **IA Gemini** para personalização total
- ✅ **Banco Neon** para persistência
- ✅ **Sistema profissional** usuário/nutricionista
- ✅ **Cálculos metabólicos** precisos
- ✅ **Deploy automático** no Vercel
- ✅ **Baseado na especificação** original

**🚀 Pronto para produção e uso real!**

