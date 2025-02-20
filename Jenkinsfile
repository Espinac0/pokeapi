pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'pokeapi-app'
        APP_PORT = '8000'
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
                    // Intentar detener y eliminar el contenedor existente si existe
                    bat '''
                        docker ps -q --filter "name=pokeapi-container" > tempFile
                        set /p CONTAINER_ID=<tempFile
                        if defined CONTAINER_ID (
                            docker stop pokeapi-container
                            docker rm pokeapi-container
                        )
                        del tempFile
                    '''
                    
                    // Verificar si el puerto está en uso
                    bat '''
                        netstat -ano | findstr :%APP_PORT% > tempPort
                        set /p PORT_IN_USE=<tempPort
                        if defined PORT_IN_USE (
                            echo "Puerto %APP_PORT% en uso, intentando liberar..."
                            for /f "tokens=5" %%a in (tempPort) do taskkill /f /pid %%a
                        )
                        del tempPort
                    '''
                    
                    // Desplegar el nuevo contenedor
                    bat 'docker run -d -p %APP_PORT%:%APP_PORT% --name pokeapi-container %DOCKER_IMAGE%'
                    
                    // Verificar que el contenedor está corriendo
                    bat '''
                        timeout /t 5 /nobreak
                        docker ps | findstr pokeapi-container
                        if errorlevel 1 (
                            echo "Error: El contenedor no está corriendo"
                            exit /b 1
                        )
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
            echo 'Pipeline ejecutado correctamente! El contenedor está corriendo en http://localhost:8000'
        }
        failure {
            echo 'La ejecución del pipeline falló.'
            
            // Intentar limpiar en caso de fallo
            script {
                bat '''
                    docker ps -q --filter "name=pokeapi-container" > tempFile
                    set /p CONTAINER_ID=<tempFile
                    if defined CONTAINER_ID (
                        docker stop pokeapi-container
                        docker rm pokeapi-container
                    )
                    del tempFile 2>nul
                '''
            }
        }
    }
}
