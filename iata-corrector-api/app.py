from flask import Flask, render_template, request, jsonify
from upload_api import upload_api
from fine_tune_api import fine_tune_api
from dotenv import load_dotenv
load_dotenv()

from corrector import correct_message

app = Flask(__name__)

app.register_blueprint(upload_api)
app.register_blueprint(fine_tune_api)
@app.route('/', methods=['GET', 'POST'])
def home():
    corrected = ""
    original = ""
    if request.method == 'POST':
        original = request.form['message']
        try:
            corrected = correct_message(original)
        except Exception as e:
            corrected = f"Error: {e}\nPlease check internet or OpenAI configuration."
    return render_template('index.html', original=original, corrected=corrected)

@app.route('/api/correct', methods=['POST'])
def api_correct():
    try:
        data = request.get_json()
        message = data.get('message', '')
        corrected = correct_message(message)
        return jsonify({'corrected': corrected}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000, debug=True)
