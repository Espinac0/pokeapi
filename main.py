from fastapi import FastAPI
from view.view import router
from utils.Logger import Logger

app = FastAPI(title="Pokémon API")
logger = Logger()

logger.add_to_log("info", "The app has started correctly .")

app.include_router(router, prefix="")  # Aseguramos que no hay prefijo

@app.get("/")
async def root():
    return {"message": "Welcome to the Pokemon API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)