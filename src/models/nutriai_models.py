from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'user' ou 'nutritionist'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Campos básicos do usuário
    age = db.Column(db.Integer)
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    goal = db.Column(db.Text)
    budget_per_meal = db.Column(db.Float)
    dietary_restrictions = db.Column(db.Text)
    
    # CAMPOS CIENTÍFICOS CORRIGIDOS
    # Dados Antropométricos
    waist_circumference = db.Column(db.Float)  # Circunferência abdominal (cm)
    weight_6_months_ago = db.Column(db.Float)  # Peso há 6 meses
    target_weight = db.Column(db.Float)  # Peso meta
    weight_variation_pattern = db.Column(db.String(50))  # "engorda_facil", "emagrece_facil", "estavel"
    
    # Comportamento Alimentar
    meal_times = db.Column(db.Text)  # JSON com horários das refeições
    eating_speed = db.Column(db.String(20))  # "rapido", "normal", "devagar"
    snacking_frequency = db.Column(db.String(20))  # "nunca", "raramente", "frequentemente"
    daily_water_intake = db.Column(db.Integer)  # Copos de água por dia
    alcohol_consumption = db.Column(db.String(30))  # "nunca", "social", "regular", "diario"
    food_dislikes = db.Column(db.Text)  # Alimentos que odeia
    
    # Estilo de Vida
    sleep_hours = db.Column(db.Float)  # Horas de sono por noite
    sleep_quality = db.Column(db.String(20))  # "ruim", "regular", "boa", "excelente"
    stress_level = db.Column(db.Integer)  # 1-10
    work_routine = db.Column(db.String(30))  # "sedentario", "ativo", "muito_ativo"
    work_schedule = db.Column(db.String(50))  # "comercial", "noturno", "irregular"
    
    # Histórico Familiar
    family_diabetes = db.Column(db.Boolean, default=False)
    family_hypertension = db.Column(db.Boolean, default=False)
    family_obesity = db.Column(db.Boolean, default=False)
    family_heart_disease = db.Column(db.Boolean, default=False)
    
    # Atividade Física - CORRIGIDO
    current_exercise = db.Column(db.String(100))  # Tipo de exercício atual
    exercise_frequency = db.Column(db.String(30))  # ✅ MUDOU: "sedentario", "leve", "moderado", "intenso", "muito_intenso"
    exercise_duration = db.Column(db.Integer)  # Minutos por sessão
    exercise_intensity = db.Column(db.String(20))  # "leve", "moderado", "intenso"
    
    # Medicamentos
    current_medications = db.Column(db.Text)  # Lista de medicamentos
    supplements = db.Column(db.Text)  # Suplementos em uso
    medication_schedule = db.Column(db.Text)  # Horários dos medicamentos
    
    # Autoavaliação
    energy_level = db.Column(db.Integer)  # 1-10
    disposition_level = db.Column(db.Integer)  # 1-10
    digestive_issues = db.Column(db.Text)  # Problemas digestivos
    bloating_frequency = db.Column(db.String(20))  # "nunca", "raramente", "frequentemente"
    hunger_satiety_pattern = db.Column(db.String(30))  # "muita_fome", "normal", "pouca_fome"
    
    # Objetivos
    monthly_weight_goal = db.Column(db.Float)  # Meta de peso por mês (kg)
    total_timeframe = db.Column(db.Integer)  # Prazo total em meses
    main_motivation = db.Column(db.Text)  # Motivação principal
    previous_diet_experience = db.Column(db.Text)  # Experiência anterior com dietas
    
    # Campos específicos do nutricionista
    crn_number = db.Column(db.String(20))  # Número do CRN
    specialization = db.Column(db.String(100))
    
    # Relacionamentos
    diet_plans = db.relationship('DietPlan', backref='user', lazy=True, foreign_keys='DietPlan.user_id')
    validated_plans = db.relationship('DietPlan', backref='nutritionist', lazy=True, foreign_keys='DietPlan.nutritionist_id')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def calculate_bmr(self):
        """Calcula Taxa Metabólica Basal usando Harris-Benedict"""
        if not self.weight or not self.height or not self.age:
            return None
            
        # Assumindo gênero masculino se não especificado (pode ser melhorado)
        # Fórmula Harris-Benedict revisada
        if hasattr(self, 'gender') and self.gender == 'female':
            bmr = 447.593 + (9.247 * self.weight) + (3.098 * self.height) - (4.330 * self.age)
        else:
            bmr = 88.362 + (13.397 * self.weight) + (4.799 * self.height) - (5.677 * self.age)
        
        return round(bmr, 2)
    
    def calculate_tdee(self):
        """Calcula Gasto Energético Total Diário"""
        bmr = self.calculate_bmr()
        if not bmr:
            return None
        
        # Fatores de atividade baseados em exercise_frequency
        activity_factors = {
            'sedentario': 1.2,
            'leve': 1.375,      # 1-3x/semana
            'moderado': 1.55,   # 3-5x/semana
            'intenso': 1.725,   # 6-7x/semana
            'muito_intenso': 1.9  # 2x/dia
        }
        
        factor = activity_factors.get(self.exercise_frequency, 1.2)
        tdee = bmr * factor
        
        return round(tdee, 2)
    
    def calculate_macros(self):
        """Calcula distribuição de macronutrientes"""
        tdee = self.calculate_tdee()
        if not tdee:
            return None
        
        # Ajusta calorias baseado no objetivo
        if self.goal == 'perder_peso':
            calories = tdee * 0.85  # Déficit de 15%
        elif self.goal == 'ganhar_peso':
            calories = tdee * 1.15  # Superávit de 15%
        else:
            calories = tdee  # Manutenção
        
        # Distribuição padrão de macros
        protein_ratio = 0.25  # 25% proteína
        carb_ratio = 0.45     # 45% carboidrato
        fat_ratio = 0.30      # 30% gordura
        
        protein_g = (calories * protein_ratio) / 4  # 4 cal/g
        carb_g = (calories * carb_ratio) / 4        # 4 cal/g
        fat_g = (calories * fat_ratio) / 9          # 9 cal/g
        
        return {
            'calories': round(calories, 0),
            'protein_g': round(protein_g, 1),
            'carb_g': round(carb_g, 1),
            'fat_g': round(fat_g, 1)
        }
    
    def to_dict(self):
        """Converte usuário para dicionário"""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'user_type': self.user_type,
            'age': self.age,
            'weight': self.weight,
            'height': self.height,
            'goal': self.goal,
            'budget_per_meal': self.budget_per_meal,
            'exercise_frequency': self.exercise_frequency,
            'bmr': self.calculate_bmr(),
            'tdee': self.calculate_tdee(),
            'macros': self.calculate_macros(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class DietPlan(db.Model):
    __tablename__ = 'diet_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    nutritionist_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    plan_data = db.Column(db.Text)  # JSON com o plano completo
    
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    validated_at = db.Column(db.DateTime)
    
    # Feedback do nutricionista
    nutritionist_feedback = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'nutritionist_id': self.nutritionist_id,
            'title': self.title,
            'description': self.description,
            'plan_data': json.loads(self.plan_data) if self.plan_data else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'validated_at': self.validated_at.isoformat() if self.validated_at else None,
            'nutritionist_feedback': self.nutritionist_feedback
        }

