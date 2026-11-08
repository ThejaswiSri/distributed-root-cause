
import random

# Service dependencies
service_dependencies = {
    "API Gateway": ["Authentication Service", "Payment Service"],
    "Payment Service": ["Database Service"],
    "Authentication Service": ["Database Service"],
    "Notification Service": ["Database Service"],
    "Database Service": [],
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

    # Generate initial latency and health status for each service
    latency_by_service = {}
    status_by_service = {}

    for service in services:
        if service == failed_service:
            latency = 500
        else:
            latency = random.randint(50, 350)

        latency_by_service[service] = latency

        if latency > 400:
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
    service_results = []

    for service in services:
        if status_by_service[service] == "Unhealthy":
            status = "Unhealthy"
            latency = latency_by_service[service]

        elif service in affected_services:
            status = "Affected"
            latency = random.randint(401, 600)

        else:
            status = "Healthy"
            latency = latency_by_service[service]

        service_results.append({
            "Service": service,
            "Latency (ms)": latency,
            "Status": status,
        })

    return service_results


def analyze_root_causes(service_results):
    """Identify root causes and explain their impact on dependent services."""

    status_by_service = {
        item["Service"]: item["Status"]
        for item in service_results
    }

    findings = []

    # Identify original unhealthy services
    root_causes = [
        service
        for service, status in status_by_service.items()
        if status == "Unhealthy"
    ]

    if not root_causes:
        if not any(status == "Affected" for status in status_by_service.values()):
            return ["All services are operating normally."]

        return ["Affected services detected. Investigate their dependencies."]

    for root_cause in root_causes:
        findings.append(
            f"ROOT CAUSE: {root_cause} is unhealthy. "
            "Investigate this service."
        )

        # Find direct and indirect affected services
        impacted_services = set()
        changed = True

        while changed:
            changed = False

            for service, dependencies in service_dependencies.items():
                if service in impacted_services or service == root_cause:
                    continue

                if any(
                    dependency == root_cause
                    or dependency in impacted_services
                    for dependency in dependencies
                ):
                    impacted_services.add(service)
                    changed = True

        for service in services:
            if (
                service in impacted_services
                and status_by_service.get(service) == "Affected"
            ):
                findings.append(
                    f"IMPACT: {service} is affected by "
                    f"{root_cause} failure."
                )

    return findings


def predict_service_risk(latency_history):
    """Estimate service failure risk using recent latency measurements."""

    if len(latency_history) < 3:
        return "Insufficient Data"

    # Use the latest five measurements
    recent_latencies = latency_history[-5:]

    average_latency = sum(recent_latencies) / len(recent_latencies)

    if average_latency >= 350:
        return "High Risk"

    elif average_latency >= 250:
        return "Medium Risk"

    else:
        return "Low Risk"
