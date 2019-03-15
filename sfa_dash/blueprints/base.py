from flask.views import MethodView


class BaseView(MethodView):
    subnav_format = {}

    def format_subnav(self, **kwargs):
        """
        """
        formatted_subnav = {}
        for url, linktext in self.subnav_format.items():
            formatted_subnav[url.format(**kwargs)] = linktext
        return formatted_subnav

    def breadcrumb_html(self, breadcrumb_dict):
        """Build the breadcrumb navigation from keyword arguments.
        """
        breadcrumb = ''
        for link_text, href in breadcrumb_dict:
            breadcrumb += f'/<a href="{href}">{link_text}</a>'
        return breadcrumb

    def get(self, **kwargs):
        template = self.env.get_template(self.template)
        if hasattr(self, 'subnav') and self.subnav is not None:
            subnav = self.subnav
        else:
            subnav = {}
        rendered = template.render(breadcrumb=self.breadcrumb_html(),
                                   current_path=self.request.uri,
                                   subnav=subnav)
        self.write(rendered)
