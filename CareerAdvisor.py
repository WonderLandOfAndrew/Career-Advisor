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
    ("likes_maths and likes_science", "Engineer"),
    ("likes_helping_people and likes_children", "Teacher"),
    ("likes_discipline and not dislikes_blood", "Policeman"),
    ("likes_law", "Lawyer"),
    ("likes_science and not dislikes_blood", "Doctor")
]


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


# --- Minimal inference ---

def infer(facts: dict, rules):
    results = []
    for condition, profession in rules:
        if eval(condition, {}, facts):
            results.append(profession)
    return results


# --- Entry point ---
if __name__ == "__main__":
    print("Career Advisor — quick demo")
    use_interactive = ask_bool("Answer questions interactively?")
    if use_interactive:
        user_facts = collect_facts()
    else:
        user_facts = facts  # use the defaults declared at the top

    recommendations = infer(user_facts, rules)
    print("\nFacts:", user_facts)
    print("Recommendations:", recommendations or ["(none matched yet)"])

