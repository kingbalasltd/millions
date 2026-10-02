"""Deterministic puzzle generators for the printable kits: word search, crossword, maze, sudoku, dot-to-dot shapes."""
import math
import random
import unicodedata


def plain(word):
    """Uppercase, strip accents and anything that is not a letter (for grids)."""
    w = unicodedata.normalize("NFD", word.upper())
    return "".join(c for c in w if "A" <= c <= "Z")


# ---------------------------------------------------------------- word search
DIRS_EASY = [(0, 1), (1, 0)]
DIRS_MEDIUM = [(0, 1), (1, 0), (1, 1)]
DIRS_HARD = [(0, 1), (1, 0), (1, 1), (-1, 1)]


def word_search(words, size=12, dirs=DIRS_MEDIUM, seed=1):
    """Return (grid, placements, placed_words). Words that cannot fit are skipped."""
    rnd = random.Random(seed)
    cleaned = []
    for w in words:
        p = plain(w)
        if 3 <= len(p) <= size and p not in [c[1] for c in cleaned]:
            cleaned.append((w, p))
    cleaned.sort(key=lambda t: -len(t[1]))
    grid = [[None] * size for _ in range(size)]
    placements = []
    for original, p in cleaned:
        options = []
        for r in range(size):
            for c in range(size):
                for dr, dc in dirs:
                    er, ec = r + dr * (len(p) - 1), c + dc * (len(p) - 1)
                    if not (0 <= er < size and 0 <= ec < size):
                        continue
                    ok, overlap = True, 0
                    for i, ch in enumerate(p):
                        g = grid[r + dr * i][c + dc * i]
                        if g is not None and g != ch:
                            ok = False
                            break
                        overlap += g == ch
                    if ok:
                        options.append((overlap, rnd.random(), r, c, dr, dc))
        if not options:
            continue
        options.sort(reverse=True)
        top = options[: max(1, len(options) // 6)]
        _, _, r, c, dr, dc = rnd.choice(top)
        for i, ch in enumerate(p):
            grid[r + dr * i][c + dc * i] = ch
        placements.append({"word": original, "plain": p, "r": r, "c": c, "dr": dr, "dc": dc})
    letters = "AAAEEEIIOOUURRSSTTNNLMCDPBGVFHJQ"
    for r in range(size):
        for c in range(size):
            if grid[r][c] is None:
                grid[r][c] = rnd.choice(letters)
    return grid, placements


# ---------------------------------------------------------------- crossword
def crossword(entries, seed=1, max_size=15):
    """Greedy crossword builder. entries: [{answer, clue}]. Returns dict or None."""
    rnd = random.Random(seed)
    items = []
    for e in entries:
        a = plain(e["answer"])
        if 2 < len(a) <= max_size and a not in [i["a"] for i in items]:
            items.append({"a": a, "clue": e["clue"], "orig": e["answer"]})
    items.sort(key=lambda i: -len(i["a"]))
    if not items:
        return None
    cells = {}
    placed = []

    def can_place(a, r, c, d):
        dr, dc = (0, 1) if d == "A" else (1, 0)
        br, bc = r - dr, c - dc
        ar, ac = r + dr * len(a), c + dc * len(a)
        if (br, bc) in cells or (ar, ac) in cells:
            return -1
        crossings = 0
        for i, ch in enumerate(a):
            rr, cc = r + dr * i, c + dc * i
            if (rr, cc) in cells:
                if cells[(rr, cc)] != ch:
                    return -1
                crossings += 1
            else:
                # no parallel neighbours
                n1 = (rr + dc, cc + dr)
                n2 = (rr - dc, cc - dr)
                if n1 in cells or n2 in cells:
                    return -1
        return crossings

    def bounds_ok(a, r, c, d):
        rs = [k[0] for k in cells] + [r, r + (len(a) - 1 if d == "D" else 0)]
        cs = [k[1] for k in cells] + [c, c + (len(a) - 1 if d == "A" else 0)]
        return max(rs) - min(rs) < max_size and max(cs) - min(cs) < max_size

    def put(item, r, c, d):
        dr, dc = (0, 1) if d == "A" else (1, 0)
        for i, ch in enumerate(item["a"]):
            cells[(r + dr * i, c + dc * i)] = ch
        placed.append({**item, "r": r, "c": c, "d": d})

    put(items[0], 0, 0, "A")
    pending = items[1:]
    for _ in range(3):
        rest = []
        for it in pending:
            best = None
            a = it["a"]
            for (pr, pc), ch in list(cells.items()):
                for i, ach in enumerate(a):
                    if ach != ch:
                        continue
                    for d in ("A", "D"):
                        r, c = (pr, pc - i) if d == "A" else (pr - i, pc)
                        score = can_place(a, r, c, d)
                        if score >= 1 and bounds_ok(a, r, c, d):
                            cand = (score, rnd.random(), r, c, d)
                            if best is None or cand > best:
                                best = cand
            if best:
                put(it, best[2], best[3], best[4])
            else:
                rest.append(it)
        pending = rest
        if not pending:
            break
    minr = min(k[0] for k in cells)
    minc = min(k[1] for k in cells)
    rows = max(k[0] for k in cells) - minr + 1
    cols = max(k[1] for k in cells) - minc + 1
    for p in placed:
        p["r"] -= minr
        p["c"] -= minc
    norm = {(r - minr, c - minc): ch for (r, c), ch in cells.items()}
    starts = sorted({(p["r"], p["c"]) for p in placed})
    numbers = {pos: i + 1 for i, pos in enumerate(starts)}
    across = sorted([(numbers[(p["r"], p["c"])], p) for p in placed if p["d"] == "A"], key=lambda t: t[0])
    down = sorted([(numbers[(p["r"], p["c"])], p) for p in placed if p["d"] == "D"], key=lambda t: t[0])
    return {"rows": rows, "cols": cols, "cells": norm, "numbers": numbers, "across": across, "down": down,
            "skipped": [i["orig"] for i in pending]}


# ---------------------------------------------------------------- maze
def maze(rows, cols, seed=1):
    """Recursive-backtracker maze. Returns walls dict and solution path (list of cells)."""
    rnd = random.Random(seed)
    walls = {(r, c): {"N": True, "S": True, "E": True, "W": True} for r in range(rows) for c in range(cols)}
    seen = {(0, 0)}
    stack = [(0, 0)]
    moves = {"N": (-1, 0, "S"), "S": (1, 0, "N"), "E": (0, 1, "W"), "W": (0, -1, "E")}
    while stack:
        r, c = stack[-1]
        opts = [(d, r + dr, c + dc, opp) for d, (dr, dc, opp) in moves.items()
                if 0 <= r + dr < rows and 0 <= c + dc < cols and (r + dr, c + dc) not in seen]
        if not opts:
            stack.pop()
            continue
        d, nr, nc, opp = rnd.choice(opts)
        walls[(r, c)][d] = False
        walls[(nr, nc)][opp] = False
        seen.add((nr, nc))
        stack.append((nr, nc))
    # solve with BFS
    start, goal = (0, 0), (rows - 1, cols - 1)
    prev = {start: None}
    q = [start]
    while q:
        cur = q.pop(0)
        if cur == goal:
            break
        r, c = cur
        for d, (dr, dc, _) in moves.items():
            if not walls[cur][d]:
                nxt = (r + dr, c + dc)
                if nxt not in prev:
                    prev[nxt] = cur
                    q.append(nxt)
    path, cur = [], goal
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    return walls, path[::-1]


# ---------------------------------------------------------------- sudoku (4x4, 6x6)
def _sudoku_solve_count(g, n, br, bc, limit=2):
    for i in range(n * n):
        r, c = divmod(i, n)
        if g[r][c] == 0:
            cnt = 0
            for v in range(1, n + 1):
                if all(g[r][k] != v for k in range(n)) and all(g[k][c] != v for k in range(n)):
                    r0, c0 = r - r % br, c - c % bc
                    if all(g[r0 + a][c0 + b] != v for a in range(br) for b in range(bc)):
                        g[r][c] = v
                        cnt += _sudoku_solve_count(g, n, br, bc, limit - cnt)
                        g[r][c] = 0
                        if cnt >= limit:
                            return cnt
            return cnt
    return 1


def sudoku(n=4, seed=1, holes=None):
    """n=4 (2x2 boxes) or n=6 (2x3 boxes). Returns (puzzle, solution)."""
    rnd = random.Random(seed)
    br, bc = (2, 2) if n == 4 else (2, 3)
    base = [[(bc * (r % br) + r // br + c) % n + 1 for c in range(n)] for r in range(n)]
    # shuffle values, rows within bands, cols within stacks
    perm = list(range(1, n + 1))
    rnd.shuffle(perm)
    sol = [[perm[v - 1] for v in row] for row in base]
    bands = [list(range(b * br, b * br + br)) for b in range(n // br)]
    rows = []
    rnd.shuffle(bands)
    for b in bands:
        rnd.shuffle(b)
        rows += b
    sol = [sol[r] for r in rows]
    puzzle = [row[:] for row in sol]
    cells = [(r, c) for r in range(n) for c in range(n)]
    rnd.shuffle(cells)
    target = holes if holes is not None else (8 if n == 4 else 18)
    removed = 0
    for r, c in cells:
        if removed >= target:
            break
        keep = puzzle[r][c]
        puzzle[r][c] = 0
        if _sudoku_solve_count([row[:] for row in puzzle], n, br, bc) != 1:
            puzzle[r][c] = keep
        else:
            removed += 1
    return puzzle, sol


# ---------------------------------------------------------------- dot-to-dot shapes (unit coordinates 0..1)
def shape_points(name, n=None):
    if name == "estrela":
        pts = []
        for i in range(10):
            ang = math.pi / 2 + i * math.pi / 5
            rad = 0.48 if i % 2 == 0 else 0.2
            pts.append((0.5 + rad * math.cos(ang), 0.5 + rad * math.sin(ang)))
        return pts
    if name == "arvore":
        return [(0.5, 0.95), (0.62, 0.78), (0.56, 0.78), (0.72, 0.58), (0.62, 0.58), (0.82, 0.36), (0.56, 0.36),
                (0.56, 0.2), (0.44, 0.2), (0.44, 0.36), (0.18, 0.36), (0.38, 0.58), (0.28, 0.58), (0.44, 0.78),
                (0.38, 0.78)]
    if name == "sino":
        pts = [(0.5, 0.92)]
        for i in range(1, 8):
            t = i / 8
            pts.append((0.5 + 0.12 + 0.24 * t ** 1.6, 0.92 - 0.72 * t))
        pts += [(0.5 + 0.06, 0.14), (0.5 - 0.06, 0.14)]
        for i in range(7, 0, -1):
            t = i / 8
            pts.append((0.5 - 0.12 - 0.24 * t ** 1.6, 0.92 - 0.72 * t))
        return pts
    if name == "presente":
        return [(0.2, 0.15), (0.8, 0.15), (0.8, 0.6), (0.85, 0.6), (0.85, 0.72), (0.62, 0.72), (0.72, 0.9),
                (0.56, 0.85), (0.5, 0.74), (0.44, 0.85), (0.28, 0.9), (0.38, 0.72), (0.15, 0.72), (0.15, 0.6),
                (0.2, 0.6)]
    if name == "coracao":
        pts = []
        for i in range(n or 18):
            t = 2 * math.pi * i / (n or 18)
            x = 16 * math.sin(t) ** 3
            y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
            pts.append((0.5 + x / 38, 0.52 + y / 38))
        return pts
    if name == "vela":
        return [(0.38, 0.12), (0.62, 0.12), (0.62, 0.62), (0.56, 0.62), (0.58, 0.72), (0.5, 0.9), (0.42, 0.72),
                (0.44, 0.62), (0.38, 0.62)]
    if name == "lua":
        pts = []
        for i in range(10):
            a = math.pi * (0.25 + 1.5 * i / 9)
            pts.append((0.5 + 0.4 * math.cos(a), 0.5 + 0.4 * math.sin(a)))
        for i in range(8, 0, -1):
            a = math.pi * (0.35 + 1.3 * i / 9)
            pts.append((0.62 + 0.3 * math.cos(a), 0.5 + 0.3 * math.sin(a)))
        return pts
    if name == "casa":
        return [(0.2, 0.15), (0.8, 0.15), (0.8, 0.55), (0.88, 0.55), (0.5, 0.88), (0.12, 0.55), (0.2, 0.55)]
    raise ValueError(name)


# ---------------------------------------------------------------- pixel art (color by number)
PIXEL_ART = {
    "Árvore de Natal": ("""
.......3........
......333.......
.......1........
......111.......
.....11211......
....1111111.....
.......1........
......1111......
.....112111.....
....111111211...
...1111111111...
.......44.......
.......44.......
......5555......
""", {"1": ("verde", "#2E8B57"), "2": ("vermelho", "#D62828"), "3": ("amarelo", "#F4C430"), "4": ("marrom", "#7B4A2A"),
      "5": ("vermelho", "#D62828")}),
    "Estrela": ("""
.......1.......
......111......
......111......
.....11111.....
111111111111111
.111112111111..
..11111111111..
...111111111...
...111111111...
..11111.11111..
..1111...1111..
.111.......111.
.1...........1.
""", {"1": ("amarelo", "#F4C430"), "2": ("laranja", "#F28C28")}),
    "Presente": ("""
....2.....2....
.....2...2.....
......222......
.1111112111111.
.1111112111111.
.3333332333333.
..11111211111..
..11111211111..
..11111211111..
..11111211111..
..11111211111..
..11111211111..
""", {"1": ("vermelho", "#D62828"), "2": ("amarelo", "#F4C430"), "3": ("verde", "#2E8B57")}),
    "Sol de Verão": ("""
.......3.......
..3....1....3..
...3..111..3...
.....11111.....
....1111111....
33.111111111.33
....1111111....
.....11111.....
...3..111..3...
..3....1....3..
.......3.......
""", {"1": ("amarelo", "#F4C430"), "3": ("laranja", "#F28C28")}),
    "Vela": ("""
.......2.......
......232......
......232......
.......2.......
......444......
.....11111.....
.....11111.....
.....11111.....
.....11111.....
.....11111.....
.....11111.....
...55555555....
""", {"1": ("vermelho", "#D62828"), "2": ("amarelo", "#F4C430"), "3": ("laranja", "#F28C28"), "4": ("preto", "#333333"),
      "5": ("verde", "#2E8B57")}),
    "Coração": ("""
..111...111..
.11111.11111.
1111111111111
1111211111111
1112111111111
.11111111111.
..111111111..
...1111111...
....11111....
.....111.....
......1......
""", {"1": ("vermelho", "#D62828"), "2": ("rosa", "#F4A6B7")}),
}


def pixel_grid(name):
    art, legend = PIXEL_ART[name]
    rows = [r for r in art.strip("\n").split("\n")]
    width = max(len(r) for r in rows)
    rows = [r.ljust(width, ".") for r in rows]
    return rows, legend
