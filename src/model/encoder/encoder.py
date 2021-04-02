import pandas as pd
from sklearn.preprocessing import OneHotEncoder


class Encoder:

    def __init__(self):
        self.one_hot_encoder = OneHotEncoder()

    def fit(self, x, with_numerics=False):
        if with_numerics:
            return self.one_hot_encoder.fit(x)
        number_type_columns, encoded_columns = Encoder.__get_numeric_and_categorical_columns(x)
        self.one_hot_encoder.fit(x[encoded_columns])
        return self.one_hot_encoder

    def transform(self, x, with_numerics=False):
        if with_numerics:
            return self.one_hot_encoder.transform(x)
        number_type_columns, encoded_columns = Encoder.__get_numeric_and_categorical_columns(x)
        decoded_df = pd.DataFrame(self.one_hot_encoder.transform(x[encoded_columns]).toarray())
        return pd.concat([decoded_df, x[number_type_columns]], axis=1)

    def fit_transform(self, x, with_numerics=False):
        self.fit(x, with_numerics)
        return self.transform(x, with_numerics)

    @staticmethod
    def __get_numeric_and_categorical_columns(x):
        number_type_columns = x.select_dtypes(include=['number']).columns.values
        encoded_columns = list(set(x.columns) - set(number_type_columns))
        return sorted(number_type_columns), sorted(encoded_columns)
