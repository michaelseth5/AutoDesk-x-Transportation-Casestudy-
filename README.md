# LA 405 Integrated Rail + Bus Feeder Concept

An interactive 3D map (MapLibre GL JS + OpenFreeMap, no API key required) visualizing a
conceptual elevated/underground rail trunk along the I-405 corridor in Los Angeles, paired
with express bus feeder routes for last-mile access into surrounding neighborhoods. Built
as a transit case study — "rail for speed, buses for last-mile access" — ahead of the 2028
LA Olympics.

**Live demo:** _(add your Streamlit Community Cloud URL here after deploying — see below)_

## What's in this repo

| File | Purpose |
|---|---|
| `app.py` | Streamlit wrapper that embeds the map for public hosting |
| `la_405_3d_map.html` | The self-contained 3D map (HTML/CSS/JS in one file, no build step) |
| `requirements.txt` | Python dependencies for the Streamlit app |
| `generate_map.py` / `generate_schematic.py` | Companion scripts producing a 2D Folium map and a presentation schematic PNG (not required to run the Streamlit app) |
| `output/` | Generated outputs from the two scripts above |

## Run locally

Requires Python 3.9+.

```bash
pip install -r requirements.txt
streamlit run app.py
```

Streamlit will print a local URL (usually `http://localhost:8501`) — open it in your browser.

## Deploy to Streamlit Community Cloud (free)

### 1. Push this project to GitHub

Create an empty repository on [github.com](https://github.com/new) first (don't initialize it
with a README/license — this folder already has one), then from inside this project folder:

```bash
git init
git add .
git commit -m "Initial commit: LA 405 rail + bus feeder concept"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```

Replace `<your-username>/<your-repo-name>` with your actual GitHub username and the repo name
you created.

### 2. Deploy on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account
   (click "Continue with GitHub" and authorize Streamlit if prompted).
2. Click **"Create app"** → **"Deploy a public app from GitHub"**.
3. Select:
   - **Repository:** the repo you just pushed
   - **Branch:** `main`
   - **Main file path:** `app.py` (if the repo root isn't the project folder, use the path
     to `app.py` relative to the repo root, e.g. `la_405_transit/app.py`)
4. Double-check under "Advanced settings" (optional but worth confirming):
   - **Python version:** 3.11 (or any 3.9+ — this app has no version-specific dependencies)
5. Click **"Deploy"**.

Deployment typically takes **1-3 minutes** the first time (it installs `streamlit` from
`requirements.txt` and boots the app). You'll land on a build log page that auto-refreshes into
the live app when it's ready.

Your live URL will look like:

```
https://<your-app-name>-<random-id>.streamlit.app
```

or, if you claim a custom subdomain during setup:

```
https://<your-chosen-name>.streamlit.app
```

Once it's live, copy that URL into the **Live demo** line at the top of this README (edit,
commit, push — Streamlit Cloud auto-redeploys on every push to `main`).
