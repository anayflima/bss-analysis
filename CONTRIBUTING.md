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

```data_preprocessing/script_trips_duration_remove_outliers.py.py```
Read csv for year 2018 completed. Time = 2.150841474533081
For year = 2018, number of outliers = 3376 and percentage = 0.003024883610076733

Read csv for year 2019 completed. Time = 25.181352853775024
For year = 2019, number of outliers = 4029 and percentage = 0.0014485594222157026

Read csv for year 2020 completed. Time = 59.51447510719299
For year = 2020, number of outliers = 639 and percentage = 0.0002713411514121842

Read csv for year 2021 completed. Time = 46.23645734786987
For year = 2021, number of outliers = 488 and percentage = 0.00024099848437633494

Read csv for year 2022 completed. Time = 39.204540491104126
For year = 2022, number of outliers = 760 and percentage = 0.0012140090251986741

Time required to finish removing outliers from trip duration : 184.31453585624695


```script data_loading/script_load_trips.py```
len(df[(df['age'] < 0) | (df['age'] > 100)])
0
1116076
1116076
['tripduration', 'start_station_name_old', 'start_station_id', 'starttime', 'end_station_name_old', 'end_station_id', 'stoptime', 'birth_year', 'age', 'per_day', 'hour', 'week_day', 'weekend', 'holiday', 'start_station_name', 'end_station_name']
Time to complete trips data loading for year 2018: 247.46633911132812

len(df[(df['age'] < 0) | (df['age'] > 100)])
0
2781382
2781382
['tripduration', 'start_station_name_old', 'start_station_id', 'starttime', 'end_station_name_old', 'end_station_id', 'stoptime', 'birth_year', 'age', 'per_day', 'hour', 'week_day', 'weekend', 'holiday', 'start_station_name', 'end_station_name']
Time to complete trips data loading for year 2019: 645.9902968406677

len(df[(df['age'] < 0) | (df['age'] > 100)])
1643
10483
12126
['tripduration', 'start_station_name_old', 'start_station_id', 'starttime', 'end_station_name_old', 'end_station_id', 'stoptime', 'birth_year', 'age', 'per_day', 'hour', 'week_day', 'weekend', 'holiday', 'start_station_name', 'end_station_name']
Time to complete trips data loading for year 2020: 535.2631723880768

len(df[(df['age'] < 0) | (df['age'] > 100)])
1383
5556
6939
['tripduration', 'start_station_name_old', 'start_station_id', 'starttime', 'end_station_name_old', 'end_station_id', 'stoptime', 'birth_year', 'age', 'per_day', 'hour', 'week_day', 'weekend', 'holiday', 'start_station_name', 'end_station_name']
Time to complete trips data loading for year 2021: 373.0135705471039

len(df[(df['age'] < 0) | (df['age'] > 100)])
662
2381
3043
['tripduration', 'start_station_name_old', 'start_station_id', 'starttime', 'end_station_name_old', 'end_station_id', 'stoptime', 'birth_year', 'age', 'per_day', 'hour', 'week_day', 'weekend', 'holiday', 'start_station_name', 'end_station_name']
Time to complete trips data loading for year 2022: 156.89114546775818

len(df[(df['age'] < 0) | (df['age'] > 100)])
3688
3915878
3919566
['tripduration', 'start_station_name_old', 'start_station_id', 'starttime', 'end_station_name_old', 'end_station_id', 'stoptime', 'birth_year', 'age', 'per_day', 'hour', 'week_day', 'weekend', 'holiday', 'start_station_name', 'end_station_name']
Time to complete all trips data loading: 1920.34131193161

```python3 data_loading/script_join_trips.py```

Read csv completed. Time = 14.927061557769775
Join trips completed. Time = 12.433847665786743
Set index completed. Time = 0.008301496505737305
Save to csv completed. Time = 43.18208575248718
Time to join all trips: 70.55132055282593

```python3 data_preprocessing/script_trip_duration_remove_outliers.py```
Read csv for year 2018 completed. Time = 1.7772905826568604
For year = 2018, number of outliers = 3376 and percentage = 0.003024883610076733
Read csv for year 2019 completed. Time = 23.784977197647095
For year = 2019, number of outliers = 4029 and percentage = 0.0014485604638269753
Read csv for year 2020 completed. Time = 49.618144273757935
For year = 2020, number of outliers = 639 and percentage = 0.00027134138185375844
Read csv for year 2021 completed. Time = 41.71724772453308
For year = 2021, number of outliers = 298 and percentage = 0.00017290467672337516
Read csv for year 2022 completed. Time = 31.911243438720703
For year = 2022, number of outliers = 950 and percentage = 0.0010243239192573976
Time required to finish removing outliers from trip duration : 164.103942155838

```python3 data_preprocessing/script_trip_duration_remove_outliers_all_trips.py```

Read csv completed. Time = 16.715409517288208
For all trips, number of outliers = 9292 and percentage = 0.0010436510534956526
Time required to finish removing outliers from trip duration : 165.79472088813782

```python3 data_analysis/data_grouping/script_group_trips_by_day.py ```
Read csv completed. Time = 18.444847583770752
Group trips by day completed. Time = 0.7548930644989014
Save to csv completed. Time = 0.031673431396484375
Time to complete data grouping: 128.52215242385864

```python3 data_analysis/data_grouping/script_group_trips_by_week.py```
Read csv completed. Time = 19.180222034454346
Group trips by week completed. Time = 0.8159840106964111
Save to csv completed. Time = 0.008592844009399414
Time to complete data grouping: 128.9572606086731


```python3 data_analysis/data_grouping/script_group_trips_by_month.py```
Read csv completed. Time = 18.115416765213013
Transformation to time series completed. Time = 109.26228165626526
Group trips by month completed. Time = 0.6926479339599609
Save to csv completed. Time = 0.004079580307006836
Time to complete data grouping: 128.0744366645813

```python3 data_loading/script_load_all_trips.py ```
Time to complete all trips data loading: 1940.8311522006989

```python3 data_loading/script_load_trips_separated_by_year.py```

Time to complete trips data loading for year 2018: 253.9763445854187
Time to complete trips data loading for year 2019: 673.0248618125916
Time to complete trips data loading for year 2020: 551.5179438591003
Time to complete trips data loading for year 2021: 371.62895917892456
Time to complete trips data loading for year 2022: 163.98176503181458
Time to complete trips data loading, separated by year: 2014.1299316883087

```python3 data_analysis/circular_trips/script_circular_trips_percentage.py```
Circular trips selection completed. Time = 124.24235844612122


## Problems with data treatment

### Birth years that do not exist

