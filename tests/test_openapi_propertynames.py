from enum import Enum
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

class Keys(str, Enum):
    A = "a"
    B = "b"

class Model(BaseModel):
    data: dict[Keys, int]

def test_property_names_in_openapi():
    app = FastAPI()

    @app.post("/items")
    def create_item(m: Model):
        return m

    client = TestClient(app)
    schema = client.get("/openapi.json").json()
    data_schema = schema["components"]["schemas"]["Model"]["properties"]["data"]
    assert "propertyNames" in data_schema
    assert data_schema["propertyNames"]["enum"] == ["a", "b"]
