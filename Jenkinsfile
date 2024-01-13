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
		    bat 'kubectl run -i --tty ldap --image=alpine --namespace=default --restart=Never -- sh'
                    bat 'echo success Ldap  helm'
		    bat 'kubectl get pods'
                }
            }
        }

        stage('run flask') {
            steps {
                script {
                    bat 'python3 main.py'
                    bat 'app seccess'
                }
            }
        }
	stage('expose flask ') {
            steps {
                script {
                    bat 'kubectl port-forward debug 5001:5001'
                    bat 'flask is expose'
                 }
            }
        }    
          
    } 
}

