from packages.ai_flashcards.providers_base import AIProvider


class AppleIntelligenceProvider(AIProvider):

    def generate(self, prompt: str, temperature: float = 0.2):
