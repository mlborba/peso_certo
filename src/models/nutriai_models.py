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
    
    # NOVOS CAMPOS CIENTÍFICOS
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
    
    # Atividade Física
    current_exercise = db.Column(db.String(100))  # Tipo de exercício atual
    exercise_frequency = db.Column(db.Integer)  # Vezes por semana
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
            
        # Fator de atividade baseado no exercício
        activity_factors = {
            'sedentario': 1.2,
            'leve': 1.375,
            'moderado': 1.55,
            'intenso': 1.725,
            'muito_intenso': 1.9
        }
        
        # Determina fator baseado na frequência de exercício
        if not self.exercise_frequency or self.exercise_frequency == 0:
            factor = activity_factors['sedentario']
        elif self.exercise_frequency <= 2:
            factor = activity_factors['leve']
        elif self.exercise_frequency <= 4:
            factor = activity_factors['moderado']
        elif self.exercise_frequency <= 6:
            factor = activity_factors['intenso']
        else:
            factor = activity_factors['muito_intenso']
            
        return round(bmr * factor, 2)
    
    def calculate_target_calories(self):
        """Calcula calorias alvo baseado no objetivo"""
        tdee = self.calculate_tdee()
        if not tdee:
            return None
            
        if not self.goal:
            return tdee
            
        goal_lower = self.goal.lower()
        if 'perder' in goal_lower or 'emagrecer' in goal_lower:
            # Déficit de 20% para perda de peso
            return round(tdee * 0.8, 2)
        elif 'ganhar' in goal_lower or 'massa' in goal_lower:
            # Superávit de 15% para ganho de massa
            return round(tdee * 1.15, 2)
        else:
            # Manutenção
            return tdee
    
    def calculate_macros(self):
        """Calcula distribuição de macronutrientes"""
        target_calories = self.calculate_target_calories()
        if not target_calories:
            return None
            
        goal_lower = self.goal.lower() if self.goal else ''
        
        if 'ganhar' in goal_lower or 'massa' in goal_lower:
            # Alto em proteína para ganho de massa
            protein_ratio = 0.30
            carbs_ratio = 0.40
            fat_ratio = 0.30
        elif 'perder' in goal_lower or 'emagrecer' in goal_lower:
            # Moderado em proteína, baixo em carboidratos
            protein_ratio = 0.35
            carbs_ratio = 0.30
            fat_ratio = 0.35
        else:
            # Distribuição balanceada
            protein_ratio = 0.25
            carbs_ratio = 0.45
            fat_ratio = 0.30
        
        protein_g = round((target_calories * protein_ratio) / 4, 1)  # 4 cal/g
        carbs_g = round((target_calories * carbs_ratio) / 4, 1)      # 4 cal/g
        fat_g = round((target_calories * fat_ratio) / 9, 1)          # 9 cal/g
        
        return {
            'protein_g': protein_g,
            'carbs_g': carbs_g,
            'fat_g': fat_g,
            'total_calories': target_calories
        }
    
    def to_dict(self):
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
            'dietary_restrictions': self.dietary_restrictions,
            
            # Campos científicos
            'waist_circumference': self.waist_circumference,
            'weight_6_months_ago': self.weight_6_months_ago,
            'target_weight': self.target_weight,
            'weight_variation_pattern': self.weight_variation_pattern,
            'meal_times': self.meal_times,
            'eating_speed': self.eating_speed,
            'snacking_frequency': self.snacking_frequency,
            'daily_water_intake': self.daily_water_intake,
            'alcohol_consumption': self.alcohol_consumption,
            'food_dislikes': self.food_dislikes,
            'sleep_hours': self.sleep_hours,
            'sleep_quality': self.sleep_quality,
            'stress_level': self.stress_level,
            'work_routine': self.work_routine,
            'work_schedule': self.work_schedule,
            'family_diabetes': self.family_diabetes,
            'family_hypertension': self.family_hypertension,
            'family_obesity': self.family_obesity,
            'family_heart_disease': self.family_heart_disease,
            'current_exercise': self.current_exercise,
            'exercise_frequency': self.exercise_frequency,
            'exercise_duration': self.exercise_duration,
            'exercise_intensity': self.exercise_intensity,
            'current_medications': self.current_medications,
            'supplements': self.supplements,
            'medication_schedule': self.medication_schedule,
            'energy_level': self.energy_level,
            'disposition_level': self.disposition_level,
            'digestive_issues': self.digestive_issues,
            'bloating_frequency': self.bloating_frequency,
            'hunger_satiety_pattern': self.hunger_satiety_pattern,
            'monthly_weight_goal': self.monthly_weight_goal,
            'total_timeframe': self.total_timeframe,
            'main_motivation': self.main_motivation,
            'previous_diet_experience': self.previous_diet_experience,
            
            # Campos nutricionista
            'crn_number': self.crn_number,
            'specialization': self.specialization,
            
            # Cálculos científicos
            'bmr': self.calculate_bmr(),
            'tdee': self.calculate_tdee(),
            'target_calories': self.calculate_target_calories(),
            'macros': self.calculate_macros(),
            
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class DietPlan(db.Model):
    __tablename__ = 'diet_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    nutritionist_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Dados do plano
    goal = db.Column(db.Text, nullable=False)
    budget_per_meal = db.Column(db.Float, nullable=False)
    dietary_restrictions = db.Column(db.Text)
    
    # Plano gerado pela IA (JSON)
    ai_plan = db.Column(db.Text, nullable=False)  # JSON string
    
    # Status e validação
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    nutritionist_feedback = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    validated_at = db.Column(db.DateTime)
    
    def get_ai_plan(self):
        """Retorna o plano da IA como dicionário"""
        try:
            return json.loads(self.ai_plan)
        except:
            return {}
    
    def set_ai_plan(self, plan_dict):
        """Define o plano da IA a partir de um dicionário"""
        self.ai_plan = json.dumps(plan_dict)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'nutritionist_id': self.nutritionist_id,
            'goal': self.goal,
            'budget_per_meal': self.budget_per_meal,
            'dietary_restrictions': self.dietary_restrictions,
            'ai_plan': self.get_ai_plan(),
            'status': self.status,
            'nutritionist_feedback': self.nutritionist_feedback,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'validated_at': self.validated_at.isoformat() if self.validated_at else None,
            'user_name': self.user.name if self.user else None,
            'nutritionist_name': self.nutritionist.name if self.nutritionist else None
        }

class FoodPrice(db.Model):
    __tablename__ = 'food_prices'
    
    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(100), nullable=False)
    price_per_unit = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)  # kg, g, unidade, etc
    supermarket = db.Column(db.String(50))
    location = db.Column(db.String(100))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'food_name': self.food_name,
            'price_per_unit': self.price_per_unit,
            'unit': self.unit,
            'supermarket': self.supermarket,
            'location': self.location,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plan_type = db.Column(db.String(20), nullable=False)  # 'smart', 'plus'
    status = db.Column(db.String(20), default='active')  # active, cancelled, expired
    price = db.Column(db.Float, nullable=False)
    
    # Datas
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento
    user = db.relationship('User', backref='subscriptions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plan_type': self.plan_type,
            'status': self.status,
            'price': self.price,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

