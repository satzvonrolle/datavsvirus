# Datavsvirus

## Inspiration

The data basis for epidemiology potentially can be improved. The data basis of the Robert-Koch-Institut (RKI) and of Johns Hopkins University are our starting points, but we want to improve their usability and add features like time resolved infection rate, etc. .

## What we need

We need to get the data from RKI on a daily basis. Which additional data sources could we use to merge with other data? Have you any suggestions for useful features, especially from a medical or epidemiological standpoint?

## Development

Use a common virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pandas
pip install requests

# optional
pip install wheel  # for interactive jupyter mode
pip install ipython
´´´
