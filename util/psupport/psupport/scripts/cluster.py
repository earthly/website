import os
import pickle
from textwrap import dedent
from typing import List, Tuple

import guidance
import numpy as np
from guidance import assistant, gen, system, user
from openai import APIError, OpenAI
from sklearn.cluster import KMeans
from sklearn.neighbors import LocalOutlierFactor

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

CACHE_FILE = "./blog/_data/embeddings_cache.pkl"
CLUSTER_TITLE_FILE = "./blog/_data/cluster_title_cache.pkl"

# Initialize blacklist and whitelist
BLACKLIST : List[str] = ["- News", "- Articles"]
# WHITELIST : List[str] = ["- Tutorials"]
WHITELIST : List[str] = []

def load_cache(cache_file: str) -> dict:
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    return {}

cache = load_cache(CACHE_FILE)
cluster_title_cache = load_cache(CLUSTER_TITLE_FILE)

def save_cache(cache: dict, cache_file: str) -> None:
    with open(cache_file, 'wb') as f:
        pickle.dump(cache, f)

def extract_slug(filename: str) -> str:
    parts = filename.split('-')
    if len(parts) > 3:
        slug = '-'.join(parts[3:])
        slug = slug.rsplit('.', 1)[0]
        return slug
    return filename

def load_markdown_files(folder_path: str) -> Tuple[List[str], List[str]]:
    all_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    markdown_texts = []
    filtered_files = []

    for file in all_files:
        with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as f:
            content = f.read()
            # Check blacklist
            if any(blacklist_item in content for blacklist_item in BLACKLIST):
                continue
            # Check whitelist
            if WHITELIST and not all(whitelist_item in content for whitelist_item in WHITELIST):
                continue
            markdown_texts.append(content)
            filtered_files.append(file)

    return filtered_files, markdown_texts

def get_embedding(text: str, filename: str, model: str = "text-embedding-3-small") -> List[float]:
    if filename in cache:
        return cache[filename]

    print(f"get embedding: {filename}")
    while True:
        try:
            embedding = client.embeddings.create(input=text, model=model).data[0].embedding
            cache[filename] = embedding
            return embedding
        except APIError as e:
            if "maximum context length" in str(e):
                print(f"{filename}: dropping lines")
                lines = text.split("\n")
                if len(lines) > 10:
                    text = "\n".join(lines[:-10])  # Drop last 10 lines
                else:
                    print("Less than 10 left")
                    # If the document has fewer than 10 lines, return an empty embedding
                    return [0.0] * 1536
            else:
                raise e

def generate_embeddings(markdown_texts: List[str], filenames: List[str]) -> List[List[float]]:
    embeddings = [get_embedding(text, filename) for text, filename in zip(markdown_texts, filenames)]
    return embeddings

def handle_nan_in_embeddings(embeddings: List[List[float]]) -> List[List[float]]:
    cleaned_embeddings = []
    for embedding in embeddings:
        if np.isnan(np.sum(embedding)):
            cleaned_embedding = [0 if np.isnan(val) else val for val in embedding]
            cleaned_embeddings.append(cleaned_embedding)
        else:
            cleaned_embeddings.append(embedding)
    return cleaned_embeddings

# 3. Clustering
def cluster_embeddings(embeddings: List[List[float]], n_clusters: int) -> List[int]:
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(embeddings)
    return kmeans.labels_


def cluster_embeddings_with_outlier_removal(embeddings: List[List[float]], n_clusters: int, all_files : List[str], contamination: float = 0.1, n_neighbors: int = 20) -> Tuple[List[int], List[int]]:
    # Detect outliers using LOF
    lof = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=contamination)
    labels = lof.fit_predict(embeddings)

    # Filter out outliers
    inliers = [index for index, label in enumerate(labels) if label != -1]
    outliers = [index for index, label in enumerate(labels) if label == -1]

    print(f"Number of outliers detected: {len(outliers)}")
    outlier_files = [all_files[index] for index in outliers]
    outlier_list = "\n".join(outlier_files)
    print(f"Removing the following outliers:\n{outlier_list}")

    filtered_embeddings = [embeddings[i] for i in inliers]

    # Apply KMeans clustering on the filtered embeddings
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(filtered_embeddings)
    cluster_labels = kmeans.labels_

    # Map back to original indices, using -1 for outliers
    final_labels = [-1] * len(embeddings)
    for i, label in zip(inliers, cluster_labels):
        final_labels[i] = label

    return final_labels, inliers


def generate_cluster_name(slugs: List[str]) -> str:
    if str(slugs) in cluster_title_cache:
        return cluster_title_cache[str(slugs)]

    lm = guidance.models.OpenAI("gpt-3.5-turbo-16k")
    with system():
        lm += dedent("""
            You are an assistant that generates a concise name for a cluster of related articles.
            Given a list of article slugs, return a concise and relevant name for the cluster.""")
    with user():
         lm += dedent("""
              - python-frameworks
              - python-libraries
              - python-web-scraping
                      """)
    with assistant():
         lm += dedent("Python")
    with user():
        lm += dedent("\n  - ".join(slugs))
    with assistant():
        lm += gen('summary', max_tokens=100)
    cluster_name = lm['summary'].strip()
    cluster_title_cache[str(slugs)] = cluster_name
    return cluster_name

# 4. Display the Clusters
def display_clusters(clusters: List[List[str]]) -> None:
    for cluster in clusters:
        if len(cluster) < 3:
            continue
        slugs = [extract_slug(file_path) for file_path in cluster]
        cluster_name = generate_cluster_name(slugs)
        print(f"{cluster_name}:")
        for slug in slugs:
            print(f"  - {slug}")

def main() -> None:
    try:
        folder_path = "./blog/_posts"
        n_clusters = 30  # Adjust as necessary
        contamination = 0.2  # Adjust as necessary to control the proportion of outliers
        n_neighbors = 4  # Adjust as necessary for the sensitivity of LOF

        all_files, markdown_texts = load_markdown_files(folder_path)
        embeddings = generate_embeddings(markdown_texts, all_files)
        embeddings = handle_nan_in_embeddings(embeddings)
        labels, inliers = cluster_embeddings_with_outlier_removal(embeddings, n_clusters, all_files, contamination, n_neighbors)

        clusters: List[List] = [[] for _ in range(n_clusters)]
        for idx, label in enumerate(labels):
            if label != -1:
                clusters[label].append(all_files[idx])

        display_clusters(clusters)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Save the updated cache
        save_cache(cache, CACHE_FILE)
        save_cache(cluster_title_cache, CLUSTER_TITLE_FILE)

if __name__ == "__main__":
    main()
