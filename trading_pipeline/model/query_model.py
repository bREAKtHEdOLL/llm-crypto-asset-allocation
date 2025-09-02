from openai import OpenAI

client = OpenAI(api_key="TODO")

def query_model(prompt: str, model: str = "gpt-4o", temperature: float = 0.3) -> str:
    
    response = client.chat.completions.create(
        model = model,
        messages = [
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
    )
    return response.choices[0].message.content.strip() 