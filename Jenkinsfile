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
                    def podName = sh(script: 'kubectl get pods -o jsonpath="{.items[0].metadata.name}"', returnStdout: true).trim()
                    sh "kubectl exec -it $podName -- /bin/sh"
		    sh "apk update"
		    sh "echo heloo"	
		    sh "apk update"		       
                }
            }
        }          
    } 
}

