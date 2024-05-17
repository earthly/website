import datetime
import os
import pickle
from typing import Dict, List, Tuple

import numpy as np
from openai import APIError, OpenAI
from sklearn.metrics.pairwise import cosine_similarity

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

CACHE_FILE = "./blog/_data/embeddings_cache.pkl"

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
    # Assuming filenames are in the format "YYYY-MM-DD-title.md"
    parts = filename.split('-')
    if len(parts) > 3:  # Expected to have date at the start
        slug = '-'.join(parts[3:])  # Skip date parts
        slug = slug.rsplit('.', 1)[0]  # Remove file extension
        return slug
    return filename  # Return original filename if it doesn't match the expected format

def handle_nan_in_embeddings(embeddings: List[List[float]]) -> List[List[float]]:
    cleaned_embeddings = []
    for embedding in embeddings:
        if np.isnan(np.sum(embedding)):  # Check if there are any NaN values in the embedding
            cleaned_embedding = [0 if np.isnan(val) else val for val in embedding]
            cleaned_embeddings.append(cleaned_embedding)
        else:
            cleaned_embeddings.append(embedding)
    return cleaned_embeddings

def load_markdown_files_in_path(folder_path: str, files: List[str]) -> List[Tuple[str, str]]:
    today = datetime.date.today()
    filtered_files = []
    for file in files:
        # Extract the date part from the filename
        date_part = file.split('-', 3)[:3]
        try:
            # Convert the date part to a datetime.date object
            file_date = datetime.date(int(date_part[0]), int(date_part[1]), int(date_part[2]))
            # If the file date is today or in the past, add it to the list
            if file_date <= today:
                filtered_files.append(file)
        except ValueError:
            # If the date extraction or conversion fails, skip the file
            continue

    filtered_files = sorted(filtered_files)
    markdown_texts = []

    for file in filtered_files:
        with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as f:
            markdown_texts.append(f.read())

    return list(zip(filtered_files, markdown_texts))

def load_markdown_files(folder_path: str) -> List[Tuple[str, str]]:
    all_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return load_markdown_files_in_path(folder_path, all_files)

def get_embedding(text: str, filename: str, model: str = "text-embedding-3-small") -> List[float]:
    if filename in cache:
        return cache[filename]

    while True:
        try:
            embedding = client.embeddings.create(input=text, model=model).data[0].embedding
            cache[filename] = embedding
            return embedding
        except APIError as e:
            if "maximum context length" in str(e):
                lines = text.split("\n")
                if len(lines) > 10:
                    text = "\n".join(lines[:-10])  # Drop last 10 lines
                else:
                    return [0.0] * 1536
            else:
                raise e

def find_related_posts(input_files: List[Tuple[str, str]], related_files: List[Tuple[str, str]], max_related: int = 15, min_similarity: float = 0.3) -> Dict[str, List[str]]:
    input_embeddings = [get_embedding(text, filename) for filename, text in input_files]
    related_embeddings = [get_embedding(text, filename) for filename, text in related_files]

    input_embeddings = handle_nan_in_embeddings(input_embeddings)
    related_embeddings = handle_nan_in_embeddings(related_embeddings)

    input_embeddings_matrix = np.array(input_embeddings)
    related_embeddings_matrix = np.array(related_embeddings)

    similarity_matrix = cosine_similarity(input_embeddings_matrix, related_embeddings_matrix)

    related_posts: Dict[str, List[str]] = {}

    for idx, (input_filename, _) in enumerate(input_files):
        input_slug = extract_slug(input_filename)
        similarity_scores = similarity_matrix[idx]
        related_indices = np.argsort(similarity_scores)[::-1]
        related_slugs = []
        for related_idx in related_indices:
            related_slug = extract_slug(related_files[related_idx][0])
            if input_slug == related_slug:
                continue
            related_similarity = similarity_scores[related_idx]
            if related_similarity >= min_similarity:
                related_slugs.append(related_slug)
            if len(related_slugs) >= max_related:
                break

        related_posts[input_slug] = related_slugs

    return related_posts

def print_related_posts(related: Dict[str, List[str]]) -> None:
    sorted_related_posts = sorted(related.items(), key=lambda x: len(x[1]))

    for slug, related_slugs in sorted_related_posts:
        if related_slugs:
            print(f"{slug}:")
            for related_slug in related_slugs:
                print(f" - {related_slug}")
            print("\n")

def main() -> None:
    try:
        folder_path = "./blog/_posts"
        markdown_files = load_markdown_files(folder_path)
        related_posts = find_related_posts(markdown_files, markdown_files, max_related=10, min_similarity=0.50)
        print_related_posts(related_posts)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        save_cache(cache)

if __name__ == "__main__":
    main()
