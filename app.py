from flask import Flask, render_template, request
import g4f
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.form.get('question')
    if not user_query:
        return render_template('results_page.html', question="Пустой запрос", content="Пожалуйста, введите вопрос.")

    prompt = f"Ты — эксперт по исламу. Ответь подробно на вопрос: '{user_query}'. Упомяни мнения разных мазхабов, если есть отличия. Отвечай на русском языке."

    try:
        # Используем асинхронный вызов через обертку, которая лучше работает на серверах
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
            # Убираем жесткую привязку к провайдерам, даем системе выбрать лучший доступный
        )
        
        if response:
            answer = response.replace('\n', '<br>')
        else:
            answer = "К сожалению, ИИ не смог сформировать ответ в данный момент. Попробуйте еще раз."
            
    except Exception as e:
        # Выводим конкретную ошибку в интерфейс, чтобы понять, в чем дело
        answer = f"Произошла ошибка на сервере: {str(e)}. Попробуйте сменить формулировку вопроса."

    return render_template('results_page.html', question=user_query, content=answer)

if __name__=='__main__':
    # Настройка порта для Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
