pipeline {
    agent any
    stages {
        stage('Setup Python Environment') {
            steps {
                script {
                    // Configura un entorno virtual
                    sh 'python -m venv venv'
                    sh './venv/bin/pip install --upgrade pip'
                    sh './venv/bin/pip install -r requirements.txt'
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    // Ejecuta las pruebas
                    sh './venv/bin/pytest --junitxml=results.xml'
                }
            }
        }
        stage('Post-Test Actions') {
            steps {
                // Publica los resultados de las pruebas en Jenkins
                junit 'results.xml'
            }
        }
    }
    post {
        always {
            // Limpia los archivos generados
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
