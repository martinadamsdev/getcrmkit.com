from httpx import AsyncClient


class TestRegister:
    async def test_register_201(self, client: AsyncClient):
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "new@example.com",
                "password": "Secure123",
                "name": "New User",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "new@example.com"
        assert data["name"] == "New User"
        assert "id" in data

    async def test_register_409_duplicate(self, client: AsyncClient):
        payload = {"email": "dup@example.com", "password": "Secure123", "name": "User"}
        await client.post("/api/v1/auth/register", json=payload)
        response = await client.post("/api/v1/auth/register", json=payload)
        assert response.status_code == 409
        assert response.json()["detail"]["code"] == "DUPLICATE_EMAIL"


class TestLogin:
    async def test_login_200(self, client: AsyncClient):
        await client.post(
            "/api/v1/auth/register",
            json={
                "email": "login@example.com",
                "password": "Secure123",
                "name": "User",
            },
        )
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "login@example.com",
                "password": "Secure123",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] > 0

    async def test_login_401_wrong_password(self, client: AsyncClient):
        await client.post(
            "/api/v1/auth/register",
            json={
                "email": "wrong@example.com",
                "password": "Secure123",
                "name": "User",
            },
        )
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "wrong@example.com",
                "password": "WrongPass1",
            },
        )
        assert response.status_code == 401

    async def test_login_401_nonexistent_email(self, client: AsyncClient):
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "nobody@example.com",
                "password": "Secure123",
            },
        )
        assert response.status_code == 401
        assert response.json()["detail"]["code"] == "INVALID_CREDENTIALS"


class TestRefresh:
    async def test_refresh_200(self, client: AsyncClient):
        await client.post(
            "/api/v1/auth/register",
            json={
                "email": "refresh@example.com",
                "password": "Secure123",
                "name": "User",
            },
        )
        login = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "refresh@example.com",
                "password": "Secure123",
            },
        )
        refresh_token = login.json()["refresh_token"]

        response = await client.post(
            "/api/v1/auth/refresh",
            json={
                "refresh_token": refresh_token,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["refresh_token"] != refresh_token

    async def test_refresh_401_blacklisted(self, client: AsyncClient):
        await client.post(
            "/api/v1/auth/register",
            json={
                "email": "blacklist@example.com",
                "password": "Secure123",
                "name": "User",
            },
        )
        login = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "blacklist@example.com",
                "password": "Secure123",
            },
        )
        refresh_token = login.json()["refresh_token"]

        await client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})

        response = await client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
        assert response.status_code == 401


class TestLogout:
    async def test_logout_204_then_token_rejected(self, authenticated_client: AsyncClient):
        login = await authenticated_client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "Secure123",
            },
        )
        refresh_token = login.json()["refresh_token"]

        response = await authenticated_client.post(
            "/api/v1/auth/logout",
            json={
                "refresh_token": refresh_token,
            },
        )
        assert response.status_code == 204

        response = await authenticated_client.get("/api/v1/auth/me")
        assert response.status_code == 401


class TestProfile:
    async def test_me_200(self, authenticated_client: AsyncClient):
        response = await authenticated_client.get("/api/v1/auth/me")
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["name"] == "Test User"

    async def test_update_profile_200(self, authenticated_client: AsyncClient):
        response = await authenticated_client.put(
            "/api/v1/auth/me",
            json={
                "name": "Updated Name",
                "timezone": "America/New_York",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["timezone"] == "America/New_York"

    async def test_change_password_200(self, authenticated_client: AsyncClient):
        response = await authenticated_client.put(
            "/api/v1/auth/me/password",
            json={
                "old_password": "Secure123",
                "new_password": "NewSecure456",
            },
        )
        assert response.status_code == 204

        login = await authenticated_client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "NewSecure456",
            },
        )
        assert login.status_code == 200

    async def test_me_401_no_token(self, client: AsyncClient):
        response = await client.get("/api/v1/auth/me")
        assert response.status_code == 401
