# Datavsvirus
[![Datavsvirus](https://img.youtube.com/vi/Ebte-no6nKU/0.jpg)](https://www.youtube.com/watch?v=Ebte-no6nKU)

## Motivation

To be able to actually use international time-resolved data on Corona infections, it would be crucial to have them in the same data structure, transparently acquired from official sources.

Starting from the data Johns Hopkins University uses for [their maps and charts](https://coronavirus.jhu.edu/map.html), we want to integrate high-resolution data (i.e. states instead of nations) for other countries than the US as well. So far, we started integrating:

* Germany
* Switzerland
* Italy
* South Korea,

more to follow. Later on, we could try and integrate these with measures taken against further spread, such as closing schools.

## Installation

Use a virtual environment to make sure not to mess with other stuff.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pandas
pip install requests
pip install json
pip install lxml

# optional
pip install wheel  # for interactive jupyter mode
pip install matplotlib
pip install ipython
pip install descartes  # for visualization
```

## Usage

Run `python generate.py`, which will:

1) Collect raw data from the internet by running the scripts `datavsvirus/load/load_<country>.py`, which saves them to `data/raw/<country>/...csv`.
2) Convert this raw data to something identical to the format of `data/reference.csv`, and save it to `data/converted/<country>.csv`
3) Fuse these, replace by-country data in reference dataset by by-state data, and save the result to `data/converted/fused.csv`, where it's ready for further usage analysis :)


## Where to go from here

Having just the high-res data on a large area is nice. However, things will get really interesting when this is combined with data on countermeasures on the same scale.

Any suggestions for useful features, especially from a medical or epidemiological standpoint?
