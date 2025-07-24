import pytest
from fastapi import FastAPI, Form
from fastapi.testclient import TestClient

def test_multiple_form_fields():
    app = FastAPI()
    @app.post("/submit")
    async def submit(name: str = Form(...), age: int = Form(...)):
        return {"name": name, "age": age}
    client = TestClient(app)
    response = client.post("/submit", data={"name": "Alice", "age": "30"})
    assert response.status_code == 200
    assert response.json() == {"name": "Alice", "age": 30}

def test_missing_form_field():
    app = FastAPI()
    @app.post("/submit")
    async def submit(name: str = Form(...), age: int = Form(...)):
        return {"name": name, "age": age}
    client = TestClient(app)
    response = client.post("/submit", data={"name": "Alice"})
    assert response.status_code == 422

from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

app = FastAPI(openapi_prefix="/api/v1")


@app.get("/app")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}


client = TestClient(app)


def test_main():
    response = client.get("/app")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World", "root_path": "/api/v1"}


def test_openapi():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/app": {
                "get": {
                    "summary": "Read Main",
                    "operationId": "read_main_app_get",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        }
                    },
                }
            }
        },
        "servers": [{"url": "/api/v1"}],
    }
