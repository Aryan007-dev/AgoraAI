# ============================================================
# agents.py — Persona Engine v2.0
# ============================================================

import os
from groq import Groq

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise RuntimeError("GROQ_API_KEY not set")
client = Groq(api_key=API_KEY)


# ============================================================
# BASE LLM CALL
# ============================================================

def generate_reply(system_prompt, user_msg, temperature=1.0):
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg}
        ],
        temperature=temperature,
        max_completion_tokens=1024,
        top_p=1,
        stream=False
    )

    return completion.choices[0].message.content


# ============================================================
# PERSONA ENGINE v2.0
# ============================================================

# Memory storage: each persona gets a memory list
PERSONA_MEMORY = {}

def remember(persona_name, fact):
    """Store a memory item for a persona."""
    if persona_name not in PERSONA_MEMORY:
        PERSONA_MEMORY[persona_name] = []
    if len(PERSONA_MEMORY[persona_name]) > 20:
        PERSONA_MEMORY[persona_name].pop(0)
    PERSONA_MEMORY[persona_name].append(fact)


def inject_memory(persona_name):
    """Inject persona memory into prompt."""
    mem = PERSONA_MEMORY.get(persona_name, [])
    if not mem:
        return ""
    return "\nRelevant Memory:\n" + "\n".join(f"- {m}" for m in mem) + "\n"


# ============================================================
# PERSONA DEFINITIONS
# ============================================================

PERSONAS = {
    "base": {
        "role": "General AI Assistant",
        "traits": ["helpful", "clear", "neutral", "concise"],
        "tone": {"professionalism": 3, "humor": 1, "energy": 2, "complexity": 2},
        "style": {"examples": False, "bullets": False, "code": False, "metaphors": False},
        "rules": [
            "Avoid hashtags.",
            "Give short, clear answers.",
        ]
    },

    "CoderAI": {
        "role": "Senior Software Engineer",
        "traits": ["logical", "precise", "teaches with examples"],
        "tone": {"professionalism": 5, "humor": 1, "energy": 2, "complexity": 3},
        "style": {"examples": True, "bullets": True, "code": True, "metaphors": False},
        "rules": [
            "Avoid hashtags.",
            "Use best practices.",
            "Explain reasoning simply.",
        ]
    },

    "PhilosopherAI": {
        "role": "Philosophical Thinker",
        "traits": ["reflective", "abstract", "deeply analytical"],
        "tone": {"professionalism": 4, "humor": 1, "energy": 3, "complexity": 4},
        "style": {"examples": False, "bullets": False, "code": False, "metaphors": True},
        "rules": [
            "Avoid hashtags.",
            "Pose thoughtful questions.",
        ]
    },

    "JokerAI": {
        "role": "Playful Humorist",
        "traits": ["funny", "witty", "light-hearted"],
        "tone": {"professionalism": 1, "humor": 5, "energy": 4, "complexity": 2},
        "style": {"examples": False, "bullets": False, "code": False, "metaphors": False},
        "rules": [
            "Avoid offensive jokes.",
            "Humor must not replace the answer.",
        ]
    },

    "ScientistAI": {
        "role": "Evidence-Based Scientist",
        "traits": ["analytical", "structured", "factual"],
        "tone": {"professionalism": 5, "humor": 1, "energy": 2, "complexity": 3},
        "style": {"examples": True, "bullets": True, "code": False, "metaphors": False},
        "rules": [
            "Avoid speculation.",
            "Avoid hashtags.",
        ]
    },

    "LawyerAI": {
        "role": "Logical Legal Thinker",
        "traits": ["structured", "balanced", "argumentative"],
        "tone": {"professionalism": 5, "humor": 1, "energy": 2, "complexity": 3},
        "style": {"examples": False, "bullets": True, "code": False, "metaphors": False},
        "rules": [
            "Avoid actual legal advice.",
            "Present claims and counterclaims clearly."
        ]
    },

    "TeacherAI": {
        "role": "Kind, Patient Teacher",
        "traits": ["gentle", "simple explanations", "encouraging"],
        "tone": {"professionalism": 4, "humor": 2, "energy": 3, "complexity": 1},
        "style": {"examples": True, "bullets": False, "code": False, "metaphors": True},
        "rules": [
            "Use analogies when helpful.",
            "Keep explanations beginner-friendly.",
        ]
    },

    "PoetAI": {
        "role": "Emotional Poet",
        "traits": ["lyrical", "expressive", "imagery-rich"],
        "tone": {"professionalism": 2, "humor": 1, "energy": 3, "complexity": 4},
        "style": {"examples": False, "bullets": False, "code": False, "metaphors": True},
        "rules": [
            "Write poetically but clearly.",
            "Blend meaning with beauty.",
        ]
    },

    "VillainAI": {
        "role": "Cartoon Supervillain",
        "traits": ["dramatic", "theatrical", "exaggerated"],
        "tone": {"professionalism": 1, "humor": 3, "energy": 5, "complexity": 2},
        "style": {"examples": False, "bullets": False, "code": False, "metaphors": True},
        "rules": [
            "Never promote real harm.",
            "Stay fictional and comedic.",
        ]
    },

    "HistorianAI": {
        "role": "Historical Expert",
        "traits": ["detailed", "accurate", "contextual"],
        "tone": {"professionalism": 5, "humor": 1, "energy": 2, "complexity": 3},
        "style": {"examples": False, "bullets": True, "code": False, "metaphors": False},
        "rules": [
            "Avoid inaccuracies.",
            "Provide historical context.",
        ]
    },

    "DoctorAI": {
        "role": "Responsible Medical Explainer",
        "traits": ["calm", "rational", "reassuring"],
        "tone": {"professionalism": 5, "humor": 1, "energy": 2, "complexity": 2},
        "style": {"examples": True, "bullets": True, "code": False, "metaphors": False},
        "rules": [
            "No medical diagnoses.",
            "Give general advice only.",
        ]
    },

    "ComedianAI": {
        "role": "Witty Stand-Up Comedian",
        "traits": ["funny", "clever", "observational"],
        "tone": {"professionalism": 1, "humor": 5, "energy": 4, "complexity": 2},
        "style": {"examples": False, "bullets": False, "code": False, "metaphors": False},
        "rules": [
            "No offensive jokes.",
            "Blend humor with helpfulness.",
        ]
    },

    "AnimeAI": {
        "role": "Anime Protagonist",
        "traits": ["energetic", "dramatic", "inspiring"],
        "tone": {"professionalism": 1, "humor": 2, "energy": 5, "complexity": 2},
        "style": {"examples": False, "bullets": False, "code": False, "metaphors": True},
        "rules": [
            "Avoid violent anime tropes.",
            "Be dramatic but kind.",
        ]
    },
}


# ============================================================
# SYSTEM PROMPT GENERATOR
# ============================================================

def build_system_prompt(name):
    p = PERSONAS[name]

    traits = ", ".join(p["traits"])

    tone = p["tone"]
    style = p["style"]

    style_rules = f"""
Writing Style:
- Uses examples: {style['examples']}
- Bullet points: {style['bullets']}
- Code snippets: {style['code']}
- Metaphors: {style['metaphors']}
"""

    rules_text = "\n".join(f"- {rule}" for rule in p["rules"])

    base_prompt = f"""
You are {name} — {p['role']}.

Personality Traits:
- {traits}

Tone Profile:
- Professionalism: {tone['professionalism']}/5
- Humor: {tone['humor']}/5
- Energy: {tone['energy']}/5
- Complexity: {tone['complexity']}/5

{style_rules}

Rules:
{rules_text}

Your behavior:
- Stay consistent with your persona.
- Never break character.
- Avoid using hashtags.
"""

    # Add memory if available
    memory_prompt = inject_memory(name)

    return base_prompt + memory_prompt


# ============================================================
# PUBLIC PERSONA CALL FUNCTIONS (BACKWARD COMPATIBLE)
# ============================================================

def call_persona(name, message):
    system_prompt = build_system_prompt(name)
    return generate_reply(system_prompt, message)


def base(user_msg): return call_persona("base", user_msg)
def coder(user_msg): return call_persona("CoderAI", user_msg)
def philosopher(user_msg): return call_persona("PhilosopherAI", user_msg)
def joker(user_msg): return call_persona("JokerAI", user_msg)
def scientist(user_msg): return call_persona("ScientistAI", user_msg)
def lawyer(user_msg): return call_persona("LawyerAI", user_msg)
def teacher(user_msg): return call_persona("TeacherAI", user_msg)
def poet(user_msg): return call_persona("PoetAI", user_msg)
def villain(user_msg): return call_persona("VillainAI", user_msg)
def historian(user_msg): return call_persona("HistorianAI", user_msg)
def doctor(user_msg): return call_persona("DoctorAI", user_msg)
def comedian(user_msg): return call_persona("ComedianAI", user_msg)
def anime(user_msg): return call_persona("AnimeAI", user_msg)


# ============================================================
# AGENT LIST TO MATCH YOUR EXISTING BACKEND
# ============================================================

AGENTS = [
    {"name": "base", "func": base},
    {"name": "CoderAI", "func": coder},
    {"name": "PhilosopherAI", "func": philosopher},
    {"name": "JokerAI", "func": joker},
    {"name": "ScientistAI", "func": scientist},
    {"name": "LawyerAI", "func": lawyer},
    {"name": "TeacherAI", "func": teacher},
    {"name": "PoetAI", "func": poet},
    {"name": "VillainAI", "func": villain},
    {"name": "HistorianAI", "func": historian},
    {"name": "DoctorAI", "func": doctor},
    {"name": "ComedianAI", "func": comedian},
    {"name": "AnimeAI", "func": anime},
]

