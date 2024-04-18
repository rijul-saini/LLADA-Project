import pandas as pd
import os
import warnings

def set_api_key(key):
    """
    Sets the OpenAI API key for the session.
    :param key: string, OpenAI API key
    """

    global _api_key
    _api_key = key


def get_api_key():
    """
    Retrieves the OpenAI API key.
    :return: string, the OpenAI API key
    """

    if _api_key is not None:
        return _api_key
    return os.getenv("OPENAI_API_KEY", None)


def get_column_properties(df: pd.DataFrame, n_samples: int=3) -> list[dict]:
    """
    Analyzes column properties of a DataFrame.
    """
    
    properties_list = []
    for column in df.columns:
        dtype = df[column].dtype
        properties = {}
        if dtype in [int, float, complex]:
            properties["dtype"] = "number"
            properties["std"] = self.check_type(dtype, df[column].std())
            properties["min"] = self.check_type(dtype, df[column].min())
            properties["max"] = self.check_type(dtype, df[column].max())

        elif dtype == bool:
            properties["dtype"] = "boolean"
        elif dtype == object:
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    pd.to_datetime(df[column], errors='raise')
                    properties["dtype"] = "date"
            except ValueError:
                if df[column].nunique() / len(df[column]) < 0.5:
                    properties["dtype"] = "category"
                else:
                    properties["dtype"] = "string"
        elif pd.api.types.is_categorical_dtype(df[column]):
            properties["dtype"] = "category"
        elif pd.api.types.is_datetime64_any_dtype(df[column]):
            properties["dtype"] = "date"
        else:
            properties["dtype"] = str(dtype)

        if properties["dtype"] == "date":
            try:
                properties["min"] = df[column].min()
                properties["max"] = df[column].max()
            except TypeError:
                cast_date_col = pd.to_datetime(df[column], errors='coerce')
                properties["min"] = cast_date_col.min()
                properties["max"] = cast_date_col.max()
        nunique = df[column].nunique()
        if "samples" not in properties:
            non_null_values = df[column][df[column].notnull()].unique()
            n_samples = min(n_samples, len(non_null_values))
            samples = pd.Series(non_null_values).sample(
                n_samples, random_state=42).tolist()
            properties["samples"] = samples
        properties["num_unique_values"] = nunique
        properties["semantic_type"] = ""
        properties["description"] = ""
        properties_list.append(
            {"column": column, "properties": properties})

    return properties_list


def json_summary(df: pd.DataFrame):
    
    properties = get_column_properties(df)
    
    summary = {
        "dataset_name": "",
        "num_entries": int(df.shape[0]),
        "num_fields": int(df.shape[1]),
        "fields": properties
    }
    
    return summary

