"""bin-01's expectations, recomputed with Python's own integers and never with tools/judge.c (T65). check.py runs it
(python3 -I docs/evidence/bin-01.py) and requires its lines to be vectors.txt's: ID | expectation."""


def b(n):
    """n in base 2, as Python writes it."""
    return format(n, "b")


def two(s):
    return int(s, 2)


rows = [
    # BN1A: what comes after 1011 when you count in binary.
    ("BN1A", f"BASE=2:{b(two('1011') + 1)}"),
    ("BN1AA", "TEXT=1012"),                                   # slip: the last digit counted on as in tens
    ("BN1AB", f"BASE=2:{b(two('1011') - 1)}"),                # slip: counted down, not up
    # BN1B: 11010 in our ten symbols.
    ("BN1B", f"BASE=10:{two('11010')}"),
    ("BN1BA", f"BASE=10:{two('11010'[::-1])}"),               # slip: the places read from the left, 01011
    ("BN1BB", "BASE=10:11010"),                               # slip: the digits typed again as a number in tens
    # BN1C: 44 in binary.
    ("BN1C", f"BASE=2:{b(44)}"),
    ("BN1CA", f"BASE=2:{b(44)[::-1]}"),                       # slip: written smallest place first
    ("BN1CB", "BASE=2:" + "".join(b(int(d)) for d in "44")),  # slip: each digit of 44 on its own, 4 and 4
    # BN1D: 1011 + 111 in binary.
    ("BN1D", f"BASE=2:{b(two('1011') + two('111'))}"),
    ("BN1DA", f"BASE=2:{b(two('1011') ^ two('111'))}"),       # slip: every column added with no carry
    # BN1E: counting 0 to 7 in binary, the digits down the fours column, from 0 down.
    ("BN1E", "TEXT=" + "".join(str(n >> 2 & 1) for n in range(8))),
    ("BN1EA", "TEXT=" + "".join(str(n >> 1 & 1) for n in range(8))),   # slip: the twos column down the same count
]

# BN1F: one column of a sum, for each pair of digits a and b (rows 0 0, 0 1, 1 0, 1 1): the sum digit, then the carry.
pairs = [(a, c) for a in (0, 1) for c in (0, 1)]
rows.append(("BN1F", "GRID=" + ",".join(f"{(a + c) % 2},{(a + c) // 2}" for a, c in pairs)))
rows.append(("BN1FA", "GRID=" + ",".join(f"{a | c},{a & c}" for a, c in pairs)))          # slip: the sum digit 1 for 1 + 1
rows.append(("BN1FB", "GRID=" + ",".join(f"{(a + c) // 2},{(a + c) % 2}" for a, c in pairs)))  # slip: sum and carry swapped

for vid, exp in rows:
    print(f"{vid} | {exp}")
