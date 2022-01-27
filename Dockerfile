FROM registry.access.redhat.com/ubi8/python-38

# Add application sources with correct permissions for OpenShift
USER 0

COPY access.redhat.com.tgz ./access.redhat.com.tgz
COPY entrypoint.sh ./entrypoint.sh
COPY ./requirements.txt ./requirements.txt
COPY ./app ./
COPY ./data/cve.json ./data/
COPY ./data/cvrf.json ./data/
COPY ./data/oval.json ./data/
COPY ./data/ovalstreams.json ./data/
COPY ./cves ./data/cves/

RUN chown -R 1001:0 ./
USER 1001

# Install dependencies
RUN /opt/app-root/bin/python3 -m pip install --no-cache-dir --upgrade -r ./requirements.txt

EXPOSE 8080

# Run application
#CMD ["uvicorn", "main:app", "--access-log", "--log-level", "info", "--host", "0.0.0.0", "--port", "8080"]
#CMD ["python3", "main.py"]
ENTRYPOINT ["./entrypoint.sh"]
