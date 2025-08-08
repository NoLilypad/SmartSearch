import os
from dotenv import load_dotenv
from mistralai import Mistral

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Get API_KEY from environment variables
API_KEY = os.getenv('API_KEY')

model = "mistral-embed"

client = Mistral(api_key=API_KEY)

embeddings_batch_response = client.embeddings.create(
    model=model,
    inputs=["Embed this sentence.", "As well as this one."],
)

print(embeddings_batch_response)