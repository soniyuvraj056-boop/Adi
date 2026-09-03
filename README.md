# Adi — Your Personal Schedule & Reminder Website

A simple website to manage your schedule, important events, and notes —
supports multiple user accounts, each person only sees their own events.

---

## 1. Run it on your laptop (right now, 2 minutes)

**Step 1 — Install Flask** (only needed once):
```
pip install flask
```

**Step 2 — Run the app:**
```
python app.py
```

**Step 3 — Open it:**
Go to `http://127.0.0.1:5000` in your browser (Chrome/Edge). Register an account,
log in, and start adding events.

That's it — it's fully working on your laptop already.

---

## 2. Put it permanently online (so anyone, anywhere can use it)

Right now it only runs while your laptop is on and the script is running.
To make it a "real" website reachable 24/7 from any device, you deploy it to a
free hosting service. Easiest option: **Render.com**

### Steps:
1. Create a free account at https://render.com
2. Create a free account at https://github.com and upload this `adi` folder
   as a new repository (or ask me to walk you through this with Git).
3. In Render, click **New +** → **Web Service** → connect your GitHub repo.
4. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Click **Deploy**. Render gives you a live link like
   `https://adi-yourname.onrender.com` — this works on any phone or computer.

I've included a `requirements.txt` file below for this step.

**Note:** The free tier may "sleep" after inactivity and take ~30 seconds to
wake up on the next visit — that's normal for free hosting.

---

## 3. How to use Adi (quick reference — ask me anytime, too)

- **Register/Login** — each person creates their own username + password.
  Your events are private to your account.
- **+ New Event** — add a title, date, time (optional), and notes (optional).
- **Dashboard** — shows all your events, soonest first.
  - 🟡 Yellow highlight = due **today**
  - 🔴 Red highlight = **overdue**
- **Browser reminders** — the first time you open Adi, your browser will ask
  for notification permission. Say **Allow**. Then, any time you open the
  dashboard and something is due today, you'll get a popup reminder — even
  if you're doing something else on your laptop/phone at that moment (as
  long as the Adi tab is open).
- **Edit/Delete** — click the links under any event card.

If you ever forget how something works, just come back and ask me — I can
re-explain any part of this any time.
