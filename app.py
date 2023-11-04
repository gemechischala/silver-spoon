from fastapi import FastAPI, HTTPException
import g4f
import asyncio
import logging

app = FastAPI()

# Llama2r GPT model setup
model = "gpt-3.5-turbo"

# Create an asyncio lock
lock = asyncio.Lock()

# Configure logging
logging.basicConfig(level=logging.ERROR)

@app.post("/generate-response/")
async def generate_response(user_message: str, provider_name: str):
    try:
        # Dynamically import the specified provider module
        pname = provider_name
        pjoin = "g4f.Provider." + pname

        # Get the provider from the imported module
        provider = getattr(g4f.Provider, pname)

        async with lock:
            # Generate a response using the specified GPT model and provider
            response = g4f.ChatCompletion.create(
                model=model,
                provider=provider,
                messages=[{"role": "user", "content": user_message}],
                #stream=True,
            )

            formatted_response = ""  # Initialize an empty response

            for message in response:
                formatted_response += message  # Accumulate messages

            # Return the formatted response
            return {"response": formatted_response}

    except Exception as e:
        errors = f"Error generating response: {e}"
        logging.error(errors)
        return {"response": errors}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
