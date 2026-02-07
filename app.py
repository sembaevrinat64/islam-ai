import os
from flask import Flask, render_template, request
import g4f

# Инициализация приложения
# Теперь, когда ты создал папку templates, Flask найдет файлы автоматически
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.form.get('question')
    if not user_query:
        return render_template('results_page.html', question="Пустой запрос", content="Пожалуйста, введите вопрос.")

    # Инструкция для ИИ
    prompt = f"Ты — эксперт по исламу. Ответь на вопрос: '{user_query}'. Разбери мнения мазхабов, если есть отличия. Отвечай подробно на русском языке."

    try:
        # Запрос к нейросети
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        
        if response:
            # Список фраз-приветствий, которые нужно вырезать
            junk_phrases = [
                "Привет! Я Ариа помощник от опера",
                "созданный с использованием передовых технологии",
                "созданный с использованием передовых технологий",
                "как я могу помочь вам сегодня?",
                "Как я могу помочь вам сегодня?",
                "Я — Ариа,",
                "помощник от Opera"
            ]
            
            clean_answer = response
            for phrase in junk_phrases:
                clean_answer = clean_answer.replace(phrase, "")
            
            # Чистим лишние символы в начале и заменяем переносы на HTML-теги
            answer = clean_answer.strip().lstrip('.,! ').replace('\n', '<br>')
        else:
            answer = "К сожалению, сервер ИИ не прислал ответ. Попробуйте нажать кнопку еще раз."
            
    except Exception as e:
        answer = f"Произошла техническая ошибка: {str(e)}"

    return render_template('results_page.html', question=user_query, content=answer)

if __name__=='__main__':
    # Эта часть обязательна для работы на Render.com
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
