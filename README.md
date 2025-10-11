# GMADCH — H-Design Software Modularization Algorithm

## What is GMADCH?

GMADCH is an algorithm for benchmarking and modularizing software systems with incoherent or disconnected call graphs.  
It uses vocabulary congruence, Levenshtein (“H design”) scoring, and tag-based clustering to group code files by conceptual similarity.

## How does it work?

- You provide a dictionary of important keywords, tags, or libraries.
- The script scans all code files (any language) in your project.
- For each file, it calculates Levenshtein-based “H” scores for all words.
- It detects the top 3 conceptual tags for each file.
- It shows which files in each folder share similar top tags, increasing maintainability.

## Example Output

```
main.py -> ccxt, numpy, leven
utils.py -> ccxt, pandas, tasks
...
Folder1:
  Tag 'ccxt': main.py, utils.py
```

## How to use

1. Update the `user_dict` in GMADCH.py with your vocabulary/tags.
2. Run `python GMADCH.py` in your project root.
3. View the output for file-to-tag mapping and folder groupings.

## Reference

Based on GMADC (https://github.com/mablue/GMADC), improved with “H” design for even better maintainability and code understanding.