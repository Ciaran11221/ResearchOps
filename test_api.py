from dotenv import load_dotenv
load_dotenv()

import anthropic

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=100,
    messages=[{"role": "user", "content": "Say hello in one sentence."}]
)
print(response.content[0].text)