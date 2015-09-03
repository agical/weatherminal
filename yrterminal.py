
import pickle
import shutil
import math

from yrexample import read_example

weather_symbols = {'1' : '☀',
                   '2' : '☀☁',
                   '3' : '☁☀',
                   '4' : '☁',

                   # Showers
                   '40': '☀☂', # Light
                   '5' : '☀☂', 
                   '41': '☀☂', # Heavy

                   # Showers with thunderstorm
                   '24': '☀☂☈', # Light
                   '6' : '☀☂☈', 
                   '25': '☀☂☈', # Heavy

                   # Sleet showers
                   '42': '☀☂❄', # Light
                   '7' : '☀☂❄', 
                   '43': '☀☂❄', # Heavy

                   # Sleet showers with thunderstorm
                   '26': '☀☂❄☈', # Light
                   '20': '☀☂❄☈', 
                   '27': '☀☂❄☈', # Heavy

                   # Snow showers█
                   '44': '☀❄', # Light
                   '8' : '☀❄', 
                   '45': '☀❄', # Heavy

                   # Snow showers with thunderstorm
                   '28': '☀❄☈', # Light
                   '21': '☀❄☈', 
                   '29': '☀❄☈', # Heavy

                   # Rain
                   '46': '☂', # Light
                   '9' : '☂',
                   '10': '☂', # Heavy

                   # Rain with thunderstorm

                   # Sleet

                   # Sleet with thunderstorm
                   
                   # Snow
                   '49': '❄', # Light
                   '13': '❄',
                   '50': '❄', # Heavy

                   # Snow with thunderstorm
                   
                   # Fog
                   '15': '▒'}

def pick_forecast(weatherdata):
    return weatherdata['weatherdata']['forecast']['tabular']['time']
    
def pick_hour_data(weatherdata):
    return [{'instant': hour_data['@from'],
             'temperature': hour_data['temperature']['@value'],
             'symbol': hour_data['symbol']['@numberEx'],
             'precip': int(round(float(hour_data['precipitation']['@value'])))}
            for hour_data in pick_forecast(weatherdata)]

def pick_hour(instant):
    return instant[11:13]

def format_cell(data):
    return "{:>4}".format(data)

def format_row(data_row, columns):
    return "".join([format_cell(cell) for cell in data_row])[0:columns]

def symbol_for(number):
    return weather_symbols[number] if number in weather_symbols else number

def bar_for(number):
    precip_bars = {0: ' ', 1: '▁', 2: '▂', 3: '▃', 4: '▄', 5: '▅', 6: '▆', 7: '▇', 8: '█'}
    return precip_bars[max(0, min(8, math.ceil(number / 2)))]
    
def space_for_zero(number):
    return str(number) if number is not 0 else ''  

def format_forecast(hours):
    columns = shutil.get_terminal_size().columns
    return [format_row([symbol_for(hour['symbol']) + ' ' for hour in hours], columns),
            format_row([hour['temperature'] + '°' for hour in hours], columns),
            format_row([bar_for(hour['precip']) + ' ' for hour in hours], columns),
            format_row([space_for_zero(hour['precip']) + ' ' for hour in hours], columns),
            format_row([pick_hour(hour['instant']) + ' ' for hour in hours], columns)]




hour_by_hour_forecast = read_example('mount_everest')
hour_data = pick_hour_data(hour_by_hour_forecast)

#print(hour_by_hour_forecast)

