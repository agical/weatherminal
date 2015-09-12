import shutil
from decimal import Decimal, ROUND_HALF_UP
from functools import reduce

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
    
def precip_bars(datapoints, columns):
    return [format_row([bar_for(dp['precip']['min']) + bar_for(dp['precip']['value']) + bar_for(dp['precip']['max']) for dp in datapoints], columns)]
            

def precip_values(datapoints, columns):
    return [format_row([space_for_zero(dp['precip']['value']) + ' ' for dp in datapoints], columns)]

def wind_row(datapoints, columns):
    return [format_row([str(dp['wind']['speed']) + arrow_for(dp['wind']['direction']) for dp in datapoints], columns)]

def hour_row(datapoints, columns):
    return [format_row([pick_hour(dp['instant']) + 'h' for dp in datapoints], columns)]

def credit_rows(credit):
    return ['',
            credit['text'],
            credit['link']]

def calculate_columns(max_cells):
    terminal_columns = shutil.get_terminal_size().columns
    cells = min(terminal_columns // 4, max_cells)
    return cells * 4

def graph_format(datapoints, credit, max_datapoints, args):
    columns = calculate_columns(max_datapoints)
    return [row
            for rows in [symbol_row(datapoints, columns),
                         temperature_graph(datapoints, columns) if args['temp'] == 'graph' else [],
                         temperature_line(datapoints, columns) if args['temp'] == 'line' else [],
                         precip_bars(datapoints, columns) if args['precip'] in ['all', 'bars'] else [],
                         precip_values(datapoints, columns) if args['precip'] in ['all', 'values'] else [],
                         wind_row(datapoints, columns),
                         hour_row(datapoints, columns),
                         credit_rows(credit)]
            for row in rows]

def _table_rows(datapoints):
    def format_row(result, value):
        return result + '|{:>4}'.format(value)
    return [reduce(format_row, 
                   [pick_hour(dp['instant']) + 'h',
                    symbol_for(dp['symbol']),
                    str(dp['temperature']) + '°',
                    space_for_zero(dp['precip']['value']),
                    bar_for(dp['precip']['min']) + bar_for(dp['precip']['value']) + bar_for(dp['precip']['max']),
                    str(dp['wind']['speed']) + arrow_for(dp['wind']['direction'])],
                   '')
            for dp in datapoints]
    
def table_format(datapoints, credit, max_datapoints, args):
    return [row
            for rows in [_table_rows(datapoints[0:max_datapoints]),
                         credit_rows(credit)]
            for row in rows]
