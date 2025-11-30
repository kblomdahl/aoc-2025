# Advent of Code 2025

Python solutions for the Advent of Code puzzles for 2025. No specific performance or time goal other then to have fun and enjoy the Christmas feelings.

## Setup

This project uses a [Nix flake](https://nixos.wiki/wiki/Flakes) to manage the development environment, providing `python` and `uv`.

```bash
nix develop
```

Or if you use `direnv`:

```bash
direnv allow
```

## Usage

```
uv run apps/01.py < fixtures/01.txt
```

## Tests

```
uv run pytest
```
