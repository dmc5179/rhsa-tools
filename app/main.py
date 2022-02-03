import os
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import Response
from starlette.responses import HTMLResponse
from starlette.responses import PlainTextResponse
from starlette.templating import Jinja2Templates
from starlette.responses import JSONResponse
from mimetypes import guess_type
import uvicorn
import json
import jmespath
import copy

f = open("./data/cve.json", "r")
cve_json = json.load(f)
f.close()
#with open('./data/cve_jq.json') as f:
#    cve_json = [json.loads(line) for line in f]

templates = Jinja2Templates(directory='templates')

#routes = [
#    Mount('/sites', StaticFiles(directory="sites")),
#    Mount('/webassets', StaticFiles(directory="webassets")),
#    Mount('/default', StaticFiles(directory="default")),
#    Mount('/css', StaticFiles(directory="css"))
#]

def startup():
  print("Ready to go")

#app = Starlette(debug=True, routes=routes, on_startup=[startup])
app = Starlette(debug=True)

@app.route('/')
async def homepage(request):
    template = "index.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context)

@app.route("/css/{whatever:path}")
async def get_css(request):
    whatever = request.path_params.get("whatever")
    with open("./css/"+whatever) as f:
        content = f.read()

    content_type, _ = guess_type(whatever)
    return Response(content, media_type=content_type)

@app.route("/default/{whatever:path}")
async def get_default(request):
    whatever = request.path_params.get("whatever")
    with open("./default/"+whatever) as f:
        content = f.read()

    content_type, _ = guess_type(whatever)
    return Response(content, media_type=content_type)

@app.route("/sites/{whatever:path}")
async def get_sites(request):
    whatever = request.path_params.get("whatever")
    with open("./sites/"+whatever) as f:
        content = f.read()

    content_type, _ = guess_type(whatever)
    return Response(content, media_type=content_type)

@app.route("/webassets/{whatever:path}")
async def get_webassets(request):
    whatever = request.path_params.get("whatever")
    with open("./webassets/"+whatever) as f:
        content = f.read()

    content_type, _ = guess_type(whatever)
    return Response(content, media_type=content_type)

@app.route("/libs/{whatever:path}")
async def get_webassets(request):
    whatever = request.path_params.get("whatever")
    with open("./libs/"+whatever) as f:
        content = f.read()

    content_type, _ = guess_type(whatever)
    return Response(content, media_type=content_type)

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
  return "[?public_date<='"+before+"']"

async def select_after(after):
  print("Selecting after: " + after)
  return "[?public_date>='"+before+"']"

async def select_value(key, values):
  v = values.split(',')
  qry = "[?"+key+"=='" + v[0] + "'"

  if len(v) > 1:
    for i in v[1:]:
      qry += "|| "+key+" =='" + i + "'"

  qry += "]"

  print("Selecting by "+key+": " + values)
  print("Query: " + qry )

  return qry

async def select_ids(ids):
  cves = ids.split(',')
  qry = "[?CVE=='" + cves[0] + "'"

  if len(cves) > 1:
    for cve in cves[1:]:
      qry += "|| CVE =='" + cve + "'"

  qry += "]"

  print("Selecting by id: " + ids)
  print("Query: " + qry )

  return qry

async def select_package(keys):
  packages = keys.split(',')
  if len(packages) == 1:
    qry = "[?length(affected_packages[?starts_with(@, '"+packages[0]+"')])>to_number('0')]"

  print("Selecting by package: " + keys)
  print("Qry: " + qry)

  return qry

# Much more complex. Needs to lookup the CVE full details
async def select_product(keys):
  print("Selecting by product: " + keys)
  products = keys.split(',')
  if len(products) == 1:
    return "[?=='" + products[0] + "']"
  else:
    return "unsupported"

async def select_cvss(cvss_score):
  qry = "[?5<=cvss_score]"
  print("Selecting by cvss score: " + cvss_score)
  print("Qry: " + qry)
  return qry

async def select_cvss3(cvss3_score):
  print("Selecting by cvss3 score: " + cvss3_score)

async def select_create(created_days_ago):
  print("Selecting by created days ago: "+ created_days_ago)

async def paginate(page, per_page):
  print("Pagination is not yet supported")

@app.route("/hydra/rest/securitydata/cve.json")
async def cve_search(request):
    qp = request.query_params
    jmes_qry = ""
    response = copy.deepcopy(cve_json)
    page = ""
    per_page = 1000

# Build jq select statement
    for key in qp.keys():
      print("REST param: " + key)
      jmes_qry = ""
      if key == "before":
        jmes_qry = await select_before(qp['before'])
      elif key == "after":
        jmes_qry = await select_after(qp['after'])
      elif key == "ids":
        jmes_qry = await select_value("CVE", qp['ids'])
      elif key == "bug":
        jmes_qry = await select_value("bugzilla", qp['bug'])
      elif key == "advisory":
        # Might need to be its own function with affected_packages
        jmes_qry = await select_value("advisories", qp['advisory'])
      elif key == "severity":
        jmes_qry = await select_value("severity", qp['severity'])
      elif key == "package":
        jmes_qry = await select_package(qp['package'])
      #if key == "product":
      #  jmes_qry = await select_product(qp['product'])
      elif key == "cwe":
        jmes_qry = await select_value("CWE", qp['cwe'])
      elif key == "cvss_score":
        jmes_qry = await select_cvss(qp['cvss_score'])
      elif key == "cvss3_score":
        jmes_qry = await select_cvss3(qp['cvss3_score'])
      #elif key == "created_days_ago":
      #  jmes_qry = await select_create(qp['created_days_ago'])
      elif key == "page":
        page = key
      elif key == "per_page":
        per_page = key
      else:
        print(key + " is not a valid query parameter for this API ")

      if len(jmes_qry) > 0:
        print("Query: " + jmes_qry)
        response = jmespath.search(jmes_qry, response)

    # Paginate response
    if len(page) > 0:
      response = await paginate(page, per_page)

    return JSONResponse(response)

#@app.route("/hydra/rest/securitydata/cve/{dan}")
#async def cve(request):
#    content = '%s %s' % (request.method, request.url.path)
#    content = os.path.basename(os.path.normpath(content))
#
#    filename = './solutions/' + content
#
#    print("File: " + filename)

#    if not os.path.isfile(filename):
#        return Response(status_code=404)
#
#    with open(filename) as f:
#        content = f.read()

  #print("CVE: " + str(cve))
#  qp = request.query_params
#  print("Returning CVE: " + cve)
#  response = "[]"
#  if len(qp.keys()) > 0:
#    print("Checking: " + "./cves/"+qp[0]+".json")
#    if os.path.exists("./cves/"+qp[0]+".json"):
#      c = open("./cves/"+qp[0]+".json", "r")
#      response = json.load(c)
#      c.close()
#
#  return JSONResponse(response)

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
