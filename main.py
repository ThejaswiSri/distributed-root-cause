from dataclasses import dataclass

LATENCY_LIMIT_MS = 300
ERROR_RATE_LIMIT = 0.10


@dataclass
class ServiceMetrics:
    name: str
    latency_ms: float
    error_rate: float


def simulate_services():
    """Simulate three connected services with one injected failure."""

    payment = ServiceMetrics("payment", 650.0, 0.02)
    inventory = ServiceMetrics("inventory", 80.0, 0.01)

    # The order service depends on payment and inventory.
    order = ServiceMetrics(
        "order",
        payment.latency_ms + inventory.latency_ms + 40.0,
        0.15,
    )

    return [payment, inventory, order]


def check_health(service):
    if (
        service.latency_ms > LATENCY_LIMIT_MS
        or service.error_rate > ERROR_RATE_LIMIT
    ):
        return "UNHEALTHY"

    return "HEALTHY"


def main():
    services = simulate_services()

    print("\nDISTRIBUTED SYSTEM HEALTH REPORT")
    print("-" * 60)
    print(f"{'Service':<12}{'Latency (ms)':<16}{'Error rate':<14}{'Status'}")
    print("-" * 60)

    for service in services:
        status = check_health(service)
        print(
            f"{service.name:<12}"
            f"{service.latency_ms:<16.1f}"
            f"{service.error_rate:<14.1%}"
            f"{status}"
        )

    print("-" * 60)
    print("Injected failure: payment service is unusually slow.")


if __name__ == "__main__":
    main()