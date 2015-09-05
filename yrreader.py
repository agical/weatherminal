import pickle
import os
from datetime import datetime

from yr.libyr import Yr

def _cache_dir():
    return os.path.expanduser('~/.yrterminal-cache/')
    
def _filename_for(location):
    return _cache_dir() + location.replace('/', '-') + '.dat'

def _mins_since_last_modified(filename):
    return (datetime.now() - datetime.fromtimestamp(os.path.getmtime(filename))).total_seconds() / 60
    
def _read_from_cache(location):
    with open(_filename_for(location), 'rb') as f:
        return pickle.loads(f.read())

def _write_to_cache(location, weatherdata):
    os.makedirs(_cache_dir(), exist_ok=True)
    with open(_filename_for(location), 'wb') as f:
        f.write(pickle.dumps(weatherdata))

def _exists_in_cache(location):
    filename = _filename_for(location)
    return os.path.isfile(filename) and _mins_since_last_modified(filename) < 15
    
def _fetch_weatherdata_from_yr(location):
    return Yr(location_name=location, forecast_link='forecast_hour_by_hour').dictionary

def forecast_for(location):
    if _exists_in_cache(location):
        print('Reading weatherdata from cache (' + str(int(_mins_since_last_modified(_filename_for(location)))) + ' mins old)')
        return _read_from_cache(location)
    else:
        print('Reading weatherdata from yr.no')
        weatherdata = _fetch_weatherdata_from_yr(location)
        _write_to_cache(location, weatherdata)
        return weatherdata
