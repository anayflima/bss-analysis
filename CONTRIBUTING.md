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

```python3 data_loading/script_load_all_trips.py ```
Time to complete adding columns: 2886.8249270915985
Time to complete all trips data loading: 3113.757824420929

```python3 data_loading/script_load_trips_separated_by_year.py```

 python3 data_loading/script_load_trips_separated_by_year.py 
Time to complete trips data loading for year 2018: 262.47457814216614
Time to complete trips data loading for year 2019: 732.0868294239044
Time to complete trips data loading for year 2020: 573.6293625831604
Time to complete trips data loading for year 2021: 372.20327067375183
Time to complete trips data loading for year 2022: 162.44092321395874
Time to complete trips data loading, separated by year: 2102.835031747818

```python3 data_analysis/circular_trips/script_circular_trips_percentage.py```
Circular trips selection completed. Time = 124.24235844612122

```python3 data_analysis/particular_trips/script_particular_trips_percentage.py```
Data preparation completed. Time = 210.30523920059204
Monthly percentages calculation completed. Time = 5.183893442153931
Percentage of particular trips completed. Time = 215.48913264274597

## Problems with data treatment

### Birth years that do not exist



## WITH A i7 core COMPUTER

```python3 data_treatment/script_trips_data_treatment.py```

Transforming xlsx to csv
Copying csv files to destination folder
Fixing accents and column names
Padronizing filenames
DataTreatment completed
Time to complete trip data treatment: 357.31073665618896

```python3 data_loading/script_load_all_trips.py```
Time to complete loading trips files: 1904.4382495880127
Time to complete adding columns: 71.85755348205566
Time to complete all trips data loading: 2228.53213095665

python3 data_preprocessing/script_trip_duration_remove_outliers_all_trips.py
sys:1: DtypeWarning: Columns (8) have mixed types.Specify dtype option on import or set low_memory=False.
Read csv completed. Time = 41.10229301452637
For all trips, number of outliers = 8938 and percentage = 0.00105621515497399
Time required to finish removing outliers from trip duration : 205.16493678092957

 python3 data_analysis/script_separate_trips_covid.py
sys:1: DtypeWarning: Columns (8) have mixed types.Specify dtype option on import or set low_memory=False.
Read csv completed. Time = 31.85250687599182
Before covid: Save to csv completed. Time = 162.50528717041016
During covid: Save to csv completed. Time = 67.52227759361267
Time to complete trips separation: 261.88009428977966


python3 data_analysis/data_grouping/script_group_trips_by_week.py 
sys:1: DtypeWarning: Columns (8) have mixed types.Specify dtype option on import or set low_memory=False.
Read csv completed. Time = 40.04763221740723
Transformation to time series completed. Time = 100.05472159385681
Group trips by week completed. Time = 1.6687214374542236
Save to csv completed. Time = 0.011386632919311523
Time to complete data grouping: 141.78248596191406

python3 data_analysis/data_grouping/script_group_trips_by_month.py 
sys:1: DtypeWarning: Columns (8) have mixed types.Specify dtype option on import or set low_memory=False.
Read csv completed. Time = 37.64999866485596
Transformation to time series completed. Time = 100.66694927215576
Group trips by month completed. Time = 1.5107622146606445
Save to csv completed. Time = 0.0042226314544677734
Time to complete data grouping: 139.83196115493774

python3 data_analysis/data_grouping/script_group_trips_by_day.py 
sys:1: DtypeWarning: Columns (8) have mixed types.Specify dtype option on import or set low_memory=False.
Read csv completed. Time = 38.42503118515015
Transformation to time series completed. Time = 90.11483764648438
Group trips by day completed. Time = 1.532224416732788
Save to csv completed. Time = 0.08030843734741211
Time to complete data grouping: 130.15242958068848

python3 data_loading/script_load_trips_separated_by_year.py 
Time to complete trips data loading for year 2018: 443.4300260543823
Time to complete trips data loading for year 2019: 985.4648771286011
Time to complete trips data loading for year 2020: 1687.5627753734589
Time to complete trips data loading for year 2021: 522.2375364303589
Time to complete trips data loading for year 2022: 141.03629422187805
Time to complete trips data loading, separated by year: 3779.7315378189087

