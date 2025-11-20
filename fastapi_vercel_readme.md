# FastAPI on Vercel — Instant Deploy Template

Ovaj projekat predstavlja minimalan FastAPI template spreman za **trenutni deploy na Vercel**.

## 📁 Struktura projekta
```
project-root/
│
├── API/
│   └── main.py
│
├── requirements.txt
│
└── vercel.json
```

---

## 🧩 1. `API/main.py`
Minimalna FastAPI aplikacija sa health-check endpointom.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "Health check is successful"}
```

---

## 📦 2. `requirements.txt`

```
fastapi
uvicorn
```

---

## ⚙️ 3. `vercel.json`
Ovo govori Vercelu kako da build-uje Python FastAPI aplikaciju.

```json
{
  "builds": [
    {
      "src": "API/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "API/main.py"
    }
  ]
}
```

---

# 🚀 Deploy uputstvo

## 1. Instaliraj Node.js (ako već nemaš)
Node je potreban zbog Vercel CLI.

https://nodejs.org

---

## 2. Instaliraj Vercel CLI

```bash
npm install -g vercel
```

---

## 3. Uloguj se u Vercel

```bash
vercel login
```

Potvrdi email ili GitHub prijavu.

---

## 4. Deploy projekta
U root folderu projekta pokreni:

```bash
vercel .
```

Odgovori na pitanja:
- Create a new project? → **Yes**
- Project name → pritisni Enter
- Which directory is your code in? → **.**

Vercel će automatski deploy-ovati aplikaciju.

---

## 🛠 Ako se pojavi greška (trenutni Vercel bug)
U slučaju da aplikacija ne radi odmah:

1. Idi na Vercel Dashboard → **Settings** projekta
2. Nađi sekciju **Node.js Version**
3. Promeni na **18.x**
4. Sačuvaj
5. Ponovo deploy:

```bash
vercel .
```

---

# ✔️ Gotov deploy
Posle build-a dobićeš URL poput:
```
https://tvoj-projekat.vercel.app
```

Otvaranjem rute `/` dobijaš:
```
{"status": "Health check is successful"}
```

Aplikacija je sada javno dostupna i besplatno hostovana.

---

# 🎯 Šta dalje?
- Dodaj nove rute u `main.py`
- Poveži frontend (React, Next.js, Vue...)
- Proširi API sa bazom ili autentifikacijom

Ako želiš, mogu dodati i **automatski GitHub deploy**, **napredniju strukturu projekta**, ili **detaljniji vodič**.

