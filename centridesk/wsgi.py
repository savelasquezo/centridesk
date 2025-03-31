"""
WSGI config for centridesk project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os, socket
from django.core.wsgi import get_wsgi_application
from urllib3.connection import HTTPConnection, HTTPSConnection

HTTPConnection.default_socket_options = (
    HTTPConnection.default_socket_options + [
        (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1),
        (socket.SOL_TCP, socket.TCP_KEEPIDLE, 300),
        (socket.SOL_TCP, socket.TCP_KEEPINTVL, 45)
    ]
)

HTTPSConnection.default_socket_options = (
    HTTPSConnection.default_socket_options + [
        (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1),
        (socket.SOL_TCP, socket.TCP_KEEPIDLE, 300),
        (socket.SOL_TCP, socket.TCP_KEEPINTVL, 45)
    ]
)

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry.instrumentation.botocore import BotocoreInstrumentor
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.grpc import GrpcInstrumentorClient
from opentelemetry.instrumentation.mysql import MySQLInstrumentor
from opentelemetry.instrumentation.pika import PikaInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.urllib3 import URLLib3Instrumentor
from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'centridesk.settings')

BotocoreInstrumentor().instrument()
DjangoInstrumentor().instrument()
GrpcInstrumentorClient().instrument()
MySQLInstrumentor().instrument()
PikaInstrumentor().instrument()
RequestsInstrumentor().instrument()

def strip_query_params(url: str) -> str:
    return url.split("?")[0]

URLLib3Instrumentor().instrument(
    # Remove all query params from the URL attribute on the span.
    url_filter=strip_query_params,
)

resource = Resource.create(attributes={
    "service.name": os.environ.get('OTEL_SERVICE_NAME')
})

trace.set_tracer_provider(TracerProvider(resource=resource))
span_processor = BatchSpanProcessor(
    OTLPSpanExporter(endpoint=os.environ.get('OTEL_EXPORTER_OTLP_TRACES_ENDPOINT'))
)
trace.get_tracer_provider().add_span_processor(span_processor)

application = get_wsgi_application()
application = OpenTelemetryMiddleware(application)

