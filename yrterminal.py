import argparse
from decimal import Decimal, ROUND_HALF_UP

import yrreader
from formatters import graph_formatter

    
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

def extract_credit(weatherdata):
    return {'text': "".join(weatherdata['weatherdata']['credit']['link']['@text']),
            'link': weatherdata['weatherdata']['credit']['link']['@url']}


def formatter_for(format):
    formatters = {'graph': graph_formatter}
    return formatters[format]

def print_forecast(lines):
    print("\n".join(lines))

def argument_parser():
    parser = argparse.ArgumentParser(description="A terminal-based weather forecast",
                                     epilog="Weather forecast from yr.no, delivered by the Norwegian Meteorological Institute and the NRK")
    parser.add_argument('location', metavar='LOCATION', help='Location name in /-notation, eg: Sweden/Stockholm/Stockholm')
    parser.add_argument('--format', choices=['graph'], default='graph', help='Forecast format')
    parser.add_argument('--temperature', choices=['graph', 'line', 'off'], default='graph', help='Different modes for displaying temperature')
    parser.add_argument('--precipitation', choices=['all', 'bars', 'values', 'off'], default='all', help='Different modes for displaying precipitation')
    parser.add_argument('--datapoints', type=int, default=48, help='Number of datapoints to display in forecast')
    return parser

    
if __name__ == '__main__':
    args = argument_parser().parse_args()
    weatherdata = yrreader.forecast_for(args.location)
    formatter = formatter_for(args.format)
    print_forecast(formatter.format(extract_datapoints(weatherdata),
                                    extract_credit(weatherdata),
                                    {'temp': args.temperature,
                                     'precip': args.precipitation,
                                     'max_cells': args.datapoints}))
    
    
