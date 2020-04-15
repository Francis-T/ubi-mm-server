import csv
import pandas as pd
import os

# # Set the path of the target csv file
# PATH_TARGET_FILE="work/reduced-data.csv"

def extract_activity_data(csv_file_path=None):
    if csv_file_path == None:
        print("ERROR: No file path provided")
        return None

    if not os.path.exists(csv_file_path):
        print("ERROR: File does not exist")
        return None
    
    # Use pandas to read the csv file into a data frane
    df = pd.read_csv(csv_file_path)

    # Convert the time string in the csv file to the proper time object in Python
    df['time'] = pd.to_datetime(df['time'])

    # Create a list of different activities based on the csv file columns (minus the time column)
    activity_cols = list(df.columns)
    activity_cols.remove("time")

    # Track the transitions for each activity
    ##  For each activity, copy the value of the activity column but shift it backwards by one
    ##    We will use this in the next step to check for activity transitions
    for actv in activity_cols:
        next_actv_col = "next_{}".format(actv)
        df[next_actv_col] = df[actv].shift(-1, fill_value=int(0))
    ##  Now, check for the activity transitions (i.e. value of activity column is different
    ##    from the value in the next activity column) on each row and save it as a new column
    ##    named 'trans_{activity name here}'
    for actv in activity_cols:
        transit_col = "trans_{}".format(actv)
        next_actv_col = "next_{}".format(actv)

        df[transit_col] = (df[actv] != df[next_actv_col])

    # Initialize a list for different activity data frames
    actv_df_list = []

    # For each known activity from the activity column list
    for actv in activity_cols:
        # Get the name of the transition column
        #    The format is simply 'trans_{activity name here}'
        trans_col = 'trans_{}'.format(actv)

        # Get the start and end time of all transitions for this activity
        #    (df[trans_col])    Gets the rows where the transition column has a 'True' value
        #    (df[actv] == 0)    Gets the rows where the activity column has a 0 value --
        #                       this is used to catch transitions from 0 --> 1 value
        #    (df[actv] == 1)    Gets the rows where the activity column has a 1 value --
        #                       this is used to catch transitions from 1 --> 0 value
        actv_start_ts = df[(df[trans_col]) & (df[actv] == 0)]['time']
        actv_end_ts   = df[(df[trans_col]) & (df[actv] == 1)]['time']


        # Check if the start and end events for this activity dont match up
        if len(list(actv_start_ts)) != len(list(actv_end_ts)):
            print("ERROR: Start and end event counts for {} don't match up".format(actv))
            print("Disconnecting...")
            return None

        # Create the data frame
        actv_df = pd.DataFrame()
        actv_df['start_time'] = actv_start_ts.tolist()
        actv_df['end_time'] = actv_end_ts.tolist()
        actv_df['duration'] = actv_df['end_time'] - actv_df['start_time']
        actv_df.insert(0, 'actv', actv)
        actv_df.insert(1, 'date', actv_df['start_time'].dt.date)

        # Add it to the list
        actv_df_list.append(actv_df)

    return actv_df_list
