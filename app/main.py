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

#f = open("./hydra/rest/securitydata/cve.json", "r")
f = open("./cve.json", "r")
cve_json = json.load(f)
f.close()

#with open("./hydra/rest/securitydata/cve.json", "r") as read_file:
#    data = json.load(read_file)

#async def cve(request)
#  return PlainTextResponse("In CVE section")

templates = Jinja2Templates(directory='templates')

app = Starlette(debug=True)
#app.mount('/static', StaticFiles(directory='statics'), name='static')
#app.mount('/solutions', StaticFiles(directory='access.redhat.com/solutions/'), name='solutions')

#@app.route('/')
#async def homepage(request):
#    template = "index.html"
#    context = {"request": request}
#    return templates.TemplateResponse(template, context)

@app.route("/solutions/{id}")
async def example(request):
    content = '%s %s' % (request.method, request.url.path)
    content = os.path.basename(os.path.normpath(content))

    filename = './access.redhat.com/solutions/' + content

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

    filename = './access.redhat.com/errata/' + content

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

    filename = './access.redhat.com/security/cve/' + content

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

@app.route("/hydra/rest/securitydata/cve.json")
async def cve_search(request):
    before=""
    after=""
    ids=""
    bug=""
    advisory=""
    severity="low"
    package=""
    product=""
    cwe=""
    cvss_score=""
    cvss3_score=""
    page=1
    per_page=1000
    created_days_ago=""

    results=[]

    for key in cve_json:
      if severity and key['severity'] != severity:
        continue
      results.append(key);

    #qp = request.query_params
    #print(str(qp))
    ## > foo=bar

    #return JSONResponse({k: v for (k, v) in qp.items()})
    return JSONResponse(results)

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
    uvicorn.run(app, host='0.0.0.0', port=8000)
