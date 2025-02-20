pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'pokeapi-app'
        APP_PORT = '8000'
    }
    
    stages {
        stage('Check Docker') {
            steps {
                script {
                    bat 'docker version'
                }
            }
        }

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
                    // Limpiar contenedor existente si existe
                    bat 'docker rm -f pokeapi-container || exit /b 0'
                    
                    // Desplegar nuevo contenedor
                    bat 'docker run -d -p %APP_PORT%:%APP_PORT% --name pokeapi-container %DOCKER_IMAGE%'
                    
                    // Verificar que el contenedor está corriendo
                    bat 'timeout /t 5 /nobreak > nul && docker ps | findstr pokeapi-container'
                }
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline ejecutado correctamente! La API está disponible en http://localhost:8000'
        }
        failure {
            echo 'La ejecución del pipeline falló. Revisa los logs para más detalles.'
            bat 'docker rm -f pokeapi-container || exit /b 0'
        }
        always {
            cleanWs()
        }
    }
}
