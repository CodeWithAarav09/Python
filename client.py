import requests

command = '''
 [15:50, 08/04/2025] Aarav Garg: https://youtube.com/shorts/RkKueLd9L84?si=A8gAHEs5s4Q4pti-
[16:53, 12/04/2025] Vipan Papa: Hi Aarav,
Welcome to PW. Your registration no. is 22529247.
Kindly fill out the ADMISSION FORM with a link attached to complete the procedure.
https://erp.pw.live/Scholar/PWRegistrationForm?param=dovpsgdovjsxmxcdov

Visit your PW center to complete your pending admission formalities and to complete the payment of your pending fee before classes start.

Thanks,
'''
response = requests.post(
    "https://api.aimlapi.com/v1/chat/completions",
    headers={
        "Content-Type":"application/json", 

        # Insert your AIML API Key instead of <YOUR_AIMLAPI_KEY>:
        "Authorization":"Bearer 07308d90102d4dc3b398e3dfe4738f92",
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
