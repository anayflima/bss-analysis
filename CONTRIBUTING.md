## Runtime of scripts

The code was run in a i5 CORE, 256 SSD

```script_trips_data_treatment.py```
Time to complete trip data treatment: 258.33559370040894

```join_trips.py```
Read csv completed. Time = 17.123382329940796
Join trips completed. Time = 6.246486186981201
Set index completed. Time = 3.87420916557312
Save to csv completed. Time = 43.309144496917725
Time to join all trips: 70.5532877445221

```data_analysis/script_group_data_by_day_and_month.py```
Read csv completed. Time = 16.172327280044556
Group trips by day completed. Time = 93.81764578819275
Group trips by month completed. Time = 0.011400699615478516
Save to csv completed. Time = 0.03283286094665527
Time to complete data grouping: 110.03422355651855

```data_analysis/script_group_data_by_day_and_month.py``` - after distance
In plots, make y axis lower limit equal to zero

sys:1: DtypeWarning: Columns (14,15) have mixed types.Specify dtype option on import or set low_memory=False.
Read csv completed. Time = 30.456192016601562
/home/ana/Documents/ic/bss-analysis/data_analysis/modules/DataPreparation.py:42: SettingWithCopyWarning: 
A value is trying to be set on a copy of a slice from a DataFrame

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  df['age'][(df['age'] < 0) | (df['age'] > 100) ] = None
Group trips by day completed. Time = 502.0877923965454
Group trips by month completed. Time = 0.004772186279296875
Save to csv completed. Time = 0.023777484893798828
Time to complete data grouping: 532.5725593566895

## Problems with data treatment

### Birth years that do not exist

