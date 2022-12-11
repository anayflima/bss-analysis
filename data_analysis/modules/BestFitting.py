import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
import datetime
import sys
sys.path.append('./data_analysis')
sys.path.append('../../data_analysis')
from modules.DataPreparation import DataPreparation
import os

class BestFitting:
    def __init__(self, destination_folder_path):
        self.destination_folder_path = destination_folder_path

            
    def alt_bands(self, start, end, ax=None, color = 'black', label = ''):
        ax = ax or plt.gca()
        x_left, x_right = ax.get_xlim()
        if label == '':
            ax.axvspan(start, end, facecolor=color, alpha=0.1)
        else:
            ax.axvspan(start, end, facecolor=color, alpha=0.1, label = label)
        ax.set_xlim(x_left, x_right)

    def find_best_plot_fit(self, trips, variable,
                           break_dates = {os.environ['FIRST_DAY_COVID'] : "Lockdown in SP (" + str(os.environ['FIRST_DAY_COVID']) + ")"},
                                        poly_degree = 1, save = True, filename = '', analysis = False):
        plt.clf()
        plt.figure(figsize =(12, 8))
        df = trips.copy(deep=True)
        df['range'] = list(range(len(df)))

        xs = []
        ys = []
        coeffs = []
        y_hats = []

        
        keys = list(break_dates.keys())
        if analysis:
            initial_i = 1
        else:
            initial_i = 0
        if len(break_dates) > 0:
            for i in range(initial_i, len(break_dates) + 1):
                if i == 0:
                    end_date = pd.to_datetime(keys[i]) + datetime.timedelta(days=-1)
                    x = df.loc[:end_date,'range']
                    y = df.loc[:end_date, variable]
                else:
                    # start_date = pd.to_datetime(keys[i-1]) + datetime.timedelta(days=1)
                    start_date = pd.to_datetime(keys[i-1])
                    if i == len(break_dates):
                        x = df.loc[start_date:,'range']
                        y = df.loc[start_date:, variable]
                    else:
                        end_date = pd.to_datetime(keys[i]) + datetime.timedelta(days=-1)
                        x = df.loc[start_date:end_date,'range']
                        y = df.loc[start_date:end_date, variable]
                xs.append(x)
                ys.append(y)
                coeff = np.polyfit(x, y, poly_degree)
                poly_eqn = np.poly1d(coeff)
                y_hat = poly_eqn(x)
                coeffs.append(coeff)
                y_hats.append(y_hat)

        fig, ax = plt.subplots()
        fig.set_figwidth(20)
        fig.set_figheight(10)

        # '2020-10-06': 'Fase Verde'
        # '2020-11-30': 'Fase Amarela',

        # self.alt_bands(start = pd.to_datetime('2020-10-06'), end = pd.to_datetime('2020-11-30'), color= 'green')

        # ax.plot(df[keys[0]:].index, df.loc[keys[0]:, variable], 'ro')
        ax.plot(df.index, df.loc[:, variable], 'ro')

        for i in range(len(y_hats)):
            extended_y_hat = []
            for j in range(len(y_hats)):
                if i == j:
                    extended_y_hat = np.append(extended_y_hat, y_hats[i])
                else:
                    extended_y_hat = np.append(extended_y_hat, [None]*len(xs[j]))
            y_hats[i] = extended_y_hat
        
        if analysis:
            for y_hat in y_hats:
                line = plt.plot(trips[keys[0]:].index,y_hat)
        else:
            for y_hat in y_hats:
                line = plt.plot(trips[:].index,y_hat)
        plt.ylim(bottom=0)

        # plt.xlim(left=datetime.date(2018,1,1))
        plt.ylim(top=trips[variable].max()*1.05)
        colors = 2 * list(mcolors.TABLEAU_COLORS.keys()) + list(mcolors.CSS4_COLORS.keys())
        # ax.axvline(pd.to_datetime(df.index[0]), color= colors[0], linestyle="--", 
        #             label=df.index[0].strftime('%Y-%m-%d'))

        for i in range(len(break_dates)):
            ax.axvline(pd.to_datetime(keys[i]), color=colors[i+1],
                                    linestyle="--",  label=break_dates[keys[i]] + " (" + keys[i] +")")

        # '2020-05-27': 'Plano SP de retomada consciente', 
        # '2020-10-06': 'Fase Verde', 

        if analysis:
            self.alt_bands(start = '2020-05-27', end = '2020-10-06', color= 'orange', label = 'Retomada das atividades')
            self.alt_bands(start = '2022-01-10', end = '2022-04-30', color= 'orange', label = '')
            self.alt_bands(start = '2020-10-06', end = '2020-11-30', color= 'green', label = 'Durante a Fase Verde')
            self.alt_bands(start = '2021-08-17', end = '2021-11-01', color= 'green', label = '')
            self.alt_bands(start = '2021-01-04', end = '2021-08-17', color= 'red', label = 'Fase Laranja, Vermelha e Emergencial e de Transição')


        # set monthly locator
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        # set formatter
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
        # set font and rotation for date tick labels
        plt.gcf().autofmt_xdate()
        
        # '2021-02-06': 'Fase Vermelha',
               # '2021-03-01': 'Fase Laranja',
               # '2021-03-06': 'Fase Vermelha',
               # '2021-03-15': 'Fase Emergencial',
               # '2021-04-12': 'Fase Vermelha',
        # '2021-08-17': "Fase Verde",
        # '2021-11-01': 'Fim das restrições'
        # set font and rotation for date tick labels
        plt.gcf().autofmt_xdate()

        ax.set_xlabel('date', color='k', fontsize=22, labelpad = 10)
        ax.set_ylabel('{variable}'.format(variable = variable), color='k', fontsize=22, labelpad = 10)

        title = 'Linear fit for {variable} variable'.format(variable = variable)
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontsize(16)
        plt.title(title, size=28, pad = 15)
        # lgd = ax.legend(bbox_to_anchor=(1, 1), loc='upper left', fontsize = 18)
        lgd = ax.legend(bbox_to_anchor=(0, 1), loc='upper left', fontsize = 18)
        # ax.legend(loc = 'lower right',fontsize = 22)
        # ax.legend(loc = 'upper left',fontsize = 22)
        if save:
            file = variable + '_' + str(list(break_dates.keys())) + '_' + str(poly_degree) + '.png'
            plt.savefig(self.destination_folder_path + file, bbox_extra_artists=(lgd,), bbox_inches='tight')
        return coeffs