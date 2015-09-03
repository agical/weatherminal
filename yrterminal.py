
import pickle

with open('example-forecast.dat', 'rb') as f:
    forecast = pickle.loads(f.read())

print(forecast)
