from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('prvni_stranka.html'), 200

@app.route('/registrace', methods=['GET', 'POST'])
def registrace():
    if request.method == 'POST':
        # Zde můžete zpracovat data z formuláře, pokud budete chtít.

        # Přesměrování zpět na úvodní stránku po odeslání formuláře
        return render_template('prvni_stranka.html'), 200
    return render_template('registrace.html'), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
