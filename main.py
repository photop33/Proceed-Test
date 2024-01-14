from flask import Flask, render_template, request, redirect, url_for
import pyotp
from qrcode import make as make_qr  # Explicitly import 'make' function from 'qrcode'
import os

app = Flask(__name__, template_folder='C:\\Users\liorsw\\.jenkins\\workspace\\procced')
app.static_folder = 'C:\\Users\\liorsw\\PycharmProjects\\lorelvant'
users = {'lior': {'password': '12345', 'secret': None}}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username]['password'] == password:
            # Generate and save a new secret key for the user
            print (username,password)
            users[username]['secret'] = pyotp.random_base32()
            return redirect(url_for('enable_mfa', username=username))
        else:
            return "Invalid username or password."
    return render_template('login.html')

@app.route('/enable-mfa/<username>', methods=['GET', 'POST'])
def enable_mfa(username):
    if request.method == 'POST':
        user_secret = users[username]['secret']
        totp = pyotp.TOTP(user_secret)
        provided_otp = request.form['otp']

        if totp.verify(provided_otp):
            return f"Multi-Factor Authentication enabled for {username}."
        else:
            return "Invalid OTP. MFA setup failed."

    # Generate QR code URL for the template
    user_secret = users[username]['secret']
    totp = pyotp.TOTP(user_secret)
    uri = totp.provisioning_uri(name=username, issuer_name="YourApp")

    # Save or display the QR code as needed
    img = make_qr(uri)
    img_path = os.path.join(app.static_folder, 'qrcode.png')  # Save the QR code image in the static folder
    img.save(img_path)

    qr_code_url = url_for('static', filename='qrcode.png', _external=True)  # URL to the saved QR code

    return render_template('enable_mfa.html', username=username, qr_code_url=qr_code_url)

if __name__ == '__main__':
    app.run(debug=True , port=5000)

