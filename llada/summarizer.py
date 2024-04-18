import pandas as pd
import json
import openai
from .utils import json_summary, get_api_key



def generateJsonSummary(summary) -> dict:

    system_prompt = "You are an experienced data analyst that can annotate datasets. Your instructions are as follows:\ni) ALWAYS generate the name of the dataset and the dataset_description\nii) ALWAYS generate a field description.\niii.) ALWAYS generate a semantic_type (a single word) for each field given its values e.g. company, city, number, supplier, location, gender, longitude, latitude, url, ip address, zip code, email, etc\nYou must return an updated JSON dictionary without any preamble or explanation."
    user_prompt = json.dumps(summary)

    temperature = 0.5  # How creative the response should be (0 = deterministic, 1 = most creative)
    max_tokens = 4000  # Maximum length of the response

    api_key = get_api_key()
    client = openai.OpenAI(api_key=api_key,)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            }
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )

    response = json.loads(response.choices[0].message.content)

    return response


def generateTextSummary(summary):
    
    system_prompt = "You are an experienced data analyst that can annotate datasets. Your instructions are as follows: 1) Generate a brief text summary of the dataset"
    user_prompt = json.dumps(summary)

    temperature = 0.6   # How creative the response should be (0 = deterministic, 1 = most creative)
    max_tokens = 500    # Maximum length of the response

    api_key = get_api_key()
    client = openai.OpenAI(api_key=api_key,)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            }
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )

    response = response.choices[0].message.content

    return response


def summarize(data: pd.DataFrame, show: bool=False):
    """
    Generates a JSON summary of the dataset and prints a text summary.
    :param data: Pandas DataFrame of the data
    :return: JSON summary of the dataset
    """

    raw_summary = json_summary(data)

    summary = generateJsonSummary(raw_summary)

    if show:
        text_summary = generateTextSummary(summary)
        print(text_summary)

    return summary