import os
import pickle
import yaml
from openai import APIError, OpenAI
from textwrap import dedent

import guidance
from guidance import assistant, gen, system, user

gpt35turbo = guidance.models.OpenAI("gpt-3.5-turbo-16k")

CACHE_FILE = "./blog/_data/short_title_cache.pkl"

def load_cache() -> dict:
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'rb') as f:
            return pickle.load(f)
    return {}

cache = load_cache()

def save_cache(cache: dict) -> None:
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump(cache, f)

def extract_slug(filename: str) -> str:
    parts = filename.split('-')
    if len(parts) > 3:
        slug = '-'.join(parts[3:])
        slug = slug.rsplit('.', 1)[0]
        return slug
    return filename

def generate_minimal_title(original_title: str) -> str:
    if original_title in cache:
        return cache[original_title]
    
    lm = gpt35turbo
    with system():
        lm += dedent("""
                You generate two or three word titles from longer titles.
                Return a two to four word title for an article with the following title. Return just the two to four word answer.
                """)
    with user():
         lm += dedent(f"Cosine Similarity and Text Embeddings In Python with OpenAI")
    with assistant():
         lm += dedent(f"Cosine Similarity In Python") 
    with user():
         lm += dedent(f"Getting Started with containerd in Docker")
    with assistant():
         lm += dedent(f"containerd in Docker") 
    with user():
        lm += dedent(original_title)
    with assistant():
        lm += gen('summary', max_tokens=100)
    minimal_title = lm['summary'].strip()
    cache[original_title] = minimal_title
    return minimal_title

def load_markdown_titles(folder_path: str) -> dict:
    all_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith('.md')]
    titles = {}

    for file in all_files:
        with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as f:
            content = f.read()
            parts = content.split('---')
            if len(parts) >= 3:
                front_matter = parts[1]
                data = yaml.safe_load(front_matter)
                original_title = data.get('title', 'Untitled')
                minimal_title = generate_minimal_title(original_title)
                slug = extract_slug(file)
                titles[slug] = minimal_title

    return titles

def print_titles_as_yaml(titles: dict) -> None:
    for slug, short_title in titles.items():
        print(f"{slug}: '{short_title}'")

def main() -> None:
    try:
        folder_path = "./blog/_posts"
        titles = load_markdown_titles(folder_path)
        print_titles_as_yaml(titles)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        save_cache(cache)

if __name__ == "__main__":
    main()
