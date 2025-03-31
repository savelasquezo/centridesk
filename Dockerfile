# syntax=docker/dockerfile:1.7-labs

FROM python:3.12.4-bullseye as builder

RUN mkdir /code
WORKDIR /code

# install system dependencies
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends wget ffmpeg procps libkrb5-3 \
       libgfortran5 libcairo2 libglib2.0-0 libpango-1.0-0 libpangocairo-1.0-0 \
       libevent-openssl-2.1-7 libcurl4 libgnutls-openssl27 libssl1.1 libaio1 \
       gcc git pkg-config libevent-dev libcurl4-openssl-dev libgnutls28-dev libssl-dev \
    && apt remove -y default-libmysqlclient-dev \
    && apt autoremove -y

RUN OUTPUT_DIR=$(mktemp -d) \
    && cd ${OUTPUT_DIR} \
    && for i in https://dev.mysql.com/get/Downloads/MySQL-8.0/libmysqlclient21_8.0.37-1debian11_amd64.deb https://dev.mysql.com/get/Downloads/MySQL-8.0/libmysqlclient-dev_8.0.37-1debian11_amd64.deb https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-client_8.0.37-1debian11_amd64.deb https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-common_8.0.37-1debian11_amd64.deb https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-community-client-core_8.0.37-1debian11_amd64.deb https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-community-client-plugins_8.0.37-1debian11_amd64.deb https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-community-client_8.0.37-1debian11_amd64.deb https://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python-8.4.0-src.tar.gz; do wget ${i}; done \
    && dpkg -i *.deb \
    && gzip -dc mysql-connector-python-8.4.0-src.tar.gz | tar -xf - \
    && cd mysql-connector-python-8.4.0-src/mysql-connector-python/ \
    && python setup.py install --with-mysql-capi=/usr \
    && python setup.py bdist_wheel --with-mysql-capi=/usr \
    && mkdir -p /wheels \
    && cp dist/mysql_connector_python-8.4.0-cp312-cp312-linux_x86_64.whl /wheels

COPY . /code
ENV PIP_CONFIG_FILE=/code/pip.conf

# install python dependencies
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt \
    && rm /wheels/mysql_connector_python-8.4.0-cp312-cp312-manylinux_2_17_x86_64.whl

# pull official base image
FROM python:3.12.4-slim-bullseye

RUN mkdir /code
WORKDIR /code

RUN apt-get update \
    && apt-get install -y --no-install-recommends adduser wget ffmpeg procps libkrb5-3 \
       libgfortran5 libcairo2 libglib2.0-0 libpango-1.0-0 libpangocairo-1.0-0 \
       libevent-openssl-2.1-7 libcurl4 libgnutls-openssl27 libssl1.1 libaio1 \
    && apt remove -y default-libmysqlclient-dev \
    && apt autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN OUTPUT_DIR=$(mktemp -d) \
    && cd ${OUTPUT_DIR} \
    && for i in https://dev.mysql.com/get/Downloads/MySQL-8.0/libmysqlclient21_8.0.37-1debian11_amd64.deb https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-common_8.0.37-1debian11_amd64.deb https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-community-client-core_8.0.37-1debian11_amd64.deb https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-community-client-plugins_8.0.37-1debian11_amd64.deb; do wget ${i}; done \
    && dpkg -i *.deb

# create the app user
RUN addgroup --system centribal && adduser --system --group centribal

COPY --from=builder /wheels /wheels

RUN pip install --break-system-packages --no-cache /wheels/* \
    && pip install coverage

COPY --exclude=pip.conf . /code

RUN chown -R centribal:centribal /code \
    && mkdir /var/tmp/django_cache \
    && chown centribal:centribal /var/tmp/django_cache

USER centribal

EXPOSE 8080

ENV OTEL_PYTHON_EXCLUDED_URLS=/api/v1/status
ENV OTEL_PYTHON_DJANGO_EXCLUDED_URLS=/api/v1/status
ENV OTEL_PYTHON_URLLIB3_EXCLUDED_URLS=/api/v1/status
ENV OTEL_EXCLUDED_HTTP_URLS=api/v1/status
ENV OTEL_SERVICE_NAME=centridesk
ENV OTEL_TRACES_EXPORTER=otlp
ENV OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://opentelemetry-collector-collector.kube-system.svc.cluster.local:4317
ENV DJANGO_SETTINGS_MODULE=centridesk.settings

CMD ["python3", "-m", "gunicorn", "centridesk.wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "3", "--worker-class", "gevent", "--worker-connections", "1000"]

