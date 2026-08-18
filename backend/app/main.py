from fastapi import FastAPI

app = FastAPI(title="Rah-e-Ravaan API")


@app.get("/")
def root():
    return {"message": "Rah-e-Ravaan backend is running rn"}