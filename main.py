from flask import Flask, request, render_template
from ldap3 import Server, Connection, ALL

app = Flask(__name__, template_folder='C:\\Users\\liorsw\\.jenkins\\workspace\\procced\\')

def ldap_authenticate(username, password):
    ldap_server = Server('ldap://localhost:481',get_info=ALL)
    ldap_base = 'dc=my-domain,dc=com'
    ldap_filter = f'(uid={username})'

    try:
        # Bind with the full DN of the user
        with Connection(ldap_server, user=f'uid={username},ou=people,{ldap_base}', password=password) as conn:
            print("Before bind")
            if conn.bind():
                print("Bind successful")
                return True
            else:
                print("Bind failed")
                return False
    except Exception as e:
        print(f"LDAP error: {str(e)}")
        return False

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # LDAP authentication
    if ldap_authenticate(username, password):
        return 'Login successful!'
    else:
        return 'Invalid credentials. Login failed.'

if __name__ == '__main__':
    app.run(debug=True)
