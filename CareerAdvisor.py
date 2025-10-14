rules = [
    {
         ("likes_math and not likes_creativity", "recommend_engineering"),
         ("likes_creativity", "recommend_design")
    }
]

facts = {
    "likes_math": True,
    "likes_coding": True,
    "likes_creativity": True,
    "likes_teamwork": True,
    "wants_remote": True,
    "risk_averse": True,
    "dislikes_blood": True
}

