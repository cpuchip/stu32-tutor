---
id: rpn-01
title: The stack and ENTER
status: vectors and keys only (prose waits for abacus's review of the shape)
setup: BLUE MODE 33s GOLD DISP FIX 4
display: FIX 4
---

# The stack and ENTER

Setup, once: press

```keys setup
BLUE MODE 33s GOLD DISP FIX 4
```

(The setup above is pressed before every example below; the checker prepends it.)

## Two numbers, one operation

```keys S01
7 ENTER 5 +
```

X shows <disp v="S01">12.0000</disp>.

```keys S02
7 ENTER 5 −
```

```keys S03
20 ENTER 8 ÷
```

X shows <disp v="S03">2.5000</disp>.

## ENTER copies

```keys S04
6 ENTER
```

```keys S05
6 ENTER ×
```

## Results keep going

```keys S06
3 ENTER 4 + 5 ×
```

```keys S07
2 ENTER 3 + 4 ENTER 6 +
```

```keys S08
2 ENTER 3 + 4 ENTER 6 + ×
```

## Moving the stack

```keys S09
5 ENTER 20 x↔y ÷
```

```keys S10
1 ENTER 2 ENTER 3 ENTER 4 R↓
```

## LAST x

```keys S11
12 ENTER 4 ÷ GOLD LASTx
```

```keys S12
12 ENTER 4 ÷ GOLD LASTx ×
```

## Negative numbers

```keys S13
5 +/− ENTER 3 −
```

X shows <disp v="S13">-8.0000</disp>.

## T copies down

```keys S14
1.05 ENTER ENTER ENTER × × ×
```

X shows <disp v="S14">1.2155</disp>.
