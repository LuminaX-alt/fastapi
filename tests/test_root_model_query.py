# tests/test_root_model_query.py
from fastapi import FastAPI, Query
from fastapi.testclient import TestClient
from pydantic import RootModel

class MyRootModel(RootModel[str]):
    pass

def test_root_model_as_query_param():
    app = FastAPI()

    @app.get("/items")
    async def read_items(q: MyRootModel = Query(...)):
        return {"q": q.root}

    client = TestClient(app)
    response = client.get("/items?q=hello")
    assert response.status_code == 200
    assert response.json() == {"q": "hello"}
