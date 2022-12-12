podTemplate(containers: [
    containerTemplate(
        name: 'ubuntu', 
        image: 'ubuntu:20.04'
    ),
    containerTemplate(
        name: 'kaniko',
        image: 'gcr.io/kaniko-project/executor:debug'
    )
  ]) {

    node(POD_LABEL) {

        container('ubuntu') {
            
            stage('Setup') {
                steps{
                    sh 'apt -y update'
                    sh 'apt -y install apt-utils'
                    sh 'export DEBIAN_FRONTEND=noninteractive'
                    sh 'apt -y install tzdata'
                    sh 'ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime'
                    sh 'dpkg-reconfigure --frontend noninteractive tzdata'
                    sh 'apt -y install net-tools python3.9 python3-pip mysql-client libmysqlclient-dev'
                    sh 'apt -y install python3-dev'
                    sh 'apt -y upgrade'
                    sh 'apt -y install curl'
                    sh 'pip install --upgrade pip setuptools wheel'
                    sh 'python3 -m pip install --upgrade pip --user'
                    sh 'curl -sSL https://install.python-poetry.org | python3 -'
                    sh 'python3 -m pip install --upgrade pip'
                    sh 'python3 -m pip install --upgrade build'
                    sh 'apt -y install python3.8-venv'
                }
            }

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

            stage('Build contaier') {
                container('kaniko') {
                    stage('Kaniko exec') {
                        sh '/kaniko/executor --context `pwd` --destination rheamer/calca'
                    }
                }
            }

            stage("Build container and deploy with kubectl"){
                steps{
                    docker.build("rheamer/calculator")
                    sh 'curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"'
                    sh 'kubectl apply -f deploy/'
                }
            }
        }

    }
}