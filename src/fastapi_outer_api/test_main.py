# test_main.py

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, Response, RequestError, HTTPStatusError
from main import app, SPRING_API_URL, UserRequest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_forward_to_spring_success():
    mock_response = {"message": "Processed successfully", "username": "john"}

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = Response(
            status_code=200,
            json=mock_response,
            request=None
        )

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/submit", json={
                "username": "john",
                "password": "123",
                "security_question": "first pet?"
            })

        assert response.status_code == 200
        assert response.json() == mock_response

@pytest.mark.asyncio
async def test_forward_to_spring_request_error():
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.side_effect = RequestError("Connection failed", request=None)

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/submit", json={
                "username": "john",
                "password": "123",
                "security_question": "first pet?"
            })

        assert response.status_code == 502
        assert "Spring API connection error" in response.text

@pytest.mark.asyncio
async def test_forward_to_spring_http_status_error():
    error_response = Response(
        status_code=500,
        request=None,
        content=b'{"error":"Internal Server Error"}'
    )

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = error_response
        mock_post.return_value.raise_for_status = AsyncMock(side_effect=HTTPStatusError("Internal Server Error", request=None, response=error_response))

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/submit", json={
                "username": "john",
                "password": "123",
                "security_question": "first pet?"
            })

        assert response.status_code == 500
        assert "Spring API error" in response.text

@pytest.mark.asyncio
async def test_forward_to_spring_invalid_request():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/submit", json={
            "username": "john"  # Missing password and security_question
        })
    assert response.status_code == 422  # Unprocessable Entity
