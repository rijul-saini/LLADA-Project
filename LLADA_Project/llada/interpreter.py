import openai
import json
from .utils import get_api_key

def interpret(results: list):
	"""
	Generates text interpretation of the analysis results produced by Analyzer.
	:param results: list of generated analysis results
    :return: Result interpretation
	"""

	api_key = get_api_key()
	client = openai.OpenAI(api_key=api_key)

	temperature = 0.7  # How creative the response should be (0 = deterministic, 1 = most creative)
	max_tokens = 2000  # Maximum length of the response

	system_prompt = "You are an experienced data analyst that can INTERPRET python analysis results. Your instructions are as follows: 1) Generate text interpretation of the 'analysis_results' for each 'question'. There may only be a single question included, ENSURE that you only answer questions that are provided in the analysis_results; 2) Your answer should ALWAYS follow the format:'Question:' question text, followed by 'Result:' in the next line with your interpretation. If there are more than 1 question then show all questions and interpretations in your answer with each question separated by printing a long dashed line. IF there is just 1 question then don't add a dashed line; 3) Add some context for what the results signify in your interpretation; 4) ALWAYS make sure your answer contains no preamble or explanations other than the given format."
	user_prompt = json.dumps(results)

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
	print(response)

	return response