# GMADCH: H-Design Modularization Algorithm for Software Systems

## Overview

GMADCH is a modularization and benchmarking algorithm for software systems, especially those with incoherent or disconnected call graphs. It leverages Levenshtein-based vocabulary congruence ("H-design") to detect conceptual clusters, aiding maintainability, code comprehension, and architectural analysis.

## Features

- **Language-Agnostic**: Supports Python, Java, C/C++, JS, PHP, Go, Ruby, Rust, Kotlin, and more.
- **Multiprocessed**: Accelerates analysis on large codebases.
- **User Options**: Use either an automatically built dictionary (from all words in all files) or provide your own tag list.
- **Progress Bar**: Visual progress during analysis.
- **Keyword Filtering**: Filters programming keywords and stopwords for meaningful clustering.

## Usage

1. Run `python GMADCH.py` in your project root.
2. Select dictionary mode:
    - **Option 1**: Auto-detect tags from all code files.
    - **Option 2**: Enter your own tags/keywords as a comma-separated list (e.g., `ccxt, numpy, trading`).
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

## Theoretical Foundations

GMADCH uses Levenshtein string distance and vocabulary congruence to measure conceptual similarity, inspired by graph-theoretic and clustering approaches:

- For each word in a file:
    \[
    \text{score}(w) = \text{freq}(w) + \sum_{\substack{w' \in D\\w' \neq w}} \frac{\text{freq}(w')}{\text{Levenshtein}(w, w')}
    \]
    where $D$ is the dictionary (auto or user).

- Top tags are selected per file; files are grouped in folders by shared tags.

- Modularization quality is evaluated using metrics such as MoJo, MoJoFM, and $MQ = \frac{i}{i+j}$, where $i$ is the number of internal edges and $j$ the number of external edges.

See the academic article (`GMADCH.pdf`) for deeper theory, algorithms, and references.

## References

- Izadkhah, H., Elgedawy, I., & Isazadeh, A. (2016). E-CDGM: An Evolutionary Call-Dependency Graph Modularization Approach for Software Systems. *Cybernetics and Information Technologies*, 70-90.
- Pourasghar, B., Izadkhah, H., Isazadeh, A., & Lotf, S. (2020). A Graph-based Algorithm for Software Systems Modularization by Considering the Depth of Relationships.
- Levenshtein, V.I. (1966). Binary codes capable of correcting deletions, insertions, and reversals. *Soviet Physics Doklady*, 10(8), 707–710.
- Sokal, R.R., & Michener, C.D. (1958). A statistical method for evaluating systematic relationships. *University of Kansas Scientific Bulletin*.
- Gusfield, D. (1997). Algorithms on Strings, Trees and Sequences. *Cambridge University Press*.
- Ducasse, S., & Pollet, D. (2009). Software architecture reconstruction: A process-oriented taxonomy. *IEEE Transactions on Software Engineering*, 35(4), 573–591.
- Navarro, G. (2001). A guided tour to approximate string matching. *ACM Computing Surveys*, 33(1), 31–88.
- Andritsos, P., & Tzerpos, V. (2005). Information-theoretic software clustering. *IEEE Transactions on Software Engineering*, 31(2), 150–165.
- Cormen, T.H., Leiserson, C.E., & Rivest, R.L. (1990). Introduction to Algorithms. *MIT Press and McGraw-Hill*.
- Estivill-Castro, V. (2002). Why so many clustering algorithms. *ACM SIGKDD Explorations Newsletter*, 4(1), 65–75.
