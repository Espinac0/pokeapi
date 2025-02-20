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
                    // Verificar que Docker está disponible
                    bat '''
                        echo "Verificando Docker..."
                        docker info
                        if errorlevel 1 (
                            echo "Error: Docker no está disponible"
                            exit /b 1
                        )
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Usar pwd para obtener la ruta actual
                    bat '''
                        echo "Construyendo imagen desde %CD%"
                        docker build -t %DOCKER_IMAGE% "%CD%"
                    '''
                }
            }
        }
        
        stage('Run Tests in Docker') {
            steps {
                script {
                    bat '''
                        echo "Ejecutando tests..."
                        docker run --rm %DOCKER_IMAGE% python -m pytest
                    '''
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    // Intentar detener y eliminar el contenedor existente si existe
                    bat '''
                        echo "Limpiando contenedores antiguos..."
                        for /f "tokens=*" %%i in ('docker ps -aq --filter "name=pokeapi-container"') do (
                            docker stop %%i 2>nul
                            docker rm %%i 2>nul
                        )
                    '''
                    
                    // Verificar si el puerto está en uso
                    bat '''
                        echo "Verificando puerto %APP_PORT%..."
                        netstat -ano | findstr ":%APP_PORT%" > nul
                        if not errorlevel 1 (
                            echo "Puerto %APP_PORT% en uso, intentando liberar..."
                            for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":%APP_PORT%"') do (
                                taskkill /f /pid %%a 2>nul
                            )
                        )
                    '''
                    
                    // Desplegar el nuevo contenedor
                    bat '''
                        echo "Desplegando nuevo contenedor..."
                        docker run -d -p %APP_PORT%:%APP_PORT% --name pokeapi-container %DOCKER_IMAGE%
                        
                        echo "Esperando a que el contenedor esté listo..."
                        timeout /t 5 /nobreak > nul
                        
                        echo "Verificando estado del contenedor..."
                        docker ps | findstr "pokeapi-container"
                        if errorlevel 1 (
                            echo "Error: El contenedor no está corriendo"
                            exit /b 1
                        )
                        
                        echo "Contenedor desplegado correctamente en http://localhost:%APP_PORT%"
                    '''
                }
            }
        }
    }
    
    post {
        always {
            script {
                bat '''
                    echo "Limpieza post-pipeline..."
                    for /f "tokens=*" %%i in ('docker ps -aq --filter "name=pokeapi-container" 2^>nul') do (
                        docker stop %%i 2>nul
                        docker rm %%i 2>nul
                    )
                '''
            }
            cleanWs()
        }
        success {
            echo 'Pipeline ejecutado correctamente! La API está disponible en http://localhost:8000'
        }
        failure {
            echo 'La ejecución del pipeline falló. Revisa los logs para más detalles.'
        }
    }
}
