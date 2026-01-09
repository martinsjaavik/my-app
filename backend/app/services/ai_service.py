import json
from typing import AsyncGenerator

from ollama import AsyncClient

from app.config import settings


class AIService:
    def __init__(self):
        self.client = AsyncClient(host=settings.ollama_url)
        self.model = settings.ollama_model

    async def get_hint(
        self,
        remaining_words: list[str],
        solved_count: int = 0,
    ) -> dict:
        """Generate a hint for the player."""
        prompt = f"""You are helping solve a NYT Connections puzzle.

The game has 16 words that form 4 groups of 4 related words each.
Categories range from easy (yellow) to hard (purple).
The harder categories often involve wordplay, puns, or less obvious connections.

Remaining words: {', '.join(remaining_words)}
Already solved: {solved_count} categories

Your task: Identify ONE group of 4 words that share a connection.

Think step by step:
1. Look for obvious categories first (foods, animals, movies, etc.)
2. Consider wordplay (words that can follow/precede a common word)
3. Look for less obvious connections (purple category is often tricky!)

Provide a SUBTLE hint about ONE category without giving away the exact answer.
The hint should guide the player to discover the connection themselves.

Respond with ONLY valid JSON in this exact format:
{{"hint": "your subtle hint here", "confidence": 0.0-1.0, "suggested_words": ["word1", "word2", "word3", "word4"]}}
"""

        try:
            response = await self.client.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                format="json",
            )

            content = response["message"]["content"]
            result = json.loads(content)

            return {
                "hint": result.get("hint", "Look for words that might share a common theme."),
                "confidence": float(result.get("confidence", 0.5)),
                "suggested_words": result.get("suggested_words", [])[:4],
            }
        except Exception as e:
            print(f"AI hint error: {e}")
            return {
                "hint": "Try grouping words by a common theme or pattern.",
                "confidence": 0.3,
                "suggested_words": remaining_words[:4] if remaining_words else [],
            }

    async def auto_solve_step(
        self,
        remaining_words: list[str],
        mistakes_remaining: int,
        solved_categories: list[dict],
    ) -> AsyncGenerator[dict, None]:
        """Generate step-by-step solve with reasoning (streaming)."""
        solved_info = ""
        if solved_categories:
            solved_info = "\nAlready solved:\n"
            for cat in solved_categories:
                solved_info += f"- {cat['name']}: {', '.join(cat['words'])}\n"

        prompt = f"""You are solving a NYT Connections puzzle step by step.

Remaining words: {', '.join(remaining_words)}
Mistakes remaining: {mistakes_remaining}
{solved_info}

Think through this methodically:
1. First, share your observations about potential patterns
2. Identify the EASIEST category you can find
3. Explain your reasoning
4. Make your guess

Format your response as:
OBSERVATIONS: [Your initial thoughts about word patterns]
ANALYSIS: [Deeper analysis of potential categories]
REASONING: [Why you're choosing this specific group]
GUESS: ["word1", "word2", "word3", "word4"]
"""

        try:
            stream = await self.client.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
            )

            buffer = ""
            async for chunk in stream:
                content = chunk.get("message", {}).get("content", "")
                buffer += content

                yield {
                    "type": "thinking",
                    "content": content,
                }

            # Extract the guess from the buffer
            if "GUESS:" in buffer:
                guess_part = buffer.split("GUESS:")[-1].strip()
                # Try to parse the guess
                try:
                    import re
                    match = re.search(r'\[([^\]]+)\]', guess_part)
                    if match:
                        words_str = match.group(1)
                        words = [w.strip().strip('"\'') for w in words_str.split(',')]
                        yield {
                            "type": "guess",
                            "content": "Making my guess...",
                            "words": words[:4],
                        }
                except Exception:
                    pass

        except Exception as e:
            print(f"AI solve error: {e}")
            yield {
                "type": "error",
                "content": f"AI error: {str(e)}",
            }


# Singleton instance
ai_service = AIService()
