import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.set_page_config(page_title="LG Launcher Placement - Spain", page_icon="TV", layout="wide", initial_sidebar_state="collapsed")

# ============================================================
# DATA
# ============================================================
APPS = ['Netflix', 'Prime Video', 'Disney+', 'Mediaset Infinity', 'Atresplayer']
PL = [True, True, True, False, False]
MU = [14_000_000, 12_600_000, 6_600_000, 3_600_000, 3_400_000]
AD = 39_000_000
LB = 5_380_000
AUD = [2_714_400, 1_918_000, 1_379_600, 226_400, 192_300]
AA_R = [37.8, 44.3, 42.3, 0.0, 0.0]
AA_L = [25.8, 42.2, 45.6, 92.7, 93.6]
AA_G = [33.1, 1.1, 0.0, 0.0, 0.0]
AA_H = [0.0, 0.8, 0.3, 0.0, 0.0]
AA_O = [round(100 - AA_R[i] - AA_L[i] - AA_G[i] - AA_H[i], 1) for i in range(5)]
LP = [u / LB * 100 for u in AUD]
MP = [u / AD * 100 for u in MU]
CI = [LP[i] / MP[i] for i in range(5)]
AW = float(np.mean(CI[:3]))
AWO = float(np.mean(CI[3:]))
C = {
    'placed': '#2D8A4E', 'not_placed': '#C0392B', 'lg': '#A50034',
    'remote': '#FF6B6B', 'launcher': '#4ECDC4', 'gip': '#45B7D1',
    'home': '#FFA07A', 'other': '#C0C0C0', 'dark': '#1a1a2e',
    'gold': '#F39C12', 'blue': '#3498DB', 'purple': '#9B59B6'
}

CHAPTERS = [
    "Cover",
    "The Landscape",
    "The Evidence",
    "The Insight",
    "The Opportunity",
    "The Price",
    "The Strategy",
    "Glossary"
]
TOTAL = len(CHAPTERS)

# ============================================================
# SESSION STATE
# ============================================================
if "ch" not in st.session_state:
    st.session_state.ch = 0

def go_next():
    if st.session_state.ch < TOTAL - 1:
        st.session_state.ch += 1

def go_prev():
    if st.session_state.ch > 0:
        st.session_state.ch -= 1

def go_to(i):
    st.session_state.ch = i

ch = st.session_state.ch

# ============================================================
# CSS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
.hero { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); padding: 3rem 2rem; border-radius: 20px; text-align: center; margin-bottom: 2rem; position: relative; overflow: hidden; }
.hero h1 { color: white; font-size: 2.8rem; font-weight: 800; margin: 0; line-height: 1.2; }
.hero .accent { color: #FF6B6B; }
.hero p { color: rgba(255,255,255,0.7); font-size: 1.1rem; margin-top: 1rem; }
.hero .tag { display: inline-block; background: rgba(165,0,52,0.3); color: #FF6B6B; padding: 0.3rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600; margin-top: 1rem; border: 1px solid rgba(165,0,52,0.5); }
.kpi-row { display: flex; gap: 1rem; margin: 1.5rem 0; flex-wrap: wrap; }
.kpi { flex: 1; min-width: 140px; padding: 1.3rem; border-radius: 16px; text-align: center; }
.kpi-red { background: linear-gradient(135deg, #A50034, #D4004B); color: white; box-shadow: 0 8px 25px rgba(165,0,52,0.3); }
.kpi-dark { background: linear-gradient(135deg, #1a1a2e, #16213e); color: white; box-shadow: 0 8px 25px rgba(26,26,46,0.3); }
.kpi-green { background: linear-gradient(135deg, #2D8A4E, #27ae60); color: white; box-shadow: 0 8px 25px rgba(45,138,78,0.3); }
.kpi-gold { background: linear-gradient(135deg, #F39C12, #e67e22); color: white; box-shadow: 0 8px 25px rgba(243,156,18,0.3); }
.kpi .number { font-size: 2rem; font-weight: 800; margin: 0; }
.kpi .label { font-size: 0.78rem; opacity: 0.85; margin-top: 0.3rem; }
.chapter { margin: 2rem 0 1rem 0; padding-bottom: 0.5rem; border-bottom: 3px solid #A50034; }
.chapter h2 { font-size: 1.8rem; font-weight: 700; color: #1a1a2e; margin: 0; }
.chapter .num { color: #A50034; font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; }
.insight-card { background: #f8f9fa; border-radius: 16px; padding: 1.5rem; margin: 1rem 0; border-left: 5px solid #A50034; transition: transform 0.2s; }
.insight-card:hover { transform: translateX(5px); }
.insight-card h4 { color: #A50034; margin: 0 0 0.5rem 0; font-size: 1rem; }
.insight-card p { color: #444; margin: 0; font-size: 0.95rem; line-height: 1.6; }
.verdict { background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%); padding: 2rem; border-radius: 16px; color: white; text-align: center; margin: 2rem 0; }
.verdict h3 { font-size: 1.5rem; margin: 0 0 0.5rem 0; }
.verdict .big { font-size: 3rem; font-weight: 800; color: #FF6B6B; }
.verdict p { opacity: 0.8; margin-top: 0.5rem; }
.quote-box { background: #FFF3F5; border-left: 5px solid #A50034; padding: 1.2rem 1.5rem; border-radius: 0 12px 12px 0; margin: 1.5rem 0; font-style: italic; color: #333; }
.cta-box { background: linear-gradient(135deg, #2D8A4E, #27ae60); padding: 1.5rem 2rem; border-radius: 16px; color: white; text-align: center; margin: 1.5rem 0; box-shadow: 0 8px 25px rgba(45,138,78,0.3); }
.cta-box h3 { margin: 0; font-size: 1.3rem; }
.cta-box p { margin: 0.5rem 0 0 0; opacity: 0.9; }
.vs-table { width: 100%; border-collapse: separate; border-spacing: 0; border-radius: 12px; overflow: hidden; margin: 1rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.08); }
.vs-table th { background: #1a1a2e; color: white; padding: 0.8rem 1rem; font-size: 0.85rem; text-align: center; }
.vs-table td { padding: 0.7rem 1rem; text-align: center; border-bottom: 1px solid #eee; font-size: 0.9rem; }
.vs-table tr:nth-child(even) { background: #f8f9fa; }
.vs-table .good { color: #2D8A4E; font-weight: 700; }
.vs-table .bad { color: #C0392B; font-weight: 700; }
.timeline-item { display: flex; gap: 1rem; margin: 1rem 0; align-items: flex-start; }
.timeline-dot { min-width: 40px; height: 40px; border-radius: 50%; background: #A50034; color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.85rem; }
.timeline-content { background: #f8f9fa; padding: 1rem 1.2rem; border-radius: 12px; flex: 1; }
.timeline-content strong { color: #1a1a2e; }
.timeline-content p { color: #555; margin: 0.3rem 0 0 0; font-size: 0.9rem; }
details { background: #f8f9fa; padding: 0.8rem 1.2rem; border-radius: 10px; margin: 0.5rem 0; cursor: pointer; }
details summary { font-weight: 600; font-size: 0.95rem; color: #1a1a2e; list-style: none; display: flex; align-items: center; gap: 0.5rem; }
details summary::before { content: '+ '; color: #A50034; font-weight: 800; font-size: 1.1rem; }
details[open] summary::before { content: '- '; }
details p { color: #555; margin-top: 0.5rem; font-size: 0.9rem; line-height: 1.6; }
div[data-testid="stMetric"] { background-color: #F8F9FA; padding: 1rem; border-radius: 12px; border: 1px solid #E9ECEF; }
.nav-btn { display: inline-block; padding: 0.6rem 2rem; border-radius: 10px; font-weight: 700; font-size: 0.95rem; cursor: pointer; text-align: center; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### Navigation")
    st.markdown(f"**Chapter {ch}/{TOTAL-1}**")
    st.progress(ch / (TOTAL - 1))
    st.markdown("---")
    for i, name in enumerate(CHAPTERS):
        prefix = ">> " if i == ch else ""
        if st.button(f"{prefix}{i}. {name}", key=f"nav_{i}", use_container_width=True):
            go_to(i)
            st.rerun()
    st.markdown("---")
    st.caption("LG Electronics Spain\nJune 2026 | Confidential")

# ============================================================
# PROGRESS BAR (top)
# ============================================================
st.progress(ch / (TOTAL - 1))

# ============================================================
# CHAPTER 0: COVER
# ============================================================
if ch == 0:
    st.markdown("""
    <div class="hero">
        <div class="tag">LG ELECTRONICS SPAIN &bull; CONFIDENTIAL &bull; JUNE 2026</div>
        <h1>What happens when your app<br><span class="accent">isn't on the Launcher?</span></h1>
        <p>A data-driven analysis of Launcher Placement impact on LG Smart TVs in Spain.<br>
        5 apps. 5.38 million TVs. One clear conclusion.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="kpi-row">
        <div class="kpi kpi-red"><div class="number">3.1x</div><div class="label">Placement Multiplier<br>(brand-adjusted)</div></div>
        <div class="kpi kpi-dark"><div class="number">-56%</div><div class="label">Potential Lost<br>by non-placed apps</div></div>
        <div class="kpi kpi-green"><div class="number">93%+</div><div class="label">Single Channel<br>Dependency</div></div>
        <div class="kpi kpi-gold"><div class="number">EUR 70K-190K</div><div class="label">Recommended Price<br>(Spain-adjusted)</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("This presentation walks you through **6 chapters** of analysis. Use the **Next** button below or the sidebar to navigate.")

# ============================================================
# CHAPTER 1: LANDSCAPE
# ============================================================
elif ch == 1:
    st.markdown("""<div class="chapter"><span class="num">Chapter 1</span><h2>The Landscape: 5.38M LG TVs, One Question</h2></div>""", unsafe_allow_html=True)
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown("""
        Spain has **5.38 million active LG Smart TVs** and streaming is the dominant use case.
        HDMI usage has dropped 43% since 2016 as viewers migrate to apps.

        **Three global players** pay EUR 300K-400K/year for a guaranteed spot on the Launcher Bar.
        **Two local broadcasters** with millions of Spanish users do not.

        The question is: **how much does that matter?**
        """)
    with col2:
        st.markdown("""
        <table class="vs-table">
            <tr><th>Platform</th><th>Users Spain</th><th>Placement</th></tr>
            <tr><td>Netflix</td><td>14.0M</td><td class="good">Yes</td></tr>
            <tr><td>Prime Video</td><td>12.6M</td><td class="good">Yes</td></tr>
            <tr><td>Disney+</td><td>6.6M</td><td class="good">Yes</td></tr>
            <tr><td>Mediaset Infinity</td><td>3.4M</td><td class="bad">No</td></tr>
            <tr><td>Atresplayer</td><td>3.6M</td><td class="bad">No</td></tr>
        </table>
        """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("LG TVs in Spain", "5.38M", "Active Smart TVs")
    col2.metric("Smart TV Penetration", "64%", "14x growth since 2013")
    col3.metric("HDMI Usage Decline", "-43%", "EU5 since 2016")

# ============================================================
# CHAPTER 2: EVIDENCE
# ============================================================
elif ch == 2:
    st.markdown("""<div class="chapter"><span class="num">Chapter 2</span><h2>The Evidence: How Users Actually Access Apps</h2></div>""", unsafe_allow_html=True)
    st.markdown("When an app has placement, users access it through **multiple doors**. Without it, there is only **one way in**.")

    view = st.radio("View mode:", ["All Apps", "Placed Only", "Non-Placed Only"], horizontal=True)
    if view == "Placed Only":
        idx = [0, 1, 2]
    elif view == "Non-Placed Only":
        idx = [3, 4]
    else:
        idx = [0, 1, 2, 3, 4]

    fig = go.Figure()
    for name, data, color in [('Remote Hot Key', AA_R, C['remote']), ('Launcher', AA_L, C['launcher']), ('GIP', AA_G, C['gip']), ('Home Reco', AA_H, C['home']), ('Other', AA_O, C['other'])]:
        fig.add_trace(go.Bar(y=[APPS[i] for i in idx], x=[data[i] for i in idx], name=name, orientation='h', marker_color=color, text=[f'{data[i]:.1f}%' if data[i] > 2 else '' for i in idx], textposition='inside', textfont=dict(color='white', size=11)))
    fig.update_layout(barmode='stack', height=max(250, len(idx)*75), margin=dict(l=0, r=0, t=10, b=0), xaxis_title='% of Total App Access (Avg. Jan-May 2026)', legend=dict(orientation='h', y=-0.2, x=0.5, xanchor='center'), yaxis=dict(autorange='reversed'), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div class="insight-card"><h4>Apps WITH Placement</h4><p>Diversify across <strong>3-5 channels</strong>: Remote Hot Key (~38-44%), Launcher (~26-46%), GIP (up to 33%), Home Recommendations, and DIAL.</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="insight-card"><h4>Apps WITHOUT Placement</h4><p>Depend <strong>93%+</strong> on a single channel. No hot key, no GIP, no recommendations. The user must <strong>actively find and install</strong> the app.</p></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="quote-box">"Of course Netflix has more users. The real question is: <strong>if we remove the brand effect, does placement still matter?</strong>"</div>""", unsafe_allow_html=True)

# ============================================================
# CHAPTER 3: INSIGHT
# ============================================================
elif ch == 3:
    st.markdown("""<div class="chapter"><span class="num">Chapter 3</span><h2>The Insight: Removing the Brand Bias</h2></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="verdict"><h3>Capture Index</h3><p>LG TV Penetration (%) / Market Penetration (%)</p><p style="font-size:0.85rem; margin-top:1rem;">= 1.0 : par | &gt; 1.0 : placement amplifies | &lt; 1.0 : app loses presence</p></div>""", unsafe_allow_html=True)

    bar_colors = [C['placed'] if c >= 1 else C['not_placed'] for c in CI]
    fig = go.Figure()
    fig.add_trace(go.Bar(y=APPS, x=CI, orientation='h', marker_color=bar_colors, text=[f'{c:.2f}  ({"+" if c>=1 else ""}{(c-1)*100:.0f}%)' for c in CI], textposition='outside', textfont=dict(size=13, color=bar_colors)))
    fig.add_vline(x=1.0, line_dash="dash", line_color="#999", line_width=2, annotation_text="Par (1.0)", annotation_font_color="#999")
    fig.update_layout(height=380, margin=dict(l=0, r=160, t=10, b=0), xaxis=dict(title='Capture Index', range=[0, 2.0], gridcolor='#eee'), yaxis=dict(autorange='reversed'), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""<div class="verdict"><h3>The Verdict</h3><div class="big">{AW/AWO:.1f}x</div><p>Avg. WITH: <strong>{AW:.2f}</strong> | Avg. WITHOUT: <strong>{AWO:.2f}</strong></p></div>""", unsafe_allow_html=True)

    st.markdown("#### Market Share vs. LG Presence")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=APPS, y=MP, name='Market Penetration', marker_color=C['blue'], text=[f'{v:.1f}%' for v in MP], textposition='outside'))
    fig2.add_trace(go.Bar(x=APPS, y=LP, name='LG TV Penetration', marker_color='#E67E22', text=[f'{v:.1f}%' for v in LP], textposition='outside'))
    fig2.update_layout(barmode='group', height=400, margin=dict(l=0, r=0, t=10, b=0), yaxis_title='Penetration (%)', legend=dict(orientation='h', y=1.08, x=0.5, xanchor='center'), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig2, use_container_width=True)

# ============================================================
# CHAPTER 4: OPPORTUNITY (INTERACTIVE)
# ============================================================
elif ch == 4:
    st.markdown("""<div class="chapter"><span class="num">Chapter 4</span><h2>The Opportunity: What Placement Would Unlock</h2></div>""", unsafe_allow_html=True)
    st.markdown("Use the slider to simulate different Capture Index scenarios:")

    target_idx = st.slider("Target Capture Index for local partners", min_value=0.40, max_value=1.60, value=1.00, step=0.05, format="%.2f")

    partner = st.radio("View partner:", ["Both", "Mediaset Infinity", "Atresplayer"], horizontal=True)

    partners = {
        'Mediaset Infinity': {'users': 3_400_000, 'current_ud': 226_400, 'mkt_pen': 3_400_000/AD*100},
        'Atresplayer': {'users': 3_600_000, 'current_ud': 192_300, 'mkt_pen': 3_600_000/AD*100}
    }

    show = list(partners.keys()) if partner == "Both" else [partner]

    for name in show:
        p = partners[name]
        projected_pen = p['mkt_pen'] * target_idx
        projected_ud = int(projected_pen / 100 * LB)
        incremental = projected_ud - p['current_ud']
        growth_pct = (incremental / p['current_ud'] * 100) if p['current_ud'] > 0 else 0

        st.markdown(f"#### {name}")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Current UD", f"{p['current_ud']:,.0f}", "No Placement", delta_color="off")
        col2.metric("Projected UD", f"{projected_ud:,.0f}", f"+{incremental:,.0f}" if incremental > 0 else f"{incremental:,.0f}")
        col3.metric("Growth", f"{growth_pct:+.0f}%", f"Index = {target_idx:.2f}")
        col4.metric("LG Penetration", f"{projected_pen:.1f}%", f"vs {p['current_ud']/LB*100:.1f}% current")

    # Chart
    fig = go.Figure()
    for name in show:
        p = partners[name]
        proj_pen = p['mkt_pen'] * target_idx
        proj_ud = int(proj_pen / 100 * LB)
        fig.add_trace(go.Bar(y=[name], x=[p['current_ud']], name='Current', orientation='h', marker_color=C['not_placed'], text=[f"{p['current_ud']:,.0f}"], textposition='outside'))
        fig.add_trace(go.Bar(y=[name], x=[proj_ud], name=f'Projected (Index={target_idx:.2f})', orientation='h', marker_color=C['placed'], text=[f"{proj_ud:,.0f}"], textposition='outside'))
    fig.update_layout(barmode='group', height=250, margin=dict(l=0, r=140, t=10, b=0), xaxis_title='Unique Devices', yaxis=dict(autorange='reversed'), legend=dict(orientation='h', y=-0.3, x=0.5, xanchor='center'), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

    if target_idx >= 1.0:
        st.markdown("""<div class="cta-box"><h3>At this index, local partners recover their full market potential on LG TVs</h3><p>Placement closes the gap between market share and LG presence.</p></div>""", unsafe_allow_html=True)

# ============================================================
# CHAPTER 5: PRICE (INTERACTIVE)
# ============================================================
elif ch == 5:
    st.markdown("""<div class="chapter"><span class="num">Chapter 5</span><h2>The Price: What is Fair for Spain?</h2></div>""", unsafe_allow_html=True)
    st.markdown("Global platforms pay **EUR 300K-400K/year**. Explore what makes sense for local partners:")

    price = st.slider("Select a price point (EUR K/year)", min_value=50, max_value=250, value=120, step=5)

    if price <= 110:
        tier = "Entry"
        includes = "Launcher Placement only"
        tier_color = C['placed']
        est_devices = "+242K incremental devices (conservative)"
    elif price <= 150:
        tier = "Target"
        includes = "Launcher Placement"
        tier_color = C['blue']
        est_devices = "+242K to +350K incremental devices"
    elif price <= 190:
        tier = "Premium"
        includes = "Launcher + OOBE + Home Reco + Banner"
        tier_color = C['purple']
        est_devices = "+350K to +401K incremental devices"
    else:
        tier = "Above recommended range"
        includes = "Full package (approaching global pricing)"
        tier_color = C['gold']
        est_devices = "+401K+ incremental devices"

    discount_vs_global = round((1 - price / 350) * 100)
    est_ad_rev = round(price * 0.08, 1)

    col1, col2, col3 = st.columns(3)
    col1.metric("Selected Price", f"EUR {price}K/year")
    col2.metric("Tier", tier)
    col3.metric("Discount vs Global", f"{discount_vs_global}%", "below EUR 350K avg")

    st.markdown(f"**Includes:** {includes}")
    st.markdown(f"**Estimated impact:** {est_devices}")
    st.markdown(f"**Incremental ad revenue potential:** EUR 1.0M - EUR 1.4M/year")

    # Visual position
    fig = go.Figure()
    fig.add_vrect(x0=70, x1=110, fillcolor=C['placed'], opacity=0.15, line_width=0, annotation_text="Entry", annotation_position="top")
    fig.add_vrect(x0=110, x1=150, fillcolor=C['blue'], opacity=0.15, line_width=0, annotation_text="Target", annotation_position="top")
    fig.add_vrect(x0=150, x1=190, fillcolor=C['purple'], opacity=0.15, line_width=0, annotation_text="Premium", annotation_position="top")
    fig.add_vrect(x0=300, x1=400, fillcolor=C['gold'], opacity=0.1, line_width=0, annotation_text="Global Apps", annotation_position="top")
    fig.add_vline(x=price, line_color=C['lg'], line_width=3, annotation_text=f"EUR {price}K", annotation_font_color=C['lg'], annotation_font_size=14)
    fig.update_layout(height=200, margin=dict(l=0, r=0, t=40, b=0), xaxis=dict(title="EUR K/year", range=[0, 420]), yaxis=dict(visible=False), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    tab1, tab2 = st.tabs(["Valuation Methods", "Why the Discount?"])
    with tab1:
        methods = [("Cost per Incremental Device", "EUR 46K - EUR 76K", 46, 76, C['blue'], "EUR 350K / 1.88M incremental = EUR 0.19/device. Applied to +242K."), ("Ad Revenue Value (AVOD)", "EUR 140K - EUR 210K", 140, 210, C['placed'], "23.2M incremental sessions x EUR 20 CPM = EUR 1.4M. Fee = 10-15%."), ("Premium Sub Conversion", "EUR 140K - EUR 210K", 140, 210, C['purple'], "24.2K new subs x EUR 3.99 x 12 = EUR 1.16M. Fee = 12-18%."), ("Market Proportionality", "EUR 85K - EUR 120K", 85, 120, '#E67E22', "3.4M users x EUR 0.025/user x 1.35 = EUR 115K.")]
        for name, rng, lo, hi, color, desc in methods:
            st.markdown(f"""<details style="border-left:4px solid {color};"><summary>{name} = {rng}/year</summary><p>{desc}</p></details>""", unsafe_allow_html=True)
    with tab2:
        st.markdown("""
        <table class="vs-table">
            <tr><th>Factor</th><th>Spain</th><th>UK</th><th>US</th></tr>
            <tr><td>Pay-TV Penetration</td><td class="bad">&lt;45%</td><td>~65%</td><td>~85%</td></tr>
            <tr><td>AVOD/FAST Weekly</td><td><strong>75%</strong></td><td>~45%</td><td>~50%</td></tr>
            <tr><td>SVoD ARPU</td><td class="bad">~EUR 8.2/mo</td><td>~EUR 11-12</td><td>~EUR 13-15</td></tr>
            <tr><td>Telco Bundles</td><td class="bad">41.3%</td><td>~25%</td><td>~15%</td></tr>
        </table>
        """, unsafe_allow_html=True)

# ============================================================
# CHAPTER 6: STRATEGY
# ============================================================
elif ch == 6:
    st.markdown("""<div class="chapter"><span class="num">Chapter 6</span><h2>The Strategy: How to Close the Deal</h2></div>""", unsafe_allow_html=True)
    st.markdown("#### The Domino Effect")
    st.markdown("Mediaset and Atresmedia compete for the **same audience**. If one gets placement, the other faces **immediate disadvantage**. Present to both simultaneously.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div class="insight-card" style="border-left-color: #E67E22;"><h4 style="color: #E67E22;">Mediaset Infinity</h4><p>+23% YoY digital users<br>3.4M users, only 4.2% LG penetration<br>FIFA Club World Cup rights<br>+242K to +401K incremental devices<br>If Atresplayer signs first, loses ground</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="insight-card" style="border-left-color: #3498DB;"><h4 style="color: #3498DB;">Atresplayer</h4><p>Best visitors since May 2024 (3.2M, +20% YoY)<br>3.6M users, only 3.6% LG penetration<br>Most national premieres<br>+303K to +471K incremental devices<br>If Mediaset enters Launcher, loses share</p></div>""", unsafe_allow_html=True)

    st.markdown("#### Timeline")
    for dot, title, desc in [("Jun", "June 2026", "Send formal proposal to both partners."), ("Jul", "July 2026", "Negotiation meetings with weighted data."), ("Aug", "August 2026", "Close at least one deal before LaLiga."), ("Q4", "Q4 2026", "Measure results. Build success case for partner #2."), ("Q1", "Q1 2027", "Both placed. Target DAZN, Movistar+ next.")]:
        st.markdown(f"""<div class="timeline-item"><div class="timeline-dot">{dot}</div><div class="timeline-content"><strong>{title}</strong><p>{desc}</p></div></div>""", unsafe_allow_html=True)

# ============================================================
# CHAPTER 7: GLOSSARY
# ============================================================
elif ch == 7:
    st.markdown("""<div class="chapter"><span class="num">Reference</span><h2>Glossary and Definitions</h2></div>""", unsafe_allow_html=True)

    acr_rows = ""
    for a, d in [('ARPU','Average Revenue Per User.'),('AVOD','Advertising-based Video On Demand.'),('CPM','Cost Per Mille - cost per 1,000 impressions.'),('CTV','Connected TV.'),('DIAL','Discovery and Launch protocol.'),('FAST','Free Ad-Supported Streaming TV.'),('GIP','Global Input Priority - auto-launch on power-on.'),('OOBE','Out-Of-Box Experience.'),('SVoD','Subscription Video On Demand.'),('TDT','Television Digital Terrestre.'),('UD','Unique Devices.'),('webOS','LG Smart TV OS.'),('YoY','Year-over-Year.')]:
        acr_rows += f"<tr><td><strong>{a}</strong></td><td style=\'text-align:left;\'>{d}</td></tr>"
    st.markdown(f"""<details><summary>Acronyms and Abbreviations</summary><table class="vs-table" style="margin-top:0.8rem;"><tr><th style="width:120px;">Acronym</th><th>Definition</th></tr>{acr_rows}</table></details>""", unsafe_allow_html=True)

    met_rows = ""
    for m, d in [('App Access','Total app launches.'),('App UD','Unique devices that launched an app.'),('Capture Index','LG Penetration / Market Penetration.'),('Remote Hot Key','Physical button on remote.'),('Launcher','App strip on home screen.'),('GIP','Auto-launch on power-on.'),('Home Reco','Recommended content cards.'),('Incremental Devices','Projected UD minus current UD.')]:
        met_rows += f"<tr><td><strong>{m}</strong></td><td style=\'text-align:left;\'>{d}</td></tr>"
    st.markdown(f"""<details><summary>Key Metrics and KPIs</summary><table class="vs-table" style="margin-top:0.8rem;"><tr><th style="width:160px;">Metric</th><th>Definition</th></tr>{met_rows}</table></details>""", unsafe_allow_html=True)

    term_rows = ""
    for t, d in [('Launcher Placement','Paid agreement to pre-install an app.'),('Hot Key','Branded button on remote.'),('Home Screen Shelves','Content rows above Launcher.'),('Magic Remote','LG pointer remote with mic.'),('Pay-TV','Subscription TV.'),('FTA / TDT','Free TV via antenna.'),('Telco Bundle','Streaming in telecom packages.'),('Revenue Share','Partner pays % of revenue.'),('First Mover Advantage','Edge from being first to sign.'),('Installed Base','Total active LG TVs (5.38M).')]:
        term_rows += f"<tr><td><strong>{t}</strong></td><td style=\'text-align:left;\'>{d}</td></tr>"
    st.markdown(f"""<details><summary>Industry and Technical Terms</summary><table class="vs-table" style="margin-top:0.8rem;"><tr><th style="width:180px;">Term</th><th>Definition</th></tr>{term_rows}</table></details>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""<div style="text-align:center; padding:1rem; color:#999; font-size:0.85rem;">LG Electronics Spain | Marketing and Media Department | June 2026 | Confidential<br>Data: LG webOS Analytics Jan-May 2026 | GfK DAM 2025 | JustWatch | CNMC | Futuresource</div>""", unsafe_allow_html=True)

# ============================================================
# NAVIGATION BUTTONS
# ============================================================
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if ch > 0:
        st.button("Previous", on_click=go_prev, use_container_width=True)
with col2:
    st.markdown(f"<p style=\'text-align:center; color:#999;\'>Chapter {ch} of {TOTAL-1}: {CHAPTERS[ch]}</p>", unsafe_allow_html=True)
with col3:
    if ch < TOTAL - 1:
        st.button("Next", on_click=go_next, type="primary", use_container_width=True)
