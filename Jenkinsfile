pipeline { 
    agent any
    stages {
	stage('Deploy HM') {
            steps {
                script {
		    bat 'minikube start'
                    bat 'helm install ${BUILD_NUMBER}  ./my-bitnami'
                    bat 'echo success ${BUILD_NUMBER}  helm'
		    bat 'kubectl get pods'
                }
            }
        }
        stage('set version') { 	
            steps {	
                bat "echo IMAGE_TAG=${BUILD_NUMBER} > .env"   
			    bat "more .env"
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

