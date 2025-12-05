from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl

def send_mail(email: str, subject: str, body: str):
    sender_mail = "karthiknani4221@gmail.com"  # Your email
    sender_password = "nnpl odwl apzj xouw"  # Use an App Password for security

    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = sender_mail
    message["To"] = email

    # Attach email body
    message.attach(MIMEText(body, "plain"))

    # SMTP Setup & Send Email
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_mail, sender_password)
            server.sendmail(sender_mail, email, message.as_string())
        print(f"✅ Email sent successfully to {email}")
    except Exception as e:
        print("❌ Error sending email:", e)

# **Send email when AQI is high**
def sendmail(email, name, city, aqi):
    subject = f"🚨 Urgent Air Pollution Alert for {city} - AQI {aqi}!"
    body = (
        f"Dear {name},\n\n"
        f"The Air Quality Index (AQI) in **{city}** has reached **{aqi}**, which is considered **Unhealthy**.\n"
        f"This level of pollution poses risks to your health, especially for children, seniors, and those with respiratory conditions.\n\n"
        f"✅ **Recommended Precautions:**\n"
        f"- 🚶 **Avoid outdoor activities**, especially prolonged exposure.\n"
        f"- 😷 **Wear an N95 mask** if stepping outside.\n"
        f"- 🏠 **Keep windows and doors closed** to minimize indoor pollution.\n"
        f"- 💨 **Use an air purifier** if available.\n"
        f"- 💧 **Stay hydrated** and monitor your health closely.\n\n"
        f"🌍 Let's stay safe and protect ourselves from harmful air pollution.\n\n"
        f"Best regards,\n"
        f"🌿 Air Quality Monitoring Team"
    )

    send_mail(email, subject, body)
