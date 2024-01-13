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
                    bat 'kubectl exec ldap -- sh -c "apk update && apk add openldap-back-mdb && apk add openrc && apk add openldap && apk add python3 && apk add py3-pip"'
                }
            }
        }  
        stage('commaned') {
            steps {
               script {
                    bat 'kubectl exec ldap -- sh -c "nohup slapd -h ldap://localhost -d 481 &"'
                    bat 'kubectl exec ldap -- sh -c "kubectl cp user.ldif ldap:/tmp && ldapmodify -x -D "cn=Manager,dc=my-domain,dc=com" -w secret -f usernew.ldif"'

                }
            }
        }  
    } 
}

