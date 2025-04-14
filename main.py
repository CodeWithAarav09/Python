import pyautogui
import pyperclip
import time
import requests

def is_last_message_from_sender(chat_text):
    lines = [line.strip() for line in chat_text.strip().split('] ') if line.strip()]
    
    # Find the last valid message line
    for line in reversed(lines):
        if ': ' in line:
            sender = line.split(': ', 1)[0].strip()
            return sender.lower() == 'mom'
    
    return False

# Step 1: Click to open the chat area
pyautogui.click(934, 1048)
pyautogui.click(188, 30)

# Give 3 seconds to prepare the screen
time.sleep(2)

while True:
    # Step 2: Select chat history area
    pyautogui.moveTo(903, 241, duration=0.5)
    pyautogui.dragTo(1465, 906, duration=1, button='left')

    # Step 3: Copy selected text
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)  # Wait for clipboard to update
    pyautogui.click(903, 241)

    # Step 4: Get copied text
    chatHis = pyperclip.paste()
    print("Copied text:\n", chatHis)

    if is_last_message_from_sender(chatHis):
        # Send to AIML API
        response = requests.post(
            "https://api.aimlapi.com/v1/chat/completions",
            headers={
                "Authorization": "Bearer 7fc35c46bb8344698fc24145456c4760",
                "Content-Type": "application/json"
            },
            json={
                "model": "cohere/command-r-plus",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a person named Aarav. You analyze the previous messages and respond like you're chatting. Output only the next message."
                    },
                    {
                        "role": "user",
                        "content": chatHis
                    }
                ]
            }
        )

        # Handle API response
        data = response.json()
        print("API response:\n", data)

        if 'choices' in data and len(data['choices']) > 0:
            reply = data['choices'][0]['message']['content']
            pyperclip.copy(reply)

            # Click input area and paste
            pyautogui.click(1135, 973)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')

            print("Sent:", reply)
        else:
            print("No valid content in API response.")

    else:
        print("Waiting for message from Mom...")

    time.sleep(5)
