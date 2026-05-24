import os 
from config import VAULT_PATH

import os
from config import VAULT_PATH

def get_all_notes():
    """Retourne la liste de tous les fichiers .md du vault"""
    notes = []
    for root, dirs, files in os.walk(VAULT_PATH):
        # Ignorer le dossier .obsidian (config interne)
        dirs[:] = [d for d in dirs if d != '.obsidian']
        for file in files:
            if file.endswith('.md'):
                notes.append(os.path.join(root, file))
    return notes

def read_note(filepath):
    """Lit et retourne le contenu d'une note"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def search_notes(keyword):
    """Cherche un mot-clé dans toutes les notes, retourne les passages pertinents"""
    results = []
    for filepath in get_all_notes():
        content = read_note(filepath)
        if keyword.lower() in content.lower():
            # Nom de la note sans le chemin complet
            note_name = os.path.basename(filepath)
            results.append({
                "name": note_name,
                "path": filepath,
                "preview": content[:300]  # Les 300 premiers caractères
            })
    return results

def save_note(filename, content, subfolder="Admin"):
    """Crée une nouvelle note dans le vault"""
    folder = os.path.join(VAULT_PATH, subfolder)
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return filepath


if __name__ == "__main__":
    print("Notes trouvées:")
    notes = get_all_notes()

    if not notes: 
        print("Aucune note trouvée.")
    else: 
        for note in notes:
            print(note)