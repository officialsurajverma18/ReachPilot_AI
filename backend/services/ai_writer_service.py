from flask import current_app


def generate_message(lead, tone="professional"):
    name = lead["name"]
    context = f"rating {lead['rating']}" if lead.get("rating") else "their online presence"
    # A useful deterministic fallback keeps the feature functional without misrepresenting AI availability.
    fallback = (f"Hi {name} team, I came across your business and noticed {context}. "
                "We help local businesses turn more online interest into qualified enquiries. "
                "Would you be open to a brief conversation this week?")
    key = current_app.config.get("OPENAI_API_KEY")
    if not key:
        return fallback, "template"
    # Avoid coupling the project to a rapidly changing SDK; REST remains compatible with OpenAI's API.
    import requests
    prompt = f"Write a concise {tone} outreach message for {name}. Known facts: rating={lead.get('rating')}, website={lead.get('website') or 'none'}. Do not invent facts."
    response = requests.post("https://api.openai.com/v1/chat/completions", headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}, json={"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}], "max_tokens": 160}, timeout=25)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip(), "openai"
