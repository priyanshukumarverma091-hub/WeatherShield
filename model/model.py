from sklearn.ensemble import RandomForestRegressor


def build_model(random_state=42, n_estimators=300):
    """
    Baseline weather prediction model.

    Random Forest is used first because it gives us a strong,
    interpretable baseline before moving to LSTM/GNN models.
    """
    return RandomForestRegressor(
        n_estimators=n_estimators,
        random_state=random_state,
        n_jobs=-1,
        max_features="sqrt",
    )
