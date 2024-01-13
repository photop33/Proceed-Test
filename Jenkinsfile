pipeline { 
    agent any
    stages {
	stage('set version') { 	
            steps {	
                bat "echo IMAGE_TAG=${BUILD_NUMBER} > .env"   
			    bat "more .env"
            }	
         }
	stage('Deploy HM') {
            steps {
                script {
		    bat 'minikube start'
                    bat script: 'start/min helm install ldap ./my-bitnami', returnStatus: true
		    bat script: 'helm upgrade ldap ./my-bitnami', returnStatus: true
		    bat script: 'kubectl run -i --tty ldap --image=alpine --namespace=default --restart=Never -- sh', returnStatus: true
                    bat 'echo success Ldap  helm'
		    bat 'kubectl get pods'
                }
            }
        }
        stage('installed') {
            steps {
               script {
                    bat 'kubectl exec ldap -- sh -c "apk update && apk add openldap-back-mdb && apk add openrc && apk add openldap && apk add python3 && apk add py3-pip && apk add openldap-clients"'
                }
            }
        }  
        stage('commaned') {
            steps {
               script {
                    bat 'kubectl exec ldap -- sh -c "nohup slapd -h ldap://localhost -d 481 &"'
                    bat 'kubectl cp user.ldif ldap:/tmp'
		    bat script: '''kubectl exec ldap -- sh -c "ldapadd -x -D 'cn=Manager,dc=my-domain,dc=com' -w secret -f /tmp/user.ldif"''', returnStatus: true
		    bat 'echo secsess'
                }
            }
        } 
        stage('flask') {
            steps {
               script {		                    
		    bat 'kubectl exec ldap -- sh -c "python3 -m venv /path/to/another/venv"'
                    bat 'kubectl exec ldap -- sh -c "source /path/to/another/venv/bin/activate"'
                    bat 'kubectl exec ldap -- sh -c "/path/to/another/venv/bin/pip install flask"'
		    bat 'kubectl exec ldap -- sh -c "/path/to/another/venv/bin/pip install ldap3"' 
		    bat 'kubectl exec ldap -- sh -c "nohup /path/to/another/venv/bin/python /tmp/main.py"' 
                }
            }
        }  
    } 
}
