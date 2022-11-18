import pandas as pd
import glob
import sys
sys.path.append('./data_treatment')
from modules.DataTreatment import DataTreatment

class StationsDataTreatment(DataTreatment):
    def transform_xlsx_to_csv_and_copy_to_destination_folder(self):
        if self.filename == '':
            filename = '*.xlsx'
        else:
            filename = self.filename + '.xlsx'
        
        print(self.source_folder_path + filename)

        for f in glob.glob(self.source_folder_path + filename):

            last_dot = f.rindex('.')
            file_name = f[:last_dot]

            file_name = file_name.split('/')[-1]

            xls = pd.read_excel(f, usecols='A:G')

            file_path = self.destination_folder_path + file_name + '.csv'
            
            xls.to_csv(file_path,encoding='utf-8',index=False)