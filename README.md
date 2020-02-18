# Chalice Autodoc
Autodocument a chalice API using openapi v3 spec

# Purpose
This library is used to autodocument a chalice API using the API annotations. Optionally, it can use marshmallow 
Schemas to document data types used in the REST API.

# Code Overview
```
.
├── README.md                      <-- This instructions file
├── chalice_autodoc                <-- Main python package
    └── html_template.py           <-- Contains a zip file, with flattend HTML template file inside
    └── chalice_plugin.py          <-- Adapted version of flask plugin, for use with apispec
    └── chalice_auto_doc.py        <-- Main file which contains some utils and main Chalice GET view
```

# How to use
Step 1) add to requirements.txt or install via pip
```
pip install git+https://github.com/w-hamilton/chalice_autodoc.git
```

Step 2) Document your view functions using a docstring. Example:
```python
@app.route("/cbs/v1/invalidate_key", methods=["POST"])
def cbs_invalidate_cache(json_body):
    """Invalidate Cache Key
        ---
        post:
          description: Invalidate Cache Key
          requestBody:
            content:
              application/json:
                schema: InvalidateCacheRequest
          responses:
            200:
              description: "Success"
              content:
                application/json:
                  schema: InvalidateKeyResponse
        """

    ...function body...
    return Response(body=response, headers=headers, status_code=200)
```
For each schema, make sure you reference the Marshmallow schema. If you are using dataclass_json, put the following 
code at the bottom of your schema definitions file to generate the underlaying marshmallow Schemas:

```python
# Create marshmallow schemas for each dataclass and register it
import sys
import inspect
from marshmallow.class_registry import register
for member in inspect.getmembers(sys.modules[__name__], inspect.isclass):
    if hasattr(member[1], 'schema'):
        register(f"{member[0]}Schema", member[1].schema().__class__)
```

Step 3) Add the view to your project. Visiting this url will display OpenAPI GUI:
```python
@app.route("/cbs/v1/info", methods=["GET"])
def api_info():
    """
    Get service info

    :return: Information about the service with a HTML UI
    """
    return chalice_autodoc.info_route(
        app,
        chalice_autodoc.get_route_functions(globals()),
        headers,
        f"{settings.ENV_NAME}"
    )
```