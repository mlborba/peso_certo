from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.nutriai_models import db, User, DietPlan
from src.services.gemini_service import GeminiService
from datetime import datetime

diet_plans_bp = Blueprint('diet_plans', __name__)

@diet_plans_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_diet_plan():
    """Gera plano alimentar científico personalizado"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        if user.user_type != 'user':
            return jsonify({'error': 'Apenas usuários podem gerar planos'}), 403
        
        # Verifica se dados básicos estão completos
        if not user.weight or not user.height or not user.age or not user.goal:
            return jsonify({
                'error': 'Dados básicos incompletos',
                'required': ['weight', 'height', 'age', 'goal'],
                'message': 'Complete seu perfil para gerar planos personalizados'
            }), 400
        
        # Prepara dados científicos para a IA
        user_data = user.to_dict()
        
        # Inicializa serviço Gemini
        gemini_service = GeminiService()
        
        # Gera plano com IA
        ai_plan = gemini_service.generate_scientific_diet_plan(user_data)
        
        # Cria registro do plano no banco
        diet_plan = DietPlan(
            user_id=user.id,
            goal=user.goal,
            budget_per_meal=user.budget_per_meal or 25.0,
            dietary_restrictions=user.dietary_restrictions
        )
        diet_plan.set_ai_plan(ai_plan)
        
        db.session.add(diet_plan)
        db.session.commit()
        
        return jsonify({
            'message': 'Plano alimentar gerado com sucesso',
            'plan': diet_plan.to_dict(),
            'gemini_configured': gemini_service.is_configured(),
            'scientific_analysis': {
                'bmr': user.calculate_bmr(),
                'tdee': user.calculate_tdee(),
                'target_calories': user.calculate_target_calories(),
                'macros': user.calculate_macros()
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@diet_plans_bp.route('/my-plans', methods=['GET'])
@jwt_required()
def get_my_plans():
    """Obtém histórico de planos do usuário"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Busca planos do usuário
        plans = DietPlan.query.filter_by(user_id=user.id).order_by(DietPlan.created_at.desc()).all()
        
        return jsonify({
            'plans': [plan.to_dict() for plan in plans],
            'total': len(plans),
            'user_profile': {
                'bmr': user.calculate_bmr(),
                'tdee': user.calculate_tdee(),
                'target_calories': user.calculate_target_calories(),
                'macros': user.calculate_macros()
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@diet_plans_bp.route('/pending', methods=['GET'])
@jwt_required()
def get_pending_plans():
    """Obtém planos pendentes de validação (para nutricionistas)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        if user.user_type != 'nutritionist':
            return jsonify({'error': 'Apenas nutricionistas podem acessar planos pendentes'}), 403
        
        # Busca planos pendentes
        pending_plans = DietPlan.query.filter_by(status='pending').order_by(DietPlan.created_at.desc()).all()
        
        return jsonify({
            'pending_plans': [plan.to_dict() for plan in pending_plans],
            'total': len(pending_plans),
            'nutritionist_stats': {
                'total_validated': DietPlan.query.filter_by(nutritionist_id=user.id).count(),
                'approved': DietPlan.query.filter_by(nutritionist_id=user.id, status='approved').count(),
                'rejected': DietPlan.query.filter_by(nutritionist_id=user.id, status='rejected').count()
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@diet_plans_bp.route('/<int:plan_id>/validate', methods=['POST'])
@jwt_required()
def validate_plan(plan_id):
    """Valida plano alimentar (nutricionista)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        if user.user_type != 'nutritionist':
            return jsonify({'error': 'Apenas nutricionistas podem validar planos'}), 403
        
        plan = DietPlan.query.get(plan_id)
        if not plan:
            return jsonify({'error': 'Plano não encontrado'}), 404
        
        data = request.get_json()
        action = data.get('action')  # 'approve' ou 'reject'
        feedback = data.get('feedback', '')
        
        if action not in ['approve', 'reject']:
            return jsonify({'error': 'Ação deve ser "approve" ou "reject"'}), 400
        
        # Atualiza plano
        plan.status = 'approved' if action == 'approve' else 'rejected'
        plan.nutritionist_id = user.id
        plan.nutritionist_feedback = feedback
        plan.validated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': f'Plano {"aprovado" if action == "approve" else "rejeitado"} com sucesso',
            'plan': plan.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@diet_plans_bp.route('/<int:plan_id>', methods=['GET'])
@jwt_required()
def get_plan_details(plan_id):
    """Obtém detalhes de um plano específico"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        plan = DietPlan.query.get(plan_id)
        if not plan:
            return jsonify({'error': 'Plano não encontrado'}), 404
        
        # Verifica permissão
        if user.user_type == 'user' and plan.user_id != user.id:
            return jsonify({'error': 'Acesso negado'}), 403
        
        # Nutricionistas podem ver qualquer plano
        if user.user_type == 'nutritionist':
            # Inclui dados científicos do usuário para análise
            plan_user = User.query.get(plan.user_id)
            plan_dict = plan.to_dict()
            plan_dict['user_scientific_data'] = {
                'bmr': plan_user.calculate_bmr(),
                'tdee': plan_user.calculate_tdee(),
                'target_calories': plan_user.calculate_target_calories(),
                'macros': plan_user.calculate_macros(),
                'anthropometric': {
                    'weight': plan_user.weight,
                    'height': plan_user.height,
                    'waist_circumference': plan_user.waist_circumference,
                    'weight_6_months_ago': plan_user.weight_6_months_ago
                },
                'lifestyle': {
                    'sleep_hours': plan_user.sleep_hours,
                    'stress_level': plan_user.stress_level,
                    'exercise_frequency': plan_user.exercise_frequency
                },
                'family_history': {
                    'diabetes': plan_user.family_diabetes,
                    'hypertension': plan_user.family_hypertension,
                    'obesity': plan_user.family_obesity,
                    'heart_disease': plan_user.family_heart_disease
                }
            }
            return jsonify({'plan': plan_dict}), 200
        
        return jsonify({'plan': plan.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@diet_plans_bp.route('/nutritionist-dashboard', methods=['GET'])
@jwt_required()
def nutritionist_dashboard():
    """Dashboard do nutricionista com estatísticas"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        if user.user_type != 'nutritionist':
            return jsonify({'error': 'Apenas nutricionistas podem acessar este dashboard'}), 403
        
        # Estatísticas gerais
        total_plans = DietPlan.query.count()
        pending_plans = DietPlan.query.filter_by(status='pending').count()
        my_validations = DietPlan.query.filter_by(nutritionist_id=user.id).count()
        my_approvals = DietPlan.query.filter_by(nutritionist_id=user.id, status='approved').count()
        my_rejections = DietPlan.query.filter_by(nutritionist_id=user.id, status='rejected').count()
        
        # Taxa de aprovação
        approval_rate = (my_approvals / my_validations * 100) if my_validations > 0 else 0
        
        # Planos recentes pendentes
        recent_pending = DietPlan.query.filter_by(status='pending').order_by(DietPlan.created_at.desc()).limit(5).all()
        
        # Usuários únicos atendidos
        unique_users = db.session.query(DietPlan.user_id).filter_by(nutritionist_id=user.id).distinct().count()
        
        return jsonify({
            'dashboard': {
                'total_plans_system': total_plans,
                'pending_validation': pending_plans,
                'my_validations': my_validations,
                'my_approvals': my_approvals,
                'my_rejections': my_rejections,
                'approval_rate': round(approval_rate, 1),
                'unique_patients': unique_users
            },
            'recent_pending': [plan.to_dict() for plan in recent_pending],
            'nutritionist': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

