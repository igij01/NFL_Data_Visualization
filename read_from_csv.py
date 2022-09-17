import pandas as pd

class ReadCsv:
    def __init__(self, path):
        self.data = pd.read_csv(path)

    def __get__(self, instance, owner):
        return self.data

    def __set__(self, instance, value):
        self.data = [[value]]

    def filter_column(self, key=[]):
        return self.data[key]

    def filter_column_rmdup(self, key=[]):
        return self.filter_column(self, key).drop_duplicates()



object = ReadCsv("/Users/lincolnlin/PycharmProjects/NFL_Data_Visualization/games_data/regular_season/reg_games_2009.csv")
print(object.data)