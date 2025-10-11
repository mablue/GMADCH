import os
import re
import ast
from collections import defaultdict, Counter
from multiprocessing import Pool, cpu_count

COMMON_KEYWORDS = set([
    # Python
    'def', 'class', 'for', 'if', 'else', 'elif', 'while', 'return', 'import', 'from', 'as', 'with', 'pass',
    'break', 'continue', 'try', 'except', 'finally', 'raise', 'global', 'lambda', 'yield', 'del', 'assert',
    'or', 'and', 'not', 'is', 'in', 'True', 'False', 'None',
    # Java/C/C++/C#
    'public', 'private', 'protected', 'static', 'final', 'void', 'int', 'float', 'double', 'char', 'boolean',
    'new', 'this', 'super', 'extends', 'implements', 'interface', 'package', 'throws', 'throw', 'catch',
    'case', 'switch', 'default', 'do', 'while', 'try', 'finally', 'null', 'enum', 'abstract', 'synchronized',
    'volatile', 'transient', 'goto', 'const', 'signed', 'unsigned', 'short', 'long', 'typedef', 'sizeof',
    'struct', 'union', 'register', 'extern', 'inline',
    # JS/TS
    'function', 'let', 'var', 'const', 'export', 'import', 'require', 'module', 'prototype', 'typeof',
    'undefined', 'true', 'false', 'class', 'constructor', 'return', 'await', 'async', 'yield', 'delete', 'this',
    # Go
    'func', 'package', 'type', 'map', 'chan', 'defer', 'go', 'select', 'range', 'make', 'new', 'struct', 'interface',
    'fallthrough',
    # Ruby
    'def', 'class', 'module', 'end', 'do', 'if', 'elsif', 'else', 'unless', 'while', 'until', 'for', 'break', 'next',
    'redo', 'retry', 'in', 'self', 'nil', 'true', 'false', 'yield', 'super', 'then', 'when', 'case', 'require', 'include',
    'begin', 'rescue', 'ensure', 'alias', 'undef', 'defined?', 'not', 'and', 'or',
    # PHP
    'function', 'class', 'public', 'private', 'protected', 'static', 'abstract', 'interface', 'implements', 'extends',
    'echo', 'print', 'return', 'require', 'include', 'if', 'else', 'elseif', 'while', 'do', 'for', 'foreach', 'switch',
    'case', 'default', 'break', 'continue', 'try', 'catch', 'finally', 'throw', 'global', 'var', 'const', 'true', 'false', 'null',
    # Swift/Kotlin/Scala
    'func', 'let', 'var', 'struct', 'enum', 'protocol', 'extension', 'import', 'class', 'public', 'private', 'protected',
    'internal', 'open', 'final', 'override', 'static', 'abstract', 'interface', 'package', 'object', 'companion',
    'data', 'sealed', 'lateinit', 'init', 'val', 'when', 'super', 'this', 'by', 'get', 'set', 'field',
    # Rust
    'fn', 'let', 'mut', 'pub', 'crate', 'use', 'mod', 'impl', 'trait', 'struct', 'enum', 'const', 'static', 'type',
    'match', 'if', 'else', 'for', 'loop', 'while', 'break', 'continue', 'return', 'true', 'false', 'as', 'in', 'move', 'ref',
    # Perl
    'sub', 'my', 'our', 'use', 'package', 'if', 'else', 'elsif', 'unless', 'while', 'until', 'for', 'foreach', 'next',
    'last', 'redo', 'goto', 'return', 'die', 'warn', 'local', 'state', 'BEGIN', 'END',
    # Haskell
    'let', 'in', 'where', 'module', 'import', 'data', 'type', 'class', 'instance', 'deriving', 'newtype',
    'do', 'case', 'of', 'if', 'then', 'else', 'as', 'qualified', 'default', 'foreign', 'forall',
    # Lua
    'function', 'local', 'end', 'if', 'then', 'elseif', 'else', 'for', 'in', 'do', 'while', 'repeat', 'until', 'break',
    'return', 'true', 'false', 'nil',
    # Dart
    'void', 'int', 'double', 'num', 'bool', 'String', 'dynamic', 'var', 'final', 'const', 'class', 'interface', 'extends',
    'implements', 'mixin', 'abstract', 'override', 'static', 'this', 'super', 'new', 'return', 'break', 'continue', 'if',
    'else', 'for', 'while', 'do', 'switch', 'case', 'default', 'try', 'catch', 'finally', 'throw',
    # Objective-C
    'int', 'float', 'double', 'char', 'void', 'id', 'BOOL', 'YES', 'NO', 'nil', 'self', 'super', 'if', 'else', 'for',
    'while', 'do', 'switch', 'case', 'break', 'continue', 'return', 'goto',
    '@interface', '@implementation', '@end', '@property', '@synthesize', '@dynamic', '@selector',
    # R
    'function', 'if', 'else', 'for', 'while', 'break', 'next', 'return', 'TRUE', 'FALSE', 'NA', 'NULL',
    # MATLAB
    'function', 'end', 'if', 'else', 'elseif', 'for', 'while', 'break', 'continue', 'return', 'switch', 'case', 'otherwise',
    'try', 'catch', 'global', 'persistent',
    # Shell/Bash
    'if', 'then', 'fi', 'else', 'elif', 'case', 'esac', 'for', 'while', 'until', 'do', 'done', 'in', 'function', 'select',
    'continue', 'break', 'return', 'exit', 'echo', 'readonly', 'getopts', 'shift', 'trap', 'true', 'false', 'test',
    # Fortran
    'function', 'subroutine', 'program', 'module', 'contains', 'end', 'if', 'then', 'else', 'elseif', 'do', 'while', 'cycle',
    'exit', 'return', 'goto', 'call', 'continue', 'stop', 'integer', 'real', 'double', 'complex', 'character', 'logical', 'parameter',
    # SQL
    'select', 'from', 'where', 'insert', 'into', 'update', 'delete', 'create', 'table', 'view', 'index', 'alter', 'drop',
    'join', 'on', 'group', 'by', 'having', 'as', 'distinct', 'order', 'limit', 'offset', 'values', 'set',
    # General English Stopwords (for comments)
    'the', 'and', 'a', 'an', 'of', 'to', 'in', 'on', 'by', 'for', 'is', 'it', 'at', 'be', 'as', 'or', 'not', 'with', 'was',
    'were', 'this', 'that', 'these', 'those', 'has', 'have', 'had', 'but', 'do', 'did', 'does', 'are', 'were', 'can', 'could',
    'should', 'would', 'may', 'might', 'must', 'will', 'shall', 'his', 'her', 'their', 'our', 'your', 'my', 'i', 'you', 'he', 'she', 'they', 'we'
])

def is_valid_tag(word):
    return len(word) > 2 and word.lower() not in COMMON_KEYWORDS and not word.isdigit()

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

def build_global_dictionary(all_files):
    global_word_counts = Counter()
    for file_path in all_files:
        words = extract_words_from_code(file_path)
        global_word_counts.update(word for word in words if is_valid_tag(word))
    return dict(global_word_counts)

def score_file(args):
    fpath, dictionary = args
    words = extract_words_from_code(fpath)
    scores = defaultdict(float)
    for word in words:
        if not is_valid_tag(word):
            continue
        base_count = dictionary.get(word, 0)
        score = base_count
        for other_word in dictionary:
            if word == other_word or not is_valid_tag(other_word):
                continue
            dist = levenshtein(word, other_word)
            if dist >= 1:
                score += dictionary[other_word] / dist
        scores[word] = score
    top_tags = [w for w, _ in Counter(scores).most_common(10) if is_valid_tag(w)][:3]
    folder = os.path.dirname(fpath)
    fname = os.path.basename(fpath)
    return (fpath, folder, fname, top_tags)

def show_progress(current, total, bar_length=40):
    percent = float(current) / total
    arrow = '-' * int(round(percent * bar_length)-1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    print(f"\rProgress: [{arrow}{spaces}] {int(percent*100)}% ({current}/{total})", end='')

def main():
    extensions = (
        '.py', '.js', '.java', '.cpp', '.go', '.ts', '.rb', '.php', '.cs', '.c', '.swift', '.kt', '.h', '.hpp',
        '.scala', '.rs', '.pl', '.hs', '.lua', '.dart', '.m', '.R', '.sh', '.bash', '.f', '.f90', '.sql'
    )
    all_files = []
    for root, dirs, files in os.walk('.'):
        for fname in files:
            if fname.endswith(extensions):
                fpath = os.path.join(root, fname)
                all_files.append(fpath)

    print("GMADCH Modularization Algorithm")
    print("Choose dictionary source:")
    print("1. Build from all code files (automatic)")
    print("2. Enter your own dictionary (Python dict: {'tag1':count, ...})")
    choice = input("Enter option number (1 or 2): ").strip()

    if choice == '2':
        print("Enter your dictionary as a Python dict (e.g. {'ccxt': 20, 'numpy': 10}):")
        user_dict_str = input()
        try:
            dictionary = ast.literal_eval(user_dict_str)
            if not isinstance(dictionary, dict):
                raise ValueError
        except Exception:
            print("Invalid dictionary format. Exiting.")
            return
    else:
        dictionary = build_global_dictionary(all_files)

    total = len(all_files)
    results = []
    with Pool(cpu_count()) as pool:
        for idx, result in enumerate(pool.imap(score_file, [(fpath, dictionary) for fpath in all_files]), 1):
            results.append(result)
            show_progress(idx, total)
    print()  # Newline after progress bar

    folder_tags = defaultdict(list)
    file_tags = {}
    for fpath, folder, fname, top_tags in results:
        file_tags[fpath] = top_tags
        folder_tags[folder].append((fname, top_tags))

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
    main()
