# Impacts of the COVID-19 pandemic on the São Paulo bike-sharing system

## Data Treatment

Initial steps

1 - convert all files to csv format
2 - fix accents according to iso-8859-1
3 - padronize column names
4 - padronize filenames (+-)

Load Trips

aggregate data by ____ (filter per file name)

- convert to datetime (there are two different formats!!!)
- find stations ids, name, latitude and longitude columns
- transform to time series (date as index)
- add age column
- add distance column

First, you have to run the load trips script:

```
python3 data_loading/script_load_all_trips.py
```

```
python3 data_preprocessing/script_trip_duration_remove_outliers_all_trips.py
```

```
python3 data_analysis/script_separate_trips_covid.py
```

