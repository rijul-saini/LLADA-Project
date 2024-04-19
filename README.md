# Capstone Project
## Large-Language Assisted Data Analysis Tool
<br/><br/>
LLADA is a Python package designed to facilitate the data analysis process by integrating large language models (LLMs) via the OpenAI API. This package allows users to summarize datasets, generate data analysis goals, execute analysis, and interpret the results in natural language.
<br/><br/>
### Features

- **Summarizer**: Automatically generate text and JSON summaries of input datasets.
- **Goal Generator**: Generate analysis suggestions (goals) based on dataset summaries.
- **Analyzer**: Execute Python code to analyze data according to the generated goals.
- **Interpreter**: Provide natural language explanations of the analysis results.

<br/><br/>
<br/><br/>
### Installation

Before installing LLADA, ensure you have Python 3.6 or higher installed. You can install LLADA directly from the source code using the following commands:

```bash
git clone https://github.com/rijul-saini/LLADA-Project.git
cd llada
pip install .
```

<br/><br/>
<br/><br/>
### Configuration

Before using the LLADA package, you must set the OpenAI API key that will be used to interact with the OpenAI GPT models. This can be done in two ways:

- **Environment Variable**:
```bash
export OPENAI_API_KEY='your_openai_api_key_here'
```
- **Using the Package's API**:
```python
import llada
llada.set_api_key('your_openai_api_key_here')
```

<br/><br/>
<br/><br/>
### Usage

Here is a simple example of how to use the LLADA package:

```python
import llada
import pandas as pd

# Load your dataset
data = pd.read_csv("path_to_your_dataset.csv")
```

**Summarizer**\
<br/>
Generates a JSON summary of the dataset for the goal generation step.\
Optionally, you can also print a natural language summary of the data by passing argument `show = True` (Set to False by default).\
*Note: Generating the text summary requires an additional query to the LLM API and tokens will be charged accordingly.*

```python
# Summarize the dataset
summary = llada.summarize(data)
```
```python
# Summarize the dataset
summary = llada.summarize(data, show=True)
```

**Goal Generator**\
<br/>
Generates analysis suggestions for the data, along with some rationale for why the analysis is needed.\
Number of goals to be generated can be set by specifying the `n` argument (`n = 3` by default).\
The function returns a list of 'goals', where each 'goal' is a dictionary containing: index, question, analysis, rationale.

```python
# Generate goals for data analysis
goals = llada.generateGoals(summary)
```
```python
# Generate goals for data analysis
goals = llada.generateGoals(summary, n=5)
```

**Analyzer**\
<br/>
Generates and executes Python code for the analysis goals. If multiple goals are passed as argument, all goals will be analyzed by default.\
Optionally, you can pass `i` argument to specify any particular goal by index from goals, and only that analysis will be generated.\
The generated analysis code's execution is output to the console, and the function returns a list of 'results' where each 'result' is a dictionary containing: index, question, analysis_code, analysis_result, rationale.

```python
# Perform analysis based on the goals
results = llada.analyze(data, goals)
```
```python
# Perform analysis based on the goals
results = llada.analyze(data, goals, i=1)
```

**Interpreter**\
<br/>
Generates natural language interpretation of the analysis results for the user.\
The function returns and prints a string containing the questions and their results derived from the analyses.

```python
# Interpret the results
explain = llada.interpret(results)
```

<br/>
<br/>
### Contributing

LLADA Project is still in the prototyping stage, and all contributions are welcome! If you have suggestions for improvements or bug fixes, please open an issue or submit a pull request.<br>
