from sfa_dash.handlers.base import BaseHandler


class DataDashHandler(BaseHandler):
    subnav_format = {
        "/tep/avalon_2/{asset}": "Data",
        "/tep/avalon_2/{asset}/access": "Access",
        "/tep/avalon_2/{asset}/trials": "Active Trials",
        "/tep/avalon_2/{asset}/reports": "Reports",
    }
    def initialize(self):
        asset = self.path_parts(2)
        self.subnav = self.format_subnav(asset=asset)
        super().initialize()
