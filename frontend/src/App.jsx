import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Checkbox } from '@/components/ui/checkbox.jsx'
import { 
  User, 
  Stethoscope, 
  Brain, 
  DollarSign, 
  Clock, 
  CheckCircle, 
  XCircle, 
  AlertCircle,
  Utensils,
  ShoppingCart,
  Calendar,
  TrendingUp,
  Users,
  MessageSquare,
  Settings,
  LogOut,
  Leaf,
  Activity,
  Heart,
  Scale,
  Target,
  Moon,
  Zap,
  Droplets,
  Coffee
} from 'lucide-react'
import './App.css'

function App() {
  const [userType, setUserType] = useState(null) // 'user' ou 'nutritionist'
  const [currentUser, setCurrentUser] = useState(null)
  const [currentPage, setCurrentPage] = useState('login')
  const [authToken, setAuthToken] = useState(null)

  // Estados para dados
  const [dietPlans, setDietPlans] = useState([])
  const [pendingPlans, setPendingPlans] = useState([])
  const [userProfile, setUserProfile] = useState({})

  // API Base URL
  const API_BASE = process.env.NODE_ENV === 'production' 
    ? 'https://seu-backend.vercel.app' 
    : 'http://localhost:5000'

  // Função para fazer requisições à API
  const apiRequest = async (endpoint, options = {}) => {
    const url = `${API_BASE}${endpoint}`
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...(authToken && { 'Authorization': `Bearer ${authToken}` })
      },
      ...options
    }

    try {
      const response = await fetch(url, config)
      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.error || 'Erro na requisição')
      }
      
      return data
    } catch (error) {
      console.error('API Error:', error)
      throw error
    }
  }

  // Componente de Login
  const LoginPage = () => {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [isRegistering, setIsRegistering] = useState(false)
    const [loading, setLoading] = useState(false)

    const handleAuth = async (type) => {
      setLoading(true)
      try {
        const endpoint = isRegistering ? '/api/auth/register' : '/api/auth/login'
        const data = await apiRequest(endpoint, {
          method: 'POST',
          body: JSON.stringify({
            email: email || (type === 'user' ? 'ana@email.com' : 'maria@nutricionista.com'),
            password: password || '123456',
            name: type === 'user' ? 'Ana Silva' : 'Dr. Maria Oliveira',
            user_type: type
          })
        })

        setAuthToken(data.access_token)
        setCurrentUser(data.user)
        setUserType(type)
        setCurrentPage(type === 'user' ? 'dashboard' : 'nutritionist-dashboard')
      } catch (error) {
        alert('Erro no login: ' + error.message)
      } finally {
        setLoading(false)
      }
    }

    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 flex items-center justify-center p-4">
        <Card className="w-full max-w-md">
          <CardHeader className="text-center">
            <div className="flex items-center justify-center gap-2 mb-4">
              <Leaf className="h-8 w-8 text-green-600" />
              <h1 className="text-2xl font-bold text-gray-900">NutriAI</h1>
            </div>
            <CardTitle>Sistema Científico de Nutrição</CardTitle>
            <CardDescription>
              50+ campos científicos • IA Gemini • Análise metabólica completa
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="seu@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Senha</Label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            
            <div className="space-y-3 pt-4">
              <Button 
                onClick={() => handleAuth('user')} 
                className="w-full bg-green-600 hover:bg-green-700"
                disabled={loading}
              >
                <User className="h-4 w-4 mr-2" />
                {loading ? 'Entrando...' : 'Entrar como Usuário'}
              </Button>
              <Button 
                onClick={() => handleAuth('nutritionist')} 
                variant="outline" 
                className="w-full"
                disabled={loading}
              >
                <Stethoscope className="h-4 w-4 mr-2" />
                {loading ? 'Entrando...' : 'Entrar como Nutricionista'}
              </Button>
            </div>

            <div className="text-center pt-4 border-t">
              <p className="text-sm text-gray-600 mb-2">Usuários de teste:</p>
              <p className="text-xs text-gray-500">
                Usuário: ana@email.com / 123456<br/>
                Nutricionista: maria@nutricionista.com / 123456
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  // Formulário Científico Completo
  const ScientificProfileForm = ({ onComplete }) => {
    const [formData, setFormData] = useState({
      // Dados básicos
      name: '',
      age: '',
      weight: '',
      height: '',
      goal: '',
      budget_per_meal: '',
      dietary_restrictions: '',
      
      // Dados antropométricos
      waist_circumference: '',
      weight_6_months_ago: '',
      target_weight: '',
      weight_variation_pattern: '',
      
      // Comportamento alimentar
      eating_speed: '',
      snacking_frequency: '',
      daily_water_intake: '',
      alcohol_consumption: '',
      food_dislikes: '',
      
      // Estilo de vida
      sleep_hours: '',
      sleep_quality: '',
      stress_level: '',
      work_routine: '',
      work_schedule: '',
      
      // Histórico familiar
      family_diabetes: false,
      family_hypertension: false,
      family_obesity: false,
      family_heart_disease: false,
      
      // Atividade física
      current_exercise: '',
      exercise_frequency: '',
      exercise_duration: '',
      exercise_intensity: '',
      
      // Medicamentos
      current_medications: '',
      supplements: '',
      
      // Autoavaliação
      energy_level: '',
      disposition_level: '',
      digestive_issues: '',
      bloating_frequency: '',
      hunger_satiety_pattern: '',
      
      // Objetivos
      monthly_weight_goal: '',
      total_timeframe: '',
      main_motivation: '',
      previous_diet_experience: ''
    })

    const [currentStep, setCurrentStep] = useState(0)
    const [loading, setLoading] = useState(false)

    const steps = [
      { title: 'Dados Básicos', icon: User },
      { title: 'Medidas Corporais', icon: Scale },
      { title: 'Comportamento Alimentar', icon: Utensils },
      { title: 'Estilo de Vida', icon: Activity },
      { title: 'Histórico Familiar', icon: Heart },
      { title: 'Atividade Física', icon: Zap },
      { title: 'Autoavaliação', icon: Target },
      { title: 'Objetivos', icon: TrendingUp }
    ]

    const updateField = (field, value) => {
      setFormData(prev => ({ ...prev, [field]: value }))
    }

    const handleSubmit = async () => {
      setLoading(true)
      try {
        const data = await apiRequest('/api/auth/profile', {
          method: 'PUT',
          body: JSON.stringify(formData)
        })
        
        setCurrentUser(data.user)
        onComplete()
      } catch (error) {
        alert('Erro ao salvar perfil: ' + error.message)
      } finally {
        setLoading(false)
      }
    }

    const renderStep = () => {
      switch (currentStep) {
        case 0: // Dados Básicos
          return (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label>Nome Completo</Label>
                  <Input 
                    value={formData.name} 
                    onChange={(e) => updateField('name', e.target.value)}
                    placeholder="Seu nome completo"
                  />
                </div>
                <div>
                  <Label>Idade</Label>
                  <Input 
                    type="number" 
                    value={formData.age} 
                    onChange={(e) => updateField('age', e.target.value)}
                    placeholder="Sua idade"
                  />
                </div>
                <div>
                  <Label>Peso Atual (kg)</Label>
                  <Input 
                    type="number" 
                    value={formData.weight} 
                    onChange={(e) => updateField('weight', e.target.value)}
                    placeholder="70"
                  />
                </div>
                <div>
                  <Label>Altura (cm)</Label>
                  <Input 
                    type="number" 
                    value={formData.height} 
                    onChange={(e) => updateField('height', e.target.value)}
                    placeholder="170"
                  />
                </div>
              </div>
              <div>
                <Label>Objetivo Principal</Label>
                <Select value={formData.goal} onValueChange={(value) => updateField('goal', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione seu objetivo" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="perder_peso">Perder peso</SelectItem>
                    <SelectItem value="ganhar_massa">Ganhar massa muscular</SelectItem>
                    <SelectItem value="manter_peso">Manter peso</SelectItem>
                    <SelectItem value="melhorar_saude">Melhorar saúde geral</SelectItem>
                    <SelectItem value="controlar_doenca">Controlar condição médica</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label>Orçamento por Refeição (R$)</Label>
                <Input 
                  type="number" 
                  value={formData.budget_per_meal} 
                  onChange={(e) => updateField('budget_per_meal', e.target.value)}
                  placeholder="25"
                />
              </div>
              <div>
                <Label>Restrições Alimentares</Label>
                <Textarea 
                  value={formData.dietary_restrictions} 
                  onChange={(e) => updateField('dietary_restrictions', e.target.value)}
                  placeholder="Ex: Sem lactose, vegetariano, alergia a amendoim..."
                />
              </div>
            </div>
          )

        case 1: // Medidas Corporais
          return (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label>Circunferência Abdominal (cm)</Label>
                  <Input 
                    type="number" 
                    value={formData.waist_circumference} 
                    onChange={(e) => updateField('waist_circumference', e.target.value)}
                    placeholder="Meça com fita métrica"
                  />
                </div>
                <div>
                  <Label>Peso há 6 meses (kg)</Label>
                  <Input 
                    type="number" 
                    value={formData.weight_6_months_ago} 
                    onChange={(e) => updateField('weight_6_months_ago', e.target.value)}
                    placeholder="Qual era seu peso?"
                  />
                </div>
                <div>
                  <Label>Peso Meta (kg)</Label>
                  <Input 
                    type="number" 
                    value={formData.target_weight} 
                    onChange={(e) => updateField('target_weight', e.target.value)}
                    placeholder="Quanto quer pesar?"
                  />
                </div>
                <div>
                  <Label>Padrão de Variação de Peso</Label>
                  <Select value={formData.weight_variation_pattern} onValueChange={(value) => updateField('weight_variation_pattern', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Como seu peso varia?" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="engorda_facil">Engorda facilmente</SelectItem>
                      <SelectItem value="emagrece_facil">Emagrece facilmente</SelectItem>
                      <SelectItem value="estavel">Peso estável</SelectItem>
                      <SelectItem value="varia_muito">Varia muito (efeito sanfona)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </div>
          )

        case 2: // Comportamento Alimentar
          return (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label>Velocidade para Comer</Label>
                  <Select value={formData.eating_speed} onValueChange={(value) => updateField('eating_speed', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Como você come?" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="muito_rapido">Muito rápido</SelectItem>
                      <SelectItem value="rapido">Rápido</SelectItem>
                      <SelectItem value="normal">Normal</SelectItem>
                      <SelectItem value="devagar">Devagar</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label>Frequência de Beliscadas</Label>
                  <Select value={formData.snacking_frequency} onValueChange={(value) => updateField('snacking_frequency', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Belisca entre refeições?" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="nunca">Nunca</SelectItem>
                      <SelectItem value="raramente">Raramente</SelectItem>
                      <SelectItem value="as_vezes">Às vezes</SelectItem>
                      <SelectItem value="frequentemente">Frequentemente</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label>Copos de Água por Dia</Label>
                  <Input 
                    type="number" 
                    value={formData.daily_water_intake} 
                    onChange={(e) => updateField('daily_water_intake', e.target.value)}
                    placeholder="8"
                  />
                </div>
                <div>
                  <Label>Consumo de Álcool</Label>
                  <Select value={formData.alcohol_consumption} onValueChange={(value) => updateField('alcohol_consumption', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Frequência de álcool" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="nunca">Nunca</SelectItem>
                      <SelectItem value="social">Social (fins de semana)</SelectItem>
                      <SelectItem value="regular">Regular (algumas vezes/semana)</SelectItem>
                      <SelectItem value="diario">Diário</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              <div>
                <Label>Alimentos que Você Odeia</Label>
                <Textarea 
                  value={formData.food_dislikes} 
                  onChange={(e) => updateField('food_dislikes', e.target.value)}
                  placeholder="Ex: Brócolis, fígado, peixe..."
                />
              </div>
            </div>
          )

        case 3: // Estilo de Vida
          return (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label>Horas de Sono por Noite</Label>
                  <Input 
                    type="number" 
                    step="0.5"
                    value={formData.sleep_hours} 
                    onChange={(e) => updateField('sleep_hours', e.target.value)}
                    placeholder="8"
                  />
                </div>
                <div>
                  <Label>Qualidade do Sono</Label>
                  <Select value={formData.sleep_quality} onValueChange={(value) => updateField('sleep_quality', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Como você dorme?" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="ruim">Ruim</SelectItem>
                      <SelectItem value="regular">Regular</SelectItem>
                      <SelectItem value="boa">Boa</SelectItem>
                      <SelectItem value="excelente">Excelente</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label>Nível de Estresse (1-10)</Label>
                  <Input 
                    type="number" 
                    min="1" 
                    max="10"
                    value={formData.stress_level} 
                    onChange={(e) => updateField('stress_level', e.target.value)}
                    placeholder="5"
                  />
                </div>
                <div>
                  <Label>Rotina de Trabalho</Label>
                  <Select value={formData.work_routine} onValueChange={(value) => updateField('work_routine', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Tipo de trabalho" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="sedentario">Sedentário (escritório)</SelectItem>
                      <SelectItem value="ativo">Ativo (em pé, caminhando)</SelectItem>
                      <SelectItem value="muito_ativo">Muito ativo (físico)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label>Horário de Trabalho</Label>
                  <Select value={formData.work_schedule} onValueChange={(value) => updateField('work_schedule', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Quando trabalha?" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="comercial">Comercial (9h-18h)</SelectItem>
                      <SelectItem value="noturno">Noturno</SelectItem>
                      <SelectItem value="irregular">Irregular/Turnos</SelectItem>
                      <SelectItem value="home_office">Home office</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </div>
          )

        case 4: // Histórico Familiar
          return (
            <div className="space-y-4">
              <p className="text-sm text-gray-600 mb-4">
                Marque as condições que existem na sua família (pais, irmãos, avós):
              </p>
              <div className="space-y-3">
                <div className="flex items-center space-x-2">
                  <Checkbox 
                    id="family_diabetes"
                    checked={formData.family_diabetes}
                    onCheckedChange={(checked) => updateField('family_diabetes', checked)}
                  />
                  <Label htmlFor="family_diabetes">Diabetes</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <Checkbox 
                    id="family_hypertension"
                    checked={formData.family_hypertension}
                    onCheckedChange={(checked) => updateField('family_hypertension', checked)}
                  />
                  <Label htmlFor="family_hypertension">Hipertensão (pressão alta)</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <Checkbox 
                    id="family_obesity"
                    checked={formData.family_obesity}
                    onCheckedChange={(checked) => updateField('family_obesity', checked)}
                  />
                  <Label htmlFor="family_obesity">Obesidade</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <Checkbox 
                    id="family_heart_disease"
                    checked={formData.family_heart_disease}
                    onCheckedChange={(checked) => updateField('family_heart_disease', checked)}
                  />
                  <Label htmlFor="family_heart_disease">Problemas cardíacos</Label>
                </div>
              </div>
            </div>
          )

        case 5: // Atividade Física
          return (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label>Exercício Atual</Label>
                  <Input 
                    value={formData.current_exercise} 
                    onChange={(e) => updateField('current_exercise', e.target.value)}
                    placeholder="Ex: Caminhada, musculação, natação..."
                  />
                </div>
                <div>
                  <Label>Frequência (vezes por semana)</Label>
                  <Input 
                    type="number" 
                    value={formData.exercise_frequency} 
                    onChange={(e) => updateField('exercise_frequency', e.target.value)}
                    placeholder="3"
                  />
                </div>
                <div>
                  <Label>Duração (minutos por sessão)</Label>
                  <Input 
                    type="number" 
                    value={formData.exercise_duration} 
                    onChange={(e) => updateField('exercise_duration', e.target.value)}
                    placeholder="60"
                  />
                </div>
                <div>
                  <Label>Intensidade</Label>
                  <Select value={formData.exercise_intensity} onValueChange={(value) => updateField('exercise_intensity', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Intensidade do exercício" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="leve">Leve</SelectItem>
                      <SelectItem value="moderado">Moderado</SelectItem>
                      <SelectItem value="intenso">Intenso</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </div>
          )

        case 6: // Autoavaliação
          return (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label>Nível de Energia (1-10)</Label>
                  <Input 
                    type="number" 
                    min="1" 
                    max="10"
                    value={formData.energy_level} 
                    onChange={(e) => updateField('energy_level', e.target.value)}
                    placeholder="7"
                  />
                </div>
                <div>
                  <Label>Disposição Geral (1-10)</Label>
                  <Input 
                    type="number" 
                    min="1" 
                    max="10"
                    value={formData.disposition_level} 
                    onChange={(e) => updateField('disposition_level', e.target.value)}
                    placeholder="8"
                  />
                </div>
                <div>
                  <Label>Frequência de Inchaço</Label>
                  <Select value={formData.bloating_frequency} onValueChange={(value) => updateField('bloating_frequency', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Incha com frequência?" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="nunca">Nunca</SelectItem>
                      <SelectItem value="raramente">Raramente</SelectItem>
                      <SelectItem value="as_vezes">Às vezes</SelectItem>
                      <SelectItem value="frequentemente">Frequentemente</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label>Padrão de Fome</Label>
                  <Select value={formData.hunger_satiety_pattern} onValueChange={(value) => updateField('hunger_satiety_pattern', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Como é sua fome?" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="muita_fome">Muita fome sempre</SelectItem>
                      <SelectItem value="normal">Normal</SelectItem>
                      <SelectItem value="pouca_fome">Pouca fome</SelectItem>
                      <SelectItem value="sem_fome">Quase sem fome</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              <div>
                <Label>Problemas Digestivos</Label>
                <Textarea 
                  value={formData.digestive_issues} 
                  onChange={(e) => updateField('digestive_issues', e.target.value)}
                  placeholder="Ex: Azia, gases, intestino preso..."
                />
              </div>
              <div>
                <Label>Medicamentos Atuais</Label>
                <Textarea 
                  value={formData.current_medications} 
                  onChange={(e) => updateField('current_medications', e.target.value)}
                  placeholder="Liste medicamentos que toma regularmente"
                />
              </div>
              <div>
                <Label>Suplementos</Label>
                <Textarea 
                  value={formData.supplements} 
                  onChange={(e) => updateField('supplements', e.target.value)}
                  placeholder="Ex: Whey protein, vitamina D, ômega 3..."
                />
              </div>
            </div>
          )

        case 7: // Objetivos
          return (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label>Meta de Peso por Mês (kg)</Label>
                  <Input 
                    type="number" 
                    step="0.5"
                    value={formData.monthly_weight_goal} 
                    onChange={(e) => updateField('monthly_weight_goal', e.target.value)}
                    placeholder="2"
                  />
                </div>
                <div>
                  <Label>Prazo Total (meses)</Label>
                  <Input 
                    type="number" 
                    value={formData.total_timeframe} 
                    onChange={(e) => updateField('total_timeframe', e.target.value)}
                    placeholder="6"
                  />
                </div>
              </div>
              <div>
                <Label>Motivação Principal</Label>
                <Textarea 
                  value={formData.main_motivation} 
                  onChange={(e) => updateField('main_motivation', e.target.value)}
                  placeholder="Por que você quer alcançar esse objetivo?"
                />
              </div>
              <div>
                <Label>Experiência Anterior com Dietas</Label>
                <Textarea 
                  value={formData.previous_diet_experience} 
                  onChange={(e) => updateField('previous_diet_experience', e.target.value)}
                  placeholder="Já fez dietas antes? O que funcionou ou não funcionou?"
                />
              </div>
            </div>
          )

        default:
          return null
      }
    }

    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-4xl mx-auto px-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Brain className="h-6 w-6 text-green-600" />
                Perfil Científico Completo
              </CardTitle>
              <CardDescription>
                Complete seu perfil para análise nutricional personalizada com IA
              </CardDescription>
            </CardHeader>
            <CardContent>
              {/* Progress Steps */}
              <div className="mb-8">
                <div className="flex items-center justify-between mb-4">
                  {steps.map((step, index) => {
                    const Icon = step.icon
                    return (
                      <div key={index} className="flex flex-col items-center">
                        <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                          index <= currentStep ? 'bg-green-600 text-white' : 'bg-gray-200 text-gray-500'
                        }`}>
                          <Icon className="h-5 w-5" />
                        </div>
                        <span className="text-xs mt-1 text-center">{step.title}</span>
                      </div>
                    )
                  })}
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-green-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
                  />
                </div>
              </div>

              {/* Current Step Content */}
              <div className="mb-8">
                <h3 className="text-lg font-semibold mb-4">{steps[currentStep].title}</h3>
                {renderStep()}
              </div>

              {/* Navigation */}
              <div className="flex justify-between">
                <Button 
                  variant="outline" 
                  onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
                  disabled={currentStep === 0}
                >
                  Anterior
                </Button>
                
                {currentStep < steps.length - 1 ? (
                  <Button 
                    onClick={() => setCurrentStep(currentStep + 1)}
                    className="bg-green-600 hover:bg-green-700"
                  >
                    Próximo
                  </Button>
                ) : (
                  <Button 
                    onClick={handleSubmit}
                    disabled={loading}
                    className="bg-green-600 hover:bg-green-700"
                  >
                    {loading ? 'Salvando...' : 'Finalizar Perfil'}
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  // Dashboard do Usuário
  const UserDashboard = () => {
    const [showPlanGenerator, setShowPlanGenerator] = useState(false)
    const [showProfileForm, setShowProfileForm] = useState(false)
    const [userPlans, setUserPlans] = useState([])
    const [loading, setLoading] = useState(false)

    useEffect(() => {
      loadUserPlans()
    }, [])

    const loadUserPlans = async () => {
      try {
        const data = await apiRequest('/api/diet-plans/my-plans')
        setUserPlans(data.plans)
      } catch (error) {
        console.error('Erro ao carregar planos:', error)
      }
    }

    const generatePlan = async () => {
      setLoading(true)
      try {
        const data = await apiRequest('/api/diet-plans/generate', {
          method: 'POST'
        })
        
        setUserPlans(prev => [data.plan, ...prev])
        setShowPlanGenerator(false)
        alert('Plano gerado com sucesso! Aguarde validação do nutricionista.')
      } catch (error) {
        if (error.message.includes('Dados básicos incompletos')) {
          alert('Complete seu perfil científico primeiro!')
          setShowProfileForm(true)
        } else {
          alert('Erro ao gerar plano: ' + error.message)
        }
      } finally {
        setLoading(false)
      }
    }

    if (showProfileForm) {
      return <ScientificProfileForm onComplete={() => setShowProfileForm(false)} />
    }

    return (
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center gap-2">
                <Leaf className="h-6 w-6 text-green-600" />
                <span className="text-xl font-semibold">NutriAI</span>
                <Badge variant="secondary">Científico</Badge>
              </div>
              <div className="flex items-center gap-4">
                <span className="text-sm text-gray-600">Olá, {currentUser?.name}</span>
                <Button variant="ghost" size="sm" onClick={() => setShowProfileForm(true)}>
                  <Settings className="h-4 w-4" />
                </Button>
                <Button variant="ghost" size="sm" onClick={() => setCurrentPage('login')}>
                  <LogOut className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>
        </header>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            {/* Coluna Principal */}
            <div className="lg:col-span-2 space-y-6">
              
              {/* Análise Científica */}
              {currentUser?.bmr && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Activity className="h-5 w-5" />
                      Análise Metabólica Científica
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div className="text-center">
                        <p className="text-2xl font-bold text-blue-600">{currentUser.bmr}</p>
                        <p className="text-sm text-gray-600">TMB (kcal)</p>
                      </div>
                      <div className="text-center">
                        <p className="text-2xl font-bold text-green-600">{currentUser.tdee}</p>
                        <p className="text-sm text-gray-600">TDEE (kcal)</p>
                      </div>
                      <div className="text-center">
                        <p className="text-2xl font-bold text-purple-600">{currentUser.target_calories}</p>
                        <p className="text-sm text-gray-600">Meta (kcal)</p>
                      </div>
                      <div className="text-center">
                        <p className="text-2xl font-bold text-orange-600">{currentUser.macros?.protein_g}g</p>
                        <p className="text-sm text-gray-600">Proteína</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Estatísticas */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card>
                  <CardContent className="p-6">
                    <div className="flex items-center gap-2">
                      <DollarSign className="h-5 w-5 text-green-600" />
                      <div>
                        <p className="text-sm text-gray-600">Orçamento/Refeição</p>
                        <p className="text-2xl font-bold">R$ {currentUser?.budget_per_meal || 25}</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
                
                <Card>
                  <CardContent className="p-6">
                    <div className="flex items-center gap-2">
                      <Target className="h-5 w-5 text-blue-600" />
                      <div>
                        <p className="text-sm text-gray-600">Meta Mensal</p>
                        <p className="text-2xl font-bold">{currentUser?.monthly_weight_goal || 2}kg</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
                
                <Card>
                  <CardContent className="p-6">
                    <div className="flex items-center gap-2">
                      <Calendar className="h-5 w-5 text-purple-600" />
                      <div>
                        <p className="text-sm text-gray-600">Planos Gerados</p>
                        <p className="text-2xl font-bold">{userPlans.length}</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* Planos */}
              <Card>
                <CardHeader>
                  <div className="flex justify-between items-center">
                    <CardTitle className="flex items-center gap-2">
                      <Utensils className="h-5 w-5" />
                      Meus Planos Alimentares
                    </CardTitle>
                    <Button 
                      onClick={generatePlan}
                      disabled={loading}
                      className="bg-green-600 hover:bg-green-700"
                    >
                      <Brain className="h-4 w-4 mr-2" />
                      {loading ? 'Gerando...' : 'Gerar Novo Plano'}
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  {userPlans.length > 0 ? (
                    <div className="space-y-4">
                      {userPlans.map((plan) => (
                        <div key={plan.id} className="border rounded-lg p-4">
                          <div className="flex justify-between items-start mb-2">
                            <div>
                              <h4 className="font-medium">{plan.goal}</h4>
                              <p className="text-sm text-gray-600">
                                Criado em {new Date(plan.created_at).toLocaleDateString()}
                              </p>
                            </div>
                            <Badge variant={
                              plan.status === 'approved' ? 'default' : 
                              plan.status === 'rejected' ? 'destructive' : 'secondary'
                            }>
                              {plan.status === 'approved' ? 'Aprovado' : 
                               plan.status === 'rejected' ? 'Rejeitado' : 'Pendente'}
                            </Badge>
                          </div>
                          
                          {plan.ai_plan && (
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
                              {plan.ai_plan.breakfast && (
                                <div>
                                  <h5 className="font-medium text-green-700">Café da Manhã</h5>
                                  <p className="text-sm text-gray-600">{plan.ai_plan.breakfast.name || plan.ai_plan.breakfast}</p>
                                </div>
                              )}
                              {plan.ai_plan.lunch && (
                                <div>
                                  <h5 className="font-medium text-blue-700">Almoço</h5>
                                  <p className="text-sm text-gray-600">{plan.ai_plan.lunch.name || plan.ai_plan.lunch}</p>
                                </div>
                              )}
                              {plan.ai_plan.dinner && (
                                <div>
                                  <h5 className="font-medium text-purple-700">Jantar</h5>
                                  <p className="text-sm text-gray-600">{plan.ai_plan.dinner.name || plan.ai_plan.dinner}</p>
                                </div>
                              )}
                            </div>
                          )}
                          
                          {plan.nutritionist_feedback && (
                            <div className="mt-4 p-3 bg-blue-50 rounded">
                              <p className="text-sm font-medium text-blue-800">Feedback do Nutricionista:</p>
                              <p className="text-sm text-blue-700">{plan.nutritionist_feedback}</p>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8">
                      <Brain className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                      <p className="text-gray-600 mb-4">Você ainda não tem planos gerados</p>
                      <Button 
                        onClick={generatePlan}
                        disabled={loading}
                        className="bg-green-600 hover:bg-green-700"
                      >
                        <Brain className="h-4 w-4 mr-2" />
                        {loading ? 'Gerando...' : 'Gerar Primeiro Plano'}
                      </Button>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>

            {/* Sidebar */}
            <div className="space-y-6">
              {/* Perfil Científico */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Perfil Científico</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Idade:</span>
                    <span className="text-sm font-medium">{currentUser?.age || 'N/A'} anos</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Peso:</span>
                    <span className="text-sm font-medium">{currentUser?.weight || 'N/A'} kg</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Altura:</span>
                    <span className="text-sm font-medium">{currentUser?.height || 'N/A'} cm</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Exercício:</span>
                    <span className="text-sm font-medium">{currentUser?.exercise_frequency || 0}x/sem</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Sono:</span>
                    <span className="text-sm font-medium">{currentUser?.sleep_hours || 'N/A'}h</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Estresse:</span>
                    <span className="text-sm font-medium">{currentUser?.stress_level || 'N/A'}/10</span>
                  </div>
                  
                  <Button 
                    variant="outline" 
                    size="sm" 
                    className="w-full mt-4"
                    onClick={() => setShowProfileForm(true)}
                  >
                    <Settings className="h-4 w-4 mr-2" />
                    Atualizar Perfil
                  </Button>
                </CardContent>
              </Card>

              {/* Histórico Familiar */}
              {(currentUser?.family_diabetes || currentUser?.family_hypertension || 
                currentUser?.family_obesity || currentUser?.family_heart_disease) && (
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg flex items-center gap-2">
                      <Heart className="h-5 w-5 text-red-500" />
                      Histórico Familiar
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    {currentUser.family_diabetes && (
                      <Badge variant="outline" className="mr-2">Diabetes</Badge>
                    )}
                    {currentUser.family_hypertension && (
                      <Badge variant="outline" className="mr-2">Hipertensão</Badge>
                    )}
                    {currentUser.family_obesity && (
                      <Badge variant="outline" className="mr-2">Obesidade</Badge>
                    )}
                    {currentUser.family_heart_disease && (
                      <Badge variant="outline" className="mr-2">Problemas Cardíacos</Badge>
                    )}
                  </CardContent>
                </Card>
              )}
            </div>
          </div>
        </div>
      </div>
    )
  }

  // Dashboard do Nutricionista
  const NutritionistDashboard = () => {
    const [pendingPlans, setPendingPlans] = useState([])
    const [dashboardStats, setDashboardStats] = useState({})
    const [selectedPlan, setSelectedPlan] = useState(null)
    const [loading, setLoading] = useState(false)

    useEffect(() => {
      loadDashboardData()
    }, [])

    const loadDashboardData = async () => {
      try {
        const [dashboardData, pendingData] = await Promise.all([
          apiRequest('/api/diet-plans/nutritionist-dashboard'),
          apiRequest('/api/diet-plans/pending')
        ])
        
        setDashboardStats(dashboardData.dashboard)
        setPendingPlans(pendingData.pending_plans)
      } catch (error) {
        console.error('Erro ao carregar dashboard:', error)
      }
    }

    const validatePlan = async (planId, action, feedback = '') => {
      setLoading(true)
      try {
        await apiRequest(`/api/diet-plans/${planId}/validate`, {
          method: 'POST',
          body: JSON.stringify({ action, feedback })
        })
        
        // Remove o plano da lista de pendentes
        setPendingPlans(prev => prev.filter(p => p.id !== planId))
        setSelectedPlan(null)
        
        // Atualiza estatísticas
        loadDashboardData()
        
        alert(`Plano ${action === 'approve' ? 'aprovado' : 'rejeitado'} com sucesso!`)
      } catch (error) {
        alert('Erro ao validar plano: ' + error.message)
      } finally {
        setLoading(false)
      }
    }

    return (
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center gap-2">
                <Stethoscope className="h-6 w-6 text-blue-600" />
                <span className="text-xl font-semibold">NutriAI</span>
                <Badge variant="secondary">Nutricionista</Badge>
              </div>
              <div className="flex items-center gap-4">
                <span className="text-sm text-gray-600">Dr. {currentUser?.name}</span>
                <Button variant="ghost" size="sm" onClick={() => setCurrentPage('login')}>
                  <LogOut className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>
        </header>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          
          {/* Estatísticas */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center gap-2">
                  <AlertCircle className="h-5 w-5 text-orange-600" />
                  <div>
                    <p className="text-sm text-gray-600">Pendentes</p>
                    <p className="text-2xl font-bold">{dashboardStats.pending_validation || 0}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center gap-2">
                  <CheckCircle className="h-5 w-5 text-green-600" />
                  <div>
                    <p className="text-sm text-gray-600">Aprovados</p>
                    <p className="text-2xl font-bold">{dashboardStats.my_approvals || 0}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center gap-2">
                  <Users className="h-5 w-5 text-blue-600" />
                  <div>
                    <p className="text-sm text-gray-600">Pacientes</p>
                    <p className="text-2xl font-bold">{dashboardStats.unique_patients || 0}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5 text-purple-600" />
                  <div>
                    <p className="text-sm text-gray-600">Taxa Aprovação</p>
                    <p className="text-2xl font-bold">{dashboardStats.approval_rate || 0}%</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            {/* Lista de Planos Pendentes */}
            <div className="lg:col-span-2">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <AlertCircle className="h-5 w-5" />
                    Planos Aguardando Validação ({pendingPlans.length})
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {pendingPlans.length > 0 ? (
                    <div className="space-y-4">
                      {pendingPlans.map((plan) => (
                        <div 
                          key={plan.id} 
                          className={`border rounded-lg p-4 cursor-pointer transition-colors ${
                            selectedPlan?.id === plan.id ? 'border-blue-500 bg-blue-50' : 'hover:bg-gray-50'
                          }`}
                          onClick={() => setSelectedPlan(plan)}
                        >
                          <div className="flex justify-between items-start">
                            <div>
                              <h4 className="font-medium">{plan.user_name}</h4>
                              <p className="text-sm text-gray-600">{plan.goal}</p>
                              <p className="text-xs text-gray-500">
                                Orçamento: R$ {plan.budget_per_meal}/refeição
                              </p>
                            </div>
                            <div className="text-right">
                              <Badge variant="secondary">Pendente</Badge>
                              <p className="text-xs text-gray-500 mt-1">
                                {new Date(plan.created_at).toLocaleDateString()}
                              </p>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8">
                      <CheckCircle className="h-12 w-12 text-green-500 mx-auto mb-4" />
                      <p className="text-gray-600">Todos os planos foram validados!</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>

            {/* Detalhes do Plano Selecionado */}
            <div>
              {selectedPlan ? (
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Validar Plano</CardTitle>
                    <CardDescription>
                      {selectedPlan.user_name} - {selectedPlan.goal}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    
                    {/* Dados do Paciente */}
                    <div>
                      <h4 className="font-medium mb-2">Dados do Paciente:</h4>
                      <div className="text-sm space-y-1">
                        <p><strong>Orçamento:</strong> R$ {selectedPlan.budget_per_meal}/refeição</p>
                        <p><strong>Restrições:</strong> {selectedPlan.dietary_restrictions || 'Nenhuma'}</p>
                      </div>
                    </div>

                    {/* Plano da IA */}
                    {selectedPlan.ai_plan && (
                      <div>
                        <h4 className="font-medium mb-2">Plano Gerado pela IA:</h4>
                        <div className="space-y-2 text-sm">
                          {selectedPlan.ai_plan.breakfast && (
                            <div>
                              <strong className="text-green-700">Café:</strong>
                              <p className="text-gray-600">{selectedPlan.ai_plan.breakfast.name || selectedPlan.ai_plan.breakfast}</p>
                            </div>
                          )}
                          {selectedPlan.ai_plan.lunch && (
                            <div>
                              <strong className="text-blue-700">Almoço:</strong>
                              <p className="text-gray-600">{selectedPlan.ai_plan.lunch.name || selectedPlan.ai_plan.lunch}</p>
                            </div>
                          )}
                          {selectedPlan.ai_plan.dinner && (
                            <div>
                              <strong className="text-purple-700">Jantar:</strong>
                              <p className="text-gray-600">{selectedPlan.ai_plan.dinner.name || selectedPlan.ai_plan.dinner}</p>
                            </div>
                          )}
                          
                          {selectedPlan.ai_plan.daily_totals && (
                            <div className="mt-3 p-3 bg-gray-50 rounded">
                              <strong>Totais Diários:</strong>
                              <p>Calorias: {selectedPlan.ai_plan.daily_totals.total_calories} kcal</p>
                              <p>Custo: R$ {selectedPlan.ai_plan.daily_totals.total_cost}</p>
                            </div>
                          )}
                        </div>
                      </div>
                    )}

                    {/* Ações */}
                    <div className="space-y-3 pt-4 border-t">
                      <Textarea 
                        placeholder="Feedback para o paciente (opcional)"
                        id="feedback"
                      />
                      
                      <div className="flex gap-2">
                        <Button 
                          onClick={() => {
                            const feedback = document.getElementById('feedback').value
                            validatePlan(selectedPlan.id, 'approve', feedback)
                          }}
                          disabled={loading}
                          className="flex-1 bg-green-600 hover:bg-green-700"
                        >
                          <CheckCircle className="h-4 w-4 mr-2" />
                          Aprovar
                        </Button>
                        
                        <Button 
                          onClick={() => {
                            const feedback = document.getElementById('feedback').value
                            validatePlan(selectedPlan.id, 'reject', feedback)
                          }}
                          disabled={loading}
                          variant="destructive"
                          className="flex-1"
                        >
                          <XCircle className="h-4 w-4 mr-2" />
                          Rejeitar
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ) : (
                <Card>
                  <CardContent className="p-8 text-center">
                    <MessageSquare className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-600">
                      Selecione um plano para validar
                    </p>
                  </CardContent>
                </Card>
              )}
            </div>
          </div>
        </div>
      </div>
    )
  }

  // Renderização principal
  if (currentPage === 'login') {
    return <LoginPage />
  } else if (currentPage === 'dashboard' && userType === 'user') {
    return <UserDashboard />
  } else if (currentPage === 'nutritionist-dashboard' && userType === 'nutritionist') {
    return <NutritionistDashboard />
  }

  return <LoginPage />
}

export default App

