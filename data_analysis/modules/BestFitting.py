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

    def find_best_plot_fit(self, trips, variable, break_dates = [os.environ['FIRST_DAY_COVID']],
                                        poly_degree = 1, save = True, filename = ''):
        plt.clf()
        plt.figure(figsize =(12, 8))
        df = trips.copy(deep=True)
        df['range'] = list(range(len(df)))

        xs = []
        ys = []
        coeffs = []
        y_hats = []
        if len(break_dates) > 0:
            for i in range(len(break_dates) + 1):
                if i == 0:
                    x = df.loc[:break_dates[i],'range']
                    y = df.loc[:break_dates[i], variable]
                else:
                    start_date = pd.to_datetime(break_dates[i-1]) + datetime.timedelta(days=1)
                    if i == len(break_dates):
                        x = df.loc[start_date:,'range']
                        y = df.loc[start_date:, variable]
                    else:
                        x = df.loc[start_date:break_dates[i],'range']
                        y = df.loc[start_date:break_dates[i], variable]
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

        ax.plot(df.index, df.loc[:, variable], 'ro')

        for i in range(len(y_hats)):
            extended_y_hat = []
            for j in range(len(y_hats)):
                if i == j:
                    extended_y_hat = np.append(extended_y_hat, y_hats[i])
                else:
                    extended_y_hat = np.append(extended_y_hat, [None]*len(xs[j]))
            y_hats[i] = extended_y_hat
        
        for y_hat in y_hats:
            line = plt.plot(df.index,y_hat)
        plt.ylim(bottom=0)
        # plt.xlim(left=datetime.date(2018,1,1))
        plt.ylim(top=trips[variable].max()*1.05)
        keys = list(mcolors.TABLEAU_COLORS.keys())
        ax.axvline(pd.to_datetime(df.index[0]), color= keys[0], linestyle="--", 
                    label=df.index[0].strftime('%Y-%m-%d'))
        for i in range(len(break_dates)):
            ax.axvline(pd.to_datetime(break_dates[i]), color=keys[i+1],
                                    linestyle="--",  label=break_dates[i])

        # set monthly locator
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))

        # set formatter
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
        
        # set font and rotation for date tick labels
        plt.gcf().autofmt_xdate()

        ax.set_xlabel('date', color='k', fontsize=22, labelpad = 10)
        ax.set_ylabel('{variable}'.format(variable = variable), color='k', fontsize=22, labelpad = 10)

        title = 'Linear fit for {variable} variable'.format(variable = variable)
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontsize(16)
        plt.title(title, size=28, pad = 15)
        ax.legend(bbox_to_anchor=(1, 1), loc='upper left', fontsize = 18)
        # ax.legend(loc = 'lower right',fontsize = 22)
        # ax.legend(loc = 'upper left',fontsize = 22)
        if save:
            filename = variable + '_' + filename + '_' + str(poly_degree) + '.png'
            plt.savefig(self.destination_folder_path + filename)
        return coeffs