import asyncio
import os
from openai import AsyncOpenAI

# Key found in the environment/files
API_KEY = "your-openai-api-key-here"

async def main():
    print(f"Testing OpenAI connection with key: {API_KEY[:10]}...")
    client = AsyncOpenAI(api_key=API_KEY)
    
    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": "Output a JSON object with a key 'message' and value 'Hello'."}
            ],
            response_format={"type": "json_object"},
        )
        print("Success! Response:")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
