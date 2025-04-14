import requests

command = '''
 your message history just for checking..
'''
response = requests.post(
    "https://api.aimlapi.com/v1/chat/completions",
    headers={
        "Content-Type":"application/json", 

        # Insert your AIML API Key instead of <YOUR_AIMLAPI_KEY>:
        "Authorization":"Bearer <Your_API_key>",
        "Content-Type":"application/json"
    },
    json={
        "model":"cohere/command-r-plus",
        "messages":[
            {
                "role": "system",
                "content": "You are a person named Aarav and analyses the past messages and responds to the chat",
                "role":"user",
                # Insert your question for the model here, instead of Hello:
                "content": command
            }
        ]
    }
)

data = response.json()
if 'choices' in data and len(data['choices']) > 0:
    print(data['choices'][0]['message']['content'])
else:
    print("No content found in the response")
