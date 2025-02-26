pipeline {
    agent any  // Usar cualquier agente disponible de Jenkins

    environment {
        DOCKER_IMAGE = 'pokeapi-app:latest'  // Nombre de la imagen Docker
        CONTAINER_NAME = 'pokeapi-container'  // Nombre del contenedor
    }

    stages {
        // 1. Limpieza: Eliminar contenedores antiguos y caché
        stage('Cleanup') {
            steps {
                script {
                    echo 'Cleaning up old Docker containers and images...'
                    bat 'docker-compose down --remove-orphans || exit /b 0'
                    bat 'docker rm -f pokeapi-container pokeapi-redis || exit /b 0'
                    bat 'docker image prune -f || exit /b 0'
                }
            }
        }

        // 2. Checkout: Obtener siempre la última versión del código
        stage('Checkout') {
            steps {
                script {
                    echo 'Fetching latest code from GitHub...'
                    bat 'git reset --hard'
                    bat 'git clean -fd'
                    bat 'git pull origin master'
                }
            }
        }

        // 3. Build Docker Image: Crear la imagen Docker
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building new Docker image...'
                    bat 'docker build -t %DOCKER_IMAGE% .'  // Usa `bat` en Windows
                }
            }
        }

        // 4. Run Docker Compose: Levantar la API y Redis
        stage('Run Docker Compose') {
            steps {
                script {
                    echo 'Starting containers with Docker Compose...'
                    bat 'docker-compose down --remove-orphans'
                    bat 'docker-compose up -d --force-recreate'  // Asegura que usa la imagen nueva
                }
            }
        }

        // 5. Run Tests: Verificar que la API funciona bien
        stage('Run Pytest') {
            steps {
                script {
                    echo 'Running API tests...'
                    bat 'docker exec %CONTAINER_NAME% python -m pytest tests/'  // Ejecutar pytest dentro del contenedor
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
