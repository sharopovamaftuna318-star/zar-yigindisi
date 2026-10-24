"""
Uchta zar (3d6) yig'indisi bo'yicha kombinatorik va ehtimollik tahlili.

Imkoniyatlar:
  * barcha yig'indilar taqsimoti (min = n, max = 6n)
  * kiritilgan yig'indi uchun: tartiblangan kombinatsiyalar, ehtimollik (kasr, o'nlik, foiz)
  * tartibsiz (multitoplam) kombinatsiyalar va har birining o'rin almashtirishlari soni
  * inklyuziya-ekskluziya formulasi bilan analitik tekshiruv
  * kumulyativ ehtimolliklar P(S <= s), P(S >= s)
  * matematik kutilma, dispersiya, standart chetlanish
  * Monte-Karlo simulyatsiyasi bilan empirik tekshiruv
"""

import random
import sys
import webbrowser
from collections import Counter
from fractions import Fraction
from itertools import product, combinations_with_replacement
from math import comb, factorial, sqrt
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TOMONLAR = 6


def barcha_natijalar(n):
    """n ta zarning barcha tartiblangan natijalari (6^n ta)."""
    return list(product(range(1, TOMONLAR + 1), repeat=n))


def taqsimot(n):
    """Har bir yig'indi nechta tartiblangan kombinatsiyada uchrashi."""
    return Counter(sum(r) for r in barcha_natijalar(n))


def formula_bilan(n, s):
    """Inklyuziya-ekskluziya: N(s) = sum_k (-1)^k C(n,k) C(s-6k-1, n-1)."""
    jami = 0
    for k in range(n + 1):
        m = s - TOMONLAR * k - 1
        if m < n - 1:
            break
        jami += (-1) ** k * comb(n, k) * comb(m, n - 1)
    return jami


def orin_almashtirishlar(toplam):
    """Multitoplamning tartiblangan ko'rinishlari soni: n! / (a! b! ...)."""
    natija = factorial(len(toplam))
    for takror in Counter(toplam).values():
        natija //= factorial(takror)
    return natija


def statistikalar(n):
    kutilma = Fraction(7, 2) * n
    dispersiya = Fraction(35, 12) * n
    return kutilma, dispersiya, sqrt(dispersiya)


def jadval_chiqar(n, tq, jami):
    eng_kop = max(tq.values())
    print(f"\n{'=' * 72}")
    print(f"  {n} TA ZAR YIG'INDISI TAQSIMOTI  (jami natijalar: 6^{n} = {jami})")
    print(f"{'=' * 72}")
    print(f"  {'S':>3} | {'soni':>4} | {'P (kasr)':>10} | {'foiz':>7} | grafik")
    print(f"  {'-' * 3}-+-{'-' * 4}-+-{'-' * 10}-+-{'-' * 7}-+-{'-' * 30}")
    for s in range(n, TOMONLAR * n + 1):
        soni = tq[s]
        ustun = "█" * round(soni / eng_kop * 30)
        print(f"  {s:>3} | {soni:>4} | {f'{soni}/{jami}':>10} | {soni / jami:>7.2%} | {ustun}")


def yigindi_tahlili(n, s, tq, jami):
    soni = tq[s]
    p = Fraction(soni, jami)
    kichik_teng = sum(tq[k] for k in range(n, s + 1))
    katta_teng = sum(tq[k] for k in range(s, TOMONLAR * n + 1))
    simmetrik = (TOMONLAR + 1) * n - s

    print(f"\n{'─' * 72}")
    print(f"  YIG'INDI = {s} TAHLILI ({n} ta zar)")
    print(f"{'─' * 72}")
    print(f"  Tartiblangan kombinatsiyalar soni : {soni}")
    print(f"  Formula bo'yicha tekshiruv        : {formula_bilan(n, s)}")
    print(f"  Ehtimollik                        : {soni}/{jami} = {p} = {float(p):.4f} ({float(p):.2%})")
    if soni:
        print(f"  Imkoniyatlar nisbati (odds)       : 1 : {(jami - soni) / soni:.2f}")
    print(f"  {f'P(S <= {s})':<34}: {kichik_teng}/{jami} = {kichik_teng / jami:.2%}")
    print(f"  {f'P(S >= {s})':<34}: {katta_teng}/{jami} = {katta_teng / jami:.2%}")
    print(f"  Simmetrik yig'indi (7n - S)       : {simmetrik}  (u ham {tq[simmetrik]} ta kombinatsiya)")

    print("\n  Formula qadamlari: N(S) = Σ (-1)^k · C(n,k) · C(S-6k-1, n-1)")
    for k in range(n + 1):
        m = s - TOMONLAR * k - 1
        if m < n - 1:
            break
        had = (-1) ** k * comb(n, k) * comb(m, n - 1)
        print(f"    k={k}: {'+' if had >= 0 else '-'} C({n},{k})·C({m},{n - 1}) = {had:+d}")

    toplamlar = [t for t in combinations_with_replacement(range(1, TOMONLAR + 1), n) if sum(t) == s]
    print(f"\n  Tartibsiz kombinatsiyalar (multitoplamlar): {len(toplamlar)} ta")
    for t in toplamlar:
        ko = orin_almashtirishlar(t)
        print(f"    {' + '.join(map(str, t))} = {s}   ->  {ko} ta o'rin almashtirish")
    print(f"    Jami: {' + '.join(str(orin_almashtirishlar(t)) for t in toplamlar)} = {soni}")

    print("\n  Barcha tartiblangan kombinatsiyalar:")
    tartibli = [r for r in barcha_natijalar(n) if sum(r) == s]
    for i, r in enumerate(tartibli, 1):
        print(f"    {i:>3}-imkoniyat: {r}")


def simulyatsiya(n, s, tq, jami, tajriba=100_000):
    tushdi = sum(
        1 for _ in range(tajriba)
        if sum(random.randint(1, TOMONLAR) for _ in range(n)) == s
    )
    nazariy = tq[s] / jami
    print(f"\n  Monte-Karlo simulyatsiyasi ({tajriba:,} ta tashlash):")
    print(f"    Empirik  : {tushdi / tajriba:.4%}")
    print(f"    Nazariy  : {nazariy:.4%}")
    print(f"    Farq     : {abs(tushdi / tajriba - nazariy):.4%}")


def main():
    n = 3
    tq = taqsimot(n)
    jami = TOMONLAR ** n
    kichik, katta = n, TOMONLAR * n

    jadval_chiqar(n, tq, jami)
    kutilma, dispersiya, sigma = statistikalar(n)
    print(f"\n  E[S] = {float(kutilma)}   D[S] = {dispersiya} = {float(dispersiya):.2f}   σ = {sigma:.3f}")
    print(f"  Eng ehtimolli yig'indilar: "
          f"{', '.join(str(s) for s in tq if tq[s] == max(tq.values()))}")

    while True:
        kirish = input(f"\nYig'indini kiriting ({kichik}-{katta}), 'html' - interfeys, 'q' - chiqish: ").strip().lstrip("﻿")
        if kirish.lower() in ("q", "quit", "exit"):
            break
        if kirish.lower() == "html":
            webbrowser.open((Path(__file__).parent / "index.html").resolve().as_uri())
            continue
        try:
            s = int(kirish)
        except ValueError:
            print("  Xato: butun son kiriting.")
            continue
        if not kichik <= s <= katta:
            print(f"  Xato: {n} ta zar yig'indisi {kichik} dan {katta} gacha bo'ladi. "
                  f"Ehtimollik P({s}) = 0.")
            continue
        yigindi_tahlili(n, s, tq, jami)
        simulyatsiya(n, s, tq, jami)


if __name__ == "__main__":
    main()
