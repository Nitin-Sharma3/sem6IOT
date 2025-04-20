from flask import Flask, render_template, request, redirect, url_for, session
import smtplib
import random
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = os.urandom(24)

EMAIL_ADDRESS = 'your-email@gmail.com'
EMAIL_PASSWORD = 'your-app-password'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        otp = str(random.randint(100000, 999999))
        session['otp'] = otp
        session['email'] = email
        send_email(email, otp)
        return redirect(url_for('verify'))
    return render_template('index.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        entered_otp = request.form['otp']
        if entered_otp == session.get('otp'):
            return "✅ OTP Verified Successfully!"
        else:
            return "❌ Invalid OTP. Try Again."
    return render_template('verify.html')

def send_email(to_email, otp):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = 'Your OTP Code'
    body = f"Your OTP code is: {otp}"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()

if __name__ == '__main__':
    app.run(debug=True)
