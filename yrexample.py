import pickle


def read_example():
    with open('example-forecast.dat', 'rb') as f:
        return  pickle.loads(f.read())
