import random
import time

services = {
    "User Service": "Healthy",
    "Payment Service": "Healthy",
    "Database Service": "Healthy"
}

def check_service_health():
    print("\n===== DISTRIBUTED SERVICE HEALTH MONITOR =====")

    unhealthy_services = []

    for service in services:
        response_time = random.randint(50, 500)
        failure = random.random() < 0.15

        if failure or response_time > 400:
            status = "Unhealthy"
            unhealthy_services.append(service)
        else:
            status = "Healthy"

        services[service] = status

        print(f"\nService: {service}")
        print(f"Response Time: {response_time} ms")
        print(f"Status: {status}")

    print("\n===== ROOT CAUSE ANALYSIS =====")

    if unhealthy_services:
        for service in unhealthy_services:
            print(f"Possible issue detected in: {service}")
    else:
        print("All services are operating normally.")

while True:
    check_service_health()
    time.sleep(3)