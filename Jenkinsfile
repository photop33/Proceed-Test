pipeline { 
    agent any
    stages {
	stage('Deploy HM') {
            steps {
                script {
		    bat 'minikube start'
                    bat 'helm install ldap ./my-bitnami'
                    bat 'echo success ldap helm'
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

