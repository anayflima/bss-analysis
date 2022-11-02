import pandas as pd
import glob
import shutil
import os

class DataTreatment:
    def __init__(self, source_folder_path, destination_folder_path, filename = ''):
        '''
            filename: regex of files that should be treated, without extension
        '''
        self.filename = filename
        self.source_folder_path = source_folder_path
        self.destination_folder_path = destination_folder_path

    def transform_xlsx_to_csv_and_copy_to_destination_folder(self):
        if self.filename == '':
            filename = '*.xlsx'
        else:
            filename = self.filename + '.xlsx'
        
        print(self.source_folder_path + filename)

        print(os.getcwd())

        for f in glob.glob(self.source_folder_path + filename):

            last_dot = f.rindex('.')
            file_name = f[:last_dot]

            file_name = file_name.split('/')[-1]

            xls = pd.read_excel(f, usecols='B:F')

            file_path = self.destination_folder_path + file_name + '.csv'
            
            xls.to_csv(file_path,encoding='utf-8',index=False)
    
    def copy_csv_to_destination_folder(self):
        if self.filename == '':
            filename = '*.csv'
        else:
            filename = self.filename + '.csv'
        
        for f in glob.glob(self.source_folder_path + filename):
            file_name = str(f).split('/')[-1]
            print(file_name)

            destination_file_path = self.destination_folder_path + file_name

            shutil.copyfile(f, destination_file_path)

    def fix_accents(self, text):
        try:
            return bytes(text, 'iso-8859-1').decode('utf-8')
        except UnicodeDecodeError:
            return text
        except TypeError:
            return text
    
    def fix_column_names(self, df):
        pass
    
    def padronize_dfs(self, trips = True):
        '''
            Considere that all the data is already in the destination
            folder and in csv format.
            Fix accents and padronize columns names
        '''
        if self.filename == '':
            filename = '*.csv'
        else:
            filename = self.filename + '.csv'
        
        for f in glob.glob(self.destination_folder_path + filename):
            df = pd.read_csv(f)
            self.fix_column_names(df)
            df.to_csv(f, index=False)