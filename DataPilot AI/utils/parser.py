import json
import re


def safe_parse(text: str):

    if not text:
        return {}

    try:
        # 🔥 Remove markdown ```json ```
        text = re.sub(r"```json|```", "", text).strip()

        # 🔥 Extract JSON block
        json_match = re.search(r"\{.*\}", text, re.DOTALL)

        if json_match:
            text = json_match.group()

        return json.loads(text)

    except Exception as e:
        print("❌ JSON Parse Error:", e)
        return {"raw_output": text}