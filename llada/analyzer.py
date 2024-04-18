import openai
import re
import io
from contextlib import redirect_stdout
import pandas as pd
from .utils import get_api_key

def analyze(data: pd.DataFrame, goals: list[dict], i: int=-1):
    """
    Executes generated Python code based on analysis goals.
    :param data: Pandas DataFrame of the data
    :param goals: Generated goals to analyze
    :param i: Optional param to input index of a specific goal from goals list
    :return: Analysis results
    """

    api_key = get_api_key()
    client = openai.OpenAI(api_key=api_key)
    
    temperature = 0.5  # How creative the response should be (0 = deterministic, 1 = most creative)
    max_tokens = 4000  # Maximum length of the response

    results = []
    
    # If goal index is specified, only analyze specific goal
    if i >= 1 and i <= len(goals):
        index = goals[i-1]["index"]
        question = goals[i-1]["question"]
        rationale = goals[i-1]["rationale"]

        analysis_code = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Given the question '{question}', write Python code to analyze the data "
                     f"using the following approach: '{goals[i-1]['analysis']}'. Your output should only contain complete and executable Python code with no preamble or explanations. Assume the data is stored in a pandas dataframe called 'data'. You can import any required libraries for the analyses if required, like sklearn, keras, numpy, etc.. Check whether the output you generated can be run in a Python environment without making any changes to it. ALWAYS make sure that your code should use print statements to show variable values instead of just using the variable names."}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        code = analysis_code.choices[0].message.content
        
        if "```" in code:
            pattern = r"```(?:\w+\n)?([\s\S]+?)```"
            matches = re.findall(pattern, code)
            if matches:
                code = matches[0]

        code = code.replace("```", "")
        
        try:
            exec(code)
            with redirect_stdout(io.StringIO()) as f:
                exec(code)
            analysis_result = f.getvalue()
            results.append(
                {
                    "index": index,
                    "question": question,
                    "analysis_code": code,
                    "analysis_result": analysis_result,
                    "rationale": rationale,
                }
            )
        except Exception as e:
            results.append(
                {
                    "index": index,
                    "question": question,
                    "analysis_result": f"Error: Failed to execute generated code. ({e})",
                    "rationale": rationale,
                }
            )

    # If goal index is not specified, analyze all goals
    else:
        for i, goal in enumerate(goals):
            index = goal["index"]
            question = goal["question"]
            rationale = goal["rationale"]

            analysis_code = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"Given the question '{question}', write Python code to analyze the data "
                         f"using the following approach: '{goal['analysis']}'. Your output should only contain complete and executable Python code with no preamble or explanations. Assume the data is stored in a pandas dataframe called 'data'. You can import any required libraries for the analyses if required, like sklearn, keras, numpy, etc.. Check whether the output you generated can be run in a Python environment without making any changes to it. ALWAYS make sure that your code should use print statements to show variable values instead of just using the variable names."}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            code = analysis_code.choices[0].message.content
            
            if "```" in code:
                pattern = r"```(?:\w+\n)?([\s\S]+?)```"
                matches = re.findall(pattern, code)
                if matches:
                    code = matches[0]

            code = code.replace("```", "")
            print("\n\n*************************************** Analysis ",(i+1)," ***************************************\n")
            
            try:
                exec(code)
                with redirect_stdout(io.StringIO()) as f:
                    exec(code)
                analysis_result = f.getvalue()
                results.append(
                    {
                        "index": index,
                        "question": question,
                        "analysis_code": code,
                        "analysis_result": analysis_result,
                        "rationale": rationale,
                    }
                )
            except Exception as e:
                results.append(
                    {
                        "index": index,
                        "question": question,
                        "analysis_result": f"Error: Failed to execute generated code. ({e})",
                        "rationale": rationale,
                    }
                )

    return results
