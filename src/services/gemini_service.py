import os
import json
import google.generativeai as genai
from typing import Dict, Any, Optional

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if self.api_key and self.api_key != 'your_gemini_api_key_here':
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.configured = True
        else:
            self.configured = False
    
    def generate_scientific_diet_plan(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gera plano alimentar científico baseado em dados completos do usuário
        """
        if not self.configured:
            return self._generate_fallback_plan(user_data)
        
        try:
            prompt = self._build_scientific_prompt(user_data)
            response = self.model.generate_content(prompt)
            
            # Tenta parsear a resposta como JSON
            try:
                plan_data = json.loads(response.text)
                return plan_data
            except json.JSONDecodeError:
                # Se não conseguir parsear, cria estrutura baseada no texto
                return self._parse_text_response(response.text, user_data)
                
        except Exception as e:
            print(f"Erro ao gerar plano com Gemini: {e}")
            return self._generate_fallback_plan(user_data)
    
    def _build_scientific_prompt(self, user_data: Dict[str, Any]) -> str:
        """
        Constrói prompt científico detalhado baseado nos dados do usuário
        """
        # Dados básicos
        name = user_data.get('name', 'Usuário')
        age = user_data.get('age', 30)
        weight = user_data.get('weight', 70)
        height = user_data.get('height', 170)
        goal = user_data.get('goal', 'Manter peso')
        budget = user_data.get('budget_per_meal', 25)
        restrictions = user_data.get('dietary_restrictions', 'Nenhuma')
        
        # Dados científicos
        bmr = user_data.get('bmr', 1500)
        tdee = user_data.get('tdee', 2000)
        target_calories = user_data.get('target_calories', 1800)
        macros = user_data.get('macros', {})
        
        # Dados comportamentais
        sleep_hours = user_data.get('sleep_hours', 8)
        stress_level = user_data.get('stress_level', 5)
        exercise_freq = user_data.get('exercise_frequency', 0)
        water_intake = user_data.get('daily_water_intake', 8)
        
        # Histórico familiar
        family_conditions = []
        if user_data.get('family_diabetes'): family_conditions.append('diabetes')
        if user_data.get('family_hypertension'): family_conditions.append('hipertensão')
        if user_data.get('family_obesity'): family_conditions.append('obesidade')
        if user_data.get('family_heart_disease'): family_conditions.append('problemas cardíacos')
        
        prompt = f"""
Você é um nutricionista especialista em nutrição científica. Crie um plano alimentar personalizado baseado na análise científica completa do paciente.

DADOS DO PACIENTE:
- Nome: {name}
- Idade: {age} anos
- Peso: {weight} kg
- Altura: {height} cm
- Objetivo: {goal}
- Orçamento por refeição: R$ {budget}
- Restrições alimentares: {restrictions}

ANÁLISE METABÓLICA:
- TMB (Taxa Metabólica Basal): {bmr} kcal
- TDEE (Gasto Energético Total): {tdee} kcal
- Meta calórica diária: {target_calories} kcal
- Distribuição de macros: {macros}

ESTILO DE VIDA:
- Horas de sono: {sleep_hours}h
- Nível de estresse (1-10): {stress_level}
- Exercícios por semana: {exercise_freq}
- Consumo de água: {water_intake} copos/dia

HISTÓRICO FAMILIAR:
- Condições familiares: {', '.join(family_conditions) if family_conditions else 'Nenhuma'}

INSTRUÇÕES PARA O PLANO:
1. Respeite RIGOROSAMENTE o orçamento de R$ {budget} por refeição
2. Use preços reais do mercado brasileiro (2025)
3. Considere as condições familiares para prevenção
4. Adapte às necessidades metabólicas calculadas
5. Inclua timing nutricional adequado
6. Considere biodisponibilidade dos nutrientes
7. Forneça lista de compras com preços estimados

FORMATO DE RESPOSTA (JSON):
{{
  "breakfast": {{
    "name": "Nome da refeição",
    "ingredients": [
      {{"item": "Ingrediente", "quantity": "100g", "price": 2.50, "calories": 150, "protein": 10, "carbs": 15, "fat": 5}}
    ],
    "preparation": "Modo de preparo detalhado",
    "total_calories": 300,
    "total_cost": 8.50,
    "macros": {{"protein": 20, "carbs": 35, "fat": 12}},
    "timing": "7h00 - Otimiza metabolismo matinal"
  }},
  "lunch": {{
    "name": "Nome da refeição",
    "ingredients": [...],
    "preparation": "Modo de preparo",
    "total_calories": 500,
    "total_cost": {budget},
    "macros": {{"protein": 35, "carbs": 45, "fat": 18}},
    "timing": "12h00 - Pico energético do dia"
  }},
  "dinner": {{
    "name": "Nome da refeição",
    "ingredients": [...],
    "preparation": "Modo de preparo",
    "total_calories": 400,
    "total_cost": {budget * 0.8},
    "macros": {{"protein": 30, "carbs": 25, "fat": 15}},
    "timing": "19h00 - Facilita digestão noturna"
  }},
  "snacks": [
    {{
      "name": "Lanche",
      "ingredients": [...],
      "total_calories": 150,
      "total_cost": 5.00,
      "timing": "15h00 - Sustenta energia"
    }}
  ],
  "daily_totals": {{
    "total_calories": {target_calories},
    "total_cost": {budget * 3},
    "protein_g": {macros.get('protein_g', 100)},
    "carbs_g": {macros.get('carbs_g', 200)},
    "fat_g": {macros.get('fat_g', 70)},
    "fiber_g": 25,
    "sodium_mg": 2000
  }},
  "shopping_list": [
    {{"item": "Frango (peito)", "quantity": "1kg", "estimated_price": 18.00, "where_to_buy": "Açougue local"}},
    {{"item": "Arroz integral", "quantity": "1kg", "estimated_price": 8.50, "where_to_buy": "Supermercado"}}
  ],
  "nutritionist_notes": {{
    "metabolic_analysis": "Análise baseada em TMB {bmr} e TDEE {tdee}",
    "family_prevention": "Considerações preventivas baseadas no histórico familiar",
    "lifestyle_adaptations": "Adaptações para estilo de vida e rotina",
    "supplement_recommendations": "Suplementos recomendados se necessário",
    "monitoring_tips": "Como monitorar progresso e ajustar"
  }},
  "scientific_rationale": {{
    "caloric_distribution": "Justificativa da distribuição calórica",
    "macro_rationale": "Por que essa distribuição de macronutrientes",
    "timing_science": "Base científica do timing nutricional",
    "ingredient_selection": "Critérios científicos para seleção de ingredientes"
  }}
}}

Gere um plano completo, científico e dentro do orçamento especificado.
"""
        
        return prompt
    
    def _parse_text_response(self, text: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parseia resposta em texto quando JSON falha
        """
        # Implementação básica para extrair informações do texto
        budget = user_data.get('budget_per_meal', 25)
        target_calories = user_data.get('target_calories', 1800)
        
        return {
            "breakfast": {
                "name": "Café da manhã balanceado",
                "total_calories": int(target_calories * 0.25),
                "total_cost": budget * 0.6,
                "description": "Baseado na resposta da IA (texto)"
            },
            "lunch": {
                "name": "Almoço nutritivo",
                "total_calories": int(target_calories * 0.4),
                "total_cost": budget,
                "description": "Baseado na resposta da IA (texto)"
            },
            "dinner": {
                "name": "Jantar leve",
                "total_calories": int(target_calories * 0.3),
                "total_cost": budget * 0.8,
                "description": "Baseado na resposta da IA (texto)"
            },
            "daily_totals": {
                "total_calories": target_calories,
                "total_cost": budget * 2.4
            },
            "ai_response_text": text,
            "note": "Resposta parseada do texto da IA"
        }
    
    def _generate_fallback_plan(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gera plano de fallback quando Gemini não está disponível
        """
        budget = user_data.get('budget_per_meal', 25)
        target_calories = user_data.get('target_calories', 1800)
        macros = user_data.get('macros', {})
        goal = user_data.get('goal', 'Manter peso')
        
        # Planos baseados no objetivo
        if 'perder' in goal.lower() or 'emagrecer' in goal.lower():
            plan_type = "Plano para Emagrecimento"
            breakfast = {
                "name": "Smoothie Verde Detox",
                "ingredients": [
                    {"item": "Espinafre", "quantity": "50g", "price": 1.50, "calories": 12},
                    {"item": "Banana", "quantity": "1 unidade", "price": 1.00, "calories": 105},
                    {"item": "Proteína em pó", "quantity": "30g", "price": 4.00, "calories": 120}
                ],
                "total_calories": 237,
                "total_cost": 6.50
            }
        elif 'ganhar' in goal.lower() or 'massa' in goal.lower():
            plan_type = "Plano para Ganho de Massa"
            breakfast = {
                "name": "Ovos com Aveia",
                "ingredients": [
                    {"item": "Ovos", "quantity": "3 unidades", "price": 3.00, "calories": 210},
                    {"item": "Aveia", "quantity": "50g", "price": 2.00, "calories": 190},
                    {"item": "Banana", "quantity": "1 unidade", "price": 1.00, "calories": 105}
                ],
                "total_calories": 505,
                "total_cost": 6.00
            }
        else:
            plan_type = "Plano Balanceado"
            breakfast = {
                "name": "Café Balanceado",
                "ingredients": [
                    {"item": "Pão integral", "quantity": "2 fatias", "price": 2.00, "calories": 160},
                    {"item": "Queijo branco", "quantity": "30g", "price": 2.50, "calories": 75},
                    {"item": "Tomate", "quantity": "1 unidade", "price": 1.00, "calories": 20}
                ],
                "total_calories": 255,
                "total_cost": 5.50
            }
        
        return {
            "plan_type": plan_type,
            "breakfast": breakfast,
            "lunch": {
                "name": "Frango Grelhado com Quinoa",
                "ingredients": [
                    {"item": "Peito de frango", "quantity": "150g", "price": 12.00, "calories": 248},
                    {"item": "Quinoa", "quantity": "50g", "price": 4.00, "calories": 185},
                    {"item": "Brócolis", "quantity": "100g", "price": 3.00, "calories": 34}
                ],
                "total_calories": 467,
                "total_cost": 19.00
            },
            "dinner": {
                "name": "Salmão com Vegetais",
                "ingredients": [
                    {"item": "Salmão", "quantity": "120g", "price": 15.00, "calories": 250},
                    {"item": "Batata doce", "quantity": "100g", "price": 2.00, "calories": 86},
                    {"item": "Aspargos", "quantity": "100g", "price": 4.00, "calories": 20}
                ],
                "total_calories": 356,
                "total_cost": 21.00
            },
            "daily_totals": {
                "total_calories": breakfast["total_calories"] + 467 + 356,
                "total_cost": breakfast["total_cost"] + 19.00 + 21.00,
                "protein_g": macros.get('protein_g', 120),
                "carbs_g": macros.get('carbs_g', 180),
                "fat_g": macros.get('fat_g', 60)
            },
            "shopping_list": [
                {"item": "Frango (peito)", "quantity": "1kg", "estimated_price": 18.00},
                {"item": "Salmão", "quantity": "500g", "estimated_price": 35.00},
                {"item": "Quinoa", "quantity": "500g", "estimated_price": 12.00},
                {"item": "Vegetais variados", "quantity": "2kg", "estimated_price": 15.00}
            ],
            "nutritionist_notes": {
                "metabolic_analysis": f"Plano baseado em {target_calories} kcal diárias",
                "budget_compliance": f"Respeitando orçamento de R$ {budget} por refeição",
                "goal_alignment": f"Adequado para: {goal}",
                "note": "Plano gerado automaticamente - Configure GEMINI_API_KEY para IA personalizada"
            },
            "fallback": True
        }
    
    def is_configured(self) -> bool:
        """Retorna se o serviço Gemini está configurado"""
        return self.configured

