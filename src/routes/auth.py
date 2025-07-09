from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.models.nutriai_models import db, User
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Registra novo usuário com dados científicos completos"""
    try:
        data = request.get_json()
        
        # Validações básicas
        if not data.get('email') or not data.get('password') or not data.get('name'):
            return jsonify({'error': 'Email, senha e nome são obrigatórios'}), 400
        
        # Verifica se usuário já existe
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email já cadastrado'}), 400
        
        # Cria novo usuário
        user = User(
            email=data['email'],
            name=data['name'],
            user_type=data.get('user_type', 'user')
        )
        user.set_password(data['password'])
        
        # Dados básicos
        user.age = data.get('age')
        user.weight = data.get('weight')
        user.height = data.get('height')
        user.goal = data.get('goal')
        user.budget_per_meal = data.get('budget_per_meal')
        user.dietary_restrictions = data.get('dietary_restrictions')
        
        # Dados científicos antropométricos
        user.waist_circumference = data.get('waist_circumference')
        user.weight_6_months_ago = data.get('weight_6_months_ago')
        user.target_weight = data.get('target_weight')
        user.weight_variation_pattern = data.get('weight_variation_pattern')
        
        # Comportamento alimentar
        user.meal_times = data.get('meal_times')
        user.eating_speed = data.get('eating_speed')
        user.snacking_frequency = data.get('snacking_frequency')
        user.daily_water_intake = data.get('daily_water_intake')
        user.alcohol_consumption = data.get('alcohol_consumption')
        user.food_dislikes = data.get('food_dislikes')
        
        # Estilo de vida
        user.sleep_hours = data.get('sleep_hours')
        user.sleep_quality = data.get('sleep_quality')
        user.stress_level = data.get('stress_level')
        user.work_routine = data.get('work_routine')
        user.work_schedule = data.get('work_schedule')
        
        # Histórico familiar
        user.family_diabetes = data.get('family_diabetes', False)
        user.family_hypertension = data.get('family_hypertension', False)
        user.family_obesity = data.get('family_obesity', False)
        user.family_heart_disease = data.get('family_heart_disease', False)
        
        # Atividade física
        user.current_exercise = data.get('current_exercise')
        user.exercise_frequency = data.get('exercise_frequency')
        user.exercise_duration = data.get('exercise_duration')
        user.exercise_intensity = data.get('exercise_intensity')
        
        # Medicamentos
        user.current_medications = data.get('current_medications')
        user.supplements = data.get('supplements')
        user.medication_schedule = data.get('medication_schedule')
        
        # Autoavaliação
        user.energy_level = data.get('energy_level')
        user.disposition_level = data.get('disposition_level')
        user.digestive_issues = data.get('digestive_issues')
        user.bloating_frequency = data.get('bloating_frequency')
        user.hunger_satiety_pattern = data.get('hunger_satiety_pattern')
        
        # Objetivos
        user.monthly_weight_goal = data.get('monthly_weight_goal')
        user.total_timeframe = data.get('total_timeframe')
        user.main_motivation = data.get('main_motivation')
        user.previous_diet_experience = data.get('previous_diet_experience')
        
        # Campos específicos do nutricionista
        if user.user_type == 'nutritionist':
            user.crn_number = data.get('crn_number')
            user.specialization = data.get('specialization')
        
        db.session.add(user)
        db.session.commit()
        
        # Cria token de acesso
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(days=30)
        )
        
        return jsonify({
            'message': 'Usuário registrado com sucesso',
            'access_token': access_token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login do usuário"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email e senha são obrigatórios'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Email ou senha inválidos'}), 401
        
        # Cria token de acesso
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(days=30)
        )
        
        return jsonify({
            'message': 'Login realizado com sucesso',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Obtém perfil do usuário logado"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Atualiza perfil do usuário com dados científicos"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        data = request.get_json()
        
        # Atualiza dados básicos
        if 'name' in data:
            user.name = data['name']
        if 'age' in data:
            user.age = data['age']
        if 'weight' in data:
            user.weight = data['weight']
        if 'height' in data:
            user.height = data['height']
        if 'goal' in data:
            user.goal = data['goal']
        if 'budget_per_meal' in data:
            user.budget_per_meal = data['budget_per_meal']
        if 'dietary_restrictions' in data:
            user.dietary_restrictions = data['dietary_restrictions']
        
        # Atualiza dados científicos
        scientific_fields = [
            'waist_circumference', 'weight_6_months_ago', 'target_weight', 'weight_variation_pattern',
            'meal_times', 'eating_speed', 'snacking_frequency', 'daily_water_intake', 
            'alcohol_consumption', 'food_dislikes', 'sleep_hours', 'sleep_quality', 
            'stress_level', 'work_routine', 'work_schedule', 'family_diabetes', 
            'family_hypertension', 'family_obesity', 'family_heart_disease', 
            'current_exercise', 'exercise_frequency', 'exercise_duration', 'exercise_intensity',
            'current_medications', 'supplements', 'medication_schedule', 'energy_level',
            'disposition_level', 'digestive_issues', 'bloating_frequency', 'hunger_satiety_pattern',
            'monthly_weight_goal', 'total_timeframe', 'main_motivation', 'previous_diet_experience'
        ]
        
        for field in scientific_fields:
            if field in data:
                setattr(user, field, data[field])
        
        # Campos específicos do nutricionista
        if user.user_type == 'nutritionist':
            if 'crn_number' in data:
                user.crn_number = data['crn_number']
            if 'specialization' in data:
                user.specialization = data['specialization']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Perfil atualizado com sucesso',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@auth_bp.route('/validate-token', methods=['GET'])
@jwt_required()
def validate_token():
    """Valida se o token JWT ainda é válido"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Token inválido'}), 401
        
        return jsonify({
            'valid': True,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

