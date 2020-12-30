import time
import pandas as pd
import numpy as np
import calendar
import datetime as dt

#get some info from https://www.geeksforgeeks.org/, stackoverflow, codecademy and udacity

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    #create list for cities, months and days
    cities = ['chicago', 'new york city', 'washington']
    months = [single_month.lower() for single_month in list(calendar.month_name[1:7])]
    months.append("all")
    days = [single_day.lower() for single_day in list(calendar.day_name)]
    days.append("all")
    city = ''
    month = ''
    day = ''
    
    #che if input values are right
    while(city not in cities):
        city = input("Enter a city between: Chicago, New york city, Washington\n").lower()
    
    while(month not in months):
        month = input("Enter a month between January and June, or type 'all'\n").lower()
        
    while(day not in days):
        day = input("Enter a week day or type 'all'\n").lower()
    
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #create dataframe from the city csv chosed by user
    df = pd.read_csv(city.replace(' ', '_') + '.csv')
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    #create three new columns for week day, month and hour
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['month'] = df['Start Time'].dt.month
    df['hour'] = df['Start Time'].dt.hour
    
    #filter rows by month and day if needed
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #find the most common month, day and start hour of dataframe
    most_popular_month = df['month'].mode()[0]
    print("Most popular month: ", calendar.month_name[most_popular_month])

    print("Most popular day: ", df['day_of_week'].mode()[0])

    print("Most popular hour: ", df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #find the most common start, end station and the combination of these two
    print("Most popular start station: ", df['Start Station'].mode()[0])

    print("Most popular end station: ", df['End Station'].mode()[0])

    print("Most popular combination of start station and end station trip: ", 
          (df['Start Station'] + " -> " + df['End Station']).mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #find the total time travelled (in minutes)
    tot_seconds_travelled = df['Trip Duration'].sum()
    tot_minutes_travelled = tot_seconds_travelled/60
    print("Total minutes travelled: ", tot_minutes_travelled)

    #find the mean time travelled (in minutes)
    mean_seconds_travelled = df['Trip Duration'].mean()
    mean_minutes_travelled = mean_seconds_travelled/60
    print("Mean minutes travelled: ", mean_minutes_travelled)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #display the counts of user types
    print(df['User Type'].value_counts())

    #find the number of male and female in the dataframe
    if 'Gender' in df:
        print(df['Gender'].value_counts())

    #find the earliest, most recent and common birth year
    if 'Birth Year' in df: 
        print('Earlier year: ', df['Birth Year'].min())
        print('Most recent year: ', df['Birth Year'].max())
        print('Most common year:', df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def display_data(df):
    #display the dataframe to the user, 5 row unless he/she types 'no' on the keyboard 
    start_loc = 0
    view_data = ''
    while view_data not in ['yes', 'no']:
        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    if view_data == 'yes':
        while view_data == 'yes':
            print(df.iloc[start_loc:start_loc+5])
            start_loc += 5
            view_data = ''
            while view_data not in ['yes', 'no']:
                view_data = input("Do you wish to continue?: ").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
