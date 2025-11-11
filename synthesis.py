from __future__ import annotations
from itertools import product
import argparse
from dataclasses import dataclass
from typing import Dict, Protocol, List
import json


Env = Dict[str, int]

class Node(Protocol):
    def eval(self, env: Env) -> int: ...
    def __str__(self) -> str: ...

@dataclass(frozen=True)
class VarX:
    def eval(self, env: Env) -> int:
        return int(env['x'])
    def __str__(self) -> str:
        return "x"

@dataclass(frozen=True)
class VarY:
    def eval(self, env: Env) -> int:
        return int(env['y'])
    def __str__(self) -> str:
        return "y"

@dataclass(frozen=True)
class BinOp:
    op: str
    left: Node
    right: Node

    def eval(self, env: Env) -> int:
        a = self.left.eval(env)
        b = self.right.eval(env)
        if self.op == '+':
            return a + b
        if self.op == '-':
            return a - b
        if self.op == '*':
            return a * b
        if self.op == '/':
            if b == 0:
                raise ZeroDivisionError("division by zero")
            return int(a / b)
        raise ValueError(f"invalid operator {self.op}")

    def __str__(self) -> str:
        return f"({self.left} {self.op} {self.right})"

# Convenience constructors
def Add(l: Node, r: Node) -> BinOp: return BinOp('+', l, r)
def Sub(l: Node, r: Node) -> BinOp: return BinOp('-', l, r)
def Mul(l: Node, r: Node) -> BinOp: return BinOp('*', l, r)
def Div(l: Node, r: Node) -> BinOp: return BinOp('/', l, r)

# Example
# expr = Mul(Add(VarX(), VarY()), Sub(VarY(), VarX()))
# print(expr)                      # ((x + y) * (y - x))
# print(expr.eval({'x': 2, 'y': 5}))  # -> 21

def matches_examples(expr: Node, examples: List[Dict[str, int]]) -> bool:
    """
    Check if expr.eval(env) == out for all examples.
    Prints any mismatches.
    """
    ok = True
    for ex in examples:
        env = {'x': ex['x'], 'y': ex['y']}
        expected = ex['out']
        try:
            val = expr.eval(env)
        except ZeroDivisionError:
            # print(f"{expr} | env={env} -> ZeroDivisionError (expected {expected})")
            ok = False
            continue
        if val != expected:
            # print(f"{expr} | env={env} -> {val} (expected {expected})")
            ok = False
    return ok

def load_examples(path: str) -> List[Dict[str, int]]:
    """
    Load examples from a JSON file.
    Each example must have keys 'x', 'y', and 'out' (integers).
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("JSON root must be a list of examples")
    for i, ex in enumerate(data):
        if not all(k in ex for k in ('x', 'y', 'out')):
            raise ValueError(f"Example {i} missing keys: {ex}")
    return data


# Example:
# expr = Add(VarX(), VarY())
# examples = [{'x':1,'y':2,'out':3}, {'x':5,'y':7,'out':13}]
# matches_examples(expr, examples)

def all_exprs(max_depth: int) -> Iterator[Node]:
    """Generate all possible expressions up to max_depth."""
    if max_depth < 1:
        return
    # Depth 1: variables only
    if max_depth == 1:
        yield VarX()
        yield VarY()
        return

    # Generate smaller subexpressions recursively
    subexprs = [list(all_exprs(d)) for d in range(1, max_depth)]
    for left_depth in range(1, max_depth):
        for right_depth in range(1, max_depth):
            for left, right in product(subexprs[left_depth - 1], subexprs[right_depth - 1]):
                for op in ['+', '-', '*', '/']:
                    yield BinOp(op, left, right)

# Goal 3: What if you are provided with a special Hole class and a partial expression?
# If you want to give it a crack, uncomment below!
# @dataclass(frozen=True)
#class Hole:
    #"""Represents a placeholder in an expression that must be filled."""
#
    #def eval(self, env: dict) -> int:
        #raise RuntimeError("Cannot evaluate a Hole; it must be filled first.")
#
    #def __str__(self) -> str:
        #return "□"  # or any symbol to indicate a hole
#
# def fill_holes_all(expr: Node, max_depth: int) -> Iterator[Node]:


# Example: print all expressions up to depth 3
def main():
    parser = argparse.ArgumentParser(description="Search for an expression matching examples.")
    parser.add_argument("examples_file", help="Path to JSON file with examples")
    parser.add_argument("--max-depth", type=int, default=8, help="Maximum depth of expressions to search")
    args = parser.parse_args()

    examples = load_examples(args.examples_file)

    for depth in range(1, args.max_depth + 1):
        print(f"Searching expressions with depth {depth}...")
        counted = 0
        for expr in all_exprs(depth):
            counted += 1
            if matches_examples(expr, examples):
                print(f"Found matching expression: {expr}")
                return
        print(f"Explored {counted} candidates")
    print("No matching expression found.")

if __name__ == "__main__":
    main()
