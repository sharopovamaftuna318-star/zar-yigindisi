# Zar yig'indisi laboratoriyasi

3 ta olti yoqli zar tashlanganda berilgan yig'indi (3–18) necha xil usulda tushishi va uning ehtimolligini tahlil qiluvchi loyiha.

**Jonli sahifa:** https://sharopovamaftuna318-star.github.io/zar-yigindisi/

## Imkoniyatlar

- Yig'indi kiritiladi (min 3, max 18) va quyidagilar hisoblanadi:
  - tartiblangan kombinatsiyalar soni va ehtimollik (kasr, o'nlik, foiz)
  - P(S ≤ s), P(S ≥ s) va imkoniyatlar nisbati (odds)
- Tartibsiz kombinatsiyalar va har birining o'rin almashtirishlari soni (masalan, 1+3+6 → 6 ta).
- Inklyuziya-ekskluziya formulasi: N(S) = Σ(−1)ᵏ·C(n,k)·C(S−6k−1, n−1)
- Kutilma E = 10.5, dispersiya D = 8.75, σ ≈ 2.958, moda va z-ball.
- Monte-Karlo simulyatsiyasi, 95% ishonch oralig'i va χ² testi.

## Fayllar

| Fayl | Vazifasi |
|------|----------|
| `index.html` | Interaktiv veb-interfeys (HTML + CSS + JS) |
| `main.py` | Terminal versiyasi (Python, faqat standart kutubxona) |

## Ishga tushirish

```
python main.py
```

Veb-versiya uchun `index.html` ni brauzerda oching yoki yuqoridagi jonli linkdan foydalaning.

## Misol: yig'indi 10

27 ta kombinatsiya, P = 27/216 = 1/8 = 12.50%

| Tartibsiz to'plam | O'rin almashtirishlar |
|---|---|
| 1 + 3 + 6 | 6 |
| 1 + 4 + 5 | 6 |
| 2 + 2 + 6 | 3 |
| 2 + 3 + 5 | 6 |
| 2 + 4 + 4 | 3 |
| 3 + 3 + 4 | 3 |
