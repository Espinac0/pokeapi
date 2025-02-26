# PokeAPI - Pokemon Fetcher

## English

### Project Description
This project is a Python-based API client that retrieves Pokémon data from the PokeAPI by **ID** or **Type**. It is designed to run in a Windows WSL environment and is integrated with Jenkins and Docker for automated deployment.

### Features
- Fetches Pokémon by **ID** (e.g., `GET /pokemon/1` → Bulbasaur).
- Fetches Pokémon by **Type** (e.g., `GET /type/water` → List of Water-type Pokémon).
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
2. Access the service at `http://localhost:8000/docs`.

### API Endpoints
| Method | Endpoint          | Description |
|--------|------------------|-------------|
| GET    | `/pokemon/{id}`  | Get Pokémon by ID |
| GET    | `/type/{type}`   | Get Pokémon by Type |
| GET    | `/water-pokemons` | Get all Water-type Pokémon |

### Jenkins Integration
1. Ensure Jenkins is installed and running.
2. Use the `Jenkinsfile` included in the project to set up the pipeline.
3. Trigger a build and verify deployment.

---

## Español

### Descripción del Proyecto
Este proyecto es un cliente de API basado en Python que recupera información de Pokémon desde la PokeAPI por **ID** o **Tipo**. Está diseñado para ejecutarse en un entorno Windows WSL y está integrado con Jenkins y Docker para su despliegue automatizado.

### Características
- Obtiene Pokémon por **ID** (Ejemplo: `GET /pokemon/1` → Bulbasaur).
- Obtiene Pokémon por **Tipo** (Ejemplo: `GET /type/water` → Lista de Pokémon de tipo Agua).
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
2. Accede al servicio en `http://localhost:8000/docs`.

### Endpoints de la API
| Método | Endpoint          | Descripción |
|--------|------------------|-------------|
| GET    | `/pokemon/{id}`  | Obtiene un Pokémon por su ID |
| GET    | `/type/{type}`   | Obtiene Pokémon por tipo |
| GET    | `/water-pokemons` | Obtiene todos los Pokémon de tipo Agua |

### Integración con Jenkins
1. Asegura que Jenkins esté instalado y en ejecución.
2. Usa el `Jenkinsfile` incluido en el proyecto para configurar el pipeline.
3. Inicia una compilación y verifica el despliegue.
