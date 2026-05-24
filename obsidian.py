import os
from config import VAULT_PATH

def get_all_notes():
    """Retourne la liste de tous les fichiers .md du vault"""
    notes = []
    for root, dirs, files in os.walk(VAULT_PATH):
        dirs[:] = [d for d in dirs if d != '.obsidian']
        for file in files:
            if file.endswith('.md'):
                notes.append(os.path.join(root, file))
    return notes

def read_note(filepath):
    """Lit et retourne le contenu d'une note"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def search_notes(keywords):
    if isinstance(keywords, str):
        keywords = [keywords]
    results = []
    for filepath in get_all_notes():
        content = read_note(filepath)
        if any(kw.lower() in content.lower() for kw in keywords):
            note_name = os.path.basename(filepath)
            results.append({
                "name": note_name,
                "path": filepath,
                "content": content[:500],
                "preview": content[:300]
            })
    return results

def append_or_create_note(filename, content, subfolder="Admin"):
    folder = os.path.join(VAULT_PATH, subfolder)
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(content)
    return filepath

def save_note(filename, content, subfolder="Admin"):
    folder = os.path.join(VAULT_PATH, subfolder)
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return filepath

if __name__ == "__main__":
    notes = get_all_notes()
    if not notes:
        print("Aucune note trouvée.")
    else:
        for note in notes:
            print(note)