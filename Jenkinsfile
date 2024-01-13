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
		    bat 'echo 1'
                    def ldapPod = bat('kubectl get pods -l app.kubernetes.io/name=my-bitnami,app.kubernetes.io/instance=ldap -o jsonpath="{.items[0].metadata.name}"').trim()
		    bat "kubectl exec -it $podName -- /bin/sh"
		    bat 'echo 2'
                    sh "apk update"
                    sh "echo hello"
                    sh "apk update"	       
                }
            }
        }          
    } 
}

