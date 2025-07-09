import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Importa modelos e rotas
from src.models.nutriai_models import db
from src.routes.auth import auth_bp
from src.routes.diet_plans import diet_plans_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configurações
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'nutriai_flask_secret_key_2025')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'nutriai_super_secret_key_2025')

# CORS
CORS(app, origins=os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173').split(','))

# JWT
jwt = JWTManager(app)

# Banco de dados
database_url = os.getenv('NEON_DATABASE_URL')
if database_url and database_url != 'your_neon_database_url_here':
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    print("✅ Conectado ao banco Neon")
else:
    # Fallback para SQLite local
    os.makedirs(os.path.join(os.path.dirname(__file__), 'database'), exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
    print("⚠️ Usando SQLite local. Configure NEON_DATABASE_URL para produção.")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa banco
db.init_app(app)

# Registra blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(diet_plans_bp, url_prefix='/api/diet-plans')

# Cria tabelas e dados de exemplo
with app.app_context():
    db.create_all()
    
    # Cria usuários de exemplo se não existirem
    from src.models.nutriai_models import User
    
    # Usuário exemplo com dados científicos
    if not User.query.filter_by(email='ana@email.com').first():
        user = User(
            email='ana@email.com',
            name='Ana Silva',
            user_type='user',
            age=34,
            weight=70.0,
            height=165.0,
            goal='Perder peso e controlar hipertensão',
            budget_per_meal=25.00,
            dietary_restrictions='Sem lactose',
            
            # Dados científicos de exemplo
            waist_circumference=85.0,
            weight_6_months_ago=75.0,
            target_weight=65.0,
            weight_variation_pattern='engorda_facil',
            eating_speed='rapido',
            snacking_frequency='frequentemente',
            daily_water_intake=6,
            alcohol_consumption='social',
            sleep_hours=7.0,
            sleep_quality='regular',
            stress_level=7,
            work_routine='sedentario',
            work_schedule='comercial',
            family_diabetes=True,
            family_hypertension=True,
            family_obesity=False,
            family_heart_disease=False,
            current_exercise='Caminhada',
            exercise_frequency=2,
            exercise_duration=30,
            exercise_intensity='leve',
            energy_level=6,
            disposition_level=7,
            bloating_frequency='frequentemente',
            hunger_satiety_pattern='muita_fome',
            monthly_weight_goal=2.0,
            total_timeframe=6,
            main_motivation='Melhorar saúde e autoestima',
            previous_diet_experience='Já tentei várias dietas mas sempre desisto'
        )
        user.set_password('123456')
        db.session.add(user)
    
    # Nutricionista exemplo
    if not User.query.filter_by(email='maria@nutricionista.com').first():
        nutritionist = User(
            email='maria@nutricionista.com',
            name='Dr. Maria Oliveira',
            user_type='nutritionist',
            crn_number='CRN-3 12345',
            specialization='Nutrição Clínica e Esportiva'
        )
        nutritionist.set_password('123456')
        db.session.add(nutritionist)
    
    # Segundo usuário exemplo
    if not User.query.filter_by(email='carlos@email.com').first():
        user2 = User(
            email='carlos@email.com',
            name='Carlos Santos',
            user_type='user',
            age=28,
            weight=80.0,
            height=180.0,
            goal='Ganhar massa muscular',
            budget_per_meal=30.00,
            dietary_restrictions='Nenhuma',
            
            # Dados científicos diferentes
            waist_circumference=78.0,
            weight_6_months_ago=75.0,
            target_weight=85.0,
            weight_variation_pattern='estavel',
            eating_speed='normal',
            snacking_frequency='raramente',
            daily_water_intake=10,
            alcohol_consumption='nunca',
            sleep_hours=8.0,
            sleep_quality='boa',
            stress_level=4,
            work_routine='ativo',
            work_schedule='comercial',
            family_diabetes=False,
            family_hypertension=False,
            family_obesity=False,
            family_heart_disease=False,
            current_exercise='Musculação',
            exercise_frequency=5,
            exercise_duration=90,
            exercise_intensity='intenso',
            energy_level=8,
            disposition_level=9,
            bloating_frequency='nunca',
            hunger_satiety_pattern='normal',
            monthly_weight_goal=1.0,
            total_timeframe=12,
            main_motivation='Competir em fisiculturismo',
            previous_diet_experience='Sempre mantive dieta regrada'
        )
        user2.set_password('123456')
        db.session.add(user2)
    
    db.session.commit()
    print("✅ Usuários de exemplo criados")

# Rota para servir frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return {
            "message": "NutriAI Backend - Sistema Científico de Nutrição",
            "version": "2.0.0",
            "features": [
                "50+ campos científicos para análise nutricional",
                "Cálculos TMB, TDEE e macronutrientes",
                "IA Gemini para planos personalizados",
                "Sistema completo usuário/nutricionista",
                "Banco Neon para persistência"
            ],
            "endpoints": {
                "status": "/api/status",
                "auth": "/api/auth/*",
                "diet_plans": "/api/diet-plans/*"
            }
        }

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return {
                "message": "Frontend não encontrado",
                "note": "Coloque os arquivos do React na pasta static/",
                "backend_status": "funcionando"
            }

# Rota de status da API
@app.route('/api/status')
def api_status():
    from src.services.gemini_service import GeminiService
    
    gemini_service = GeminiService()
    
    # Estatísticas do banco
    from src.models.nutriai_models import User, DietPlan
    total_users = User.query.count()
    total_plans = DietPlan.query.count()
    pending_plans = DietPlan.query.filter_by(status='pending').count()
    
    return {
        'status': 'online',
        'message': 'NutriAI API Científica funcionando',
        'version': '2.0.0',
        'database': 'Neon' if 'neon' in app.config['SQLALCHEMY_DATABASE_URI'] else 'SQLite',
        'gemini_configured': gemini_service.is_configured(),
        'features': {
            'scientific_fields': 50,
            'metabolic_calculations': True,
            'ai_personalization': True,
            'nutritionist_validation': True
        },
        'statistics': {
            'total_users': total_users,
            'total_plans': total_plans,
            'pending_validation': pending_plans
        },
        'test_users': {
            'user': 'ana@email.com / 123456',
            'nutritionist': 'maria@nutricionista.com / 123456'
        }
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

