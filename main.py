import random
import time

# Distributed services
services = {
    "Database Service": "Unknown",
    "Authentication Service": "Unknown",
    "Payment Service": "Unknown",
    "API Gateway": "Unknown",
    "Notification Service": "Unknown"
}


def check_service_health():

    print("\n===== DISTRIBUTED SERVICE HEALTH MONITOR =====")

    unhealthy_services = []

    for service in services:

        response_time = random.randint(50, 500)

        if response_time > 400:
            status = "Unhealthy"
            unhealthy_services.append(service)
        else:
            status = "Healthy"

        services[service] = status

        print(f"\nService: {service}")
        print(f"Response Time: {response_time} ms")
        print(f"Status: {status}")

    # Root Cause Analysis
    print("\n===== ROOT CAUSE ANALYSIS =====")

    if unhealthy_services:

        for service in unhealthy_services:
            print(f"Possible issue detected in: {service}")

        print("\nRecommendation: Investigate unhealthy services.")

    else:
        print("All services are operating normally.")

    print("\n===== MONITORING COMPLETED =====")


# Continuous monitoring
try:
    while True:
        check_service_health()
        time.sleep(3)

except KeyboardInterrupt:
    print("\nMonitoring stopped by user.")