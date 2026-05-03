import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

st.set_page_config(
    page_title="Pakistan Solar Assessment Tool",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide Streamlit chrome
st.markdown("""
<style>
#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none !important; }
.block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
section[data-testid="stMain"] > div { padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── DATA FOR INJECTION ───────────────────────────────────────────────────────
CITY_SUN = {
    "Karachi": 5.5, "Lahore": 5.0, "Islamabad": 4.8, "Peshawar": 5.2,
    "Quetta": 6.0,  "Multan": 5.8, "Faisalabad": 5.1, "Hyderabad": 5.6,
    "Sialkot": 4.9, "Rawalpindi": 4.8
}
CITIES_OPTS = "".join([f'<option value="{k}" {"selected" if k=="Lahore" else ""}>{k}</option>' for k in CITY_SUN.keys()])

tips = [
    "Replace old bulbs with LED lights",
    "Use inverter AC for cooling",
    "Improve home insulation",
    "Unplug appliances when not in use",
    "Use natural ventilation in evenings",
]
tips_html = "".join(f"""<div class="fz_tip-row">
  <div class="fz_tip-left"><span class="fz_tip-check">✔</span><span>{t}</span></div>
  <div class="fz_tip-badge">✓</div>
</div>""" for t in tips)

# ── FULL DASHBOARD HTML ───────────────────────────────────────────────────────
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Plus Jakarta Sans',sans-serif;background:#F0F4F0;color:#1a2e1a}}
.fz_hdr{{background:#fff;border-bottom:3px solid #1e5631;padding:25px 20px;display:flex;align-items:center;gap:14px}}
.fz_hdr-logo{{font-size:36px;line-height:1;flex-shrink:0}}
.fz_hdr-title{{font-size:19px;font-weight:800;color:#1e5631;line-height:1.2}}
.fz_hdr-sub{{font-size:11.5px;color:#6b7280;margin-top:2px}}
.fz_main{{display:grid;grid-template-columns:1fr 1fr;gap:16px;padding:40px 20px}}
.fz_card{{background:#fff;border-radius:12px;border:1px solid #d1dbd1;overflow:hidden;box-shadow:0 1px 6px rgba(0,0,0,.06)}}
.fz_card-head{{background:#1e5631;color:#fff;padding:10px 18px;font-size:14px;font-weight:700;display:flex;align-items:center;gap:8px}}
.fz_card-body{{padding:16px 18px}}
.fz_profile-row{{display:flex;justify-content:space-between;align-items:center;padding:9px 0;border-bottom:1px solid #e8ede8;font-size:13.5px;flex-wrap:wrap;gap:8px}}
.fz_profile-row:last-child{{border-bottom:none}}
.fz_profile-label{{color:#4b5563;font-weight:500;flex:1;min-width:150px}}

/* Styled Inputs */
.fz_profile-input{{background:#f3f7f3;border:1px solid #d1dbd1;border-radius:6px;padding:5px 10px;font-weight:700;color:#1a2e1a;font-size:13px;font-family:inherit;text-align:center;width:120px}}
.fz_profile-val-static{{background:#EAF3DE;border:1px solid #27500A;border-radius:6px;padding:5px 14px;font-weight:700;color:#1e5631;font-size:13px}}

.fz_sun-strip{{background:#EAF3DE;border-left:4px solid #1e5631;border-radius:0 7px 7px 0;padding:9px 14px;font-size:13px;color:#27500A;font-weight:600;margin:12px 0 4px}}
.fz_tip-row{{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #e8ede8;font-size:13.5px;flex-wrap:wrap;gap:8px}}
.fz_tip-row:last-child{{border-bottom:none}}
.fz_tip-left{{display:flex;align-items:center;gap:9px;flex:1;min-width:0}}
.fz_tip-check{{color:#1e5631;font-size:15px;font-weight:800;flex-shrink:0}}
.fz_tip-badge{{width:22px;height:22px;border-radius:50%;background:#1e5631;color:#fff;font-size:12px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0}}
.fz_solar-inner{{display:flex;align-items:center;gap:18px;padding:18px;flex-wrap:wrap}}
.fz_solar-emoji{{font-size:62px;line-height:1;flex-shrink:0}}
.fz_solar-row{{display:flex;align-items:baseline;gap:6px;margin-bottom:7px;font-size:14px;color:#4b5563}}
.fz_solar-row strong{{font-size:16px;font-weight:800;color:#1a2e1a}}
.fz_solar-sub{{font-size:12px;color:#6b7280;margin-top:4px}}
.fz_btn-details{{background:#1e5631;color:#fff;border:none;border-radius:7px;padding:8px 18px;font-size:13px;font-weight:700;cursor:pointer;font-family:'Plus Jakarta Sans',sans-serif;margin:4px 18px 14px auto;display:flex;align-items:center;gap:6px}}
.fz_detail-panel{{display:none;background:#f3f7f3;border-radius:8px;padding:14px 16px;margin:0 18px 14px;font-size:13px;border:1px solid #d1dbd1}}
.fz_detail-panel.fz_show{{display:block}}
.fz_detail-row{{display:flex;justify-content:space-between;border-bottom:1px solid #e8ede8;padding:5px 0;flex-wrap:wrap;gap:8px}}
.fz_detail-row:last-child{{border-bottom:none}}
.fz_dk{{color:#4b5563}}.fz_dv{{font-weight:700;color:#1a2e1a}}
.fz_fin-grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.fz_fin-card{{border-radius:9px;padding:13px 15px;border:1px solid #d1dbd1}}
.fz_fin-card.fz_yellow{{background:#fffbeb;border-color:#d97706}}
.fz_fin-card.fz_white{{background:#f9fafb}}
.fz_fin-label{{font-size:11.5px;color:#6b7280;font-weight:600;margin-bottom:3px}}
.fz_fin-val{{font-size:18px;font-weight:800;color:#1a2e1a;margin-top:2px}}
.fz_fin-sub{{font-size:11px;color:#9ca3af;margin-top:3px}}
.fz_rcol{{display:flex;flex-direction:column;gap:16px}}
.fz_report-desc{{font-size:13px;color:#4b5563;line-height:1.6;margin-bottom:14px}}
.fz_btn-report{{width:100%;background:#1a3a5c;color:#fff;border:none;border-radius:8px;padding:11px;font-size:14px;font-weight:700;cursor:pointer;font-family:'Plus Jakarta Sans',sans-serif;display:flex;align-items:center;justify-content:center;gap:8px}}
.fz_report-output{{display:none;background:#fff;border:1px solid #d1dbd1;border-radius:8px;padding:16px;margin-top:12px;font-family:'Courier New',monospace;font-size:16px;white-space:pre-wrap;color:#1a2e1a;line-height:1.6;max-height:280px;overflow-y:auto}}
.fz_report-output.fz_show{{display:block}}
.fz_bot{{display:flex;gap:14px;padding:4px 20px 20px;flex-wrap:wrap}}
.fz_btn-audit{{background:#d97706;color:#fff;border:none;border-radius:9px;padding:13px 26px;font-size:14px;font-weight:700;cursor:pointer;font-family:'Plus Jakarta Sans',sans-serif;display:flex;align-items:center;gap:8px;box-shadow:0 3px 10px rgba(217,119,6,.3)}}
.fz_btn-green{{background:#1e5631;color:#fff;border:none;border-radius:9px;padding:13px 26px;font-size:14px;font-weight:700;cursor:pointer;font-family:'Plus Jakarta Sans',sans-serif;display:flex;align-items:center;gap:8px;box-shadow:0 3px 10px rgba(30,86,49,.3)}}
.fz_ftr{{text-align:center;font-size:11px;color:#9ca3af;padding:14px 20px;border-top:1px solid #d1dbd1;margin-top:4px}}

/* ─── MEDIA QUERIES FOR MOBILE RESPONSIVENESS ─── */
@media (max-width:768px){{
  .fz_hdr{{padding:20px 15px;gap:10px}}
  .fz_hdr-logo{{font-size:28px}}
  .fz_hdr-title{{font-size:16px}}
  .fz_hdr-sub{{font-size:10px}}
  .fz_main{{grid-template-columns:1fr;gap:12px;padding:20px 15px}}
  .fz_card-head{{padding:8px 14px;font-size:13px}}
  .fz_card-body{{padding:14px 14px}}
  .fz_profile-input{{width:100px;font-size:12px}}
  .fz_profile-row{{font-size:12.5px}}
  .fz_profile-label{{font-size:12.5px;min-width:130px}}
  .fz_sun-strip{{font-size:12px;padding:8px 12px}}
  .fz_tip-row{{font-size:12.5px;padding:8px 0}}
  .fz_solar-inner{{gap:12px;padding:14px}}
  .fz_solar-emoji{{font-size:48px}}
  .fz_solar-row{{font-size:13px}}
  .fz_solar-row strong{{font-size:15px}}
  .fz_solar-sub{{font-size:11px}}
  .fz_btn-details{{padding:6px 14px;font-size:12px;margin:4px 14px 12px auto}}
  .fz_detail-panel{{padding:12px 14px;margin:0 14px 12px;font-size:12px}}
  .fz_detail-row{{padding:4px 0}}
  .fz_fin-grid{{gap:8px}}
  .fz_fin-card{{padding:11px 13px}}
  .fz_fin-label{{font-size:10.5px}}
  .fz_fin-val{{font-size:16px}}
  .fz_fin-sub{{font-size:10px}}
  .fz_report-desc{{font-size:12px}}
  .fz_btn-report{{padding:9px;font-size:13px}}
  .fz_btn-audit{{padding:10px 16px;font-size:13px}}
  .fz_btn-green{{padding:10px 16px;font-size:13px}}
}}

@media (max-width:480px){{
  body{{font-size:14px}}
  .fz_hdr{{padding:15px 10px;gap:8px;flex-wrap:wrap}}
  .fz_hdr-logo{{font-size:24px}}
  .fz_hdr-title{{font-size:14px;line-height:1.1}}
  .fz_hdr-sub{{font-size:9px}}
  .fz_main{{grid-template-columns:1fr;gap:10px;padding:15px 10px}}
  .fz_card{{border-radius:8px}}
  .fz_card-head{{padding:7px 12px;font-size:12px}}
  .fz_card-body{{padding:12px 12px}}
  .fz_profile-row{{display:grid;grid-template-columns:1fr;justify-items:stretch;align-items:flex-start;gap:5px;padding:7px 0}}
  .fz_profile-label{{font-size:11.5px}}
  .fz_profile-input{{width:100%;text-align:left;font-size:11px}}
  .fz_profile-val-static{{width:100%;font-size:12px;padding:4px 10px}}
  .fz_sun-strip{{font-size:11px;padding:7px 10px;margin:8px 0 2px}}
  .fz_tip-row{{display:grid;grid-template-columns:1fr;gap:5px;padding:7px 0;font-size:12px}}
  .fz_tip-left{{gap:6px}}
  .fz_tip-badge{{width:20px;height:20px;font-size:11px}}
  .fz_solar-inner{{gap:10px;padding:12px;display:flex;flex-direction:column;align-items:flex-start}}
  .fz_solar-emoji{{font-size:40px}}
  .fz_solar-row{{font-size:12px;margin-bottom:5px}}
  .fz_solar-row strong{{font-size:13px}}
  .fz_solar-sub{{font-size:10px;margin-top:3px}}
  .fz_btn-details{{padding:6px 12px;font-size:11px;margin:3px 12px 10px auto}}
  .fz_detail-panel{{padding:10px 12px;margin:0 12px 10px;font-size:11px}}
  .fz_detail-row{{flex-direction:column;gap:3px;padding:3px 0}}
  .fz_dk{{font-size:11px}}
  .fz_dv{{font-size:11px}}
  .fz_fin-grid{{grid-template-columns:1fr;gap:7px}}
  .fz_fin-card{{padding:10px 12px;border-radius:7px}}
  .fz_fin-label{{font-size:10px;margin-bottom:2px}}
  .fz_fin-val{{font-size:14px}}
  .fz_fin-sub{{font-size:9px}}
  .fz_report-desc{{font-size:11px}}
  .fz_btn-report{{padding:8px;font-size:12px;gap:5px}}
  .fz_btn-audit{{padding:9px 14px;font-size:12px}}
  .fz_btn-green{{padding:9px 14px;font-size:12px}}
  .fz_ftr{{font-size:9px;padding:10px 10px}}
}}


</style>
</head>
<body onload="calculate()">

<div class="fz_hdr">
  <div class="fz_hdr-logo">🌞</div>
  <div>
    <div class="fz_hdr-title">Pakistan-Focused Solar &amp; Energy Efficiency Assessment Tool</div>
    <div class="fz_hdr-sub">Empowering Pakistani households with solar insights &amp; energy savings</div>
  </div>
</div>

<div class="fz_main">

  <!-- Energy Profile -->
  <div class="fz_card">
    <div class="fz_card-head">⚡ Your Energy Profile</div>
    <div class="fz_card-body">
      <div class="fz_profile-row">
        <span class="fz_profile-label">Monthly Bill / بل (PKR)</span>
        <input type="number" id="in_bill" class="fz_profile-input" value="7500" step="500" oninput="calculate()">
      </div>
      <div class="fz_profile-row">
        <span class="fz_profile-label">Location / مقام</span>
        <select id="in_loc" class="fz_profile-input" onchange="calculate()">
          {CITIES_OPTS}
        </select>
      </div>
      <div class="fz_profile-row">
        <span class="fz_profile-label">Roof Area / چھت (sq. ft.)</span>
        <input type="number" id="in_roof" class="fz_profile-input" value="200" oninput="calculate()">
      </div>
      <div class="fz_profile-row">
        <span class="fz_profile-label">Est. Monthly Units</span>
        <span class="fz_profile-val-static" id="out_units">0 kWh</span>
      </div>
      <div class="fz_sun-strip" id="out_sun_msg">☀️ Location receives ~5.0 peak sun hours/day</div>
    </div>
  </div>

  <!-- Efficiency Tips -->
  <div class="fz_card">
    <div class="fz_card-head">💡 Efficiency Tips / توانائی کی بچت</div>
    <div class="fz_card-body">{tips_html}</div>
  </div>

  <!-- Solar Recommendation -->
  <div class="fz_card">
    <div class="fz_card-head">☀️ Solar System Recommendation / شمسی نظام</div>
    <div class="fz_solar-inner">
      <div class="fz_solar-emoji">🌞🏡</div>
      <div>
        <div class="fz_solar-row">Recommended Size: <strong id="out_size">0 kW</strong></div>
        <div class="fz_solar-row">Estimated Units Offset: <strong id="out_offset">0 kWh/mo</strong></div>
        <div class="fz_solar-row">Estimated Savings: <strong id="out_ann_sav">PKR 0/Year</strong></div>
        <div class="fz_solar-sub" id="out_solar_sub">☀️ Peak Sun Hours: 0 hrs/day | ~0 panels</div>
        <div class="fz_solar-sub" style="margin-top:3px" id="out_co2">🌿 CO2 offset/year: ~0 kg</div>
      </div>
    </div>
    <div style="display:flex;justify-content:flex-end">
      <button class="fz_btn-details" onclick="toggleDetail()">🔍 See Details / مزید جانیں</button>
    </div>
    <div class="fz_detail-panel" id="detailPanel">
      <div class="fz_detail-row"><span class="fz_dk">Panels required (400W each)</span><span class="fz_dv" id="det_panels">0</span></div>
      <div class="fz_detail-row"><span class="fz_dk">Roof space needed</span><span class="fz_dv" id="det_roof">0 sq. ft.</span></div>
      <div class="fz_detail-row"><span class="fz_dk">Daily generation</span><span class="fz_dv" id="det_daily">0 kWh/day</span></div>
      <div class="fz_detail-row"><span class="fz_dk">Monthly generation</span><span class="fz_dv" id="det_monthly">0 kWh/month</span></div>
      <div class="fz_detail-row"><span class="fz_dk">CO2 offset / year</span><span class="fz_dv" id="det_co2">0 kg</span></div>
      <div class="fz_detail-row"><span class="fz_dk">Net metering eligible</span><span class="fz_dv" id="det_nm">No</span></div>
    </div>
  </div>

  <!-- Right column: Financial + Report -->
  <div class="fz_rcol">

    <div class="fz_card">
      <div class="fz_card-head">📊 Financial Summary / مالی خلاصہ</div>
      <div class="fz_card-body">
        <div class="fz_fin-grid">
          <div class="fz_fin-card fz_yellow">
            <div class="fz_fin-label">Initial Cost / ابتدائی لاگت</div>
            <div class="fz_fin-val" id="out_cost">PKR 0</div>
            <div class="fz_fin-sub">One-time installation</div>
            <div id="roof_warning"></div>
          </div>
          <div class="fz_fin-card fz_white">
            <div class="fz_fin-label">Payback Period / واپسی مدت</div>
            <div class="fz_fin-val" id="out_payback">0 <span style="font-size:13px;font-weight:500;color:#6b7280">Years / سال</span></div>
            <div class="fz_fin-sub">Based on current tariff</div>
          </div>
          <div class="fz_fin-card fz_yellow">
            <div class="fz_fin-label">Monthly Savings / ماہانہ بچت</div>
            <div class="fz_fin-val" id="out_mon_sav">PKR 0</div>
            <div class="fz_fin-sub" id="out_ann_sav_sub">Yearly: PKR 0</div>
          </div>
          <div class="fz_fin-card fz_white">
            <div class="fz_fin-label">Net-Metering Ready / نیٹ میٹرنگ</div>
            <div class="fz_fin-val" id="out_nm_label">No ❌</div>
            <div class="fz_fin-sub" id="out_nm_sub" style="background:#FCEBEB;border-radius:4px;padding:2px 6px;display:inline-block;color:#A32D2D">NEPRA approved ≥ 1 kW</div>
          </div>
        </div>
      </div>
    </div>

    <div class="fz_card">
      <div class="fz_card-head">📄 Generate Report / رپورٹ بنائیں</div>
      <div class="fz_card-body">
        <p class="fz_report-desc">Download a complete assessment based on your current inputs — system sizing, costs, savings, and efficiency tips.</p>
        <button class="fz_btn-report" onclick="generateReport()">📄 Generate Report / رپورٹ</button>
        <div class="fz_report-output" id="reportOut"></div>
        <button class="fz_btn-report" id="downloadBtn" onclick="downloadPDF()" style="display:none;margin-top:10px;">📥 Download PDF / پی ڈی ایف ڈاؤن لوڈ کریں</button>
      </div>
    </div>

  </div>
</div>

<div class="fz_ftr">
  Pakistan Solar &amp; Energy Efficiency Assessment Tool &nbsp;|&nbsp;
  Built for Pakistani households &nbsp;|&nbsp;
  Based on NEPRA tariffs &amp; AEDB guidelines
</div>

<script>
const CITY_SUN = {{
    "Karachi": 5.5, "Lahore": 5.0, "Islamabad": 4.8, "Peshawar": 5.2,
    "Quetta": 6.0,  "Multan": 5.8, "Faisalabad": 5.1, "Hyderabad": 5.6,
    "Sialkot": 4.9, "Rawalpindi": 4.8
}};

let currentData = {{}};

function calculate() {{
    const bill = parseFloat(document.getElementById('in_bill').value) || 0;
    const loc = document.getElementById('in_loc').value;
    const roof = parseFloat(document.getElementById('in_roof').value) || 0;
    const sunHrs = CITY_SUN[loc];

    const units = bill / 50;
    const size = Math.round((units / 120) * 100) / 100;
    const cost = size * 150000;
    const monSav = units * 50;
    const annSav = monSav * 12;
    const payback = annSav > 0 ? (cost / annSav).toFixed(1) : 0;
    const panels = Math.max(1, Math.round(size / 0.4));
    const co2 = Math.round(units * 12 * 0.46);
    const roofNeeded = size * 100;
    const roofOk = roof >= roofNeeded;
    const netMeter = size >= 1.0;

    // Store for report
    currentData = {{bill, loc, roof, units, size, cost, monSav, annSav, payback, panels, co2, roofNeeded, roofOk, netMeter, sunHrs}};

    // Update UI
    document.getElementById('out_units').textContent = units.toFixed(0) + " kWh";
    document.getElementById('out_sun_msg').textContent = `☀️ ${{loc}} receives ~${{sunHrs}} peak sun hours/day`;
    document.getElementById('out_size').textContent = size.toFixed(2) + " kW";
    document.getElementById('out_offset').textContent = units.toFixed(0) + " kWh/mo";
    document.getElementById('out_ann_sav').textContent = "PKR " + annSav.toLocaleString() + "/Year";
    document.getElementById('out_solar_sub').textContent = `☀️ Peak Sun Hours (${{loc}}): ${{sunHrs}} hrs/day | ~${{panels}} panels`;
    document.getElementById('out_co2').textContent = `🌿 CO2 offset/year: ~${{co2}} kg`;
    
    // Details
    document.getElementById('det_panels').textContent = panels;
    document.getElementById('det_roof').textContent = roofNeeded.toFixed(0) + " sq. ft. " + (roofOk ? "✅" : "⚠️");
    document.getElementById('det_daily').textContent = (size * sunHrs).toFixed(1) + " kWh/day";
    document.getElementById('det_monthly').textContent = units.toFixed(0) + " kWh/month";
    document.getElementById('det_co2').textContent = co2 + " kg";
    document.getElementById('det_nm').textContent = netMeter ? "Yes ✅ (NEPRA)" : "No ❌ (< 1 kW)";

    // Financials
    document.getElementById('out_cost').textContent = "PKR " + cost.toLocaleString();
    document.getElementById('out_payback').innerHTML = `${{payback}} <span style="font-size:13px;font-weight:500;color:#6b7280">Years / سال</span>`;
    document.getElementById('out_mon_sav').textContent = "PKR " + monSav.toLocaleString();
    document.getElementById('out_ann_sav_sub').textContent = "Yearly: PKR " + annSav.toLocaleString();
    
    const nmLab = document.getElementById('out_nm_label');
    const nmSub = document.getElementById('out_nm_sub');
    if(netMeter) {{
        nmLab.textContent = "Yes ✅"; nmLab.style.color = "#27500A";
        nmSub.style.background = "#EAF3DE"; nmSub.style.color = "#27500A";
    }} else {{
        nmLab.textContent = "No ❌"; nmLab.style.color = "#A32D2D";
        nmSub.style.background = "#FCEBEB"; nmSub.style.color = "#A32D2D";
    }}
    
    document.getElementById('roof_warning').innerHTML = roofOk ? "" : "<div style='font-size:16px;color:#A32D2D;margin-top:3px;'>⚠ Roof may be insufficient</div>";
}}

function toggleDetail(){{
  document.getElementById('detailPanel').classList.toggle('fz_show');
}}

function generateReport(){{
  const d = new Date().toLocaleDateString('en-PK',{{day:'2-digit',month:'long',year:'numeric'}});
  const t = `═══════════════════════════════════════════════════
   Pakistan Solar & Energy Assessment Report
   Generated: ${{d}}
═══════════════════════════════════════════════════

📍 LOCATION:           ${{currentData.loc}}, Pakistan
💰 MONTHLY BILL:       PKR ${{currentData.bill.toLocaleString()}}
🏠 ROOF AREA:          ${{currentData.roof}} sq. ft.

─── ENERGY USAGE ───────────────────────────────
⚡ Estimated Units:    ${{currentData.units.toFixed(0)}} kWh/month

─── SOLAR RECOMMENDATION ───────────────────────
☀️  System Size:        ${{currentData.size.toFixed(2)}} kW
🔢 Panels (400W each): ${{currentData.panels}}
📐 Roof Space Needed:  ${{currentData.roofNeeded.toFixed(0)}} sq. ft.
💵 Installation Cost:  PKR ${{currentData.cost.toLocaleString()}}
☀️  Peak Sun Hours:     ${{currentData.sunHrs}} hrs/day

─── FINANCIAL SUMMARY ──────────────────────────
📉 Monthly Savings:    PKR ${{currentData.monSav.toLocaleString()}}
📈 Yearly Savings:     PKR ${{currentData.annSav.toLocaleString()}}
⏱  Payback Period:     ${{currentData.payback}} Years
🔌 Net Metering:       ${{currentData.netMeter ? "Eligible ✅" : "Not Eligible ❌"}}
🌿 CO2 Saved/Year:     ${{currentData.co2}} kg

═══════════════════════════════════════════════════
Assumptions: Tariff PKR 50/unit | Cost PKR 150,000/kW
═══════════════════════════════════════════════════`;
  var o=document.getElementById('reportOut');
  o.textContent=t;
  o.classList.add('fz_show');
  
  // Show download button
  document.getElementById('downloadBtn').style.display = 'block';
}}

function downloadPDF(){{
  const d = new Date().toLocaleDateString('en-PK',{{day:'2-digit',month:'long',year:'numeric'}});
  
  // Create PDF
  const {{ jsPDF }} = window.jspdf;
  const doc = new jsPDF();
  
  // Set font
  doc.setFont("helvetica");
  
  // Title
  doc.setFontSize(16);
  doc.setFont("helvetica", "bold");
  doc.text("Pakistan Solar & Energy Assessment Report", 20, 30);
  
  // Generated date
  doc.setFontSize(10);
  doc.setFont("helvetica", "normal");
  doc.text(`Generated: ${{d}}`, 20, 40);
  
  // Line separator
  doc.setLineWidth(0.5);
  doc.line(20, 45, 190, 45);
  
  // Location and basic info
  doc.setFontSize(12);
  doc.setFont("helvetica", "bold");
  doc.text("LOCATION:", 20, 60);
  doc.setFont("helvetica", "normal");
  doc.text(`${{currentData.loc}}, Pakistan`, 60, 60);
  
  doc.setFont("helvetica", "bold");
  doc.text("MONTHLY BILL:", 20, 70);
  doc.setFont("helvetica", "normal");
  doc.text(`PKR ${{currentData.bill.toLocaleString()}}`, 60, 70);
  
  doc.setFont("helvetica", "bold");
  doc.text("ROOF AREA:", 20, 80);
  doc.setFont("helvetica", "normal");
  doc.text(`${{currentData.roof}} sq. ft.`, 60, 80);
  
  // Energy Usage section
  doc.setFontSize(14);
  doc.setFont("helvetica", "bold");
  doc.text("ENERGY USAGE", 20, 100);
  doc.setLineWidth(0.3);
  doc.line(20, 105, 80, 105);
  
  doc.setFontSize(12);
  doc.setFont("helvetica", "bold");
  doc.text("Estimated Units:", 20, 115);
  doc.setFont("helvetica", "normal");
  doc.text(`${{currentData.units.toFixed(0)}} kWh/month`, 70, 115);
  
  // Solar Recommendation section
  doc.setFontSize(14);
  doc.setFont("helvetica", "bold");
  doc.text("SOLAR RECOMMENDATION", 20, 135);
  doc.setLineWidth(0.3);
  doc.line(20, 140, 90, 140);
  
  doc.setFontSize(12);
  doc.setFont("helvetica", "bold");
  doc.text("System Size:", 20, 150);
  doc.setFont("helvetica", "normal");
  doc.text(`${{currentData.size.toFixed(2)}} kW`, 60, 150);
  
  doc.setFont("helvetica", "bold");
  doc.text("Panels (400W each):", 20, 160);
  doc.setFont("helvetica", "normal");
  doc.text(`${{currentData.panels}}`, 70, 160);
  
  doc.setFont("helvetica", "bold");
  doc.text("Roof Space Needed:", 20, 170);
  doc.setFont("helvetica", "normal");
  doc.text(`${{currentData.roofNeeded.toFixed(0)}} sq. ft.`, 70, 170);
  
  doc.setFont("helvetica", "bold");
  doc.text("Installation Cost:", 20, 180);
  doc.setFont("helvetica", "normal");
  doc.text(`PKR ${{currentData.cost.toLocaleString()}}`, 65, 180);
  
  doc.setFont("helvetica", "bold");
  doc.text("Peak Sun Hours:", 20, 190);
  doc.setFont("helvetica", "normal");
  doc.text(`${{currentData.sunHrs}} hrs/day`, 65, 190);
  
  // Financial Summary section
  doc.setFontSize(14);
  doc.setFont("helvetica", "bold");
  doc.text("FINANCIAL SUMMARY", 20, 210);
  doc.setLineWidth(0.3);
  doc.line(20, 215, 85, 215);
  
  doc.setFontSize(12);
  doc.setFont("helvetica", "bold");
  doc.text("Monthly Savings:", 20, 225);
  doc.setFont("helvetica", "normal");
  doc.text(`PKR ${{currentData.monSav.toLocaleString()}}`, 65, 225);
  
  doc.setFont("helvetica", "bold");
  doc.text("Yearly Savings:", 20, 235);
  doc.setFont("helvetica", "normal");
  doc.text(`PKR ${{currentData.annSav.toLocaleString()}}`, 60, 235);
  
  doc.setFont("helvetica", "bold");
  doc.text("Payback Period:", 20, 245);
  doc.setFont("helvetica", "normal");
  doc.text(`${{currentData.payback}} Years`, 60, 245);
  
  doc.setFont("helvetica", "bold");
  doc.text("Net Metering:", 20, 255);
  doc.setFont("helvetica", "normal");
  doc.text(`${{currentData.netMeter ? "Eligible" : "Not Eligible"}}`, 55, 255);
  
  doc.setFont("helvetica", "bold");
  doc.text("CO2 Saved/Year:", 20, 265);
  doc.setFont("helvetica", "normal");
  doc.text(`${{currentData.co2}} kg`, 60, 265);
  
  // Footer
  doc.setFontSize(10);
  doc.setFont("helvetica", "italic");
  doc.text("Assumptions: Tariff PKR 50/unit | Cost PKR 150,000/kW", 20, 285);
  
  // Save the PDF
  const filename = `Pakistan_Solar_Report_${{currentData.loc}}_${{d.replace(/ /g, '_').replace(',', '')}}.pdf`;
  doc.save(filename);
}}
</script>
</body>
</html>"""

components.html(html, height=1000, scrolling=True)