import os
from flask import Flask, render_template, request
import g4f

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.form.get('question')
    if not user_query:
        return render_template('results_page.html', question="Пустой запрос", content="Пожалуйста, введите вопрос.")

    # Добавляем в промпт требование отвечать без приветствий
    prompt = f"Инструкция: Отвечай строго по существу, без приветствий и представления себя. Вопрос: '{user_query}'. Разбери мнения мазхабов. Отвечай подробно на русском языке."

    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        
        if response:
            # Расширенный список фраз для удаления (английское и русское написание)
            junk = [
                "Привет! Я Aria", "Привет! Я Ариа",
                "твой помощник", "помощник от Opera", "помощник от опера",
                "созданный с использованием передовых AI-моделей",
                "созданный с использованием передовых технологий",
                "от OpenAI и Google", "от Google и OpenAI",
                "С удовольствием расскажу тебе",
                "как я могу помочь вам сегодня?",
                "Я — Aria,", "Я - Aria,", "Я Aria,"
            ]
            
            clean_answer = response
            for phrase in junk:
                # Используем замену без учета регистра, если это возможно, 
                # но для надежности просто перечисляем варианты
                clean_answer = clean_answer.replace(phrase, "")
            
            # Финальная чистка: убираем остатки знаков препинания и пробелов в начале
            # Это удалит лишние запятые и точки, оставшиеся после удаления "Я Aria,"
            answer = clean_answer.strip().lstrip('.,! :;-').replace('\n', '<br>')
            
            # Если после чистки ответ пустой (вдруг всё было приветствием)
            if not answer:
                answer = response.replace('\n', '<br>')
        else:
            answer = "ИИ не прислал ответ. Попробуйте еще раз."
            
    except Exception as e:
        answer = f"Ошибка: {str(e)}"

    return render_template('results_page.html', question=user_query, content=answer)

if __name__=='__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
