import arxiv
import json
from openai import OpenAI
from datetime import datetime


def get_arxiv_metadata(num_results=10):
    # Construct the default API client.
    client = arxiv.Client()

    # Search for the 10 most recent articles matching the keyword "quantum."
    search = arxiv.Search(
        query = "cs.LG",
        max_results = num_results,
        sort_by = arxiv.SortCriterion.SubmittedDate
    )

    results = client.results(search)

    result_list = []
    # `results` is a generator; you can iterate over its elements one by one...
    for r in client.results(search):
        result_list.append(
            {
                'id': r.entry_id,
                'title': r.title,
                'summary': r.summary,
                'href': r.links[-1].href
            }
        )

    return result_list


def generate_score(summary):
    client = OpenAI()

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"I would like you to evaluate whether the following paper will be of interest to me based on the abstract.\
                Some innformation about me: I am a senior data scientist interested in machine learning.\
                I am not interested in computer vision. I am keen to read papers that work with a real world dataset.\
                I am not interested in papers that are excessively maths heavy (i.e. neural network theory). I am keen to read opinionated papers that raise interesting ideas (particularly on ethical AI).\
                In response please return a json object containing a score on a scale from 1 to 100 and a concise reason for the score. Here is the abstract of the paper:'{summary}'",
            }
        ],
        model="gpt-3.5-turbo",
    )
    summary_json = json.loads(chat_completion.choices[-1].message.content)

    return summary_json


def save_results_to_json(results):
    # Get the current date in the format 'mm_dd_yyyy'
    current_date = datetime.now().strftime('%m_%d_%Y')

    # Construct the file name with the prefix 'results_' and the current date
    file_name = f'results_{current_date}.json'

    # Write the dictionary to the JSON file
    with open(file_name, 'w') as json_file:
        json.dump(results, json_file)
