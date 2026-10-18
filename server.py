import random

import pandas as pd
import streamlit as st


st.set_page_config(page_title="EcoBin AI | Smart Waste Dashboard", page_icon="♻️", layout="wide")

INITIAL_BINS = [
    {"id": "BIN-042", "name": "MBU Campus Quad", "area": "MBU Campus Zone", "lat": 13.6288, "lon": 79.4192, "fill": 92, "battery": 45, "odor": 185, "temp": 34, "waste": "Plastic & Wet Waste", "lock": "Locked", "worker": "Ramesh Kumar", "cleaned": "18 hrs ago"},
    {"id": "BIN-018", "name": "Central Bus Stand Gate 1", "area": "Tirupati Town", "lat": 13.6320, "lon": 79.4230, "fill": 68, "battery": 28, "odor": 110, "temp": 30, "waste": "Paper & Organic", "lock": "Unlocked", "worker": "Srinivas V.", "cleaned": "5 hrs ago"},
    {"id": "BIN-007", "name": "SV University Road", "area": "Tirupati Town", "lat": 13.6220, "lon": 79.4080, "fill": 24, "battery": 94, "odor": 35, "temp": 28, "waste": "Dry Trash", "lock": "Locked", "worker": "Unassigned", "cleaned": "1 hr ago"},
    {"id": "BIN-011", "name": "Railway Station Platform 1", "area": "Tirupati Town", "lat": 13.6260, "lon": 79.4150, "fill": 88, "battery": 80, "odor": 210, "temp": 33, "waste": "Food & Wet Waste", "lock": "Locked", "worker": "K. Venkatesh", "cleaned": "14 hrs ago"},
    {"id": "BIN-025", "name": "Alipiri Checkpoint", "area": "Alipiri Circle", "lat": 13.6500, "lon": 79.4000, "fill": 45, "battery": 88, "odor": 50, "temp": 27, "waste": "Plastic & Bottles", "lock": "Unlocked", "worker": "Unassigned", "cleaned": "3 hrs ago"},
    {"id": "BIN-033", "name": "Kapila Theertham Entrance", "area": "Alipiri Circle", "lat": 13.6420, "lon": 79.4100, "fill": 82, "battery": 72, "odor": 140, "temp": 31, "waste": "E-Waste & Metals", "lock": "Locked", "worker": "Anil Reddy", "cleaned": "12 hrs ago"},
]

TASKS = [
    {"Task": "TSK-101", "Bin": "BIN-042", "Area": "MBU Campus Quad", "Priority": "Urgent", "Status": "Assigned", "Worker": "Ramesh Kumar", "ETA": "15 mins"},
    {"Task": "TSK-102", "Bin": "BIN-011", "Area": "Railway Station", "Priority": "Urgent", "Status": "In-Progress", "Worker": "K. Venkatesh", "ETA": "8 mins"},
    {"Task": "TSK-103", "Bin": "BIN-033", "Area": "Kapila Theertham", "Priority": "High", "Status": "Pending", "Worker": "Anil Reddy", "ETA": "35 mins"},
    {"Task": "TSK-104", "Bin": "BIN-018", "Area": "Central Bus Stand", "Priority": "Medium", "Status": "Completed", "Worker": "Srinivas V.", "ETA": "Done"},
]

if "bins" not in st.session_state:
    st.session_state.bins = [dict(bin_data) for bin_data in INITIAL_BINS]
if "reports" not in st.session_state:
    st.session_state.reports = [
        {"Report": "CMP-801", "Bin": "BIN-042", "Issue": "Overflowing wet waste onto walkway", "Reported by": "Ananya S.", "Time": "25m ago", "Status": "In Review"},
        {"Report": "CMP-802", "Bin": "BIN-018", "Issue": "Odor issue near bus waiting bench", "Reported by": "Vikram R.", "Time": "1h ago", "Status": "Resolved"},
        {"Report": "CMP-803", "Bin": "BIN-011", "Issue": "Solar panel blocked by overhead banner", "Reported by": "Karthik M.", "Time": "3h ago", "Status": "Pending"},
    ]
if "toast" in st.session_state:
    st.toast(st.session_state.pop("toast"))

st.markdown(
    """
    <style>
    .stApp { background: #070b12; color: #e2e8f0; }
    [data-testid="stMetric"] { background: #0d1627; border: 1px solid #1e293b; padding: 14px; border-radius: 12px; }
    [data-testid="stSidebar"] { background: #0b1322; }
    h1, h2, h3 { color: #f1f5f9; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("♻️ EcoBin AI")
st.caption("SMART SOLAR WASTE DASHBOARD · ESP32 TELEMETRY GRID")

with st.sidebar:
    st.header("Control center")
    region = st.selectbox("Active region", ["All", "Tirupati Town", "MBU Campus Zone", "Alipiri Circle"])
    role = st.selectbox("Workspace role", ["Manager", "Worker", "Public"])
    st.divider()
    st.caption("IoT fleet grid")
    st.progress(1.0, text="100% online")
    if role == "Manager":
        with st.expander("Register a smart bin"):
            new_id = st.text_input("Bin serial code", placeholder="BIN-099")
            new_area = st.selectbox("Region / zone", ["MBU Campus Zone", "Tirupati Town", "Alipiri Circle"])
            if st.button("Pair & register", width="stretch"):
                bin_id = new_id.strip().upper() or f"BIN-{len(st.session_state.bins) + 15:03}"
                if any(item["id"] == bin_id for item in st.session_state.bins):
                    st.error(f"{bin_id} already exists.")
                else:
                    st.session_state.bins.append({
                        "id": bin_id, "name": f"{bin_id} ({new_area})", "area": new_area,
                        "lat": 13.629, "lon": 79.418, "fill": 10, "battery": 99, "odor": 18,
                        "temp": 27, "waste": "Dry & Recyclables", "lock": "Locked",
                        "worker": "Unassigned", "cleaned": "Just now",
                    })
                    st.session_state.toast = f"{bin_id} successfully paired."
                    st.rerun()

bins = st.session_state.bins
visible_bins = [item for item in bins if region == "All" or item["area"] == region]
if not visible_bins:
    st.info("No bins are registered in this region yet.")
    st.stop()

selected_id = st.selectbox("Focused bin", [item["id"] for item in visible_bins], label_visibility="collapsed")
selected = next(item for item in bins if item["id"] == selected_id)
alerts = sum(item["fill"] >= 80 for item in bins)
avg_fill = round(sum(item["fill"] for item in bins) / len(bins))
avg_battery = round(sum(item["battery"] for item in bins) / len(bins))

overview, map_tab, routes_tab, analytics_tab, telemetry_tab, tasks_tab, reports_tab = st.tabs(
    ["Overview", "GIS live map", "Collection routes", "Analytics & CO₂", "ESP32 telemetry", "Field staff tasks", "Public reports"]
)

with overview:
    metric_cols = st.columns(4)
    metric_cols[0].metric("Critical alerts (>80%)", f"{alerts} bins", delta="Action needed", delta_color="inverse")
    metric_cols[1].metric("Average capacity fill", f"{avg_fill}%", f"{len(bins)} connected bins")
    metric_cols[2].metric("Solar grid battery", f"{avg_battery}%", "Dual solar charging")
    metric_cols[3].metric("CO₂ saved this month", "890 kg", "AI route optimization")

    left, center, right = st.columns([1, 1.35, 1])
    with left:
        st.subheader("Monitored bins")
        st.dataframe(
            [{"Bin": b["id"], "Location": b["name"], "Fill": f'{b["fill"]}%', "Lock": b["lock"]} for b in visible_bins],
            hide_index=True,
            width="stretch",
        )
        st.subheader("Bin locations")
        st.map(pd.DataFrame([{"lat": b["lat"], "lon": b["lon"]} for b in visible_bins]), size=100)
    with center:
        st.subheader(f"Active bin · {selected['id']}")
        st.write(selected["name"], "·", selected["area"])
        st.progress(selected["fill"] / 100, text=f"Fill level · {selected['fill']}%")
        gauge_cols = st.columns(3)
        gauge_cols[0].metric("Battery", f'{selected["battery"]}%')
        gauge_cols[1].metric("Odor / gas", f'{selected["odor"]} PPM')
        gauge_cols[2].metric("Temperature", f'{selected["temp"]}°C')
        action_cols = st.columns(2)
        if action_cols[0].button("Mark as cleaned", width="stretch"):
            selected.update(fill=5, odor=15, cleaned="Just now")
            st.session_state.toast = f'{selected["id"]} marked as cleaned.'
            st.rerun()
        if action_cols[1].button(f'{selected["lock"]} · toggle lock', width="stretch"):
            selected["lock"] = "Unlocked" if selected["lock"] == "Locked" else "Locked"
            st.session_state.toast = f'{selected["id"]} lid is {selected["lock"].lower()}.'
            st.rerun()
        st.subheader("Live sensor simulator")
        selected["fill"] = st.slider("Fill level (%)", 0, 100, selected["fill"])
        selected["battery"] = st.slider("Battery (%)", 0, 100, selected["battery"])
        selected["odor"] = st.slider("Gas / odor (PPM)", 10, 300, selected["odor"])
        if st.button("Simulate sensor reading"):
            selected["fill"] = max(5, min(100, selected["fill"] + random.choice([-2, -1, 1, 2])))
            selected["odor"] = max(10, min(300, selected["odor"] + random.choice([-4, -2, 2, 4])))
            st.rerun()
    with right:
        st.subheader("AI overflow forecast")
        forecast = pd.DataFrame(
            {"Actual": [15, 35, 62, 78, selected["fill"], 95], "Predicted": [18, 38, 60, 75, 89, 94]},
            index=["06:00", "09:00", "12:00", "15:00", "18:00", "21:00"],
        )
        st.line_chart(forecast, y=["Actual", "Predicted"], color=["#f59e0b", "#34d399"])
        st.subheader("Staff roster")
        st.dataframe(pd.DataFrame(TASKS[:3])[["Worker", "Bin", "Status", "ETA"]], hide_index=True, width="stretch")
        if st.button("Send emergency dispatch", width="stretch"):
            st.toast("Dispatch alert sent to collection drivers.")

    with st.expander("Smart solar bin hardware showcase"):
        st.markdown(
            "**Solar lid:** 12V 20W monocrystalline · **Fill sensors:** dual HC-SR04 · "
            "**AI camera:** ESP32-CAM edge classifier · **Air quality:** MQ-135 · "
            "**Lid:** 12V electromagnetic lock · **Power:** LiFePO₄ battery"
        )

with map_tab:
    st.subheader("Municipal GIS mapping & GPS fleet grid")
    st.caption("Live fill-level status for registered bins in the selected area.")
    st.map(pd.DataFrame([{"lat": b["lat"], "lon": b["lon"], "fill": b["fill"]} for b in visible_bins]), size=150, color="#10b981")
    st.dataframe(pd.DataFrame(visible_bins)[["id", "name", "area", "fill", "battery", "odor", "waste", "lock"]], hide_index=True, width="stretch")

with routes_tab:
    st.subheader("AI dynamic route optimization")
    st.caption("Prioritizes bins at or above 80% capacity.")
    urgent_bins = sorted((b for b in bins if b["fill"] >= 50), key=lambda b: b["fill"], reverse=True)
    route_cols = st.columns(4)
    route_cols[0].metric("Priority bins", f"{alerts}")
    route_cols[1].metric("Route distance", "12.4 km", "3.8 km saved")
    route_cols[2].metric("Estimated fuel", "2.1 L")
    route_cols[3].metric("Collection time", "35 mins")
    if st.button("Recalculate optimal route"):
        st.toast("Optimized route generated · 3.8 km and 22 minutes saved.")
    st.dataframe(
        pd.DataFrame([{"Stop": i, "Bin": b["id"], "Location": b["name"], "Fill": f'{b["fill"]}%', "Waste": b["waste"], "ETA": f"{10 + i * 8} mins"} for i, b in enumerate(urgent_bins, 1)]),
        hide_index=True,
        width="stretch",
    )

with analytics_tab:
    st.subheader("Carbon reduction & waste analytics")
    chart_left, chart_right = st.columns(2)
    with chart_left:
        st.markdown("**AI material categorization**")
        st.bar_chart(pd.DataFrame({"Share (%)": [40, 30, 18, 12]}, index=["Organic & food", "Plastics", "Paper", "E-waste & glass"]), color="#10b981")
    with chart_right:
        st.markdown("**Monthly CO₂ emission reduction (kg)**")
        st.line_chart(pd.DataFrame({"CO₂ saved (kg)": [240, 310, 450, 520, 680, 890]}, index=["Jan", "Feb", "Mar", "Apr", "May", "Jun"]), color="#10b981")
    st.markdown("**Overflow history · weekly collections**")
    st.bar_chart(pd.DataFrame({"Overflow reports": [12, 8, 15, 19, 24, 31, 28], "Fuel saved (L)": [42, 50, 38, 30, 25, 18, 22]}, index=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]))

with telemetry_tab:
    st.subheader("IoT & ESP32 live telemetry")
    st.caption("Diagnostic readings from embedded microcontrollers, GSM modules, and solar charge controllers.")
    st.dataframe(
        pd.DataFrame([{
            "Bin": b["id"], "MCU": "ESP32-WROOM-32U", "Firmware": "v2.4.1-build8",
            "Battery": f'{b["battery"]}%', "Solar": "Active / Charging" if b["battery"] > 35 else "Obstructed",
            "Ultrasonic (mm)": round(200 - b["fill"] * 1.8), "Gas (PPM)": b["odor"],
            "Core temp (°C)": b["temp"], "Status": "ONLINE",
        } for b in visible_bins]),
        hide_index=True,
        width="stretch",
    )

with tasks_tab:
    st.subheader("Field worker task & schedule manager")
    st.dataframe(pd.DataFrame(TASKS), hide_index=True, width="stretch")
    task = st.selectbox("Task to complete", [item["Task"] for item in TASKS])
    if st.button("Complete selected task"):
        st.toast(f"Task {task} marked complete by {role}.")

with reports_tab:
    st.subheader("Community feedback & public reporting")
    st.caption("Submit a report about a damaged or overflowing smart bin.")
    with st.form("report_form", clear_on_submit=True):
        report_bin = st.selectbox("Nearest bin", [b["id"] for b in bins])
        report_issue = st.text_input("Complaint details", placeholder="Lid stuck or odor issue...")
        submitted = st.form_submit_button("Submit report")
    if submitted:
        if not report_issue.strip():
            st.error("Enter complaint details before submitting.")
        else:
            st.session_state.reports.insert(0, {
                "Report": f"CMP-{random.randint(100, 999)}", "Bin": report_bin,
                "Issue": report_issue.strip(), "Reported by": "You (Citizen)",
                "Time": "Just now", "Status": "Pending",
            })
            st.success("Report submitted. The municipal team has been alerted.")
    st.dataframe(pd.DataFrame(st.session_state.reports), hide_index=True, width="stretch")
