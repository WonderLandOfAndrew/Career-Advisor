facts = {
    "likes_helping_people": True,
    "likes_maths": False,
    "likes_creativity": False,
    "likes_law": True,
    "likes_science": False,
    "likes_discipline": True,
    "dislikes_blood": False,
    "likes_children": True,
    "good_communication": False,
    "likes_technology": True,
    "likes_problem_solving": True,
    "prefers_teamwork": False,
    "likes_outdoors": True,
    "likes_research": False,
    "high_attention_detail": True,
    "likes_leadership": False
}

rules = [
    # Engineering path: math AND (science OR technology) AND problem_solving AND NOT(prefers_teamwork)
    {"if": "(likes_maths and (likes_science or likes_technology) and likes_problem_solving and not prefers_teamwork)", 
     "then": "is_engineer"},
    
    # Teaching path: (children OR helping_people) AND good_communication
    {"if": "((likes_children or likes_helping_people) and good_communication)", 
     "then": "is_teacher"},
    
    # Police path: (discipline AND helping_people) OR (outdoors AND leadership)
    {"if": "((likes_discipline and likes_helping_people) or (likes_outdoors and likes_leadership))", 
     "then": "is_policeman"},
    
    # Law path: law AND (high_attention_detail OR likes_problem_solving) AND NOT(likes_creativity)
    {"if": "(likes_law and (high_attention_detail or likes_problem_solving) and not likes_creativity)", 
     "then": "is_lawyer"},
    
    # Medical path: (science AND NOT(dislikes_blood)) OR (helping_people AND high_attention_detail)
    {"if": "((likes_science and not dislikes_blood) or (likes_helping_people and high_attention_detail))", 
     "then": "is_doctor"},
    
    # Research path: (science OR likes_research) AND high_attention_detail
    {"if": "((likes_science or likes_research) and high_attention_detail)", 
     "then": "is_researcher"},
    
    # IT path: technology AND (problem_solving OR maths) AND NOT(prefers_teamwork)
    {"if": "(likes_technology and (likes_problem_solving or likes_maths) and not prefers_teamwork)", 
     "then": "is_it_specialist"}
]

recommendation_map = {
    "is_engineer": "Engineer - Ideal for analytical problem-solvers who enjoy technical work",
    "is_teacher": "Teacher - Perfect for those who excel in communication and knowledge sharing",
    "is_policeman": "Police Officer - Suited for disciplined individuals who want to serve society",
    "is_lawyer": "Lawyer - Excellent for detail-oriented problem solvers interested in justice",
    "is_doctor": "Doctor - Great for those who combine scientific interest with caring for others",
    "is_researcher": "Researcher - Ideal for detail-oriented individuals who love discovery",
    "is_it_specialist": "IT Specialist - Perfect for tech-savvy independent problem solvers"
}

# --- Interactive input helpers ---
def ask_bool(prompt: str) -> bool:
    return input(f"{prompt} (y/n): ").strip().lower().startswith("y")


def collect_facts() -> dict:
    f = {}
    f["likes_helping_people"] = ask_bool("Do you like helping people?")
    f["likes_maths"] = ask_bool("Do you like maths?")
    f["likes_creativity"] = ask_bool("Do you enjoy creative work?")
    f["likes_law"] = ask_bool("Are you interested in law?")
    f["likes_science"] = ask_bool("Do you like science?")
    f["likes_discipline"] = ask_bool("Do you value discipline and structure?")
    f["dislikes_blood"] = ask_bool("Do you dislike seeing blood?")
    f["likes_children"] = ask_bool("Do you like working with children?")
    f["good_communication"] = ask_bool("Are you good at communication?")
    f["likes_technology"] = ask_bool("Do you enjoy working with technology?")
    f["likes_problem_solving"] = ask_bool("Do you enjoy solving complex problems?")
    f["prefers_teamwork"] = ask_bool("Do you prefer working in teams?")
    f["likes_outdoors"] = ask_bool("Do you enjoy outdoor activities?")
    f["likes_research"] = ask_bool("Do you enjoy conducting research?")
    f["high_attention_detail"] = ask_bool("Do you have high attention to detail?")
    f["likes_leadership"] = ask_bool("Do you enjoy taking leadership roles?")
    return f


# --- Simple Forward Chaining ---

def forward_chain(initial_facts: dict, rules: list[dict[str, str]]):
    """
    Repeatedly apply rules of the form {"if": <expr>, "then": <symbol>}.
    When a rule's condition is true under the current facts, assert its consequent
    as True in the fact base. Continue until no new facts are derived.
    Returns: (final_facts, newly_derived_keys)
    """
    facts = dict(initial_facts)  # work on a copy
    derived: set[str] = set()
    changed = True
    while changed:
        changed = False
        for rule in rules:
            condition = rule["if"]
            consequent = rule["then"]
            # If we already know the consequent is true, skip
            if facts.get(consequent) is True:
                continue
            # Evaluate the rule's condition in the context of current facts
            if eval(condition, {}, facts):
                facts[consequent] = True
                derived.add(consequent)
                changed = True
    return facts, derived


def collect_recommendations(facts: dict, derived: set[str]) -> list[str]:
    """Turn derived proposition symbols into human-readable recommendations."""
    recs = []
    for sym in derived:
        label = recommendation_map.get(sym)
        if label:
            recs.append(label)
    # Sort alphabetically for deterministic output
    return sorted(recs)


# --- Entry point ---
if __name__ == "__main__":
    print("Career Advisor — quick demo")
    use_interactive = ask_bool("Answer questions interactively?")
    if use_interactive:
        user_facts = collect_facts()
    else:
        user_facts = facts  # use the defaults declared at the top

    final_facts, derived = forward_chain(user_facts, rules)
    recommendations = collect_recommendations(final_facts, derived)

    print("\nFacts:", final_facts)
    print("Derived facts:", sorted(list(derived)) or ["(none)"])
    print("Recommendations:", recommendations or ["(none matched yet)"])
