import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_vinyl(client: AsyncClient, auth_headers):
    response = await client.post(
        "/api/vinyl-records",
        headers=auth_headers,
        json={
            "band": "ACDC",
            "album": "Back in Black",
            "year": 2010,
            "number_of_tracks": 10,
            "photo_url": "https://www.image",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["band"]["value"] == "ACDC"
    assert data["album"]["value"] == "Back in Black"
    assert data["year"] == 2010
    assert data["number_of_tracks"] == 10
    assert data["photo"]["url"] == "https://www.image"
    assert "id" in data
    assert "user_id" in data


@pytest.mark.asyncio
async def test_list_vinyl(client: AsyncClient):
    response = await client.get("/api/vinyl-records")
    assert response.status_code == 200
    data = response.json()
    assert data == []


@pytest.mark.asyncio
async def test_update_vinyl(client: AsyncClient, auth_headers):
    create = await client.post(
        "/api/vinyl-records",
        headers=auth_headers,
        json={
            "band": "ACDC",
            "album": "Back in Black",
            "year": 2010,
            "number_of_tracks": 10,
            "photo_url": "https://www.image",
        },
    )
    record_id = create.json()["id"]

    response = await client.put(
        f"/api/vinyl-records/{record_id}",
        headers=auth_headers,
        json={
            "band": "ACDC",
            "album": "Back in Black",
            "year": 2020,
            "number_of_tracks": 20,
            "photo_url": "https://www.image",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["year"] == 2020
    assert data["number_of_tracks"] == 20


@pytest.mark.asyncio
async def test_delete_vinyl(client: AsyncClient, auth_headers):
    create = await client.post(
        "/api/vinyl-records",
        headers=auth_headers,
        json={
            "band": "ACDC",
            "album": "Back in Black",
            "year": 2010,
            "number_of_tracks": 10,
            "photo_url": "https://www.image",
        },
    )
    record_id = create.json()["id"]

    response = await client.delete(
        f"/api/vinyl-records/{record_id}", headers=auth_headers
    )
    assert response.status_code == 204
