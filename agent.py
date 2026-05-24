import anthropic
import re
from config import ANTHROPIC_API_KEY, VAULT_PATH
from obsidian import search_notes, append_or_create_note
from datetime import date

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """# RÔLE
Tu es l'assistant administratif personnel de Winston. Ton unique mission est de l'aider à liquider les tâches administratives qu'il a tendance à procrastiner. Tu es ultra-efficace, pragmatique et orienté action.

# DIRECTIVES DE COMPORTEMENT
- **Pas de blabla :** Supprime les formules de politesse inutiles ("Bonjour Winston", "J'espère que tu vas bien", "Voici les étapes..."). Entre directement dans le vif du sujet.
- **Ton :** Direct, factuel, légèrement directif mais bienveillant. Tu es là pour faire avancer les choses.
- **Concision :** Réponses courtes. Va à l'essentiel.

# FORMAT DE RÉPONSE
1. **Plan d'action :** Présente la solution sous forme d'étapes numérotées claires, chronologiques et actionnables immédiatement.
2. **Section de fin :** Termine obligatoirement et strictement chaque réponse par la section Obsidian ci-dessous.

---

## 📝 Note Obsidian
```markdown
## [Titre de la tâche]
- **Statut :** En cours
- **Date :** {{date}}
- **Résumé :** [Insérer un résumé ultra-court en 1 ou 2 phrases max]
- **Prochaine action :** [La toute première action que Winston doit faire]"""


def ask(question):
    # 1. Extraction des mots-clés
    words = re.findall(r'\b\w{4,}\b', question.lower())

    # 2. Recherche dans le vault
    contexte_notes = ""
    if words:
        notes_trouvees = search_notes(words)
        if notes_trouvees:
            contexte_notes = "\n\n=== CONTEXTE DE TON VAULT OBSIDIAN ===\n"
            for note in notes_trouvees[:3]:
                contexte_notes += f"--- {note['name']} ---\n{note['content']}\n\n"
            contexte_notes += "======================================\n"

    # 3. Appeler Claude pour la réponse
    print("Laisse moi réfléchir...")
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": f"{contexte_notes}Question de Winston : {question}"}
        ]
    )
    answer = response.content[0].text
    print("\n" + answer)

    # 4. Générer un titre intelligent pour la note
    today = date.today().strftime("%Y-%m-%d")
    title_response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=20,
        messages=[{"role": "user", "content": f"Donne un titre de 3 mots max pour cette question : {question}. Réponds uniquement le titre, rien d'autre."}]
    )
    theme = title_response.content[0].text.strip()
    filename = f"{today} - {theme}.md"

    # 5. Sauvegarder dans le vault
    note_content = f"## ❓ {question}\n\n{answer}\n\n---\n"
    filepath = append_or_create_note(filename, note_content)
    print(f"\nNote MAJ : {filepath}")

    return answer


if __name__ == "__main__":
    ask("J'ai fait une demande de renouvellement de carte de residence permanente au canada le 19 mars. Je n'ai toujours rien que faire ?")