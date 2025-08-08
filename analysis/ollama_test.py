from ollama import embed

response = embed(model='mxbai-embed-large', input=['Llamas are members of the camelid family', 'lol'])

print(response['embeddings'][1])