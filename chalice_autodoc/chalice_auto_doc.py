import json
import logging
from typing import Callable

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from chalice import Chalice, Response

from .chalice_plugin import generate_plugin
from .html_template import html_data


def is_endpoint(v: Callable) -> bool:
    return v.__doc__ is not None and '---' in v.__doc__ and 'responses' in v.__doc__


def get_route_functions(glob: dict) -> dict:
    return {k: v for k, v in glob.items() if is_endpoint(v)}


def get_json(app: Chalice, route_functions: dict, route_prefix: str, version="1.0.0"):
    spec = APISpec(
        title=app.app_name,
        version=version,
        openapi_version="3.0.2",
        plugins=[generate_plugin(app)(), MarshmallowPlugin()],
        servers=[{"url": f"/{route_prefix}", "description": f"Host on /"}],
    )

    fn_list = {[fn_name.view_name for fn_name in r.values()][0] for path, r in app.routes.items()}
    for fn_name in [fn_name for fn_name in fn_list if fn_name in route_functions]:
        try:
            spec.path(view=route_functions[fn_name])
        except (TypeError, KeyError, ValueError) as e:
            logging.warning(f"Error parsing docstring: {e}")
    return json.dumps(spec.to_dict())


DEFAULT_HEADERS = {'Content-type': 'application/json'}


def info_route(app: Chalice, route_functions: dict, headers=None, route_prefix="") -> Response:
    """
    Get service info

    :return: Information about the service with a HTML UI
    """
    if headers is None:
        headers = DEFAULT_HEADERS
    json_url = "?openapi_spec=json"
    req = app.current_request
    is_json = req.query_params is not None and req.query_params.get("openapi_spec", "") == "json"
    if is_json:
        return Response(body=get_json(app, route_functions, route_prefix), headers=headers, status_code=200)
    else:
        html = html_data.encode('utf-8', errors='surrogatepass').replace('<<openapi_spec_url>>', json_url)
        return Response(body=html, headers={**headers, "Content-Type": "text/html"}, status_code=200)
