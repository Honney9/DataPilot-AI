# services/llm_service.py

import os
import time
from openai import OpenAI
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()


class LLMService:
    def __init__(self):

        # ---------------------------
        # API Clients
        # ---------------------------
        self.groq_client = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )

        self.openrouter_client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )


        # ---------------------------
        # Model Mapping (FIXED)
        # ---------------------------
        self.models = {
            "fast": "llama-3.1-8b-instant",
            "reasoning": "gemini-2.0-flash",
            "heavy": "llama-3.3-70b-versatile",
            "fallback": "meta-llama/llama-3.3-70b-instruct"
        }

    # ---------------------------
    # GROQ
    # ---------------------------
    def _call_groq(self, prompt, model):
        response = self.groq_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    # ---------------------------
    # GEMINI
    # ---------------------------
    def _call_gemini(self, prompt, model):
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt
            )
            return response.text

        except Exception as e:
            print("Gemini error:", e)
            raise e

    # ---------------------------
    # OPENROUTER
    # ---------------------------
    def _call_openrouter(self, prompt, model):
        response = self.openrouter_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    # ---------------------------
    # AUTO ROUTING (UPGRADED)
    # ---------------------------
    def generate(self, prompt: str, task: str = "fast", retries: int = 2):

        for attempt in range(retries):
            try:
                print(f"🧠 LLM Task: {task}")

                # ---------------------------
                # ROUTING LOGIC
                # ---------------------------
                if task == "reasoning":
                    try:
                        print("🧠 Trying Gemini...")
                        return self._call_gemini(prompt, self.models["reasoning"])

                    except Exception as e:
                        print("⚠️ Gemini failed → switching to Groq heavy")
                        return self._call_groq(prompt, self.models["heavy"])

                elif task == "heavy":
                    return self._call_groq(prompt, self.models["heavy"])

                elif task == "fast":
                    return self._call_groq(prompt, self.models["fast"])

                elif task == "backup":
                    return self._call_openrouter(prompt, self.models["fallback"])

                else:
                    return self._call_groq(prompt, self.models["fast"])

            except Exception as e:
                print(f"[Attempt {attempt+1}] Error: {e}")
                time.sleep(1)

        # ---------------------------
        # FINAL FALLBACK CHAIN
        # ---------------------------
        print("⚠️ Falling back to backup models...")

        try:
            return self._call_groq(prompt, self.models["fast"])
        except:
            try:
                return self._call_gemini(prompt, self.models["reasoning"])
            except:
                return self._call_openrouter(prompt, self.models["fallback"])