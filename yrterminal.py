
import pickle


def pick_hour_data(forecast):
    innerforecast = forecast['weatherdata']['forecast']
    hour_by_hour_data = innerforecast['tabular']['time']
    return [(hour_data['@from'], hour_data['temperature']['@value'])
            for hour_data in hour_by_hour_data]


def read_example():
    with open('example-forecast.dat', 'rb') as f:
        return  pickle.loads(f.read())

hour_by_hour_forecast = read_example()
hour_data = pick_hour_data(hour_by_hour_forecast)
#print(hour_by_hour_forecast)

