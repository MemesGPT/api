import fastapi
import pytest

import tests.functional.utils.types as test_utils_types


@pytest.mark.asyncio()
async def test_health_liveness(http_client: test_utils_types.TestClient) -> None:
    response = http_client.get("/api/v1/health/liveness")

    assert response.status_code == fastapi.status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}
