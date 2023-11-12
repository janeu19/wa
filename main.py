from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Předpokládaná data
data = {
    "users": []
}

@app.route('/')
def home():
    return render_template('prvni_stranka.html', users=data['users'])

@app.route('/registrace', methods=['GET', 'POST'])
def registrace():
    if request.method == 'POST':
        nick = request.form.get('nick')
        je_plavec = request.form.get('je_plavec')
        kanoe_kamarad = request.form.get('kanoe_kamarad', '')

        # Kontroly dat formuláře (zadání 2 a 4)
        if not (je_plavec == '1' and 2 <= len(nick) <= 20 and (not kanoe_kamarad or 2 <= len(kanoe_kamarad) <= 20)):
            return jsonify({'error': 'Neplatné údaje'}), 400

        # Kontrola duplicity nickname (zadání 5)
        if any(user['nick'] == nick for user in data['users']):
            return jsonify({'error': 'Nickname již existuje'}), 400

        data['users'].append({'nick': nick, 'je_plavec': je_plavec, 'kanoe_kamarad': kanoe_kamarad})
        return jsonify({'success': 'Uživatel úspěšně zaregistrován'}), 200

    return render_template('druha_stranka.html')

@app.route('/api/check-nickname', methods=['GET'])
def check_nickname():
    nickname = request.args.get('nick')
    exists = any(user['nick'] == nickname for user in data['users'])
    return jsonify(exists=exists)

if __name__ == '__main__':
    app.run(debug=True)
