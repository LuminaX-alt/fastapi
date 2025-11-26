from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import conint

def test_path_param_with_constraints():
    app = FastAPI()
    @app.get("/items/{item_id}")
    def read_item(item_id: conint(gt=0)):
        return {"item_id": item_id}
    client = TestClient(app)
    response = client.get("/items/5")
    assert response.status_code == 200
    assert response.json() == {"item_id": 5}
    response = client.get("/items/-1")
    assert response.status_code == 422
