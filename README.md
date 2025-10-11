# GMADCH: H-Design Modularization Algorithm

## Overview

GMADCH is an advanced algorithm for modularizing and benchmarking software systems, especially those with incoherent or disconnected call graphs. It uses Levenshtein-based vocabulary congruence ("H-design") to detect conceptual clusters, aiding maintainability, code understanding, and architecture analysis.

## Features

- **Language-Agnostic**: Supports most programming languages (Python, Java, C/C++, JS, PHP, Go, Ruby, Rust, Kotlin, etc.).
- **Multiprocessed**: Speeds up large codebases.
- **User Options**: Use either a global dictionary (all words in all files) or provide your own dictionary.
- **Progress Bar**: Visual feedback during analysis.
- **Keyword Filtering**: Filters out programming keywords and common stopwords for meaningful results.

## Usage

1. Run `python GMADCH.py` in your project root.
2. Choose dictionary mode:
    - Option 1: Auto-detect from all code files.
    - Option 2: Enter your own vocabulary/counts as a Python dict.
3. View output:
    - Per-file top tags.
    - Folder-level grouping of files by shared tags.

## Example Output

```
main.py -> trading, market, ccxt
utils.py -> ccxt, pandas, tasks

Folders and grouped files:

src:
  Tag 'ccxt': main.py, utils.py
```

## Theory

GMADCH leverages Levenshtein string distance and vocabulary congruence to measure conceptual similarity:

- For each file, word scores are calculated:
    - \[
      \text{score}(w) = \text{freq}(w) + \sum_{w' \neq w} \frac{\text{freq}(w')}{\text{Levenshtein}(w, w')}
      \]
    - Top tags are selected per file.
    - Files are grouped in folders by shared tags.

See the accompanying academic article (`GMADCH_v2_HDesign.tex`) for mathematical details and references.

## References

- Izadkhah, H., Elgedawy, I., & Isazadeh, A. (2016). E-CDGM: An Evolutionary Call-Dependency Graph Modularization Approach for Software Systems. *Cybernetics and Information Technologies*, 70-90.
- Pourasghar, B., Izadkhah, H., Isazadeh, A., & Lotf, S. (2020). A Graph-based Algorithm for Software Systems Modularization by Considering the Depth of Relationships.
- Levenshtein, V.I. (1966). Binary codes capable of correcting deletions, insertions, and reversals. *Soviet Physics Doklady*, 10(8), 707–710.
