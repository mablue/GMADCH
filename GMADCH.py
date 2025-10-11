import os
import re
from collections import defaultdict, Counter

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def extract_words_from_code(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    words = re.findall(r'\b\w+\b', content)
    return words

def calculate_scores(words, dictionary):
    scores = defaultdict(float)
    for word in words:
        base_count = dictionary.get(word, 0)
        score = base_count
        for other_word in dictionary:
            if word == other_word:
                continue
            dist = levenshtein(word, other_word)
            if dist >= 1:
                score += dictionary[other_word] / dist
        scores[word] = score
    return scores

def main(dictionary):
    folder_tags = defaultdict(list)
    file_tags = {}
    for root, dirs, files in os.walk('.'):  
        for fname in files:
            if fname.endswith(('.py', '.js', '.java', '.cpp', '.go', '.ts', '.rb', '.php', '.cs', '.c', '.swift', '.kt')):
                fpath = os.path.join(root, fname)
                words = extract_words_from_code(fpath)
                scores = calculate_scores(words, dictionary)
                top_tags = [w for w, _ in Counter(scores).most_common(3)]
                file_tags[fpath] = top_tags
                folder_tags[root].append((fname, top_tags))

    for fpath, tags in file_tags.items():
        print(f"{os.path.relpath(fpath)} -> {', '.join(tags)}")
    print("\nFolders and grouped files:")
    for folder, files in folder_tags.items():
        print(f"\n{folder}:")
        tags_in_folder = defaultdict(list)
        for fname, tags in files:
            for tag in tags:
                tags_in_folder[tag].append(fname)
        for tag, grouped_files in tags_in_folder.items():
            if len(grouped_files) > 1:
                print(f"  Tag '{tag}': {', '.join(grouped_files)}")

if __name__ == "__main__":
    # Example: replace with your dictionary of important terms
    user_dict = {
        'ccxt': 20,
        'numpy': 15,
        'leven': 12,
        'pandas': 10,
        'tasks': 7,
        'utils': 5
    }
    main(user_dict)