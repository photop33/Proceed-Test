pipeline {
    agent any

    environment {
        BUILD_NUMBER = currentBuild.number.toString()
        POD_NAME = "ldap-${BUILD_NUMBER}"
        HELM_CHART = "./my-bitnami" // Adjust this path if needed
    }
           stage('Deploy K8S Ldap') {
            steps {
                script {
                    bat 'minikube start'
                    bat script: 'start/min helm install ldap ${HELM_CHART}', returnStatus: true
                    bat script: 'helm upgrade ldap ${HELM_CHART}', returnStatus: true
                    bat "sed 's|POD_NAME_PLACEHOLDER|${POD_NAME}|' deployment.yaml | kubectl apply -f -"
                    bat script: 'kubectl run -i --tty ${POD_NAME} --image=alpine --namespace=default --restart=Never -- sh', returnStatus: true
                    bat 'echo success Ldap helm'
                    bat 'kubectl get pods'
                }
            }
       }

    stages {
        stage('Set Version') {
            steps {
                echo "Build Number: ${BUILD_NUMBER}"
                echo "Pod Name: ${POD_NAME}"
            }

        stage('installed') {
            steps {
                script {
                    bat 'kubectl exec ${POD_NAME} -- sh -c "apk update && apk add openldap-back-mdb && apk add openrc && apk add openldap && apk add python3 && apk add py3-pip && apk add openldap-clients"'
                }
            }
        }

        stage('Create Ldap') {
            steps {
                script {
                    def escapedPodName = POD_NAME.replaceAll("'", "\\'")
                    bat """
                        kubectl exec ${escapedPodName} -- sh -c "nohup slapd -h ldap://localhost -d 481 &"
                        kubectl cp new_ldap.ldif ${escapedPodName}:/tmp
                        kubectl cp new_user.ldif ${escapedPodName}:/tmp
                        kubectl exec ${escapedPodName} -- sh -c 'ldapadd -x -D cn=Manager,dc=my-domain,dc=com -w secret -f /tmp/new_ldap.ldif'
                        kubectl exec ${escapedPodName} -- sh -c 'ldapadd -x -D cn=Manager,dc=my-domain,dc=com -w secret -f /tmp/new_user.ldif'
                        echo success
                    """
                }
            }
        }
        stage('Flask') {
            steps {
                script {
                    bat 'start/min main.py'
                    sleep time: 300, unit: 'SECONDS'
                }
            }
        }

        stage('Fronted&backend Test') {
            steps {
                script {
                    bat 'Backend_test.py > backend_test.txt 2>&1'
                    bat 'Front_test.py > front_print.txt 2>&1'
                    bat 'echo front_print success'
                    bat 'echo backend_test success'
                }
            }
        }
    }
}
