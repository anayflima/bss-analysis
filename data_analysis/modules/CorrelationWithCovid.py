import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys
sys.path.append('./data_analysis')
sys.path.append('../../data_analysis')
from modules.DataPreparation import DataPreparation
import os

class CorrelationWithCovid:
    def __init__(self, data_folder, frequency, source_folder_path = 'trips/preprocessed/grouped/',
                 destination_folder_path = 'charts/covid/'):
        self.data_folder = data_folder
        self.frequency = frequency
        self.source_folder_path = data_folder + source_folder_path
        self.destination_folder_path = data_folder + destination_folder_path
    
    def import_and_prepare_covid_data(self,
            file_path = 'covid/grouped/covid_grouped_by_{frequency}_mean.csv'):
        file_path = file_path.format(frequency = self.frequency)
        covid_data = pd.read_csv(self.data_folder + file_path)     
        dp = DataPreparation()
        covid_data = dp.transform_to_datetime(covid_data, ['date'])
        covid_data = dp.transform_to_time_series(covid_data, 'date', drop=True)
        self.covid_data = covid_data
    
    def import_and_prepare_trips_data(self,
            file_path = 'trips/preprocessed/grouped/trips_grouped_by_{frequency}_mean.csv', period = 'all'):
        file_path = file_path.format(frequency = self.frequency)
        trips = pd.read_csv(self.data_folder + file_path)  
        dp = DataPreparation()
        trips = dp.transform_to_datetime(trips, ['date'])
        trips = dp.transform_to_time_series(trips, 'date', drop = True)
        trips = trips['2018-02':]
        if period == 'before':
            trips = trips[:os.environ['LAST_DAY_BEFORE_COVID']]
        elif period == 'during':
            # trips = trips[os.environ['FIRST_DAY_COVID']:]
            trips = trips['2019-05':]
        self.trips = trips
    
    def merge_trips_and_covid_data(self):
        trips_and_covid = pd.merge(self.trips, self.covid_data,
                                    how = 'outer',left_index=True, right_index=True)
        trips_and_covid = trips_and_covid[:os.environ['LAST_DAY_TRIPS']]
        self.trips_and_covid = trips_and_covid
    
    def plot_all_correlations(self):
        # get the data correlation matrix
        corr = self.trips_and_covid.corr()
        plt.figure(figsize=(9, 7))
        plt.imshow(corr.abs(), cmap='Blues', interpolation='none', aspect='auto')
        plt.colorbar()
        plt.xticks(range(len(corr)), corr.columns, rotation='vertical')
        plt.yticks(range(len(corr)), corr.columns)
        plt.suptitle('Correlation between variables', fontsize=15, fontweight='bold')
        plt.grid(False)
        plt.show()
        return corr

    def plot_target_variable_correlation(self, corr, target_variable, save = False):
        correlation = np.array(corr[target_variable])

        # remove correlation with itself
        correlation = np.delete(correlation, np.where(correlation == 1))
        columns = np.array(self.trips_and_covid.keys())
        columns =  np.delete(columns, np.where(columns == target_variable))

        # If some column has a boolean type, it won't appear in the correlation matrix.
        # So, we have to remove it from the columns variable before plotting.
        if len(corr) < len(columns):
            columns = [x for x in columns if x in corr.columns]

        plt.figure(figsize=(15, 7))
        plt.bar(columns, correlation)
        for i in range(len(correlation)):
            if correlation[i] > 0:
                va="bottom"
            else:
                va="top"
            plt.text(i, correlation[i], round(correlation[i], 2), ha="center", va=va)
        
        title = "Correlation with '{variable}' variable".format(variable = target_variable)
        plt.title(title)
        if save:
            filename = target_variable + '.png'
            plt.savefig(self.destination_folder_path + 'correlation/' + filename)
        plt.show(True)
    
    def plot_variable_and_covid_with_phases(self, variable, covid_variable, phases = False, save = False):
        trips_and_covid_plot = self.trips_and_covid.filter([variable, covid_variable])
        plt.gcf().set_size_inches(20, 1)
        ax = trips_and_covid_plot.plot(secondary_y = covid_variable, ylim=(0,None), label = 'Número médio de viagens diárias',
                                    figsize = (20,11))
        title = "'{variable}' vs '{covid_variable}'".format(variable = variable, covid_variable = covid_variable)
        plt.title(title)
        if phases:
            ax.axvline('2020-03-24', color="black", linestyle="--",  label='Início do lockdown em SP')
            ax.axvline('2020-05-27', color="purple", linestyle="--",  label='Plano SP de retomada consciente')
            ax.axvline('2020-10-06', color="green", linestyle="--",  label='Fase Verde')
            ax.axvline('2020-11-30', color="yellow", linestyle="--",  label='Fase Amarela')
            ax.axvline('2021-03-15', color="red", linestyle="--",  label='Fase Emergencial')
            ax.axvline('2021-08-17', color="green", linestyle="--",  label='Fase Verde')
            ax.axvline('2021-11-01', color="m", linestyle="--",  label='Fim das restrições')
            
        plt.ylim(bottom=0)
        plt.axis([None, None, 0, None])
        ax.legend(bbox_to_anchor=(1.15, 1), loc='upper left')
        if save:
            filename = variable + '_vs_'+ covid_variable+'.png'
            plt.savefig(self.destination_folder_path + 'versus_covid/'+filename)
        plt.show()
    
    def alt_bands(start, end, ax=None, color = 'black'):
        ax = ax or plt.gca()
        x_left, x_right = ax.get_xlim()
        ax.axvspan(start, end, facecolor=color, alpha=0.1)
        ax.set_xlim(x_left, x_right)

    def plot_variable_and_covid_together(self, variable, covid_variables, show_key_pandemic_moments = True, show_all_phases = False, save = False):
        if not isinstance(covid_variables, list):
            covid_variables = [covid_variables]
        
        variables = [variable] + covid_variables
        trips_and_covid_plot = self.trips_and_covid[:].filter(variables)

        fig, ax = plt.subplots()
        fig.set_figwidth(20)
        fig.set_figheight(10)

        # ax.plot(trips_and_covid_plot.index, trips_and_covid_plot[variable], 'g', marker = 'o', label = variable)
        ax.plot(trips_and_covid_plot.index, trips_and_covid_plot[variable], 'g', label = variable)
        
        if show_key_pandemic_moments:
            ax.axvline(pd.to_datetime('2020-03-24'), color="black", linestyle="--",  label='Lockdown in SP', linewidth = 3.0)
            ax.axvline(pd.to_datetime('2021-11-01'), color="m", linestyle="--",  label='Fim das restrições', linewidth = 3.0)
            # ax.axvline(pd.to_datetime('2018-02-01'), color="black", linestyle="--",  label='Início dos dados')
        if show_all_phases:
            ax.axvline(pd.to_datetime('2020-05-27'), color="purple", linestyle="--",  label='Plano SP de retomada consciente')
            ax.axvline(pd.to_datetime('2020-10-06'), color="green", linestyle="--",  label='Fase Verde')
            ax.axvline(pd.to_datetime('2020-11-30'), color="yellow", linestyle="--",  label='Fase Amarela')
            ax.axvline(pd.to_datetime('2021-03-15'), color="red", linestyle="--",  label='Fase Emergencial')
            ax.axvline(pd.to_datetime('2021-08-17'), color="green", linestyle="--",  label='Fase Verde')
            # ax.axvline(pd.to_datetime('2022-01-15'), color="m", linestyle="--",  label='Quebra')
        
        # Verify if a secondary axis is necessary 
        if len(covid_variables) > 0:
            ax2 = ax.twinx()
            if (len(covid_variables) > 1):
                variable1 = 'new_cases_ma'
                variable2 = 'new_deaths_ma'
                ax2.plot(trips_and_covid_plot.index,
                        trips_and_covid_plot[variable2] * 30, 'r-',
                        label = variable2)
                ax2.plot(trips_and_covid_plot.index,
                        trips_and_covid_plot[variable1], 'b-',
                        label = variable1)
                label_y2 =  variable1 + " / " + variable2 + ' * 30'
                title = "'{variable}' vs '{variable1} and {variable2}'".format(variable = variable,
                                            variable1 = variable1, variable2 = variable2)
            else:
                covid_variable = covid_variables[0]
                ax2.plot(trips_and_covid_plot.index,
                        trips_and_covid_plot[covid_variable], 'b-')
                label_y2 = covid_variable
                title = "'{variable}' vs '{covid_variable}'".format(variable = variable, covid_variable = covid_variable)
            
            ax2.set_ylim(0)
            ax2.set_ylabel(label_y2, color='k', fontsize=20, labelpad = 20)
            ax2.legend(bbox_to_anchor = (0,  1), loc = 'lower left', fontsize = 18)
            for label in (ax2.get_xticklabels() + ax2.get_yticklabels()):
                label.set_fontsize(16)
        else:
            title = "'{variable}'".format(variable = variable)
        
        
        ax.set_ylim(0)
        ax.set_xlabel('Date', fontsize=20, labelpad = 20)
        ax.set_ylabel(variable, color='k', fontsize=20, labelpad = 20)
        if len(covid_variables) == 0:
            lgd = ax.legend(bbox_to_anchor = (0, 1), loc = 'upper left', fontsize = 18)
        else:
            lgd = ax.legend(bbox_to_anchor = (0, 1), loc = 'upper left', fontsize = 18)
        
        # Set tick font size
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontsize(16)
        
        
        # set monthly locator
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        # set formatter
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
        # set font and rotation for date tick labels
        plt.gcf().autofmt_xdate()
        
        plt.title(title, size=25, pad = 20)

        plt.ylim(bottom=0)
        plt.axis([None, None, 0, None])
        
        if save:
            filename = variable + '_vs_'+ str(covid_variables) + '_' + str(show_key_pandemic_moments) + '_' + str(show_all_phases) +  '.png'
            plt.savefig(self.destination_folder_path + 'versus_covid/' + filename, bbox_extra_artists=(lgd,), bbox_inches='tight')
            # fig.savefig('samplefigure', bbox_extra_artists=(lgd,), bbox_inches='tight')
        
        plt.show()