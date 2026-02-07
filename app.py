from flask import Flask, render_template, request
import g4f

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.form.get('question')
    prompt = f"Эксперт по исламу. Кратко и четко ответь на вопрос: '{user_query}', учитывая мазхабы."
    
    try:
        # Пытаемся использовать более быстрых провайдеров через список
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4, # GPT-4 часто работает качественнее и быстрее
            messages=[{"role": "user", "content": prompt}],
            provider=g4f.Provider.Bing, # Bing обычно один из самых быстрых
            stream=False # Отключаем потоковую передачу для скорости обработки
        )
        answer = response.replace('\n', '<br>')
    except Exception:
        # Если быстрый провайдер упал, используем стандартный
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.replace('\n', '<br>')

    return render_template('results_page.html', question=user_query, content=answer)

if __name__=='__main__':
    app.run(debug=True)