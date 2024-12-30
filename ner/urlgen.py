# Generate unique URLs with paths and query arguments (manual query string generation)
import random
from faker import Faker

def generate_urls(count=1000):
    """
    Generate a list of unique URLs with paths and query arguments.
    """
    faker = Faker()
    unique_urls_with_paths = set()
    while len(unique_urls_with_paths) < 1000:
        base_url = faker.url()
        path = faker.uri_path()
        # Generate a random query string
        query_params = "&".join(
            [f"{faker.word()}={random.randint(1, 100)}" for _ in range(random.randint(1, 3))]
        )
        query = f"?{query_params}"
        unique_urls_with_paths.add(f"{base_url.rstrip('/')}/{path.lstrip('/')}{query}")

    return list(unique_urls_with_paths)
