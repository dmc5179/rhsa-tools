import os
import subprocess
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
import pyjq

jq_cmd = "jq -c -r"

#f = open("./data/cve.json", "r")
#cve_json = json.load(f)
#f.close()
with open('./data/cve_jq.json') as f:
    cve_json = [json.loads(line) for line in f]

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
  return 'map(. | select(.public_date |. != null and . != "")) | map(select(.public_date | . <= $e + "z")) | select(length>0)'

async def select_after(after):
  print("Selecting after: " + after)

async def select_ids(ids):
  return ".[] | select(.CVE == \"" + ids + "\")"

@app.route("/hydra/rest/securitydata/cve.json")
async def cve_search(request):
    qp = request.query_params
    jq_qry = ""
    jq_args = ""

# Build jq select statement
    for key in qp.keys():
      if key == "before":
        jq_qry += await select_before(qp['before'])
        jq_args += '--arg e ' + qp['before']
      if key == "after":
        jq_qry += await select_after(qp['after'])
      if key == "ids":
        jq_qry += await select_ids(qp['ids'])
      if key == "bug":
        jq_qry += await select_(qp[''])
      if key == "advisory":
        jq_qry += await select_(qp[''])
      if key == "severity":
        jq_qry += await select_(qp[''])
      if key == "package":
        jq_qry += await select_(qp[''])
      if key == "product":
        jq_qry += await select_(qp[''])
      if key == "cwe":
        jq_qry += await select_(qp[''])
      if key == "cvss_score":
        jq_qry += await select_(qp[''])
      if key == "cvss3_score":
        jq_qry += await select_(qp[''])
      if key == "created_days_ago":
        jq_qry += await select_(qp[''])

# build subprocess command
    cmd = jq_cmd + " "
    if len(jq_args) > 0:
      cmd += jq_args + " "

    cmd += "'" + jq_qry + "'" + " ./data/cve_jq.json"
    print("Running cmd: " + cmd)
    results = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)

    if results.stdout[0] == '[':
      response = json.dumps(results.stdout)
      #print(results.stdout.split())
    else:
      response = json.loads(results.stdout)
      print("Object")

    # Some queries result in a single json object. Some queries result in a json array
    # with multiple top level objets. json.loads cannot handle mutliple top level objects
    # So, some queries reply with {} and some with [{},{}]
    # The second example above is what json.loads cannot handle
    # Supposedly [{},{}] is not valid json but its hard to think jq returns invalid json
    #response = json.loads(data_array)
######

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
