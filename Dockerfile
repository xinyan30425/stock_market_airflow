FROM quay.io/astronomer/astro-runtime:12.0.0

ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow"

# Install additional Python packages
RUN pip install minio


# Install additional Python packages
RUN pip install minio astro-sdk-python