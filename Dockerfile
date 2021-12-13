FROM registry.access.redhat.com/ubi8/python-38

# Add application sources with correct permissions for OpenShift
USER 0

ADD ./requirements.txt ./requirements.txt

ADD ./app ./
ADD ./cvrfs ./ 
ADD ./cves ./

RUN chown -R 1001:0 ./
USER 1001

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r ./requirements.txt

EXPOSE 8080

# Run application
CMD ["uvicorn", "main:app", "--access-log", "--log-level", "info", "--host", "0.0.0.0", "--port", "8080"]
