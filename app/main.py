import os
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import Response
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from starlette.responses import JSONResponse
import uvicorn
import json
import jmespath

f = open("/tmp/rhsa-tools/cve_page1.json", "r")
cve_json = json.load(f)
f.close()
#with open('./data/cve_jq.json') as f:
#    cve_json = [json.loads(line) for line in f]

templates = Jinja2Templates(directory='templates')

app = Starlette(debug=True)

@app.route('/')
async def homepage(request):
    template = "index.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context)

@app.route("/solutions/{id}")
async def example(request):
    content = '%s %s' % (request.method, request.url.path)
    content = os.path.basename(os.path.normpath(content))

    filename = './solutions/' + content

    if not os.path.isfile(filename):
        return Response(status_code=404)

    with open(filename) as f:
        content = f.read()

    #content_type, _ = guess_type(filename)
    return Response(content, media_type='html')

@app.route("/errata/{id}")
async def errata(request):
    content = '%s %s' % (request.method, request.url.path)
    content = os.path.basename(os.path.normpath(content))

    filename = './errata/' + content

    if not os.path.isfile(filename):
        return Response(status_code=404)

    with open(filename) as f:
        content = f.read()

    #content_type, _ = guess_type(filename)
    return Response(content, media_type='html')

@app.route("/security/cve/{id}")
async def cve_html(request):
    content = '%s %s' % (request.method, request.url.path)
    content = os.path.basename(os.path.normpath(content))

    filename = './security/cve/' + content

    if not os.path.isfile(filename):
        return Response(status_code=404)

    with open(filename) as f:
        content = f.read()

    #content_type, _ = guess_type(filename)
    return Response(content, media_type='html')

@app.route("/hydra/rest/securitydata/cvrf/{id}.json")
async def cvrf(request):
    qp = request.query_params

    print(str(qp))
    # > foo=bar

    return JSONResponse({k: v for (k, v) in qp.items()})

async def select_before(before):
  print("Selecting before: " + before)
  return "[?public_date<='2016-10-21']"
  #return 'map(. | select(.public_date |. != null and . != "")) | map(select(.public_date | . <= $e + "z")) | select(length>0)'

async def select_after(after):
  print("Selecting after: " + after)

async def select_ids(ids):
  cves = ids.split(',')
  if len(cves) == 1:
    return "[?CVE=='" + cves[0] + "']"
  else:
    return "unsupported"
  #return ".[] | select(.CVE == \"" + ids + "\")"

async def select_bug(bugs):
  print("Selecting by ")

async def select_advisory(advisories):
  print("Selecting by ")

async def select_severity(severities):
  print("Selecting by ")

async def select_package(packages):
  print("Selecting by ")

async def select_product(products):
  print("Selecting by ")

async def select_cwe(cwes):
  print("Selecting by ")

async def select_cvss(cvss_score):
  print("Selecting by ")

async def select_cvss3(cvss3_score):
  print("Selecting by ")

async def select_create(created_days_ago):
  print("Selecting by ")


@app.route("/hydra/rest/securitydata/cve.json")
async def cve_search(request):
    qp = request.query_params
    jmes_qry = ""
    #jq_qry = ""
    #jq_args = ""

# Build jq select statement
    for key in qp.keys():
      if key == "before":
        jmes_qry += await select_before(qp['before'])
        #jq_qry += await select_before(qp['before'])
        #jq_args += '--arg e ' + qp['before']
      if key == "after":
        jmes_qry += await select_after(qp['after'])
      if key == "ids":
        jmes_qry += await select_ids(qp['ids'])
      if key == "bug":
        jmes_qry += await select_bug(qp['bug'])
      if key == "advisory":
        jmes_qry += await select_advisory(qp['advisory'])
      if key == "severity":
        jmes_qry += await select_severity(qp['severity'])
      if key == "package":
        jmes_qry += await select_package(qp['package'])
      if key == "product":
        jmes_qry += await select_product(qp['product'])
      if key == "cwe":
        jmes_qry += await select_cwe(qp['cwe'])
      if key == "cvss_score":
        jmes_qry += await select_cvss(qp['cvss_score'])
      if key == "cvss3_score":
        jmes_qry += await select_cvss3(qp['cvss3_score'])
      if key == "created_days_ago":
        jmes_qry += await select_create(qp['created_days_ago'])


    response = jmespath.search(jmes_qry, cve_json)


####
# pageniate if needed
    page=1
    per_page=1000
####
    return JSONResponse(response)

@app.route("/hydra/rest/securitydata/cve/{id}.json")
async def cve(request):
    qp = request.query_params

    print(str(qp))
    # > foo=bar

    return JSONResponse({k: v for (k, v) in qp.items()})

@app.route('/error')
async def error(request):
    """
    An example error. Switch the `debug` setting to see either tracebacks or 500 pages.
    """
    raise RuntimeError("Oh no")


@app.exception_handler(404)
async def not_found(request, exc):
    """
    Return an HTTP 404 page.
    """
    template = "404.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=404)


@app.exception_handler(500)
async def server_error(request, exc):
    """
    Return an HTTP 500 page.
    """
    template = "500.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8080)
