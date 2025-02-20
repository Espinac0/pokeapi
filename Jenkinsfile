pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'pokeapi-app'
    }
    
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    bat 'docker build -t %DOCKER_IMAGE% .'
                }
            }
        }
        
        stage('Run Tests in Docker') {
            steps {
                script {
                    bat 'docker run --rm %DOCKER_IMAGE% python -m pytest'
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    bat '''
                        docker ps -q --filter "name=pokeapi-container" && docker stop pokeapi-container && docker rm pokeapi-container || exit 0
                        docker run -d -p 8000:8000 --name pokeapi-container %DOCKER_IMAGE%
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
