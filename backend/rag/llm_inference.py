import openai
import streamlit as st

class LLM:
    def __init__(self, api_key=None):
        if api_key:
            self.client = openai.OpenAI(api_key=api_key)
        else:
            self.client = openai.OpenAI()  # reads OPENAI_API_KEY from env var

    def infer(self, prompt, temperature=0.2, max_tokens=500):
            model_to_use = "gpt-4-turbo"

            try:
                response = self.client.chat.completions.create(
                    model=model_to_use,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content

            except openai.NotFoundError:
                st.warning(f"Model {model_to_use} not available. Falling back to gpt-3.5-turbo.")
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content

            except openai.RateLimitError:
                st.error("OpenAI API quota exceeded. Please check your billing or switch API key.")
                return "API quota exceeded."

            except Exception as e:
                st.error(f"Unexpected error: {e}")
                return "An error occurred during inference."

        #return "Mocked recommendation: Use BART for chatbot project."

        
    