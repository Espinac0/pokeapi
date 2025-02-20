pipeline {
    agent any  // Usar cualquier agente disponible de Jenkins
    
    environment {
        DOCKER_IMAGE = 'pokeapi-app'  // Mantenemos el nombre original de la imagen
        CONTAINER_NAME = 'pokeapi-container'  // Mantenemos el nombre original del contenedor
        APP_PORT = '8000'  // Puerto de la aplicación
    }

    stages {
        // 1. Checkout: Obtener el código del repositorio
        stage('Checkout') {
            steps {
                git url: 'https://github.com/Espinac0/pokeapi.git', branch: 'master'  // Clonar el repositorio
            }
        }

        // 2. Build Docker Image: Crear la imagen Docker con el Dockerfile
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    bat 'docker build -t %DOCKER_IMAGE% .'  // Construir imagen
                }
            }
        }

        // 3. Run Docker Compose: Levantar tanto la aplicación como Redis
        stage('Run Docker Compose') {
            steps {
                script {
                    echo 'Running Docker Compose...'
                    // Primero detenemos contenedores existentes si los hay
                    bat 'docker-compose down || exit /b 0'
                    // Levantamos los servicios en segundo plano
                    bat 'docker-compose up -d'
                }
            }
        }

        // 4. Run Tests: Ejecutar los tests en el contenedor
        stage('Run Pytest') {
            steps {
                script {
                    echo 'Running Pytest...'
                    // Esperamos unos segundos para asegurar que los servicios estén listos
                    bat 'powershell -Command "Start-Sleep -Seconds 5"'
                    // Ejecutar tests en el contenedor
                    bat 'docker exec %CONTAINER_NAME% python -m pytest tests/'
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
            script {
                // Limpieza en caso de fallo
                bat 'docker-compose down || exit /b 0'
            }
        }
        always {
            cleanWs()  // Limpieza del workspace
        }
    }
}