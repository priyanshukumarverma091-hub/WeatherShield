# Weather Intelligence Model

This is the model-first part of the Weather + Severe Weather project.

## Current phase

The first milestone is a reliable baseline:

CSV Dataset
    ↓
Preprocessing
    ↓
Random Forest Regression
    ↓
Temperature Prediction
    ↓
MAE / RMSE / R²
    ↓
Saved Model

## Project structure

```text
weather_model/
├── model/
│   ├── __init__.py
│   ├── config.py
│   ├── preprocessing.py
│   ├── dataset.py
│   ├── model.py
│   ├── train.py
│   ├── evaluate.py
│   └── predict.py
├── data/
│   ├── raw/
│   │   └── weather.csv
│   └── processed/
├── saved_models/
├── requirements.txt
└── README.md
```

## Install

```bash
pip install -r requirements.txt
```

## Train

```bash
python -m model.train
```

## Evaluate

```bash
python -m model.evaluate
```

## Test a prediction

```bash
python -m model.predict
```

## Important

This Random Forest is the baseline model, not the final research model.

After the real dataset is inspected, the next stages can be:

1. Time-series forecasting
2. Multi-variable weather prediction
3. Severe-weather risk classification
4. Cyclone track prediction
5. Spatio-temporal GNN
6. GNN + LSTM/Transformer
7. Live weather/API integration
