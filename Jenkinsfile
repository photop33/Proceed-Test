pipeline {
    agent any

    stages {
        // environment {
        //     BUILD_NUMBER = currentBuild.number.toString()
        //     POD_NAME = "ldap-${BUILD_NUMBER}"
        // }
        // stages {
        //     stage('Set Version') {
        //         steps {
        //             echo "Build Number: ${BUILD_NUMBER}"
        //             echo "Pod Name: ${POD_NAME}"
        //         }
        //     }
        // }
        stage('Deploy jenkins') {
            steps {
                script {
                    bat 'minikube start'
                    bat 'helm install jenkins ./jenkins'
                    bat 'echo success jenkins'
                    def podStatus
        for (int i = 0; i < 10; i++) {
    podStatus = bat(script: 'kubectl get pods jenkins-0 -o jsonpath="{.status.phase}"', returnStatus: true)
    if (podStatus != null && podStatus.toString().toLowerCase().contains("running")) {
        break
    }
    sleep time: 60, unit: 'SECONDS'
}


                    // Port-forward to Jenkins service
                    bat 'kubectl --namespace default port-forward svc/jenkins 8080:8080'
                }
            }
        }
        stage('Deploy HM') {
            steps {
                script {
                    bat script: 'helm install ldap ./my-bitnami', returnStatus: true
                    bat script: 'helm upgrade ldap ./my-bitnami', returnStatus: true
                    bat script: 'kubectl run -i --tty ldap --image=alpine --namespace=default --restart=Never -- sh', returnStatus: true
                    bat 'echo success ldap helm'
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

        stage('Create Ldap') {
            steps {
                script {
                    bat 'kubectl exec ldap -- sh -c "nohup slapd -h ldap://localhost -d 481 &"'
                    bat 'kubectl cp base.ldif ldap:/tmp'
                    bat 'kubectl cp new_user.ldif ldap:/tmp'
                    bat script: '''kubectl exec ldap -- sh -c " ldapadd -x -D 'cn=Manager,dc=my-domain,dc=com' -w secret -f /tmp/base.ldif"''', returnStatus: true
                    bat script: '''kubectl exec ldap -- sh -c " ldapadd -x -D 'cn=Manager,dc=my-domain,dc=com' -w secret -f /tmp/new_user.ldif"''', returnStatus: true
                    bat 'echo success'
                }
            }
        }

        stage('Flask') {
            steps {
                script {
                    bat 'start/min main.py'
                //    sleep time: 60, unit: 'SECONDS'
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
