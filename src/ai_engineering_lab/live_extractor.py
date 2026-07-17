from dotenv import load_dotenv
from google import genai
from google.genai import types

from ai_engineering_lab.earnings_models import EarningsExtraction

# Load the .env file so the API key is available
load_dotenv()

# The client automatically picks up the GEMINI_API_KEY environment variable
client = genai.Client()


def extract_earnings_live(text: str) -> EarningsExtraction:
    """
    Extracts financial metrics from text using the live Gemini API.
    Enforces the output to match the EarningsExtraction Pydantic model.
    """
    prompt = f"Extract the financial earnings data from the following text:\n\n{text}"

    # 1. Call client.models.generate_content to generate the response from the Gemini model.
    response = client.models.generate_content(
        # 2. Use the specified model: "gemini-2.5-flash".
        model="gemini-2.5-flash",
        # 3. Pass the prompt as the contents for the API request.
        contents=prompt,
        # 4. Use the config parameter to enforce a structured JSON response matching our Pydantic model.
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=EarningsExtraction,
        ),
    )
    # 5. Return the structured, parsed Pydantic object using response.parsed.
    return response.parsed
