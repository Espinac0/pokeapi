pipeline {
    agent any  // Usar cualquier agente disponible de Jenkins
    
    environment {
        DOCKER_IMAGE = 'pokeapi-app:latest'  // Nombre para la imagen Docker
        CONTAINER_NAME = 'pokeapi-container'  // Nombre para el contenedor Docker
    }

    stages {
        // 1. Checkout: Obtener el código del repositorio
        stage('Checkout') {
            steps {
                git url: 'https://github.com/Espinac0/pokeapi.git', branch: 'main'  // Clonar el repositorio
            }
        }

        // 2. Build Docker Image: Crear la imagen Docker con el Dockerfile
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    sh 'docker build -t $DOCKER_IMAGE .'  // Construir imagen
                }
            }
        }

        // 4. Run Tests: Ejecutar los tests en el contenedor
        stage('Run Pytest') {
            steps {
                script {
                    echo 'Running Pytest...'
                    sh 'docker exec pokeapi-container /app/venv/bin/pytest tests/'  // Ejecutar tests en el contenedor
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully.'  // Si la ejecución es exitosa
        }
        failure {
            echo 'There was an issue with the pipeline.'  // Si ocurre algún error
        }
    }
}