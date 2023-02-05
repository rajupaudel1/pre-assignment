import pandas as pd
import sqlite3


class Backend:
    """
    simple backend class
    """
    def __init__(self, db_name: str = 'assignment.db'):
        # name of database
        self.db_name = db_name

        # create connection to sqlite
        self.connection = sqlite3.connect(self.db_name)

        # journey data table name
        self.journey_table_name = 'journey'

    def push_journey_data(self):
        """
        This function pushes journey data to sqlite
        """
        # load journey data
        journey_data = Backend.load_journey_data()

        # use pandas function to push to journey data
        journey_data.to_sql(name=self.journey_table_name, con=self.connection)

    @staticmethod
    def load_meta_data():
        """
        This function loads meta data information of those stations
        """
        # load meta data related to journey
        meta_df = pd.read_csv('https://opendata.arcgis.com/datasets/726277c507ef4914b0aec3cbcfcbfafc_0.csv')

        """
        remove unnecessary columns from meta_data. There are same information with different naming like nimi, name,
        namn, etc and also, we don't need operator info as well as it says data belongs to specific operator.
        """
        remove_cols_list = ['FID, Nimi,Namn,Osoite,Kaupunki,Stad,Operaattor']

        # remove columns
        meta_df = meta_df.drop(remove_cols_list, axis=1)
        return meta_df

    @staticmethod
    def load_journey_data():
        """
        downloads journey data and do some pre-process
        """
        # These are the csv links provided in the task
        csv_links = ['https://dev.hsl.fi/citybikes/od-trips-2021/2021-05.csv',
                     'https://dev.hsl.fi/citybikes/od-trips-2021/2021-06.csv',
                     'https://dev.hsl.fi/citybikes/od-trips-2021/2021-07.csv']

        # make a list of dataframes
        df_lists = []

        # read those csv links one by one
        for file_name in csv_links:
            # fetch and read csv file
            df = pd.read_csv(file_name)

            # don't include less than 10 seconds
            df = df.loc[df['Duration (sec.)'] > 10]

            # don't include those data that are less than 10 meter
            df = df.loc[df['Covered distance (m)'] > 10]

            # finally append that dataframe to df_lists
            df_lists.append(df)

        # concat those above list of dataframe
        data = pd.concat(df_lists, ignore_index=True)

        return data
