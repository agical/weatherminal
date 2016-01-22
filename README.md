# Weatherminal
A terminal-based weather forecast written in Python 3

## Weather Forecasts
Forecasts are fetched from [yr.no](http://www.yr.no) via the [python-yr](https://github.com/wckd/python-yr) library. python-yr caches forecasts in order to comply with YR's guidelines for forecast usage. Always adhere the terms of usage found at http://om.yr.no/verdata/free-weather-data/ when using Weatherminal.

## Installation
* Clone repository
* Install dependencies with pip

## Example Usage
`python3 weatherminal.py Sweden/Stockholm/Stockholm`

## Dependecies
* python-yr (https://github.com/wckd/python-yr)
* xmltodict (used by python-yr)
* A terminal with support for unicode will produce nicer results
