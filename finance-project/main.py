from fastapi import FastAPI, Request
from api.users import users_router
from api.assets import assets_router
from domain.user.factory import InvalidUsername
from starlette.responses import JSONResponse

app = FastAPI(
    debug=True,
    title="Fintech Portfolio API",
    description="A webserver with a REST API for keeping track of your different financial assets,"
    " stocks & crypto, and see/compare their evolution",
    version="0.3.0",
)

app.include_router(users_router)
app.include_router(assets_router)


@app.exception_handler(InvalidUsername)
def return_invalid_username(_: Request, e: InvalidUsername):
    return JSONResponse(
        status_code=400, content="Username is not valid! Error: " + str(e)
    )


if __name__ == "__main__":
    import subprocess

    subprocess.run(["uvicorn", "main:app", "--reload"])
