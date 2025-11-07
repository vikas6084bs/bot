import requests

class QueryGenerator:
    def __init__(self, openrouter_api_key):
        self.openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com",
            "X-Title": "Database Chatbot"
        }

    def _call_openrouter_api(self, messages, temperature=0.1, max_tokens=1000):
        payload = {
            "messages": messages,
            "model": "meta-llama/llama-3.1-70b-instruct",
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        try:
            response = requests.post(self.openrouter_url, headers=self.headers, json=payload, timeout=30)
            if response.status_code == 200:
                response_data = response.json()
                return response_data["choices"][0]["message"]["content"]
            else:
                return f"Error: API returned status {response.status_code}"
        except Exception as e:
            return f"API call failed: {str(e)}"
