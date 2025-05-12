import pandas as pd
import numpy as np

def test():
    # Create a DataFrame with NaN values
    df = pd.DataFrame({
        'A': [1, 2, np.nan, 4],
        'B': [np.nan, 5, 6, 7],
        'C': [8, 9, 10, np.nan]
    })

    # Fill NaN values with the mean of each column
    df_filled = df.fillna(df.mean())

    # Check if the filled DataFrame has no NaN values
    assert df_filled.isnull().sum().sum() == 0

    print("Test passed!")