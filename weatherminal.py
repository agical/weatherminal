import argparse
import urllib
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from yr.libyr import Yr

import formatters 

def forecast_for(location):
    return Yr(location_name=location, forecast_link='forecast_hour_by_hour').dictionary
    
def pick_forecast(weatherdata):
    return weatherdata['weatherdata']['forecast']['tabular']['time']
    
def round_to_int(value):
    return int(Decimal(value).quantize(Decimal('1.'), rounding=ROUND_HALF_UP))
    
def extract_datapoints(weatherdata):
    return [{'instant': time_data['@from'],
             'temperature': round_to_int(time_data['temperature']['@value']),
             'symbol': time_data['symbol']['@numberEx'],
             'precip': {'value': round_to_int(time_data['precipitation']['@value']),
                        'min': round_to_int(time_data['precipitation']['@minvalue']) if '@minvalue' in time_data['precipitation'] else 0,
                        'max': round_to_int(time_data['precipitation']['@maxvalue']) if '@maxvalue' in time_data['precipitation'] else 0},
             'wind': {'speed': round_to_int(time_data['windSpeed']['@mps']),
                      'direction': Decimal(time_data['windDirection']['@deg'])}}
            for time_data in pick_forecast(weatherdata)]

def extract_metadata(weatherdata):
    dateformat = '%Y-%m-%dT%H:%M:%S'
    return {'lastupdate': datetime.strptime(weatherdata['weatherdata']['meta']['lastupdate'], dateformat),
            'nextupdate': datetime.strptime(weatherdata['weatherdata']['meta']['nextupdate'], dateformat)}
    
def extract_credit(weatherdata):
    return {'text': "".join(weatherdata['weatherdata']['credit']['link']['@text']),
            'link': weatherdata['weatherdata']['credit']['link']['@url']}


def formatter_for(format):
    return {'graph': formatters.graph_format,
            'table': formatters.table_format}[format]

def print_forecast(lines):
    print("\n".join(lines))

def argument_parser():
    parser = argparse.ArgumentParser(description="A terminal-based weather forecast",
                                     epilog="Weather forecast from yr.no, delivered by the Norwegian Meteorological Institute and the NRK. Forecasts are fetched from yr.no via the python-yr library (https://github.com/wckd/python-yr). Forecasts are cached by python-yr to comply with required guidelines from YR. More information at http://om.yr.no/verdata/free-weather-data/ .")
    parser.add_argument('location', metavar='LOCATION', help='Location name in /-notation, eg: Sweden/Stockholm/Stockholm')
    parser.add_argument('--format', choices=['graph', 'table'], default='graph', help='Forecast format')
    parser.add_argument('--temperature', choices=['graph', 'line', 'off'], default='graph', help='Different modes for displaying temperature')
    parser.add_argument('--precipitation', choices=['all', 'bars', 'values', 'off'], default='all', help='Different modes for displaying precipitation')
    parser.add_argument('--max-datapoints', dest='max_datapoints', type=int, default=48, help='Maximum number of datapoints to display in forecast')
    return parser

    
if __name__ == '__main__':
    args = argument_parser().parse_args()
    try:
        weatherdata = forecast_for(args.location)
    except urllib.error.HTTPError:
        print("Could not fetch forecast for " + args.location)
    else:
        formatter = formatter_for(args.format)
        print_forecast(formatter(extract_datapoints(weatherdata),
                                 extract_metadata(weatherdata),
                                 extract_credit(weatherdata),
                                 args.max_datapoints,
                                 {'temp': args.temperature,
                                  'precip': args.precipitation}))

    

    
    
