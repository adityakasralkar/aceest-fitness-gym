"""OpenTelemetry setup: sends this API's errors and request metrics to the
AIDevOps monitoring server (https://github.com/adityakasralkar/aidevops-monitoring).

Does nothing unless AIDEVOPS_API_KEY is set, and never runs during tests,
so local runs without monitoring are unaffected.
"""

import atexit
import logging
import os


def init_monitoring(app):
    """Turns on OpenTelemetry for the app. Returns True if it was enabled."""
    api_key = os.getenv("AIDEVOPS_API_KEY")
    if not api_key or app.config.get("TESTING"):
        return False

    # Imported here so the app and its tests work without these packages.
    from opentelemetry import metrics
    from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
    from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
    from opentelemetry.instrumentation.flask import FlaskInstrumentor
    from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
    from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
    from opentelemetry.sdk.resources import Resource

    endpoint = os.getenv("AIDEVOPS_URL", "http://localhost:8080").rstrip("/")
    headers = {"x-api-key": api_key}

    # Who is sending: service name and deployed version, so errors can be
    # traced back to the deployment that introduced them.
    resource = Resource.create(
        {
            "service.name": os.getenv("OTEL_SERVICE_NAME", "aceest-gym-api"),
            "service.version": os.getenv("APP_VERSION", "dev"),
            "deployment.environment": app.config.get("ENVIRONMENT", "development"),
        }
    )

    # Logs: WARNING and above from the whole app are sent to AIDevOps. This
    # includes every unhandled exception, which Flask (or, in debug mode,
    # Werkzeug) logs as an ERROR with its stack trace.
    logger_provider = LoggerProvider(resource=resource)
    logger_provider.add_log_record_processor(
        BatchLogRecordProcessor(OTLPLogExporter(endpoint=f"{endpoint}/v1/logs", headers=headers))
    )
    logging.getLogger().addHandler(
        LoggingHandler(level=logging.WARNING, logger_provider=logger_provider)
    )

    # Metrics: request count and duration for every Flask route.
    reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=f"{endpoint}/v1/metrics", headers=headers),
        export_interval_millis=int(os.getenv("AIDEVOPS_METRICS_INTERVAL_MS", "15000")),
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(meter_provider)
    FlaskInstrumentor().instrument_app(app, meter_provider=meter_provider)

    # Send whatever is still buffered when the process stops.
    atexit.register(logger_provider.shutdown)
    atexit.register(meter_provider.shutdown)

    print(f"AIDevOps monitoring enabled -> {endpoint}")
    return True
