from flask import Flask
from handler.setup_handler import SetupHandler
from view.flask_app import FlaskAppSetup

# Crea la aplicación Flask
app = Flask(__name__)

# Configura la aplicación Flask
def setup():
    # Instalación de dependencias
    SetupHandler.instalar_dependencias()
    
    # Comprobar si el directorio existe
    SetupHandler.comprobar_existencias('/var/www/pokemon')
    
    # Configurar la aplicación Flask
    FlaskAppSetup.configurar_flask_app()

# Llama a la configuración en el bloque principal
if __name__ == '__main__':
    setup()  # Configura todo antes de iniciar
    app.run(host='0.0.0.0', port=8000)
