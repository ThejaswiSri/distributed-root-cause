import random
import time

services = {
    "User Service": "Healthy",
    "Payment Service": "Healthy",
    "Database Service": "Healthy"
}

def check_service_health():
    print("\n===== DISTRIBUTED SERVICE HEALTH MONITOR =====")

    for service in services:
        response_time = random.randint(50, 500)

        if response_time > 400:
            status = "Unhealthy"
        else:
            status = "Healthy"

        services[service] = status

        print(f"\nService: {service}")
        print(f"Response Time: {response_time} ms")
        print(f"Status: {status}")

while True:
    check_service_health()
    time.sleep(3)