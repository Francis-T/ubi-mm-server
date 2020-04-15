# things.py

# Let's get this party started!
import falcon
import activity_extract as ae
import pandas as pd
import datetime as dt
import json

DEFAULT_DATE_ROLL = ['2019-05-31',
                     '2019-06-01',
                     '2019-06-02',
                     '2019-06-03',
                     '2019-06-04',
                     '2019-06-05']

DEFAULT_TIMEZONE = 'Asia/Tokyo'


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class ThingsResource(object):
    def __init__(self):
        # merge adfs
        actv_df_list = ae.extract_activity_data("data/reduced-data.csv")
        self.adf = pd.concat(actv_df_list, ignore_index=True)
        
        return
    
    def get_rolling_date(self, date_roll=DEFAULT_DATE_ROLL):
        rdt_idx = (dt.datetime(1,1,1).today().day + 6) % len(date_roll)
        return date_roll[rdt_idx]

    def get_results(self):
        api_date = self.get_rolling_date()
        today_df = self.adf[self.adf['date'] == pd.to_datetime(api_date)].sort_values(by=['start_time'])
        today_df = today_df[today_df['end_time'].dt.date == pd.to_datetime(api_date)]
        current_df = today_df[today_df['end_time'].dt.time < pd.Timestamp.now(DEFAULT_TIMEZONE).time()].reset_index(drop=True)

        current_df['date'] = current_df['date'].astype(str)
        current_df['start_time'] = current_df['start_time'].astype(str)
        current_df['end_time'] = current_df['end_time'].astype(str)
        current_df['id'] = current_df.index
        
        print(current_df)
        return current_df
        
    def on_get(self, req, resp):
        """Handles GET requests"""
        
        res = '"result" : {}'.format(self.get_results().to_json(orient='records'))
        res = "{" + res + "}"
#         print(res)
        
        resp.status = falcon.HTTP_200  # This is the default status
#         resp.body = ('\nTwo things awe me most, the starry sky '
#                      'above me and the moral law within me.\n'
#                      '\n'
#                      '    ~ Immanuel Kant\n\n')
        resp.body = res

# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
things = ThingsResource()

# things will handle all requests to the '/things' URL path
# app.add_route('/things', things)
app.add_route('/api', things)
