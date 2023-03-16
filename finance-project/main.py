from fastapi import FastAPI
from api.users import users_router

app = FastAPI(
    debug=True,
    title="Fintech Portfolio API",
    description="A webserver with a REST API for keeping track of your different financial assets,"
    " stocks & crypto, and see/compare their evolution",
    version="0.1.0",
)

app.include_router(users_router)

if __name__ == "__main__":
    import subprocess

    subprocess.run(["uvicorn", "main:app", "--reload"])
