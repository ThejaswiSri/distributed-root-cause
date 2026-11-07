import random
# Service dependencies
service_dependencies = {
    "API Gateway": ["Authentication Service", "Payment Service"],
    "Payment Service": ["Database Service"],
    "Authentication Service": ["Database Service"],
    "Notification Service": ["Database Service"],
    "Database Service": []
}

# Distributed services
services = [
    "Database Service",
    "Authentication Service",
    "Payment Service",
    "API Gateway",
    "Notification Service",
]


def check_service_health(failed_service=None):
    """Check service health and optionally simulate a failure."""
    service_results = []

    for service in services:

        if service == failed_service:
            response_time = 500
        else:
            response_time = random.randint(50, 350)

        if response_time > 400:
            status = "Unhealthy"
        else:
            status = "Healthy"

        service_results.append({
            "Service": service,
            "Latency (ms)": response_time,
            "Status": status,
        })

    return service_results

def analyze_root_causes(service_results):
    """Identify unhealthy services and their unhealthy dependencies."""

    status_by_service = {
        item["Service"]: item["Status"]
        for item in service_results
    }

    findings = []

    for service, status in status_by_service.items():

        if status == "Unhealthy":

            unhealthy_dependencies = [
                dependency
                for dependency in service_dependencies[service]
                if status_by_service.get(dependency) == "Unhealthy"
            ]

            if unhealthy_dependencies:
                findings.append(
                    f"{service} may be affected by unhealthy "
                    f"dependency: {', '.join(unhealthy_dependencies)}"
                )
            else:
                findings.append(
                    f"{service}: no unhealthy dependency detected. "
                    "Investigate this service as a possible root cause."
                )

    if not findings:
        findings.append("All services are operating normally.")

    return findings