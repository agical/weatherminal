
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
             'temperature': round_to_int(time_data['temperature']['@value']),
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


def symbol_for(number):
    return weather_symbols[number] if number in weather_symbols else number

def temperature_graph_row(datapoints, row_temp, columns):
    return format_row([(str(row_temp)+'°' if dp['temperature'] == row_temp else ' ') for dp in datapoints], columns)

def bar_for(number):
    precip_bars = {0: ' ', 1: '▁', 2: '▂', 3: '▃', 4: '▄', 5: '▅', 6: '▆', 7: '▇', 8: '█'}
    return precip_bars[max(0, min(8, number))]
    
def space_for_zero(number):
    return str(number) if number is not 0 else ''

def arrow_for(direction):
    direction_arrows = {0: '↑', 1: '↗', 2: '→', 3: '↘', 4: '↓', 5: '↙', 6: '←',7: '↖' }
    index = int((direction / Decimal('45')).quantize(Decimal('1.'), rounding=ROUND_HALF_UP)) % 8
    return direction_arrows[index]

def pick_hour(instant):
    return instant[11:13]


def format_cell(data):
    return "{:>4}".format(data)

def format_row(data_row, columns):
    return "".join([format_cell(cell) for cell in data_row])[0:columns]


def symbol_row(datapoints, columns):
    return [format_row([symbol_for(dp['symbol']) + ' ' for dp in datapoints], columns)]
    
def temperature_graph(datapoints, columns):
    min_temp = min([dp['temperature'] for dp in datapoints])
    max_temp = max([dp['temperature'] for dp in datapoints])
    return reversed([temperature_graph_row(datapoints, step_temp, columns)
                     for step_temp in range(min_temp, max_temp + 1)])

def temperature_line(datapoints, columns):
    return [format_row([str(dp['temperature']) + '°' for dp in datapoints], columns)]
    
def precip_rows(datapoints, columns):
    return [format_row([bar_for(dp['precip']['min']) + bar_for(dp['precip']['value']) + bar_for(dp['precip']['max']) for dp in datapoints], columns),
            format_row([space_for_zero(dp['precip']['value']) + ' ' for dp in datapoints], columns)]

def wind_row(datapoints, columns):
    return [format_row([str(dp['wind']['speed']) + arrow_for(dp['wind']['direction']) for dp in datapoints], columns)]

def hour_row(datapoints, columns):
    return [format_row([pick_hour(dp['instant']) + 'h' for dp in datapoints], columns)]

def credit_rows(credit):
    return ['',
            credit['text'],
            credit['link']]


def format_rows(datapoints, credit):
    columns = shutil.get_terminal_size().columns
    return [row
            for rows in [symbol_row(datapoints, columns),
                         temperature_graph(datapoints, columns),
#                         temperature_line(datapoints, columns),
                         precip_rows(datapoints, columns),
                         wind_row(datapoints, columns),
                         hour_row(datapoints, columns),
                         credit_rows(credit)]
            for row in rows]

def format_forecast(forecast):
    return format_rows(extract_data(forecast),
                       extract_credit(forecast))

def print_forecast(lines):
    print("\n".join(lines))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A terminal-based weather forecast",
                                     epilog="Weather forecast from yr.no, delivered by the Norwegian Meteorological Institute and the NRK")
    parser.add_argument('location', metavar='LOCATION', help='Location name in /-notation, eg: Sweden/Stockholm/Stockholm')
    args = parser.parse_args()
    forecast = yrreader.forecast_for(args.location)
    print_forecast(format_forecast(forecast))
    
    
