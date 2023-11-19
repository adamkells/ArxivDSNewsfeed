from src.arxiv_analyser import get_arxiv_metadata, generate_score, save_results_to_json
from datetime import datetime
import json
import logging

logging.basicConfig(
    filename='results.log',  # File to which logs will be written
    level=logging.INFO,      # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Format of the log entries
)


metadata = get_arxiv_metadata(10)

for index, meta in enumerate(metadata):
    logging.info(f"Processing paper number {index}: {meta['title']}")
    summary_score = generate_score(meta['summary'])
    meta['score'] = summary_score['score']
    meta['reason'] = summary_score['reason']

most_interesting_papers = sorted(metadata, key=lambda x: x['score'], reverse=True)[:5]

save_results_to_json(most_interesting_papers)