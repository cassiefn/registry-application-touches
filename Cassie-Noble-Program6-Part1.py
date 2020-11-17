# Cassie Noble
# CSCI 127
# Program 6: Data Visualization
# Part 1
# 7/5/2018
# -------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------------------------

# Program Description:
# This program takes in a file of Practitioner Registry application submission data collected through the
# Early Childhood Project Practitioner Registry. Child Care Licensing rule has recently changed to require
# Practitioner Registry participation for all licensed and registered childcare providers in direct care roles,
# and so we are interested in monitoring the increase of applications in the Practitioner Registry.
# The dataframe is condensed to only include application submission dates. Then a new dataframe is created to
# cross reference the same date span and count up the number of application touches for each date (month/year).
# This information is then displayed as a line graph of number of application touches over time.

# -------------------------------------------------

# create dictionary of month string names and ints
months_dict = {}
months_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
months_values = np.arange(1, 13)

# loop through all months and connect with associated ints in dictionary
for i in range(len(months_names)):
    months_dict[months_names[i]] = months_values[i]

# -------------------------------------------------

# return month int from string
def convert_month(month_str):
    return months_dict[month_str]

# -------------------------------------------------

# create a new dataframe containing submission month and year
def create_month_year_df(file_df):
    # initialize new dataframe with month and year columns
    columns = ["month", "year"]
    month_year_df = pd.DataFrame(columns = columns)

    # loop through length of dataframe
    for i in range(len(file_df)):
        date = file_df.ix[i, "Submit Status Date"]  # pull out submission date from each row
        month_str = date[-6:-3]                     # pull out month from date
        month_int = convert_month(month_str)        # convert month from string to int
        year = int(date[-2:]) + 2000                # pull out year from date

        # create temporary dataframe containing just this row of info, then add to new dataframe
        temp_df = pd.DataFrame([[month_int, year]], columns = columns)
        month_year_df = month_year_df.append(temp_df, ignore_index = True)

    return month_year_df

# -------------------------------------------------

# count number of submissions per month and year and store in counter dataframe
def submissions_counter(month_year_df):
    # calculate minimum and maximum year in dataframe
    year_min = month_year_df["year"].min()
    year_max = month_year_df["year"].max()

    # initialize counter dataframe with month, year, date as string, and counter variable
    columns = ["month", "year", "month-year", "counter"]
    counter_df = pd.DataFrame(columns = columns)

    # create an array of all months in a year and an array of all years in dataframe
    months = np.arange(1, 13)
    years = np.arange(year_min, year_max + 1)

    # loop through all years in dataframe
    for year in years:
        # loop through all months in a year
        for month in months:
            # get month as string from months dictionary
            month_str = list(months_dict.keys())[list(months_dict.values()).index(month)]
            # create date as string
            month_year = month_str + " " + str(year)
            # create temporary dataframe containing just this row of info, then add to counter dataframe
            temp_df = pd.DataFrame([[month, year, month_year, 0]], columns = columns)
            counter_df = counter_df.append(temp_df, ignore_index = True)

    # loop through all dates in original dataframe
    for actual_date in month_year_df.values:
        # loop through length of dates in counter dataframe backwards
        for i in range(len(counter_df.values) -1, -1, -1):
            # check if years are equal
            if counter_df.values[i][1] == actual_date[1]:
                # check if months are equal
                if actual_date[0] == counter_df.values[i][0]:
                    # if matching month-date combination is found, then add one to that counter in counter dataframe
                    counter_df.loc[i, "counter"] += 1
                    break       # no need to keep searching if match has been found

    return counter_df

# -------------------------------------------------

def main():
    submission_data_frame = pd.read_csv("submission-history.csv")   # read in csv file

    month_year_df = create_month_year_df(submission_data_frame) # create new dataframe of submission date info
    counter_df = submissions_counter(month_year_df)             # create dataframe of submission date counters

    # plot submission date counter dataframe with each month as a point on the graph and total submissions on the y-axis
    counter_df.plot("month-year", "counter", legend = False)
    plt.xlim(149, 209)                              # limit display to June 2013 forward
    plt.ylim(0, counter_df["counter"][209] + 100)   # set y limits to go from 0 to slightly more than the last value
    plt.title("Registry Application Touches Over Time")
    plt.ylabel("Count of application touches")

    # create xticks array and convert xticks labels to display as month-year string combination
    xticks = np.arange(149, 210, 6)
    xticklab = []
    for x in xticks:
        xticklab.append(counter_df["month-year"][x])
    plt.xticks(xticks, xticklab, rotation = 90)

    plt.show()

# -------------------------------------------------

main()



