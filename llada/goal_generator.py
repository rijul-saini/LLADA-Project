import json
import openai
from .utils import get_api_key

def generateGoals(summary: dict, n: int=3) -> list[dict]:
    """
    Generates analytical goals based on the dataset summary.
    :param summary: JSON summary of the dataset
    :param n: Number of goals to generate
    :return: List of goals as JSON
    """

    api_key = get_api_key()
    client = openai.OpenAI(api_key=api_key)

    SYSTEM_INSTRUCTIONS = """
        You are a an experienced data analyst who can generate a given number of insightful GOALS about data, when given a summary of the data. The ANALYSES YOU RECOMMEND MUST FOLLOW ANALYSES BEST PRACTICES (e.g., use regression analysis only on data that is appropriate) AND BE MEANINGFUL (e.g., results produced should solve real world problems). Each goal must include a question, an analysis (THE ANALYSIS MUST REFERENCE THE EXACT FIELD COLUMN NAMES AS IN THE PROVIDED SUMMARY, e.g., regression of X on Y), and a rationale (JUSTIFICATION FOR WHICH dataset FIELDS ARE USED and what we will learn from the analysis). Each goal MUST ONLY mention the exact field names from the summary provided.
        """
    
    FORMAT_INSTRUCTIONS = """
        THE OUTPUT MUST BE A CODE SNIPPET OF A VALID LIST OF JSON OBJECTS. IT MUST USE THE FOLLOWING FORMAT:
        [
            { "index": 1,  "question": "How does Y affect X?", "analysis": "correlation of X and Y", "rationale": "This tells about "} ..
            
        ]
        THE OUTPUT SHOULD ONLY USE THE JSON FORMAT ABOVE.
        """
        
    user_prompt = f"""The number of GOALS to generate is {n}. The goals should be based on the data summary below, \n\n .
    {summary} \n\n"""

    user_prompt += f"""\n The generated goals SHOULD BE FOCUSED ON THE INTERESTS AND PERSPECTIVE of an experienced data analyst persona, who is insterested in complex, insightful goals about the data. \n"""

    temperature = 0.6  # How creative the response should be (0 = deterministic, 1 = most creative)
    max_tokens = 2000  # Maximum length of the response

    messages = [
        {"role": "system", "content": SYSTEM_INSTRUCTIONS},
        {"role": "user",
            "content":
            f"{user_prompt}\n\n {FORMAT_INSTRUCTIONS} \n\n. The generated {n} goals are: \n "}]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
        )

    goal_text = response.choices[0].message.content
    goals = json.loads(goal_text)
    print(json.dumps(goals, indent=2))

    return goals
