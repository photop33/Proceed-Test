from flask import Flask, render_template, request
from ldap3 import Server, Connection, ALL, SIMPLE, SUBTREE

app = Flask(__name__, template_folder='C:\Users\liorsw\.jenkins\workspace\procced')

# LDAP server configuration
LDAP_SERVER = 'ldap://localhost'
LDAP_BIND_USER = 'cn=admin,dc=example,dc=com'
LDAP_BIND_PASSWORD = 'secret'
LDAP_BASE_DN = 'dc=example,dc=com'


@app.route('/')
def login_page():
    return render_template('login.html')
# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Authenticate the user against LDAP
        if authenticate_ldap(username, password):
            return 'Login Successful!'
        else:
            return 'Login Failed!'

    return render_template('login.html')

# Function to authenticate against LDAP
def authenticate_ldap(username, password):
    try:
        server = Server(LDAP_SERVER, get_info=ALL)
        connection = Connection(server, user=LDAP_BIND_USER, password=LDAP_BIND_PASSWORD, auto_bind=True)

        # Search for the user in LDAP
        search_filter = f'(sAMAccountName={username})'  # Modify according to your LDAP schema
        connection.search(search_base=LDAP_BASE_DN, search_filter=search_filter, search_scope=SUBTREE, attributes=['dn'])

        if connection.entries:
            user_dn = connection.entries[0].dn
            # Attempt to bind with the user's DN and password
            user_connection = Connection(server, user=user_dn, password=password, auto_bind=True)
            user_connection.unbind()
            return True
        else:
            return False

    except Exception as e:
        print(f'LDAP Error: {e}')
        return False

if __name__ == '__main__':
    app.run(debug=True , port=5003)
