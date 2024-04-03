import os
import pickle
from typing import List, Dict, Tuple
import datetime

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

def load_markdown_files(folder_path: str) -> Tuple[List[str], List[str]]:
    today = datetime.date.today()
    all_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    filtered_files = []
    
    for file in all_files:
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

    return filtered_files, markdown_texts

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

def find_related_posts(folder_path: str, max_related: int = 15, min_similarity: float = 0.3) -> Dict[str, List[str]]:
    all_files, markdown_texts = load_markdown_files(folder_path)
    embeddings = [get_embedding(text, filename) for text, filename in zip(markdown_texts, all_files)]
    embeddings = handle_nan_in_embeddings(embeddings)
    embeddings_matrix = np.array(embeddings)
    similarity_matrix = cosine_similarity(embeddings_matrix)
    np.fill_diagonal(similarity_matrix, 0)  # Fill diagonal with 0s to ignore self-similarity

    related_posts = {}
    for idx, filename in enumerate(all_files):
        slug = extract_slug(filename)
        similarity_scores = similarity_matrix[idx]
        related_indices = np.argsort(similarity_scores)[::-1]
        related_slugs = []
        for related_idx in related_indices:
            if related_idx == idx:
                continue  # Skip self-similarity
            related_slug = extract_slug(all_files[related_idx])
            related_similarity = similarity_scores[related_idx]
            if related_similarity >= min_similarity:
                related_slugs.append(related_slug)
            if len(related_slugs) >= max_related:
                break

        related_posts[slug] = related_slugs

    sorted_related_posts = sorted(related_posts.items(), key=lambda x: len(x[1]))

    for slug, related_slugs in sorted_related_posts:
        if related_slugs:
            print(f"{slug}:")
            for related_slug in related_slugs:
                print(f" - {related_slug}")
            print("\n")

    return related_posts

def main() -> None:
    try:
        folder_path = "./blog/_posts"
        related_posts = find_related_posts(folder_path, max_related=10, min_similarity=0.60)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        save_cache(cache)

if __name__ == "__main__":
    main()
