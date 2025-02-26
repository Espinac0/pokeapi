pipeline {
    agent any  // Usar cualquier agente disponible de Jenkins
    
    environment {
        DOCKER_IMAGE = 'pokeapi-app:latest'  // Usar siempre la última versión de la imagen
        CONTAINER_NAME = 'pokeapi-container'  // Nombre del contenedor principal
    }

    stages {
        // 1. Checkout: Obtener siempre el código más reciente
        stage('Checkout') {
            steps {
                script {
                    echo 'Fetching latest code from GitHub...'
                    git url: 'https://github.com/Espinac0/pokeapi.git', branch: 'master'
                }
            }
        }

        // 2. Build Docker Image: Crear la imagen Docker
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building new Docker image...'
                    sh 'docker build -t $DOCKER_IMAGE .'  // Usa build directo en lugar de `docker-compose build`
                }
            }
        }

        // 3. Run Docker Compose: Levantar la API y Redis
        stage('Run Docker Compose') {
            steps {
                script {
                    echo 'Starting containers with Docker Compose...'
                    sh 'docker-compose down --remove-orphans'
                    sh 'docker-compose up -d --force-recreate'  // Asegura que usa la imagen nueva
                }
            }
        }

        // 4. Run Tests: Verificar que la API funciona bien
        stage('Run Pytest') {
            steps {
                script {
                    echo 'Running API tests...'
                    sh 'docker exec $CONTAINER_NAME /app/venv/bin/pytest tests/'  // Si usas virtual env
                }
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully! API is running at http://localhost:8000'
        }
        failure {
            echo '❌ Pipeline failed. Check logs for errors.'
        }
    }
}
