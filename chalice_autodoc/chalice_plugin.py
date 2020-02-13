"""Chalice plugin for spec generator

"""
import re
from collections import defaultdict

from apispec import BasePlugin
from apispec import yaml_utils


# from flask-restplus
RE_URL = re.compile(r"<(?:[^:<>]+:)?([^<>]+)>")


class Rule:
    def __init__(self):
        self.rule = ""
        self.methods = []


def generate_plugin(passed_app):
    current_app = passed_app

    class ChalicePlugin(BasePlugin):
        """APISpec plugin for Flask"""

        @staticmethod
        def flaskpath2openapi(path):
            """Convert a Flask URL rule to an OpenAPI-compliant path.

            :param str path: Flask path template.
            """
            return RE_URL.sub(r"{\1}", path)

        @staticmethod
        def _rule_for_view(view):
            app = current_app

            view_rules = defaultdict(Rule)
            matched_rule = None
            for path, v in app.routes.items():
                for method, r in v.items():
                    view_rules[path].methods.append(method)
                    view_rules[path].rule = path
                    if r.view_name == view.__name__:
                        matched_rule = view_rules[path]
            return matched_rule

        def path_helper(self, operations, *, view, app=None, **kwargs):
            """Path helper that allows passing a Flask view function."""
            rule = self._rule_for_view(view)
            operations.update(yaml_utils.load_operations_from_docstring(view.__doc__))
            return self.flaskpath2openapi(rule.rule)

    return ChalicePlugin
