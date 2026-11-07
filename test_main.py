from main import check_service_health


def test_all_services_healthy_without_failure():
    results = check_service_health()

    assert len(results) == 5
    assert all(item["Status"] == "Healthy" for item in results)


def test_database_failure():
    results = check_service_health("Database Service")

    database = next(
        item for item in results
        if item["Service"] == "Database Service"
    )

    assert database["Status"] == "Unhealthy"


def test_database_failure_propagates_to_dependencies():
    results = check_service_health("Database Service")

    status_by_service = {
        item["Service"]: item["Status"]
        for item in results
    }

    assert status_by_service["Authentication Service"] == "Affected"
    assert status_by_service["Payment Service"] == "Affected"
    assert status_by_service["Notification Service"] == "Affected"
    assert status_by_service["API Gateway"] == "Affected"


def test_recovery_restores_service_health():
    results = check_service_health()

    assert all(item["Status"] == "Healthy" for item in results)