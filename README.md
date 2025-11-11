# Simple AST Program Synthesizer

This repository provides a small framework for synthesizing arithmetic expressions over two variables (`x` and `y`) using a brute-force search over an abstract syntax tree (AST). It supports addition, subtraction, multiplication, division (integer), and “holes” for partial expressions.

## Features

- AST nodes: `VarX`, `VarY`, `BinOp`, `Hole`.
- Binary operations: `+`, `-`, `*`, `/`.
- Brute-force enumeration of all expressions up to a configurable depth.
- `matches_examples` function to test expressions against input-output examples.
- Partial expression support via `Hole` nodes.
- JSON-based example loading for automated testing.

## Installation

No external dependencies beyond the Python standard library. Requires Python 3.9+.

```bash
git clone <repo-url>
cd <repo>
```

## Running the Synthesizer

Use the main.py script with argparse:


```
python main.py examples.json --max-depth 4

examples.json: Path to your examples file.

--max-depth: Maximum expression depth to search (default: 4).
```

The program will enumerate expressions and print the first one that matches all examples. Failed attempts are printed for debugging.

## Using Holes

Partial expressions can use Hole() nodes. You can enumerate all ways to fill holes using `fill_holes_all`:

```
expr = Add(Hole(), VarY()) (This is how you have to define your hole expressions, there's no parser)
for candidate in fill_holes_all(expr, max_depth=2):
    if matches_examples(candidate, examples):
        print("Found matching expression:", candidate)

```
