"""
Example script for parsing data into Solar Forecast Arbiter format.
"""

import pandas as pd
import pvlib


def get_and_export_uo_data():
    # download data from U Oregon SRML.
    # returns pandas DataFrame with columns
    # variable + '_' + instrument number
    data = pvlib.iotools.read_srml_month_from_solardat('AS', 2019, 1,
                                                       filetype='RO')
    for column in ['ghi_1', 'dni_1', 'dhi_1']:
        quality_flag = (data[f'{column}_flag'] == 99).astype(int)
        # create new pandas dataframe that conforms to Arbiter rules
        export_df = pd.DataFrame({'value': data[column],
                                  'quality_flag': quality_flag})
        # export data to csv
        export_df.to_csv(f'ashland_{column}_201901.csv',
                         index_label='timestamp',
                         date_format='%Y-%m-%dT%H:%M:%S%z')


if __name__ == '__main__':
    get_and_export_uo_data()