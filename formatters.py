import shutil
from functools import reduce

from conversions import symbol_for, bar_for, arrow_for

CELL_SIZE=4

def space_for_zero(number):
    return str(number) if number is not 0 else ''


def format_row(data_row, columns):
    def format_cell(data):
        return ("{:>" + str(CELL_SIZE) + "}").format(data)
    return "".join([format_cell(cell) for cell in data_row])[0:columns]

def flatten_rows(rows_sources):
    return [row
            for rows in rows_sources
            for row in rows]



def symbol_row(datapoints, columns):
    return [format_row([symbol_for(dp['symbol']) + ' ' for dp in datapoints], columns)]



def temperature_line(datapoints, columns):
    return [format_row([str(dp['temperature']) + '°' for dp in datapoints], columns)]

def temperature_graph(datapoints, columns):
    def temperature_graph_row(datapoints, row_temp, columns):
        return format_row([(str(row_temp)+'°' if dp['temperature'] == row_temp else ' ') for dp in datapoints], columns)
    min_temp = min([dp['temperature'] for dp in datapoints])
    max_temp = max([dp['temperature'] for dp in datapoints])
    return reversed([temperature_graph_row(datapoints, step_temp, columns)
                     for step_temp in range(min_temp, max_temp + 1)])



def precip_bars(datapoints, columns):
    return [format_row([bar_for(dp['precip']['min']) + bar_for(dp['precip']['value']) + bar_for(dp['precip']['max']) for dp in datapoints], columns)]
            
def precip_values(datapoints, columns):
    return [format_row([space_for_zero(dp['precip']['value']) + ' ' for dp in datapoints], columns)]



def wind_line(datapoints, columns):
    return [format_row([str(dp['wind']['speed']) + arrow_for(dp['wind']['direction']) for dp in datapoints], columns)]



def pick_hour(instant):
    return instant[11:13]

def hour_line(datapoints, columns):
    return [format_row([pick_hour(dp['instant']) + 'h' for dp in datapoints], columns)]



def credit_rows(credit):
    return ['',
            credit['text'],
            credit['link']]



def calculate_columns(max_cells):
    terminal_columns = shutil.get_terminal_size().columns
    cells = min(terminal_columns // CELL_SIZE, max_cells)
    return cells * CELL_SIZE
    
def graph_format(datapoints, credit, max_datapoints, args):
    columns = calculate_columns(max_datapoints)
    return flatten_rows([symbol_row(datapoints, columns),
                         temperature_graph(datapoints, columns) if args['temp'] == 'graph' else [],
                         temperature_line(datapoints, columns) if args['temp'] == 'line' else [],
                         precip_bars(datapoints, columns) if args['precip'] in ['all', 'bars'] else [],
                         precip_values(datapoints, columns) if args['precip'] in ['all', 'values'] else [],
                         wind_line(datapoints, columns),
                         hour_line(datapoints, columns),
                         credit_rows(credit)])

def _table_rows(datapoints):
    def format_row(result, value):
        return result + ("|{:>" + str(CELL_SIZE) + "}").format(value)
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
    return flatten_rows([_table_rows(datapoints),
                         credit_rows(credit)])

