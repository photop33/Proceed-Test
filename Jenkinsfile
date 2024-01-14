pipeline {
    agent any

    environment {
        BUILD_NUMBER = currentBuild.number.toString()
        POD_NAME = "ldap-${BUILD_NUMBER}"
        HELM_CHART = "./my-bitnami" // Adjust this path if needed
    }

    stages {
        stage('Set Version') {
            steps {
                echo "Build Number: ${BUILD_NUMBER}"
                echo "Pod Name: ${POD_NAME}"
            }
        stage('Create Ldap') {
            steps {
                script {
                    def escapedPodName = POD_NAME.replaceAll("'", "\\'")
                    sh """
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
                    bat 'kubectl exec ${POD_NAME} -- sh -c "nohup slapd -h ldap://localhost -d 481 &"'
                    bat 'kubectl cp new_ldap.ldif ${POD_NAME}:/tmp'
                    bat 'kubectl cp new_user.ldif ${POD_NAME}:/tmp'
                    bat script: '''kubectl exec ldap -- sh -c " ldapadd -x -D 'cn=Manager,dc=my-domain,dc=com' -w secret -f /tmp/new_ldap.ldif"''', returnStatus: true
		    bat script: '''kubectl exec ldap -- sh -c " ldapadd -x -D 'cn=Manager,dc=my-domain,dc=com' -w secret -f /tmp/new_user.ldif"''', returnStatus: true                    bat script: 'kubectl exec ${POD_NAME} -- sh -c "ldapadd -x -D 'cn=Manager,dc=my-domain,dc=com' -w secret -f /tmp/new_user.ldif"', returnStatus: true
                    bat 'echo success'
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
