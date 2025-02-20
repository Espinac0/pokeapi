pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'pokeapi-app'
    }
    
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $DOCKER_IMAGE .'
                }
            }
        }
        
        stage('Run Tests in Docker') {
            steps {
                script {
                    sh 'docker run --rm $DOCKER_IMAGE pytest'
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    sh '''
                        docker ps -q --filter "name=pokeapi-container" | grep -q . && docker stop pokeapi-container && docker rm pokeapi-container || true
                        docker run -d -p 8000:8000 --name pokeapi-container $DOCKER_IMAGE
                    '''
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline ejecutado correctamente!'
        }
        failure {
            echo 'La ejecución del pipeline falló.'
        }
    }
}
