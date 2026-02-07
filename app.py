import os
from flask import Flask, render_template, request
import g4f

# Папка templates теперь на месте, поэтому инициализация стандартная
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.form.get('question')
    if not user_query:
        return render_template('results_page.html', question="Пустой запрос", content="Пожалуйста, введите вопрос.")

    prompt = f"Ты — эксперт по исламу. Ответь на вопрос: '{user_query}'. Разбери мнения мазхабов. Отвечай на русском."

    try:
        # Универсальный вызов ИИ
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        answer = response.replace('\n', '<br>') if response else "ИИ не ответил. Попробуйте еще раз."
    except Exception as e:
        answer = f"Ошибка: {str(e)}"

    return render_template('results_page.html', question=user_query, content=answer)

if __name__=='__main__':
    # ВАЖНО для Render: использование PORT из настроек сервера
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
