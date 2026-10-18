# SmartBin 360

A web app for monitoring smart waste bins, route optimization, analytics, telemetry, field tasks, and public reports. The Python Streamlit dashboard is the primary app; the original SmartBin 360 HTML dashboard remains available as a legacy option.

## Run the Python dashboard

```sh
python -m venv .venv
# Activate the environment, then:
pip install -r requirements.txt
streamlit run server.py
```

Open the local URL printed by Streamlit, usually http://localhost:8501. The dashboard supports live bin selection, fill/battery/gas simulation, bin registration, lock and clean actions, area filtering, GIS maps, route views, analytics, telemetry, staff tasks, and public reports.

## Deploy to Streamlit Community Cloud

Create an app from this repository and set **Main file path** to `server.py`. Streamlit Cloud installs `requirements.txt` and manages the web server itself.

## Run as a static site

The original SmartBin 360 dashboard can still be served directly with Node.js:

```bash
npm start
```

Then open http://localhost:3000.

## Files

- `server.py` – primary Python/Streamlit dashboard entry point
- `legacy_streamlit.py` – original Streamlit wrapper for `index.html`
- `requirements.txt` – Python dependencies
- `index.html` – original SmartBin 360 UI and JavaScript logic
- `server.js` – optional Node.js static file server
- `package.json` – npm start scripts for the static server
