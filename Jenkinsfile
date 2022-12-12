PROJECT_VERSION = "1.0.0"

pipeline {
    agent any
    triggers {
        githubPush()
    }
    stages {
        stage('Poetry Configuration') {
            steps{
                sh 'apt-get install python3'
                sh "curl -sSL https://install.python-poetry.org | python3 -"
                sh "$HOME/.poetry/bin/poetry install --no-root"
            }
        }

        stage('Check') {
            steps{
                sh "$HOME/.poetry/bin/poetry python3 project/manage.py makemigrations"
                sh "$HOME/.poetry/bin/poetry python3 project/manage.py migrate"
                sh "$HOME/.poetry/bin/poetry python3 project/manage.py check"
            }
        }

        stage("Test"){
            steps{
                sh "$HOME/.poetry/bin/poetry python3 project/manage.py test"
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
