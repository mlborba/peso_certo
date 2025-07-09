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

app = Flask(__name__, static_folder='../static', static_url_path='')

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

# Rota para servir frontend
@app.route('/')
def index():
    return app.send_static_file('index.html')

# Rota de status da API
@app.route('/api/status')
def api_status():
    from src.models.nutriai_models import User, DietPlan
    
    try:
        # Conta usuários e planos
        total_users = User.query.count()
        total_plans = DietPlan.query.count()
        pending_validation = DietPlan.query.filter_by(status='pending').count()
        
        # Verifica se IA Gemini está configurada
        gemini_configured = bool(os.getenv('GEMINI_API_KEY'))
        
        # Determina tipo de banco
        database_type = "Neon" if "neon" in app.config['SQLALCHEMY_DATABASE_URI'] else "SQLite"
        
        return {
            "status": "online",
            "message": "NutriAI API Científica funcionando",
            "version": "2.0.0",
            "database": database_type,
            "gemini_configured": gemini_configured,
            "statistics": {
                "total_users": total_users,
                "total_plans": total_plans,
                "pending_validation": pending_validation
            },
            "features": {
                "scientific_fields": 50,
                "metabolic_calculations": True,
                "ai_personalization": True,
                "nutritionist_validation": True
            },
            "test_users": {
                "user": "ana@email.com / 123456",
                "nutritionist": "maria@nutricionista.com / 123456"
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Erro no banco de dados: {str(e)}",
            "database": "disconnected"
        }, 500

# Inicialização do banco e dados de exemplo
@app.before_first_request
def create_tables():
    from src.models.nutriai_models import User, DietPlan
    
    try:
        db.create_all()
        
        # Usuário exemplo com dados científicos CORRIGIDOS
        if not User.query.filter_by(email='ana@email.com').first():
            user = User(
                email='ana@email.com',
                name='Ana Silva',
                user_type='user',
                age=28,
                weight=65.5,
                height=165.0,
                goal='perder_peso',
                budget_per_meal=25.0,
                dietary_restrictions='Sem lactose',
                waist_circumference=78.0,
                weight_6_months_ago=70.0,
                target_weight=60.0,
                weight_variation_pattern='engorda_facil',
                meal_times='{"cafe": "07:00", "almoco": "12:00", "jantar": "19:00"}',
                eating_speed='normal',
                snacking_frequency='raramente',
                daily_water_intake=8,
                alcohol_consumption='social',
                food_dislikes='Brócolis, fígado',
                sleep_hours=7.5,
                sleep_quality='regular',
                stress_level=7,
                work_routine='sedentario',
                work_schedule='comercial',
                family_diabetes=True,
                family_hypertension=True,
                family_obesity=False,
                family_heart_disease=False,
                current_exercise='Caminhada',
                exercise_frequency='leve',  # ✅ CORRIGIDO: String em vez de Integer
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
                age=35,
                weight=85.0,
                height=178.0,
                goal='ganhar_massa',
                budget_per_meal=30.0,
                dietary_restrictions='Nenhuma',
                exercise_frequency='moderado',  # ✅ CORRIGIDO: String em vez de Integer
                stress_level=5,
                energy_level=8,
                family_diabetes=False,
                family_hypertension=False
            )
            user2.set_password('123456')
            db.session.add(user2)
        
        db.session.commit()
        print("✅ Banco de dados inicializado com sucesso")
        
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")
        db.session.rollback()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

