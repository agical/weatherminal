
import pickle
import shutil

    



def pick_hour_data(forecast):
    innerforecast = forecast['weatherdata']['forecast']
    hour_by_hour_data = innerforecast['tabular']['time']
    return [{'instant': hour_data['@from'],
             'temperature': hour_data['temperature']['@value']}
            for hour_data in hour_by_hour_data]


def read_example():
    with open('example-forecast.dat', 'rb') as f:
        return  pickle.loads(f.read())

    
def pick_hour(instant):
    return instant[11:13]

def format_cell(data):
    return "{:>4}".format(data)

def format_row(data_row, columns):
    return "".join([format_cell(cell) for cell in data_row])[0:columns]

def format_forecast(hours):
    columns = shutil.get_terminal_size().columns
    return [format_row([pick_hour(hour['instant']) for hour in hours], columns),
            format_row([hour['temperature'] for hour in hours], columns)]




hour_by_hour_forecast = read_example()
hour_data = pick_hour_data(hour_by_hour_forecast)

#print(hour_by_hour_forecast)

