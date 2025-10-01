from __future__ import annotations
from fastapi import FastAPI, Query
from fastapi.testclient import TestClient
from typing import Annotated

def test_annotated_forwardref():
    app = FastAPI()
    @app.get("/items")
    async def read_items(q: Annotated["str", Query(...)]):
        return {"q": q}

    client = TestClient(app)
    response = client.get("/items?q=test")
    assert response.status_code == 200
    assert response.json() == {"q": "test"}
