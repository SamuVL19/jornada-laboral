from fastapi.testclient import TestClient


def test_happy_path_shift_lifecycle(client: TestClient) -> None:
    # 1. Iniciar jornada laboral
    start_response = client.post(
        "/api/v1/shifts/start",
        json={"identification_code": "100011"},
    )
    assert start_response.status_code == 201
    start_data = start_response.json()
    assert start_data["status"] == "ACTIVE"
    assert start_data["worker_id"] is not None
    assert start_data["start_time"] is not None

    # 2. Consultar estado actual
    current_response = client.get("/api/v1/shifts/current/100011")
    assert current_response.status_code == 200
    current_data = current_response.json()
    assert current_data["identification_code"] == "100011"
    assert current_data["active_shift"] is not None
    assert current_data["active_shift"]["status"] == "ACTIVE"

    # 3. Finalizar jornada laboral
    end_response = client.post(
        "/api/v1/shifts/end",
        json={"identification_code": "100011"},
    )
    assert end_response.status_code == 200
    end_data = end_response.json()
    assert end_data["status"] == "COMPLETED"
    assert end_data["end_time"] is not None
    assert end_data["total_minutes"] is not None
    assert end_data["total_minutes"] >= 1


def test_error_shift_already_active(client: TestClient) -> None:
    # Iniciar primera jornada con éxito
    first_start = client.post(
        "/api/v1/shifts/start",
        json={"identification_code": "100012"},
    )
    assert first_start.status_code == 201

    # Reintentar iniciar jornada cuando ya tiene una activa
    second_start = client.post(
        "/api/v1/shifts/start",
        json={"identification_code": "100012"},
    )
    assert second_start.status_code == 400
    detail = second_start.json()["detail"]
    assert detail["code"] == "SHIFT_ALREADY_ACTIVE"


def test_error_worker_not_found(client: TestClient) -> None:
    # Trabajador inexistente
    response_nonexistent = client.post(
        "/api/v1/shifts/start",
        json={"identification_code": "999999"},
    )
    assert response_nonexistent.status_code == 404
    detail_nonexistent = response_nonexistent.json()["detail"]
    assert detail_nonexistent["code"] == "WORKER_NOT_FOUND"

    # Trabajador inactivo
    response_inactive = client.post(
        "/api/v1/shifts/start",
        json={"identification_code": "100099"},
    )
    assert response_inactive.status_code == 404
    detail_inactive = response_inactive.json()["detail"]
    assert detail_inactive["code"] == "WORKER_NOT_FOUND"


def test_error_shift_not_active(client: TestClient) -> None:
    # Intentar finalizar turno sin haber iniciado previamente
    response = client.post(
        "/api/v1/shifts/end",
        json={"identification_code": "100011"},
    )
    assert response.status_code == 400
    detail = response.json()["detail"]
    assert detail["code"] == "SHIFT_NOT_ACTIVE"
