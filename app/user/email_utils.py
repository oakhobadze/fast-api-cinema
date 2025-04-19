import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "sandroahobadze@gmail.com"
SMTP_PASS = "xxhj xshz ucyi hqjm"

def send_activation_email(to_email: str, token: str):
    subject = "Activate your account"
    link = f"http://127.0.0.1:8000/users/activate/{token}"
    body = f"Click the link to activate your account: {link}"

    message = MIMEMultipart()
    message["From"] = SMTP_USER
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, to_email, message.as_string())
        print(f"[INFO] Activation email sent to {to_email}")
    except Exception as e:
        print(f"[ERROR] Failed to send email to {to_email}: {e}")

def send_reset_password_email(to_email: str, token: str, new_password: str):
    subject = "Reset your password"
    link = f"http://127.0.0.1:8000/users/reset-password/{token}?new_password={new_password}"
    body = f"Click the link to reset your password: {link}"

    message = MIMEMultipart()
    message["From"] = SMTP_USER
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, to_email, message.as_string())
        print(f"[INFO] Password reset email sent to {to_email}")
    except Exception as e:
        print(f"[ERROR] Failed to send password reset email to {to_email}: {e}")
