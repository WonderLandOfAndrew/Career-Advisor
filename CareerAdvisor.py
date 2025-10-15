facts = {
    "likes_helping_people": True,
    "likes_maths": False,
    "likes_creativity": False,
    "likes_law": True,
    "likes_science": False,
    "likes_discipline": True,
    "dislikes_blood": False,
    "likes_children": True
}

rules = [
    {"if": "likes_maths and likes_science", "then": "is_engineer"},
    {"if": "likes_helping_people and likes_children", "then": "is_teacher"},
    {"if": "likes_discipline and not dislikes_blood", "then": "is_policeman"},
    {"if": "likes_law", "then": "is_lawyer"},
    {"if": "likes_science and not dislikes_blood", "then": "is_doctor"}
]

recommendation_map = {
    "is_engineer": "Engineer",
    "is_teacher": "Teacher",
    "is_policeman": "Policeman",
    "is_lawyer": "Lawyer",
    "is_doctor": "Doctor",
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
