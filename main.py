
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
    """Check service health and simulate dependency failure propagation."""

    service_results = []
    status_by_service = {}

    # Generate initial service health
    for service in services:
        if service == failed_service:
            response_time = 500
        else:
            response_time = random.randint(50, 350)

        if response_time > 400:
            status_by_service[service] = "Unhealthy"
        else:
            status_by_service[service] = "Healthy"

    # Identify direct and indirect dependency failures
    affected_services = set()

    changed = True

    while changed:
        changed = False

        for service in services:
            if (
                status_by_service[service] == "Healthy"
                and service not in affected_services
            ):
                for dependency in service_dependencies[service]:
                    if (
                        status_by_service[dependency] == "Unhealthy"
                        or dependency in affected_services
                    ):
                        affected_services.add(service)
                        changed = True
                        break

    # Build final service results
    for service in services:
        if status_by_service[service] == "Unhealthy":
            status = "Unhealthy"
            response_time = 500

        elif service in affected_services:
            status = "Affected"
            response_time = random.randint(401, 600)

        else:
            status = "Healthy"
            response_time = random.randint(50, 350)

        service_results.append({
            "Service": service,
            "Latency (ms)": response_time,
            "Status": status,
        })

    return service_results


def analyze_root_causes(service_results):
    """Identify root causes and services affected by failures."""

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
                    f"ROOT CAUSE: {service} is unhealthy. "
                    "Investigate this service."
                )

        elif status == "Affected":
            findings.append(
                f"IMPACT: {service} is affected by another service failure."
            )

    if not findings:
        findings.append("All services are operating normally.")

    return findings


def predict_service_risk(latency_history):
    """Estimate service failure risk using recent latency measurements."""

    if len(latency_history) < 3:
        return "Insufficient Data"

    # Use the latest five measurements
    recent_latencies = latency_history[-5:]

    average_latency = (
        sum(recent_latencies) / len(recent_latencies)
    )

    if average_latency >= 350:
        return "High Risk"

    elif average_latency >= 250:
        return "Medium Risk"

    else:
        return "Low Risk"
