
class CleanData:
    def __init__(self, group):
        self.df_group = group
        self.df_data_cleaned = group
        self.df_return = group
    
    def cleanedData(self):
        # Eliminar filas que cumplen la condición y asignar el resultado a la misma DataFrame
        #self.df_data_cleaned = self.df_data_cleaned.drop(self.df_data_cleaned[(self.df_data_cleaned['pm25'] <= 0) | (self.df_data_cleaned['pm25']>=99999)].index, inplace=True)
        self.df_data_cleaned = self.df_group.drop(self.df_group[self.df_group.pm25 <= 0].index)
        self.df_data_cleaned = self.df_data_cleaned.drop(self.df_data_cleaned[self.df_data_cleaned.pm25 >= 99999].index)

    def replaceDataMean(self):
        mean = self.df_data_cleaned['pm25'].mean()
        self.replaceData(mean)

    def replaceData(self, mean):
        # Reemplazar los valores por mean
        self.df_group['pm25'] = self.df_group['pm25'].apply(lambda x: mean if x <= 0 else x)
        self.df_group['pm25'] = self.df_group['pm25'].apply(lambda x: mean if x >= 99999 else x)

    def getDataCleaned(self):
        self.cleanedData()
        self.replaceDataMean()
        return self.df_group