import streamlit as st

from core.data import load_opps, load_guidance, find_opp, get_opp_context, find_similar_opps_by_amount_and_vertical
from core.guidance import get_vertical_guidance, get_competitor_guidance, get_product_guidance, get_mkting, load_battlecard
from core.formatting import format_currency
from core.ai import get_client, generate_stage_questions, generate_market_guidance, generate_competitor_guidance

st.set_page_config(page_title="RIOT", layout="wide")

st.markdown("""
<style>
.card {
    border: 1px solid #e6e6e6;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin-bottom: 1.25rem;
    background-color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_cached():
    opps = load_opps("opportunities.csv")
    guidance = load_guidance("guidance.json")
    return opps, guidance

@st.cache_resource
def load_client():
    return get_client(st.secrets["OPENAI_API_KEY"])

opps, guidance = load_cached()
client = load_client()

st.title("Reliably Informing Opportunities Tool (RIOT)")

opp_id = st.text_input("Enter Salesforce Opportunity ID (e.g., 7465)").strip()

# Find opportunity
try:
    opp_row = find_opp(opps, opp_id)
except KeyError as e:
    st.error(str(e))
    st.stop()

# Summary
summary_container = st.container()
with summary_container:
    if opp_row is None and opp_id:
        st.warning(f"No opportunity found for ID **{opp_id}**. Double-check the ID and try again.")
    elif opp_row is not None:
        ctx = get_opp_context(opp_row)

        st.markdown("### Opportunity Summary")
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Account", ctx.account)
        c2.metric("Amount", format_currency(ctx.amount))
        c3.metric("Product", ctx.product or "—")
        c4.metric("Stage", ctx.stage or "—")
        c5.metric("Competitor", ctx.competitor or "—")

st.divider()

if opp_row is None:
    st.stop()

# Context for the rest of the app
ctx = get_opp_context(opp_row)

col1, col2 = st.columns([3, 1])

with col1:

    # -------------------------
    # Stage Questions
    # -------------------------

    
    stage_label = ctx.stage if ctx.stage else "Current Stage"
    st.subheader(f"Things to note at {stage_label} stage")

    if not ctx.stage or not ctx.vertical:
        st.info("Missing Stage or Vertical on this opportunity, so I can’t generate stage questions yet.")
    else:
        with st.spinner("Generating buyer questions…"):
            try:
                ai = generate_stage_questions(
                    client=client,
                    amount=str(ctx.amount) if ctx.amount else "",
                    stage=ctx.stage,
                    vertical=ctx.vertical,
                    competitor=ctx.competitor or "",
                )

                st.markdown("**Top questions**")
                questions = "\n".join([f"- {q}" for q in ai.get("questions", [])])
                st.markdown(questions)

                st.markdown("**One red flag to listen for**")
                red_flags = "\n".join([f"- {rf}" for rf in ai.get("red_flags", [])])
                st.markdown(red_flags)

            except Exception as e:
                st.error("AI generation failed. Check your API key / app logs.")
                st.caption(str(e))

    # -------------------------
    # Vertical Guidance
    # -------------------------

    vertical_label = ctx.vertical if ctx.vertical else "Vertical"
    st.subheader(f"{vertical_label} Specific Guidance")

    if not ctx.stage or not ctx.vertical:
        st.info("Missing Stage or Vertical on this opportunity, so I can’t generate vertical insights yet.")
    else:
        with st.spinner("Generating vertical insights…"):
            try:
                ai = generate_market_guidance(
                    client=client,
                    amount=str(ctx.amount) if ctx.amount else "",
                    stage=ctx.stage,
                    vertical=ctx.vertical,
                    competitor=ctx.competitor or "",
                )

                st.markdown("**Market Insights**")
                insights = "\n".join([f"- {i}" for i in ai.get("insights", [])])
                st.markdown(insights)

            except Exception as e:
                st.error("AI generation failed. Check your API key / app logs.")
                st.caption(str(e))

    # -------------------------
    # Competitor Guidance
    # -------------------------



    battlecard_md = load_battlecard(ctx.competitor)
    
    competitor_label = ctx.competitor if ctx.competitor else "Competitor"
    st.subheader(f"{competitor_label} Specific Guidance")

    if not ctx.stage or not ctx.competitor:
        st.info("Missing Stage or Competitor on this opportunity, so I can’t generate competitor insights yet.")
    else:
        with st.spinner("Generating competitor insights…"):
            try:
                ai = generate_competitor_guidance(
                    client=client,
                    amount=str(ctx.amount) if ctx.amount else "",
                    stage=ctx.stage or "",
                    vertical=ctx.vertical or "",
                    product=ctx.product or "",
                    competitor=ctx.competitor or "",
                    battlecard_md=battlecard_md,
                )

                st.markdown("**Compete Tips**")
                insights = "\n".join([f"- {i}" for i in ai.get("insights", [])])
                st.markdown(insights)

            except Exception as e:
                st.error("AI generation failed. Check your API key / app logs.")
                st.caption(str(e))

    # -------------------------
    # Product Guidance
    # -------------------------



    if ctx.product:
        st.subheader(f"{ctx.product} Specific Guidance")
        st.info(get_product_guidance(guidance, ctx.product))
    else:
        st.subheader("Product-Specific Guidance")
        st.info("No product listed for this opportunity.")

with col2:
    st.subheader("Similar Opportunities")

    similar = find_similar_opps_by_amount_and_vertical(
        opps,
        opp_id=opp_id,
        vertical=ctx.vertical,
        amount=ctx.amount,
        n=5,
        pct_band=0.15,   # tweak as you like (0.15 tighter, 0.40 looser)
        min_floor=10000,
    )

    st.dataframe(similar, use_container_width=True, hide_index=True)

    st.subheader("Marketing Insights")
    for mkting in get_mkting(guidance, ctx.vertical):
        st.write("•", mkting)