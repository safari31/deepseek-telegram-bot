from openai import OpenAI

client = OpenAI(
    api_key="sk-22730aaecc5e486d8d97555226f8200d",
    base_url="https://api.deepseek.com"
)

messages = [
    {
        "role": "system",
        "content": "Ти корисний AI-помічник українською мовою."
    }
]

print("AI чат запущено!")
print("Напиши 'exit' для виходу.\n")

while True:
    user_input = input("Ти: ")

    if user_input.lower() == "exit":
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )

    ai_message = response.choices[0].message.content

    print(f"\nAI: {ai_message}\n")

    messages.append({
        "role": "assistant",
        "content": ai_message
    })