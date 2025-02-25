# PokeAPI - Water Type Pokemon Fetcher

## English

### Project Description
This project is a Python-based API client that retrieves a list of Water-type Pokémon from the PokeAPI. It is designed to run in a Windows WSL environment and is integrated with Jenkins and Docker for automated deployment.

### Features
- Fetches Water-type Pokémon from the PokeAPI.
- Uses Redis for caching.
- Automated deployment using Jenkins.
- Dockerized for easy containerized execution.

### Installation
#### Prerequisites:
- Python 3.8+
- Docker & Docker Compose
- Jenkins
- Redis

#### Steps:
1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd pokeapi
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure Redis:
   ```bash
   docker-compose up -d redis
   ```
4. Run the application:
   ```bash
   python main.py
   ```

### Deployment with Docker
1. Build and run the Docker container:
   ```bash
   docker-compose up --build
   ```
2. Access the service at `http://localhost:<port>`.

### Jenkins Integration
1. Ensure Jenkins is installed and running.
2. Use the `Jenkinsfile` included in the project to set up the pipeline.
3. Trigger a build and verify deployment.

---

## Español

### Descripción del Proyecto
Este proyecto es un cliente de API basado en Python que recupera una lista de Pokémon de tipo Agua desde la PokeAPI. Está diseñado para ejecutarse en un entorno Windows WSL y está integrado con Jenkins y Docker para su despliegue automatizado.

### Características
- Obtiene Pokémon de tipo Agua de la PokeAPI.
- Usa Redis para almacenamiento en caché.
- Despliegue automatizado con Jenkins.
- Dockerizado para una ejecución sencilla en contenedores.

### Instalación
#### Requisitos Previos:
- Python 3.8+
- Docker y Docker Compose
- Jenkins
- Redis

#### Pasos:
1. Clona este repositorio:
   ```bash
   git clone <repository-url>
   cd pokeapi
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configura Redis:
   ```bash
   docker-compose up -d redis
   ```
4. Ejecuta la aplicación:
   ```bash
   python main.py
   ```

### Despliegue con Docker
1. Construye y ejecuta el contenedor Docker:
   ```bash
   docker-compose up --build
   ```
2. Accede al servicio en `http://localhost:<port>`.

### Integración con Jenkins
1. Asegura que Jenkins esté instalado y en ejecución.
2. Usa el `Jenkinsfile` incluido en el proyecto para configurar el pipeline.
3. Inicia una compilación y verifica el despliegue.

