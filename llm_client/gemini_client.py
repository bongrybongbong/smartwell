from langchain_google_genai import ChatGoogleGenerativeAI

class GeminiLLMClient:
    def __init__(self, model: str = "models/gemini-1.5-flash", temperature: float = 0.0):
        self.llm = ChatGoogleGenerativeAI(model=model, temperature=temperature)

    def get_llm(self):
        return self.llm