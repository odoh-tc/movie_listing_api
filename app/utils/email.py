import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

def send_verification_email(email: str, token: str):
    sender_email = settings.SMTP_SENDER
    receiver_email = email
    password = settings.SMTP_PASSWORD
    smtp_server = settings.SMTP_SERVER
    smtp_port = settings.SMTP_PORT

    message = MIMEMultipart("alternative")
    message["Subject"] = "Email Verification For Movie Listing API"
    message["From"] = sender_email
    message["To"] = receiver_email

    verification_link = f"{settings.BASE_URL}/auth/verify-email?token={token}"


    html = f"""
     <html>
       <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
         <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
           <h2 style="color: #333;">Verify Your Email Address</h2>
            <p style="font-size: 16px; color: #555;">
             Hi {receiver_email},
            </p>
            <p style="font-size: 16px; color: #555;">
            Your registration is successful, please verify your email by clicking the button below:
            </p>
            <p style="text-align: center;">
            <a href="{verification_link}" style="display: inline-block; background-color: #4CAF50; color: white; padding: 10px 20px; font-size: 16px; font-weight: bold; border-radius: 5px; text-decoration: none;">Verify Email</a>
            </p>
            <p style="font-size: 14px; color: #777;">
            This link will expire after 1 hour.
            If you didn’t request this, you can ignore this email.
            </p>
         </div>
       </body>
     </html>
      """


    part = MIMEText(html, "html")
    message.attach(part)

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully.")
        return f"Email sent to {receiver_email}"
    except Exception as e:
        return f"Failed to send email to {receiver_email}: {e}"

