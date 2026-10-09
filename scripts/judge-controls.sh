#!/usr/bin/env bash
# judge-controls.sh CORE_DIR: proves tools/judge_check.py can fail. Each mutant of tools/judge.c is
# built into build/judge_test in place of the real one, and judge_check.py must fail on it; the real
# judge is rebuilt at the end and must pass.
set -u
core="$1"
cc="cc -std=c11 -O2 -Wall -Wextra -Werror"
mkdir -p build/judge-mutants
red=0
total=0
plant() {   # name, sed expression applied to judge.c
    total=$((total + 1))
    sed "$2" tools/judge.c > build/judge-mutants/judge.c
    if cmp -s tools/judge.c build/judge-mutants/judge.c; then
        echo "FAIL $1: the mutant did not apply"
        return
    fi
    rm -f build/judge_test
    if ! $cc -Itools -o build/judge_test tools/judge_test.c build/judge-mutants/judge.c 2> build/judge-mutants/cc.txt; then
        echo "FAIL $1: the mutant did not build (a build failure is not a result)"
        return
    fi
    if python3 tools/judge_check.py --core "$core" > build/judge-mutants/out.txt 2>&1; then
        echo "FAIL $1: judge_check passed a judge with this fault"
    else
        echo "ok   $1"
        red=$((red + 1))
    fi
}
plant "a judge that calls every answer right" 's/    return same(&a, &b);/    return same(\&a, \&b) || 1;/'
plant "a tolerance whose edge is excluded" 's/return cmp_mag(&d, &t) <= 0;/return cmp_mag(\&d, \&t) < 0;/'
plant "trailing zeros counted as digits" 's/    while (nb > 0 \&\& buf\[nb - 1\] == 0) {    \/\* trailing zeros into the exponent \*\//    while (0) {/'
$cc -o build/judge_test tools/judge_test.c tools/judge.c
python3 tools/judge_check.py --core "$core" > /dev/null || { echo "FAIL the real judge does not pass"; exit 1; }
echo "$red/$total judge controls red as planted"
[ "$red" -eq "$total" ]
