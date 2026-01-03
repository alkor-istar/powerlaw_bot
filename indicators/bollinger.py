import pandas as pd

def bollinger_bands(df, length=20, mult=2):
    basis = df["close"].rolling(length).mean()
    dev = df["close"].rolling(length).std()

    df["bb_upper"] = basis + mult * dev
    df["bb_lower"] = basis - mult * dev
    df["basis"] = basis

    return df
