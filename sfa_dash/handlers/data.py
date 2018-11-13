from sfa_dash.handlers.dash import DataDashHandler


class DataHandler(DataDashHandler):
    template = 'data/asset.html'


class AccessHandler(DataDashHandler):
    template = 'data/access.html'


class ReportsHandler(DataDashHandler):
    template = 'data/reports.html'


class TrialsHandler(DataDashHandler):
    template = 'data/trials.html'
