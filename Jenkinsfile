PROJECT_VERSION = "1.0.0"

pipeline {
    agent any
    triggers {
        githubPush()
    }
    stages {
        stage('Poetry Configuration') {
            steps{
                sh "echo hello"
            }
        }

        stage('Check') {
            steps{
                sh 'echo hello'
            }
        }

        stage("Test"){
            steps{
                sh 'echo hello'
            }
        }

        stage("Build container and deploy with kubectl"){
            steps{
                // docker.build("rheamer/calculator")
                sh 'curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"'
                sh 'kubectl apply -f deploy/'
            }
        }
    }
}
