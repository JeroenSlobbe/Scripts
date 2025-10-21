# Prerequisite: pip install mistralai 

from mistralai import Mistral

api_key = "putYourKeyHere"
model = "mistral-large-latest"

client = Mistral(api_key=api_key)
prompt = "Tell a 250 word story about a rabbit"

chat_response = client.chat.complete(
    model= model,
    messages = [
        {
            "role": "user",
            "content": prompt,
        },
    ]
)

print(chat_response.choices[0].message.content)
