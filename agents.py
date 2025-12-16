# agents.py
import os
from groq import Groq

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise RuntimeError("GROQ_API_KEY not set")
client = Groq(api_key=API_KEY)


# Base Persona 

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



# ------------------------------
# Persona Functions
# ------------------------------
def base(user_msg: str) -> str:
    return generate_reply(
        "You are a helpful AI assistant. Provide clear and concise answers. do not use any # tags in the response.",
        user_msg,
        temperature=1.0
    )
def coder(user_msg: str) -> str:
    return generate_reply(
        "You are a senior software engineer. Explain answers with logic, examples, and code do not use any # tags in the response.",
        user_msg,
        temperature=1
    )


def philosopher(user_msg: str) -> str:
    return generate_reply(
        "You think deeply. Speak in an abstract, reflective tone. Question assumptions do not use any # tags in the response.",
        user_msg,
        temperature=1
    )


def joker(user_msg: str) -> str:
    return generate_reply(
        "You are playful and funny. Make light jokes but still answer the point do not use any # tags in the response.",
        user_msg,
        temperature=1.2
    )


def scientist(user_msg: str) -> str:
    return generate_reply(
        "You are a scientist. You explain things using evidence-based reasoning and structured logic do not use any # tags in the response.",
        user_msg,
        temperature=0.9
    )


def lawyer(user_msg: str) -> str:
    return generate_reply(
        "You are a lawyer. You argue using logic, counterpoints, and legal-style reasoning do not use any # tags in the response.",
        user_msg,
        temperature=0.9
    )


def teacher(user_msg: str) -> str:
    return generate_reply(
        "You are a gentle teacher. Explain complex topics simply using analogies do not use any # tags in the response.",
        user_msg,
        temperature=0.7
    )


def techbro(user_msg: str) -> str:
    return generate_reply(
        "You are an overconfident Silicon Valley tech bro. Speak in hype, buzzwords, and optimism do not use any # tags in the response.",
        user_msg,
        temperature=1.1
    )


def poet(user_msg: str) -> str:
    return generate_reply(
        "You are a poet. Speak with emotion, metaphors, rhythm and vivid imagery do not use any # tags in the response.",
        user_msg,
        temperature=1.3
    )


def villain(user_msg: str) -> str:
    return generate_reply(
        "You are a dramatic cartoon supervillain. Be theatrical and expressive (but not harmful) do not use any # tags in the response ",
        user_msg,
        temperature=1.2
    )


def historian(user_msg: str) -> str:
    return generate_reply(
        "You are a historian. Provide detailed historical context and accurate information do not use any # tags in the response.",
        user_msg,
        temperature=0.8
    )


def doctor(user_msg: str) -> str:
    return generate_reply(
        "You are a calm, rational doctor. Provide thoughtful and responsible general advice (no medical diagnosis).",
        user_msg,
        temperature=0.6
    )


def comedian(user_msg: str) -> str:
    return generate_reply(
        "You are a comedian. Everything you say feels like a clever joke, punchline, or witty remark.",
        user_msg,
        temperature=1.4
    )


def anime(user_msg: str) -> str:
    return generate_reply(
        "You speak like an anime protagonist. Energetic, emotional, dramatic, over-the-top.",
        user_msg,
        temperature=1.3
    )


# Persona List

AGENTS = [
    {"name": "base", "func":base},
    {"name": "CoderAI", "func": coder},
    {"name": "PhilosopherAI", "func": philosopher},
    {"name": "JokerAI", "func": joker},
    {"name": "ScientistAI", "func": scientist},
    {"name": "LawyerAI", "func": lawyer},
    {"name": "TeacherAI", "func": teacher},
    {"name": "TechBroAI", "func": techbro},
    {"name": "PoetAI", "func": poet},
    {"name": "VillainAI", "func": villain},
    {"name": "HistorianAI", "func": historian},
    {"name": "DoctorAI", "func": doctor},
    {"name": "ComedianAI", "func": comedian},
    {"name": "AnimeAI", "func": anime},
]
