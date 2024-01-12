pipeline { 
    agent any
    stages {
        stage('properties') {
            steps {
                script {
                    properties([pipelineTriggers([pollSCM('*/30 * * * *')])])
                    properties([buildDiscarder(logRotator(daysToKeepStr: '5', numToKeepStr: '20')),])
                }
                git 'https://github.com/photop33/Proceed-Test.git'
            }
        }
	stage('Deploy HM') {
            steps {
                script {
		    bat 'minikube start'
                    bat 'helm install ldap .'
                    bat 'echo success ldap helm'
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
