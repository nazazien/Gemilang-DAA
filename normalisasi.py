def normalize_data(df, columns):
    normalization_data = {}
    for col in columns:
        min_val, max_val = df[col].min(), df[col].max()
        df[col] = (df[col] - min_val) / (max_val - min_val)
        normalization_data[col] = (min_val, max_val) 
        #waktu: 𝑂 ( 𝑛 ⋅ 𝑚 ) karena ada iterasi pada 𝑚 kolom, masing-masing dengan 𝑛 elemen
        #ruang: 𝑂 ( 𝑚 ) untuk menyimpan min min dan max max dari setiap kolom
        #melibatkan iterasi di setiap kolom yang dinormalisasi (𝑚) dan untuk setiap kolom, dilakukan iterasi pada semua baris (𝑛) untuk menghitung nilai minimum, maksimum, dan melakukan transformasi data
    return df, normalization_data

def encode_categorical_variables(df, target_col, feature_cols):
    encodings = {}
    for feature in feature_cols:
        mean_values = df.groupby(feature)[target_col].mean().to_dict()
        df[feature] = df[feature].map(mean_values)        
        #waktu: 𝑂 ( 𝑛 + 𝑘 ), 𝑛 jumlah sata.
        #ruang: 𝑂 ( 𝑘 ), 𝑘 jumlah kategori unik per fitur
        encodings[feature] = mean_values
    return encodings

def train_test_split(df, test_size=0.2):
    test_set_size = int(len(df) * test_size)
    train_set = df.iloc[test_set_size:]
    test_set = df.iloc[:test_set_size]
    return train_set, test_set

def normalize_input(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val) if value else None