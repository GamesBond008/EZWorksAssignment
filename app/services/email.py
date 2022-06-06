import smtplib, ssl, os

PORT = 465 
SMTP_SERVER = "smtp.gmail.com"
SENDER_EMAIL = "bunny112001@gmail.com"
password = os.getenv('EMAIL_PASSWORD')

def send_verification_code(receiver_email, message):
	
	context = ssl.create_default_context()

	with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
		server.login(SENDER_EMAIL, password)
		server.sendmail(SENDER_EMAIL, receiver_email, message)