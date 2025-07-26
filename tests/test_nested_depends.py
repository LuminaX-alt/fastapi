from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from pydantic import BaseModel

class Inner(BaseModel):
    a: int

class Outer(BaseModel):
    inner: Inner

def test_nested_pydantic_depends_get_does_not_require_body():
    app = FastAPI()
    @app.get("/items")
    def get_items(model: Outer = Depends()):
        return model
    client = TestClient(app)
    schema = client.get("/openapi.json").json()
    params = schema["paths"]["/items"]["get"]["parameters"]
    assert any(p["name"] == "inner.a" for p in params)
