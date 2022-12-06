# Overview

# Data Treatment
- [x] Adapt existing code to new data
- [x] Modularize
- [x] Script to run complete trips data treatment
- [x] Add load trips module
- [x] Stations treatment -> consider id
- [x] Get distance of each combination of stations

# Data analysis

- [x] Fix load_trips module
- [x] Get covid data
- [x] Group covid by month
- [x] Group trips data by day, month, and week
- [x] Calculate correlation between bss trips and covid data
- [x] Plot the evolution of the following variables: 
     - [x] Number of trips
     - [x] Average of trip_duration
     - [x] Age of people
     - [x] Trip distance
- [ ] Chow test to verify if there is a structural break after COVID
- [x] Plot evolution in a beautiful way
- [ ] Modularize
     - [ ] Save all plots in a folder
     - [ ] Transform plots to a pdf or latex file
- [ ] Script to run complete trips data analysis and export
- [x] Plot trips distribution histogram for trip duration and age
     -  [ ] delivery was the cause of trip duration increase? 
- [x] In plots, make y axis lower limit equal to zero
- [ ] Find flow difference
          - flows that have stayed and flows that are gone after the pandemic
- [x] Plot covid deaths and cases in the same chart, together with a trip variable
- [ ] Find the following attributes for each trip - in a separate module, to filter trips
          - [ ] afternoon
          - [ ] lunchtime
          - [ ] non-working days
- [x] Calculate age should be in the TripsLoading module
- [x] Set all trip duration variables with more than 12 hours to null
- [x] Script to run all trip loading and data treatment/preprocessing flows
- [ ] Plot the evolution of trips variables using the rolling average for the last 30 days
- [x] Add latitude and longitude columns to the load_trips script
