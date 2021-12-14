from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles


routes = [
    Mount('/hydra/rest/securitydata/cve', app=StaticFiles(directory='./hydra/rest/securitydata/cve/'), name="cve"),
    Mount('/hydra/rest/securitydata/cvrf', app=StaticFiles(directory='./hydra/rest/securitydata/cvrf/'), name="cvrf")
]

app = Starlette(routes=routes)
