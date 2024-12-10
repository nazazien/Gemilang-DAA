def normalize_data(df, columns):
    normalization_data = {}
    for col in columns:
        min_val, max_val = df[col].min(), df[col].max()
        df[col] = (df[col] - min_val) / (max_val - min_val)
        normalization_data[col] = (min_val, max_val)
    return df, normalization_data

def encode_categorical_variables(df, target_col, feature_cols):
    encodings = {}
    for feature in feature_cols:
        mean_values = df.groupby(feature)[target_col].mean().to_dict()
        df[feature] = df[feature].map(mean_values)
        encodings[feature] = mean_values
    return encodings

def train_test_split(df, test_size=0.2):
    test_set_size = int(len(df) * test_size)
    train_set = df.iloc[test_set_size:]
    test_set = df.iloc[:test_set_size]
    return train_set, test_set

def normalize_input(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val) if value else None