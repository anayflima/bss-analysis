#install.packages('dplyr')
library(dplyr)
#install.packages('ISLR')
library(ISLR)

trips = read.csv('Documents/bss-analysis/data/trips/preprocessed/grouped/trips_grouped_by_week_mean.csv',sep=',')
trips['index'] = seq(1, nrow(trips), by=1)
trips = mutate(trips, date= as.Date(date, format= "%Y-%m-%d"))

#trips = subset(trips, date >= as.Date('2018-02-01') & date <= as.Date('2021-05-02'))
trips = subset(trips, date >= as.Date('2020-09-20'))

break_point = which(trips$date == '2020-12-06')
#break_point = 10
break_date = trips[break_point,"date"]

#load strucchange package
library(strucchange)

sctest(trips$tripduration ~ trips$index, type = "Chow", point = break_point)
