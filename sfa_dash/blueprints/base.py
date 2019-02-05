import pdb
from jinja2 import Environment, FileSystemLoader, select_autoescape
from flask import Flask, Blueprint, request
from flask.views import MethodView


class BaseView(MethodView):
    subnav_format = {}

    def initialize(self):
        template_dir = Path(__file__).parent / 'templates'
        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape([])
        )

    def path_parts(self, index=None):
        path = request.path
        parts = path.split('/')
        if index is not None:
            return parts[index+1]
        return parts

    def format_subnav(self, **kwargs):
        """
        """
        formatted_subnav = {}
        for url, linktext in self.subnav_format.items():
            formatted_subnav[url.format(**kwargs)] = linktext
        return formatted_subnav


    def make_breadcrumb_html(self):
        """Build the breadcrumb navigation from keyword arguments. 
        """
        parts = self.path_parts()
        breadcrumb = ""
        for idx, part in enumerate(parts):
            if part == "":
                continue
            breadcrumb += '/<a href="{}">{}</a>'.format('/'.join(parts[:idx+1]), part.capitalize())
        return breadcrumb

        
    def get(self, **kwargs):
        template = self.env.get_template(self.template)
        if hasattr(self, 'subnav') and self.subnav is not None:
            subnav = self.subnav
        else:
            subnav = {}
        rendered = template.render(breadcrumb=self.make_breadcrumb_html(), current_path=self.request.uri, subnav=subnav)
        self.write(rendered)
