
import pickle
import shutil
import math
from decimal import Decimal, ROUND_HALF_UP
import argparse

import yrreader

weather_symbols = {'1' : '☉',
                   '2' : '☉☁',
                   '3' : '☁☉',
                   '4' : '☁',

                   # Showers
                   '40': '☉☔', # Light
                   '5' : '☉☔', 
                   '41': '☉☔', # Heavy

                   # Showers with thunderstorm
                   '24': '☉☔☈', # Light
                   '6' : '☉☔☈', 
                   '25': '☉☔☈', # Heavy

                   # Sleet showers
                   '42': '☉☔❄', # Light
                   '7' : '☉☔❄', 
                   '43': '☉☔❄', # Heavy

                   # Sleet showers with thunderstorm
                   '26': '☉☔❄☈', # Light
                   '20': '☉☔❄☈', 
                   '27': '☉☔❄☈', # Heavy

                   # Snow showers█
                   '44': '☉❄', # Light
                   '8' : '☉❄', 
                   '45': '☉❄', # Heavy

                   # Snow showers with thunderstorm
                   '28': '☉❄☈', # Light
                   '21': '☉❄☈', 
                   '29': '☉❄☈', # Heavy

                   # Rain
                   '46': '☔', # Light
                   '9' : '☔',
                   '10': '☔', # Heavy ☂

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
    
def round_to_int(value):
    return int(Decimal(value).quantize(Decimal('1.'), rounding=ROUND_HALF_UP))
    
def extract_data(weatherdata):
    return [{'instant': time_data['@from'],
             'temperature': time_data['temperature']['@value'],
             'symbol': time_data['symbol']['@numberEx'],
             'precip': {'value': round_to_int(time_data['precipitation']['@value']),
                        'min': round_to_int(time_data['precipitation']['@minvalue']) if '@minvalue' in time_data['precipitation'] else 0,
                        'max': round_to_int(time_data['precipitation']['@maxvalue']) if '@maxvalue' in time_data['precipitation'] else 0},
             'wind': {'speed': round_to_int(time_data['windSpeed']['@mps']),
                      'direction': Decimal(time_data['windDirection']['@deg'])}}
            for time_data in pick_forecast(weatherdata)]

def extract_credit(weatherdata):
    return {'text': "".join(weatherdata['weatherdata']['credit']['link']['@text']),
            'link': weatherdata['weatherdata']['credit']['link']['@url']}

def pick_hour(instant):
    return instant[11:13]

def symbol_for(number):
    return weather_symbols[number] if number in weather_symbols else number

def bar_for(number):
    precip_bars = {0: ' ', 1: '▁', 2: '▂', 3: '▃', 4: '▄', 5: '▅', 6: '▆', 7: '▇', 8: '█'}
    return precip_bars[max(0, min(8, number))]
    
def space_for_zero(number):
    return str(number) if number is not 0 else ''

def arrow_for(direction):
    direction_arrows = {0: '↑', 1: '↗', 2: '→', 3: '↘', 4: '↓', 5: '↙', 6: '←',7: '↖' }
    index = int((direction / Decimal('45')).quantize(Decimal('1.'), rounding=ROUND_HALF_UP)) % 8
    return direction_arrows[index]

def format_cell(data):
    return "{:>4}".format(data)

def format_row(data_row, columns):
    return "".join([format_cell(cell) for cell in data_row])[0:columns]

def format_rows(datapoints, credit):
    columns = shutil.get_terminal_size().columns
    return [format_row([symbol_for(dp['symbol']) + ' ' for dp in datapoints], columns),
            format_row([dp['temperature'] + '°' for dp in datapoints], columns),
            format_row([bar_for(dp['precip']['min']) + bar_for(dp['precip']['value']) + bar_for(dp['precip']['max']) for dp in datapoints], columns),
            format_row([space_for_zero(dp['precip']['value']) + ' ' for dp in datapoints], columns),
            format_row([str(dp['wind']['speed']) + arrow_for(dp['wind']['direction']) for dp in datapoints], columns),
            format_row([pick_hour(dp['instant']) + 'h' for dp in datapoints], columns),
            '',
            credit['text'],
            credit['link']]

def format_forecast(forecast):
    return format_rows(extract_data(forecast),
                       extract_credit(forecast))

def print_forecast(lines):
    print("\n".join(lines))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Terminal-based weather forecast from yr.no')
    parser.add_argument('--location', '-l', required=True, help='Location name in /-notation, eg: Sweden/Stockholm/Stockholm')
    args = parser.parse_args()
    forecast = yrreader.forecast_for(args.location)
    print_forecast(format_forecast(forecast))
    
    
