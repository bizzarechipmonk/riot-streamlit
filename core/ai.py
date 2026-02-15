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
    product: str = "",
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
- Product: {product or "Unknown/none listed"}

Task:
Give the 3 most important questions the AE should ask the buyer RIGHT NOW at this stage.
Make questions specific to the vertical when possible.
Also include:
- 1 "red flag" signal to listen for in the buyer's response that might indicate a risk to the deal.

Return ONLY valid JSON. No markdown. No extra commentary. Return JSON with keys:
- questions (array of strings)
- red_flags (array of strings)
""".strip()

    resp = client.responses.create(
        model=model,
        instructions=instructions,
        input=user_input,
        temperature=0.3,
    )
    text = (resp.output_text or "").strip()
    return json.loads(text)

def generate_market_guidance(
    client: OpenAI,
    amount: str,
    stage: str,
    vertical: str,
    product: str = "",
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
- Vertical: {vertical} - HH stands for Home Health, HC stands for Home Care (non clinical), SNF stands for Skilled Nursing Facility, and ALF stands for Assisted Living Facility.
- Competitor: {competitor or "Unknown/none listed"}
- Product: {product or "Unknown/none listed"}

Task:
Give the 3 most important insights for this rep to know about the market so they can tailor their messaging and approach. This could include trends in the vertical, common pain points, how this competitor is typically positioned, or how this product is typically positioned.

Return ONLY valid JSON. No markdown. No extra commentary. Return JSON with keys:
- insights (array of strings)
""".strip()

    resp = client.responses.create(
        model=model,
        instructions=instructions,
        input=user_input,
        temperature=0.3,
    )
    text = (resp.output_text or "").strip()
    return json.loads(text)