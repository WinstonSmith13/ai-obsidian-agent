import anthropic
import re
from config import ANTHROPIC_API_KEY, VAULT_PATH
from obsidian import search_notes, append_or_create_note
from datetime import date

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """# ROLE
You are Winston's personal admin assistant. Your sole mission is to help him clear administrative tasks he tends to procrastinate on. You are ultra-efficient, pragmatic, and action-oriented.

# BEHAVIOR
- No filler: skip greetings and preamble. Get straight to the point.
- Tone: direct, factual, slightly firm but supportive.
- Keep it short. Cut everything that doesn't drive action.

# RESPONSE FORMAT
1. **Action plan:** Numbered steps, chronological, immediately actionable.
2. **End section:** Always close with the Obsidian note below.

---

## 📝 Obsidian Note
```markdown
## [Task title]
- **Status:** In progress
- **Date:** {{date}}
- **Summary:** [1-2 sentence max]
- **Next action:** [The very first thing Winston needs to do]"""


def ask(question):
    words = re.findall(r'\b\w{4,}\b', question.lower())

    vault_context = ""
    if words:
        found_notes = search_notes(words)
        if found_notes:
            vault_context = "\n\n=== CONTEXT FROM YOUR OBSIDIAN VAULT ===\n"
            for note in found_notes[:3]:
                vault_context += f"--- {note['name']} ---\n{note['content']}\n\n"
            vault_context += "========================================\n"

    print("Thinking...")
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": f"{vault_context}Winston's question: {question}"}
        ]
    )
    answer = response.content[0].text
    print("\n" + answer)

    today = date.today().strftime("%Y-%m-%d")
    title_response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=20,
        messages=[{"role": "user", "content": f"Give a 3-word max title for this question: {question}. Reply with the title only, nothing else."}]
    )
    filename = f"{today} - {title_response.content[0].text.strip()}.md"

    note_content = f"## ❓ {question}\n\n{answer}\n\n---\n"
    filepath = append_or_create_note(filename, note_content)
    print(f"\nNote saved: {filepath}")

    return answer


if __name__ == "__main__":
    print("Winston's Admin Agent — type 'quit' to exit\n")
    while True:
        question = input("Your question: ").strip()
        if question.lower() in ("quit", "exit", "q"):
            print("Bye.")
            break
        if not question:
            continue
        ask(question)
        print()
