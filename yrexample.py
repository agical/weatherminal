import pickle

from yr.libyr import Yr

def read_example(place):
    with open(place + '.dat', 'rb') as f:
        return pickle.loads(f.read())


def fetch_and_save_example(url, place):
    weather = Yr(location_name=url, forecast_link='forecast_hour_by_hour')
    with open(place + '.dat', 'wb') as f:
        f.write(pickle.dumps(weather.dictionary))


def fetch_stockholm():
    fetch_and_save_example('Sweden/Stockholm/Stockholm', 'stockholm')

def read_stockholm():
    return read_example('stockholm')
    
def fetch_mount_everest():
    fetch_and_save_example('Nepal/Other/Mount_Everest', 'mount_everest')

def read_mount_everest():
    return read_example('mount_everest')
    
