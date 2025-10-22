# streamlit_app.py
import streamlit as st
from CareerAdvisor import rules, forward_chain, collect_recommendations
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Career Advisor", layout="centered")

st.title("Career Advisor")
st.write("Tick the statements that are true for you, then click **Recommend**.")

# Build the facts from checkboxes (names MUST match your rules)
facts = {
    "likes_helping_people"  : st.checkbox("I like helping people."),
    "likes_maths"           : st.checkbox("I like maths."),
    "likes_creativity"      : st.checkbox("I enjoy creative work."),
    "likes_law"             : st.checkbox("I'm interested in law."),   
    "likes_science"         : st.checkbox("I like science."),
    "likes_discipline"      : st.checkbox("I value discipline and structure."),
    "dislikes_blood"        : st.checkbox("I dislike seeing blood."),
    "likes_children"        : st.checkbox("I like working with children."),
    
    "good_communication"    : st.checkbox("I am a good communicator."),
    "likes_technology"      : st.checkbox("I like technology."),
    "likes_problem_solving" : st.checkbox("I enjoy solving problems."),
    "prefers_teamwork"      : st.checkbox("I prefer working in a team."),
    "likes_outdoors"        : st.checkbox("I enjoy outdoor activities."),
    "likes_research"        : st.checkbox("I enjoy researching."),
    "high_attention_detail" : st.checkbox("I pay attention to details."),
    "likes_leadership"      : st.checkbox("I am a confident team leader.")

}

# Add career reference points for the map
CAREER_POSITIONS = {
    'Engineer': {'analytical': 90, 'social': 30},
    'Teacher': {'analytical': 50, 'social': 90},
    'Police Officer': {'analytical': 60, 'social': 80},
    'Lawyer': {'analytical': 80, 'social': 70},
    'Doctor': {'analytical': 85, 'social': 85},
    'Researcher': {'analytical': 95, 'social': 40},
    'IT Specialist': {'analytical': 85, 'social': 35}
}

def calculate_xy_scores(facts): # positions your score on the table
    # X-axis: Analytical score
    analytical_traits = ['likes_maths', 'likes_science', 'likes_technology', 
                        'likes_problem_solving', 'high_attention_detail', 'likes_research']
    x_score = sum(1 for trait in analytical_traits if facts.get(trait, False))
    x_score = (x_score / len(analytical_traits)) * 100

    # Y-axis: Social score
    social_traits = ['likes_helping_people', 'likes_children', 'good_communication',
                    'prefers_teamwork', 'likes_leadership']
    y_score = sum(1 for trait in social_traits if facts.get(trait, False))
    y_score = (y_score / len(social_traits)) * 100
    
    return x_score, y_score

def plot_preference_map(x_score, y_score):
    fig = go.Figure()
    
    # Add career reference points
    for career, pos in CAREER_POSITIONS.items():
        fig.add_trace(go.Scatter(
            x=[pos['analytical']],
            y=[pos['social']],
            mode='markers+text',
            name=career,
            text=[career],
            marker=dict(size=10),
            textposition="top center"
        ))
    
    # Add user's position
    fig.add_trace(go.Scatter(
        x=[x_score],
        y=[y_score],
        mode='markers+text',
        name='Your Profile',
        text=['You are here'],
        marker=dict(size=15, color='red'),
        textposition="top center"
    ))
    
    # Add quadrant labels
    fig.add_annotation(x=25, y=75, text="People-Oriented", showarrow=False)
    fig.add_annotation(x=75, y=75, text="Balanced Professional", showarrow=False)
    fig.add_annotation(x=25, y=25, text="Independent Contributor", showarrow=False)
    fig.add_annotation(x=75, y=25, text="Technical Expert", showarrow=False)
    
    fig.update_layout(
        title='Your Career Preference Map',
        xaxis_title='Analytical Orientation (%)',
        yaxis_title='Social Orientation (%)',
        xaxis=dict(range=[0, 100]),
        yaxis=dict(range=[0, 100]),
        # Add quadrant lines
        shapes=[
            dict(type="line", x0=50, x1=50, y0=0, y1=100, line=dict(dash="dash", color="gray")),
            dict(type="line", x0=0, x1=100, y0=50, y1=50, line=dict(dash="dash", color="gray"))
        ]
    )
    return fig

def plot_career_matches(final_facts, derived):
    matches = {}
    for rule in rules:
        career = rule["then"]
        career_name = career.replace('is_', '').title()
        
        if career in derived:
            # Calculate match percentage based on multiple factors
            trait_scores = []
            
            # Position match score (distance from ideal position)
            if career_name in CAREER_POSITIONS:
                x_score, y_score = calculate_xy_scores(final_facts)
                ideal_pos = CAREER_POSITIONS[career_name]
                distance = np.sqrt(
                    (x_score - ideal_pos['analytical'])**2 + 
                    (y_score - ideal_pos['social'])**2
                )
                position_score = max(0, 100 - distance)
                trait_scores.append(position_score)
            
            # Rule match score
            rule_conditions = rule["if"].count('and') + 1  # Count conditions
            met_conditions = sum(1 for trait, value in final_facts.items() if value and trait in rule["if"])
            rule_score = (met_conditions / rule_conditions) * 100
            trait_scores.append(rule_score)
            
            # Calculate final score as average
            matches[career_name] = sum(trait_scores) / len(trait_scores)
    
    if not matches:
        return None
        
    # Sort matches by score
    matches = dict(sorted(matches.items(), key=lambda x: x[1], reverse=True))
    
    fig = go.Figure([
        go.Bar(
            x=list(matches.keys()),
            y=list(matches.values()),
            marker_color=['rgb(26, 118, 255)' if score > 70 else 'rgb(170, 170, 170)' 
                         for score in matches.values()]
        )
    ])
    
    fig.update_layout(
        title='Career Match Percentages',
        yaxis_title='Match Score (%)',
        xaxis_title='Careers',
        yaxis=dict(range=[0, 100]),
        xaxis_tickangle=-45
    )
    return fig

if st.button("Recommend"):
    final_facts, derived = forward_chain(facts, rules)
    recs = collect_recommendations(final_facts, derived)
    
    # Calculate and plot preference map
    x_score, y_score = calculate_xy_scores(facts)
    st.plotly_chart(plot_preference_map(x_score, y_score))
    
    if recs:
        st.success("Recommendations:")
        for r in recs:
            st.write(f"- **{r}**")
        
        # Plot career matches
        match_chart = plot_career_matches(final_facts, derived)
        if match_chart:
            st.plotly_chart(match_chart)
    else:
        st.warning("No matches yet. Try different options.")

    with st.expander("Details"):
        st.write("**Derived facts:**", sorted(list(derived)) or ["(none)"])
        st.write("**Facts used:**")
        st.json(final_facts)