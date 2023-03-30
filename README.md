# Impacts of the COVID-19 pandemic on the São Paulo bike-sharing system

## Introduction

This project aims to analyze the impact of the COVID-19 pandemic on the São Paulo bike-sharing system. For this purpose, we will be using data provided by the Brazilian bike-sharing company Tembici.

To be able to run the modules and scripts provided, it is necessary to have external access to the Tembici data.

The modules of this repository are basically divided into two main steps: Data Treatment and Data Analysis. A summary of each step's flow will be explained in the next sections.

## Virtual Environment

In order to create a Python virtual environment containing all libraries required for this project, run the following script:

```
./venv.sh
```

## Data Treatment

To facilitate the reproduction of the complete data treatment and data preprocessing steps, scripts ```.py``` that use the modules created were made available. Instructions explaining each of them are described in the correspondent subsections below.

### Initial treatment

The initial steps of the data treatment are the following:

1. Convert all files to CSV format;
2. Fix accents according to iso-8859-1;
3. Padronize column names;
4. Padronize file names.

To run this script, first it is necessary to put the original Tembici data in the path: ```data/trips/original_data```, in the filename format ```trips_BikeSampa_*.csv```. The resulting files will be moved to a folder called ```data/trips/treated_data```.

To run the script, execute the following command in the root repository:

```
python3 data_treatment/script_trips_data_treatment.py
```

### Data Loading

This step will aggregate all the data, originally divided by month, as well as prepare the data for the data analysis by adding some columns and converting the data to a time series format. It contains the following steps:

1. Convert some columns to datetime format;
2. Find source and destination station ids, names, and coordinates;
3. Transform data to time series (date as index);
4. Include an age column;
5. Add a distance column.

To run this step, you must first have executed the "Initial Treatment" section, and then run the following command:

```
python3 data_loading/script_load_all_trips.py
```

The resulting files will be moved to a folder called ```data/trips/loaded_trips```.

### Data preprocessing

This step will remove outliers from the data. It will:


1. Set to null all the trip durations longer than 12 hours;
2. Remove 2018, January data.

To execute the data preprocessing flow, you can run:

```
python3 data_preprocessing/script_trip_duration_remove_outliers_all_trips.py
```

The resulting files will be moved to a folder called ```data/trips/preprocessed```.

### Data grouping

The original data contains the information of individual trips. For some parts of the posterior data analysis, it is important to group the data by day, week, and month. The following scripts use the data from the ```data/trips/preprocessed``` folder, group them, and move the results to the ```data/trips/preprocessed/grouped``` folder.

```
python3 data_analysis/data_grouping/script_group_trips_by_day.py
```
```
python3 data_analysis/data_grouping/script_group_trips_by_week.py 
```
```
python3 data_analysis/data_grouping/script_group_trips_by_month.py
```

### Data separation

In some parts of the data analysis, we will need to compare some behaviors before and after the beginning of the COVID-19 pandemic in São Paulo. For this, we created a script that separates all trips into two files, one containing data before the pandemic and another one containing data during the pandemic. You can easily modify the start date of COVID-19 by changing the corresponding variables in the `.env` file.

```
python3 data_analysis/script_separate_trips_covid.py
```

## Data Analysis

The data analysis is in the ```data_analysis``` folder. It is possible to see the results in the Jupyter notebooks present in this folder.