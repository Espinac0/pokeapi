pipeline {
    agent any  // Usar cualquier agente disponible de Jenkins
    
    environment {
        DOCKER_IMAGE = 'pokeapi-app'  // Mantenemos el nombre original de la imagen
        CONTAINER_NAME = 'pokeapi-container'  // Mantenemos el nombre original del contenedor
        APP_PORT = '8000'  // Puerto de la aplicación
    }

    stages {
        // 1. Limpieza inicial
        stage('Cleanup') {
            steps {
                script {
                    echo 'Cleaning up environment...'
                    // Detenemos y eliminamos contenedores existentes
                    bat 'docker-compose down --remove-orphans || exit /b 0'
                    bat 'docker rm -f pokeapi-container pokeapi-redis || exit /b 0'
                    // Limpiamos imágenes no utilizadas
                    bat 'docker image prune -f || exit /b 0'
                }
            }
        }

        // 2. Checkout: Obtener el código del repositorio
        stage('Checkout') {
            steps {
                git url: 'https://github.com/Espinac0/pokeapi.git', branch: 'master'  // Clonar el repositorio
            }
        }

        // 3. Build Docker Image: Crear la imagen Docker con el Dockerfile
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    bat 'docker build -t %DOCKER_IMAGE% .'  // Construir imagen
                }
            }
        }

        // 4. Run Docker Compose: Levantar tanto la aplicación como Redis
        stage('Run Docker Compose') {
            steps {
                script {
                    echo 'Running Docker Compose...'
                    // Levantamos los servicios en segundo plano
                    bat 'docker-compose up -d'
                    // Esperamos a que los contenedores estén listos
                    bat 'powershell -Command "Start-Sleep -Seconds 10"'
                    // Verificamos que los contenedores están corriendo
                    bat 'docker ps --format "{{.Names}}" | findstr pokeapi-container'
                }
            }
        }

        // 5. Run Tests: Ejecutar los tests en el contenedor
        stage('Run Pytest') {
            steps {
                script {
                    echo 'Running Pytest...'
                    // Ejecutar tests en el contenedor
                    bat 'docker exec pokeapi-container python -m pytest tests/'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully! API is available at http://localhost:8000'
        }
        failure {
            echo 'Pipeline failed. Check the logs for details.'
        }
    }
}