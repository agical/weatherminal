from decimal import Decimal, ROUND_HALF_UP

def symbol_for(number):
    return weather_symbols[number] if number in weather_symbols else number

def bar_for(number):
    return bars[max(0, min(8, number))]
    
def arrow_for(direction):
    index = int((direction / Decimal('45')).quantize(Decimal('1.'), rounding=ROUND_HALF_UP)) % 8
    return direction_arrows[index]


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


bars = {0: ' ', 1: '▁', 2: '▂', 3: '▃', 4: '▄', 5: '▅', 6: '▆', 7: '▇', 8: '█'}

direction_arrows = {0: '↑', 1: '↗', 2: '→', 3: '↘', 4: '↓', 5: '↙', 6: '←',7: '↖' }

