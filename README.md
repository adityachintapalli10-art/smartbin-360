# SmartBin 360

A lightweight web app for monitoring smart waste bins, route optimization, AI demand forecasting, alerts, and IoT simulator controls.

## Run with Streamlit

```bash
pip install -r requirements.txt
streamlit run server.py
```

Open the local URL printed by Streamlit, usually http://localhost:8501.

## Deploy to Streamlit Community Cloud

Create an app from this repository and set **Main file path** to `server.py`. Streamlit Cloud installs `requirements.txt` and manages the web server itself; `server.py` embeds the dashboard and must not bind its own socket or port.

## Run as a static site

The original dashboard can also be served directly with Node.js:

```bash
npm start
```

Then open http://localhost:3000.

## Files

- `index.html` – complete app UI and JavaScript logic
- `server.py` – Streamlit entry point that embeds the dashboard
- `requirements.txt` – Streamlit dependency for local and cloud deployment
- `server.js` – optional Node.js static file server
- `package.json` – npm start scripts for the static server
