from prometheus_client import Counter


class ObservabilityUtil:
    REQUEST_COUNT: Counter = Counter(
        "request_count",
        "Http Request Count",
        ["method", "handler", "http_status"],
    )

    @staticmethod
    def request_time(method: str, handler: str, http_status: int):
        ObservabilityUtil.REQUEST_COUNT.labels(method, handler, http_status).inc()
