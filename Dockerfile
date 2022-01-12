FROM registry.access.redhat.com/ubi8/python-38

# Add application sources with correct permissions for OpenShift
USER 0

#RUN /opt/app-root/bin/python3 -m pip install --upgrade pip

ADD ./requirements.txt ./requirements.txt

ADD ./app ./
COPY ./access.redhat.com/articles ./articles/
COPY ./access.redhat.com/chrome_themes ./chrome_themes/
COPY ./access.redhat.com/errata ./errata/
COPY ./access.redhat.com/scripts ./scripts/
COPY ./access.redhat.com/security/cve ./security/cve/
COPY ./access.redhat.com/solutions ./solutions/
COPY ./access.redhat.com/webassets ./webassets/
COPY ./access.redhat.com/sites ./sites/
##COPY ../access.redhat.com/cvrfs ./cvrf/
ADD https://access.redhat.com/security/data/metrics/cvemap.xml ./security/data/metrics/cvemap.xml
# Add the cvrf feeds
ADD https://access.redhat.com/hydra/rest/securitydata/cvrf.json ./hydra/rest/securitydata/cvrf.json
ADD https://access.redhat.com/hydra/rest/securitydata/cvrf.xml ./hydra/rest/securitydata/cvrf.xml
ADD https://access.redhat.com/hydra/rest/securitydata/cvrf ./hydra/rest/securitydata/cvrf
# Add the cve feeds
ADD https://access.redhat.com/hydra/rest/securitydata/cve.json ./hydra/rest/securitydata/cve.json
ADD https://access.redhat.com/hydra/rest/securitydata/cve.xml ./hydra/rest/securitydata/cve.xml
ADD https://access.redhat.com/hydra/rest/securitydata/cve ./hydra/rest/securitydata/cve
# Add the oval feeds
ADD https://access.redhat.com/hydra/rest/securitydata/oval.json ./hydra/rest/securitydata/oval.json
ADD https://access.redhat.com/hydra/rest/securitydata/oval.xml ./hydra/rest/securitydata/oval.xml
ADD https://access.redhat.com/hydra/rest/securitydata/oval ./hydra/rest/securitydata/oval


RUN chown -R 1001:0 ./
USER 1001

# Install dependencies
RUN /opt/app-root/bin/python3 -m pip install --no-cache-dir --upgrade -r ./requirements.txt

EXPOSE 8080

# Run application
#CMD ["uvicorn", "main:app", "--access-log", "--log-level", "info", "--host", "0.0.0.0", "--port", "8080"]
CMD ["python3", "main.py"]
