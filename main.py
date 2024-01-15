
from flask import Flask, render_template, request, redirect, url_for, session
import pyotp
from qrcode import make as make_qr
import os

app = Flask(__name__, template_folder='C:\\Users\\liorsw\\.jenkins\\workspace\\procced\\')
app.static_folder = 'C:\\Users\\liorsw\\.jenkins\\workspace\\procced\\'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def read_ldif_file(ldif_path):
    user_password = None
    cn_value = None

    with open(ldif_path, 'r') as file:
        ldif_content = file.readlines()

    for line in ldif_content:
        if line.startswith("cn: "):
            cn_value = line.strip().split(": ")[1]
        elif line.startswith("userPassword: "):
            user_password = line.strip().split(": ")[1]

    return user_password, cn_value


ldif_path = 'C:\\Users\\liorsw\\.jenkins\\workspace\\procced\\new_user.ldif'
user_password, cn_value = read_ldif_file(ldif_path)


@app.route('/', methods=['GET', 'POST'])
def login():
    error_message = None

    if request.method == 'POST':
        # Get form inputs and strip whitespaces
        username = request.form['username'].strip()
        password = request.form['password']

        ldif_path = 'C:\\Users\\liorsw\\.jenkins\\workspace\\procced\\new_user.ldif'
        user_password, cn_value = read_ldif_file(ldif_path)

        if user_password == password and cn_value.lower() == username.lower():
            # Store user data in session
            session['username'] = username
            session['password'] = password

            return redirect(url_for('enable_mfa'))
        else:
            error_message = "Incorrect username or password. Please try again."

    return render_template('login.html', error_message=error_message)


@app.route('/enable-mfa', methods=['GET', 'POST'])
def enable_mfa():
    if 'username' not in session or 'password' not in session:
        return redirect(url_for('login'))

    username = session['username']
    password = session['password']

    if request.method == 'POST':
        if 'secret' not in session or not session['secret']:
            session['secret'] = pyotp.random_base32()

        user_secret = session['secret']
        totp = pyotp.TOTP(user_secret)
        provided_otp = request.form['otp']

        if totp.verify(provided_otp):
            return f"Multi-Factor Authentication enabled for {username}."
        else:
            return "Invalid OTP. MFA setup failed."

    if 'secret' not in session:
        # If not present, generate a secret and store it in the session
        session['secret'] = pyotp.random_base32()

    user_secret = session['secret']
    totp = pyotp.TOTP(user_secret)
    uri = totp.provisioning_uri(name=username, issuer_name="YourApp")

    img = make_qr(uri)
    img_path = os.path.join(app.static_folder, 'qrcode.png')
    img.save(img_path)

    qr_code_url = url_for('static', filename='qrcode.png', _external=True)
    return render_template('enable_mfa.html', username=username, qr_code_url=qr_code_url)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
