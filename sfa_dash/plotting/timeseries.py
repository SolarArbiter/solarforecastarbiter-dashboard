from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
import pandas as pd


def build_df(json):
    """Parses a Solar Forecast Arbiter API JSON
    response into a pandas dataframe
    """
    values = json.get('values')
    if not values:
        raise ValueError('Empty Values field')
    df = pd.DataFrame(values)
    obs_df = obs_df.set_index('timestamp')
    obs_df.index = pd.to_datetime(obs_df.index)
    return obs_df


def generate_figure(metadata, json_value_response):
    """Generates a plot from timeseries values.

    Parameters
    ----------
    metadata: dict
        Metadata dictionary used to label the plot.
    json_response: dict
        The json response parsed into a dictionary.
    """
    try:
        df = build_df(json_value_response)
    except ValueError:
        # return nothing until error handling is better
        # TODO
        return None
    cds = ColumnDataSource(df)
    fig = figure(plot_width=900, plot_height=200, tools='pan,wheel_zoom,reset', x_axis_type='datetime')
    fig.line(x='timestamp', y='value', source=source)
    return components(fig)
