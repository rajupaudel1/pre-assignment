import pandas as pd
import sqlite3
import os


class Backend:
    """
    simple backend class
    """

    def __init__(self, db_name: str = 'assignment.db'):
        # name of database
        self.db_name = db_name

        # delete database in the start:
        self.remove_database()

        # create connection to sqlite
        self.connection = sqlite3.connect(self.db_name, check_same_thread=False)

        # journey data table name
        self.journey_table_name = 'journey'

        print("saving data to database")
        self.push_journey_data()
        print("journey data saved to database successfully")

    def remove_database(self):
        """
        This function does basic thing to remove the database if exists. For each application run, it will re-create
        database
        """
        try:
            os.remove(self.db_name)
        except OSError:
            pass

    def list_journey(self, hardcoded_length: int = 100):
        """
        Im not implementing pagination, so, Im putting hard corded limit of first 100  journey here
        """
        needed_fields = ['Duration (sec.)', 'Covered distance (m)', 'Departure_station_name', 'Return_station_name']
        sql_query = f" select * from {self.journey_table_name} LIMIT {hardcoded_length}"
        data = pd.read_sql(sql_query, con=self.connection)

        data = data[needed_fields]

        # display in km for duration
        data['Distance(Km)'] = data['Covered distance (m)'] / 1000

        # convert seconds to minute
        data['Duration(minutes)'] = data['Duration (sec.)'] / 60

        # final needed columns
        needed_columns = ['Departure_station_name', 'Return_station_name', 'Distance(Km)', 'Duration(minutes)']

        # select needed columns
        data = data[needed_columns]
        return data

    def departure_return_info(self):
        sql_query_departure = f"select Departure_station_name as station_name, count(Departure_station_id) " \
                              f"as departure_times from " \
                              f"{self.journey_table_name} GROUP BY Departure_station_id"

        departure_id_info = pd.read_sql(sql_query_departure, con=self.connection)

        sql_query_return = f"select Return_station_name as station_name, count(Return_station_id) as " \
                           f"return_times from {self.journey_table_name} " \
                           f"GROUP BY Return_station_id"

        return_id_info = pd.read_sql(sql_query_return, con=self.connection)

        # merged return and departure info for same stations
        merged_df = departure_id_info.merge(return_id_info, on=['station_name'])
        return merged_df

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
        remove_cols_list = ['FID', 'Nimi', 'Namn', 'Osoite', 'Kaupunki', 'Stad', 'Operaattor']

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

        # rename some few columns in proper order:
        data = data.rename(columns={'Departure station id': 'Departure_station_id',
                                    'Return station id': 'Return_station_id',
                                    'Departure station name': 'Departure_station_name',
                                    'Return station name': 'Return_station_name'})
        data['Departure_station_id'] = data['Departure_station_id'].astype(int)
        return data
