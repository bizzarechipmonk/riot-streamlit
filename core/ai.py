import json
from typing import Dict
from openai import OpenAI

def get_client(api_key: str) -> OpenAI:
    return OpenAI(api_key=api_key)

def generate_stage_questions(
    client: OpenAI,
    amount: str,
    stage: str,
    vertical: str,
    competitor: str = "",
    model: str = "gpt-4.1-mini",
) -> Dict:
    instructions = (
        "You are a world-class B2B sales enablement expert and deal coach. "
        "Your job is to help an account executive run a high-signal buyer conversation. "
        "Focus on practical, discovery-first questions that uncover pain, power, process, priorities, "
        "timeline, stakeholders, procurement, risks, and next steps."
    )

    user_input = f"""
Opportunity context:
- Amount: {amount}
- Stage: {stage}
- Vertical: {vertical}
- Competitor: {competitor or "Unknown/none listed"}

Task:
Give the 3-4 most important questions the AE should ask the buyer RIGHT NOW at this stage.
Make questions specific to the vertical when possible.
Also include:
- 2 "red flag" signals to listen for
- 2 "next step" recommendations

Return ONLY valid JSON. No markdown. No extra commentary. Return JSON with keys:
- questions (array of strings)
- red_flags (array of strings)
- next_steps (array of strings)
""".strip()

    resp = client.responses.create(
        model=model,
        instructions=instructions,
        input=user_input,
        temperature=0.3,
    )
    text = (resp.output_text or "").strip()
    return json.loads(text)