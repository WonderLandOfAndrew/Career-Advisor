# streamlit_app.py
import streamlit as st
from CareerAdvisor import rules, forward_chain, collect_recommendations

st.set_page_config(page_title="Career Advisor", layout="centered")

st.title("Career Advisor")
st.write("Tick the statements that are true for you, then click **Recommend**.")

# Build the facts from checkboxes (names MUST match your rules)
facts = {
    "likes_helping_people"  : st.checkbox("I like helping people.", value=True),
    "likes_maths"           : st.checkbox("I like maths."),
    "likes_creativity"      : st.checkbox("I enjoy creative work."),
    "likes_law"             : st.checkbox("I'm interested in law.", value=True),   
    "likes_science"         : st.checkbox("I like science."),
    "likes_discipline"      : st.checkbox("I value discipline and structure."),
    "dislikes_blood"        : st.checkbox("I dislike seeing blood."),
    "likes_children"        : st.checkbox("I like working with children.", value=True),
    
    "good_communication"    : st.checkbox("I am a good communicator."),
    "likes_technology"      : st.checkbox("I like technology."),
    "likes_problem_solving" : st.checkbox("I enjoy solving problems."),
    "prefers_teamwork"      : st.checkbox("I prefer working in a team."),
    "likes_outdoors"        : st.checkbox("I enjoy outdoor activities."),
    "likes_research"        : st.checkbox("I enjoy researching."),
    "high_attention_detail" : st.checkbox("I pay attention to details."),
    "likes_leadership"      : st.checkbox("I am a confident team leader.")

}

if st.button("Recommend"):
    final_facts, derived = forward_chain(facts, rules)
    recs = collect_recommendations(final_facts, derived)
    if recs:
        st.success("Recommendations:")
        for r in recs:
            st.write(f"- **{r}**")
    else:
        st.warning("No matches yet. Try different options.")

    with st.expander("Details"):
        st.write("**Derived facts:**", sorted(list(derived)) or ["(none)"])
        st.write("**Facts used:")
        st.json(final_facts)