import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="LG Launcher Placement - Spain",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# DATA
# ============================================================
APPS = ['Netflix', 'Prime Video', 'Disney+', 'Mediaset Infinity', 'Atresplayer']
PLACEMENT = [True, True, True, False, False]
MARKET_USERS = [14_000_000, 12_600_000, 6_600_000, 3_600_000, 3_400_000]
ADULTS_SPAIN = 39_000_000
LG_BASE = 5_380_000
APP_UD_TOTAL = [2_714_400, 1_918_000, 1_379_600, 226_400, 192_300]

AA_REMOTE = [37.8, 44.3, 42.3, 0.0, 0.0]
AA_LAUNCHER = [25.8, 42.2, 45.6, 92.7, 93.6]
AA_GIP = [33.1, 1.1, 0.0, 0.0, 0.0]
AA_HOME = [0.0, 0.8, 0.3, 0.0, 0.0]
AA_OTHER = [round(100 - AA_REMOTE[i] - AA_LAUNCHER[i] - AA_GIP[i] - AA_HOME[i], 1) for i in range(5)]

UD_REMOTE = [78.9, 60.4, 63.8, 0.0, 0.0]
UD_LAUNCHER = [71.3, 62.7, 51.0, 95.5, 95.0]
UD_GIP = [67.7, 3.9, 0.1, 0.0, 0.0]
UD_HOME = [0.0, 4.8, 2.3, 0.0, 0.0]
UD_OTHER = [1.0, 2.5, 1.5, 4.5, 5.0]
UD_LAUNCHER_JAN = [1_973_203, 1_213_952, 695_481, 215_299, 181_738]

LG_PEN = [u / LG_BASE * 100 for u in APP_UD_TOTAL]
MKT_PEN = [u / ADULTS_SPAIN * 100 for u in MARKET_USERS]
CAP_IDX = [LG_PEN[i] / MKT_PEN[i] for i in range(5)]
AVG_WITH = np.mean(CAP_IDX[:3])
AVG_WITHOUT = np.mean(CAP_IDX[3:])

C = {
    'placed': '#2D8A4E', 'not_placed': '#C0392B', 'lg': '#A50034',
    'remote': '#FF6B6B', 'launcher': '#4ECDC4', 'gip': '#45B7D1',
    'home': '#FFA07A', 'other': '#C0C0C0', 'dark': '#1a1a2e',
    'gold': '#F39C12', 'blue': '#3498DB', 'purple': '#9B59B6'
}

# ============================================================
# CSS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }

.hero {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding: 3rem 2rem; border-radius: 20px; text-align: center;
    margin-bottom: 2rem; position: relative; overflow: hidden;
}
.hero::before {
    content: ''; position: absolute; top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(165,0,52,0.15) 0%, transparent 50%);
}
.hero h1 {
    color: white; font-size: 2.8rem; font-weight: 800;
    margin: 0; line-height: 1.2; position: relative;
}
.hero .accent { color: #FF6B6B; }
.hero p {
    color: rgba(255,255,255,0.7); font-size: 1.1rem;
    margin-top: 1rem; position: relative;
}
.hero .tag {
    display: inline-block; background: rgba(165,0,52,0.3);
    color: #FF6B6B; padding: 0.3rem 1rem; border-radius: 20px;
    font-size: 0.8rem; font-weight: 600; margin-top: 1rem;
    position: relative; border: 1px solid rgba(165,0,52,0.5);
}

.kpi-row { display: flex; gap: 1rem; margin: 1.5rem 0; flex-wrap: wrap; }
.kpi {
    flex: 1; min-width: 150px; padding: 1.5rem; border-radius: 16px;
    text-align: center; position: relative; overflow: hidden;
}
.kpi-red {
    background: linear-gradient(135deg, #A50034, #D4004B);
    color: white; box-shadow: 0 8px 25px rgba(165,0,52,0.3);
}
.kpi-dark {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    color: white; box-shadow: 0 8px 25px rgba(26,26,46,0.3);
}
.kpi-green {
    background: linear-gradient(135deg, #2D8A4E, #27ae60);
    color: white; box-shadow: 0 8px 25px rgba(45,138,78,0.3);
}
.kpi-gold {
    background: linear-gradient(135deg, #F39C12, #e67e22);
    color: white; box-shadow: 0 8px 25px rgba(243,156,18,0.3);
}
.kpi .number { font-size: 2.2rem; font-weight: 800; margin: 0; }
.kpi .label { font-size: 0.8rem; opacity: 0.85; margin-top: 0.3rem; }

.chapter {
    margin: 3rem 0 1rem 0; padding-bottom: 0.5rem;
    border-bottom: 3px solid #A50034;
}
.chapter h2 {
    font-size: 1.8rem; font-weight: 700; color: #1a1a2e; margin: 0;
}
.chapter .num {
    color: #A50034; font-size: 0.9rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 2px;
}

.insight-card {
    background: #f8f9fa; border-radius: 16px; padding: 1.5rem;
    margin: 1rem 0; border-left: 5px solid #A50034;
    transition: transform 0.2s;
}
.insight-card:hover { transform: translateX(5px); }
.insight-card h4 { color: #A50034; margin: 0 0 0.5rem 0; font-size: 1rem; }
.insight-card p { color: #444; margin: 0; font-size: 0.95rem; line-height: 1.6; }

.verdict {
    background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%);
    padding: 2rem; border-radius: 16px; color: white;
    text-align: center; margin: 2rem 0;
}
.verdict h3 { font-size: 1.5rem; margin: 0 0 0.5rem 0; }
.verdict .big { font-size: 3rem; font-weight: 800; color: #FF6B6B; }
.verdict p { opacity: 0.8; margin-top: 0.5rem; }

.quote-box {
    background: #FFF3F5; border-left: 5px solid #A50034;
    padding: 1.2rem 1.5rem; border-radius: 0 12px 12px 0;
    margin: 1.5rem 0; font-style: italic; color: #333;
}

.cta-box {
    background: linear-gradient(135deg, #2D8A4E, #27ae60);
    padding: 1.5rem 2rem; border-radius: 16px; color: white;
    text-align: center; margin: 1.5rem 0;
    box-shadow: 0 8px 25px rgba(45,138,78,0.3);
}
.cta-box h3 { margin: 0; font-size: 1.3rem; }
.cta-box p { margin: 0.5rem 0 0 0; opacity: 0.9; }

.vs-table {
    width: 100%; border-collapse: separate; border-spacing: 0;
    border-radius: 12px; overflow: hidden; margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}
.vs-table th {
    background: #1a1a2e; color: white; padding: 0.8rem 1rem;
    font-size: 0.85rem; text-align: center;
}
.vs-table td {
    padding: 0.7rem 1rem; text-align: center; border-bottom: 1px solid #eee;
    font-size: 0.9rem;
}
.vs-table tr:nth-child(even) { background: #f8f9fa; }
.vs-table .good { color: #2D8A4E; font-weight: 700; }
.vs-table .bad { color: #C0392B; font-weight: 700; }

.timeline-item {
    display: flex; gap: 1rem; margin: 1rem 0; align-items: flex-start;
}
.timeline-dot {
    min-width: 40px; height: 40px; border-radius: 50%;
    background: #A50034; color: white; display: flex;
    align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.85rem;
}
.timeline-content {
    background: #f8f9fa; padding: 1rem 1.2rem; border-radius: 12px; flex: 1;
}
.timeline-content strong { color: #1a1a2e; }
.timeline-content p { color: #555; margin: 0.3rem 0 0 0; font-size: 0.9rem; }

details {
    background: #f8f9fa; padding: 0.8rem 1.2rem; border-radius: 10px;
    margin: 0.5rem 0; cursor: pointer;
}
details summary {
    font-weight: 600; font-size: 0.95rem; color: #1a1a2e;
    list-style: none; display: flex; align-items: center; gap: 0.5rem;
}
details summary::before {
    content: '+ '; color: #A50034; font-weight: 800; font-size: 1.1rem;
}
details[open] summary::before { content: '- '; }
details p {
    color: #555; margin-top: 0.5rem; font-size: 0.9rem; line-height: 1.6;
}

div[data-testid="stMetric"] {
    background-color: #F8F9FA; padding: 1rem; border-radius: 12px;
    border: 1px solid #E9ECEF;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# HERO
# ============================================================
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
    <div class="kpi kpi-red">
        <div class="number">3.1x</div>
        <div class="label">Placement Multiplier<br>(brand-adjusted)</div>
    </div>
    <div class="kpi kpi-dark">
        <div class="number">-56%</div>
        <div class="label">Potential Lost<br>by non-placed apps</div>
    </div>
    <div class="kpi kpi-green">
        <div class="number">9:1</div>
        <div class="label">Partner ROI<br>at target price</div>
    </div>
    <div class="kpi kpi-gold">
        <div class="number">EUR 70K-190K</div>
        <div class="label">Recommended Price<br>(Spain-adjusted)</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# CHAPTER 1: THE LANDSCAPE
# ============================================================
st.markdown("""
<div class="chapter">
    <span class="num">Chapter 1</span>
    <h2>The Landscape: 5.38M LG TVs, One Question</h2>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 1])
with col1:
    st.markdown("""
    Spain has **5.38 million active LG Smart TVs** and streaming is the dominant use case.
    HDMI usage has dropped 43% since 2016 as viewers migrate to apps.

    But not all apps are equal on the home screen. **Three global players** pay EUR 300K-400K/year
    for a guaranteed spot on the Launcher Bar. **Two local broadcasters** with millions of
    Spanish users do not.

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

# ============================================================
# CHAPTER 2: THE EVIDENCE
# ============================================================
st.markdown("""
<div class="chapter">
    <span class="num">Chapter 2</span>
    <h2>The Evidence: How Users Actually Access Apps</h2>
</div>
""", unsafe_allow_html=True)

st.markdown("#### Where do app launches come from?")
st.markdown("When an app has placement, users access it through **multiple doors**. Without it, there is only **one way in**.")

fig = go.Figure()
for name, data, color in [
    ('Remote Hot Key', AA_REMOTE, C['remote']),
    ('Launcher', AA_LAUNCHER, C['launcher']),
    ('GIP', AA_GIP, C['gip']),
    ('Home Reco', AA_HOME, C['home']),
    ('Other', AA_OTHER, C['other'])
]:
    fig.add_trace(go.Bar(
        y=APPS, x=data, name=name, orientation='h', marker_color=color,
        text=[f'{v:.1f}%' if v > 2 else '' for v in data],
        textposition='inside', textfont=dict(color='white', size=11)
    ))
fig.update_layout(
    barmode='stack', height=380,
    margin=dict(l=0, r=0, t=10, b=0),
    xaxis_title='% of Total App Access (Avg. Jan-May 2026)',
    legend=dict(orientation='h', y=-0.18, x=0.5, xanchor='center'),
    yaxis=dict(autorange='reversed'),
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="insight-card">
        <h4>Apps WITH Placement</h4>
        <p>Diversify across <strong>3-5 channels</strong>: Remote Hot Key (~38-44%),
        Launcher (~26-46%), GIP (up to 33%), Home Recommendations, and DIAL.</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="insight-card">
        <h4>Apps WITHOUT Placement</h4>
        <p>Depend <strong>93%+</strong> on a single channel: the Launcher. No hot key,
        no GIP, no recommendations. The user must <strong>actively find and install</strong> the app.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("#### But could this just be because Netflix is... Netflix?")
st.markdown("""
<div class="quote-box">
    "Of course Netflix has more users - it is the biggest streaming brand in the world.
    The real question is: <strong>if we remove the brand effect, does placement still matter?</strong>"
</div>
""", unsafe_allow_html=True)

# ============================================================
# CHAPTER 3: THE INSIGHT
# ============================================================
st.markdown("""
<div class="chapter">
    <span class="num">Chapter 3</span>
    <h2>The Insight: Removing the Brand Bias</h2>
</div>
""", unsafe_allow_html=True)

st.markdown("To isolate the **placement effect** from the **brand effect**, we created the **Capture Index**:")

st.markdown("""
<div class="verdict">
    <h3>Capture Index</h3>
    <p>LG TV Penetration (%) / Market Penetration (%)</p>
    <p style="font-size:0.85rem; margin-top:1rem;">
    Index = 1.0 : App performs on LG exactly as its market share predicts<br>
    Index &gt; 1.0 : Placement <strong>amplifies</strong> the app beyond its natural weight<br>
    Index &lt; 1.0 : The app <strong>loses</strong> presence on LG TVs
    </p>
</div>
""", unsafe_allow_html=True)

bar_colors = [C['placed'] if c >= 1 else C['not_placed'] for c in CAP_IDX]
fig = go.Figure()
fig.add_trace(go.Bar(
    y=APPS, x=CAP_IDX, orientation='h', marker_color=bar_colors,
    text=[f'{c:.2f}  ({"+" if c >= 1 else ""}{(c-1)*100:.0f}%)' for c in CAP_IDX],
    textposition='outside', textfont=dict(size=13, color=bar_colors)
))
fig.add_vline(x=1.0, line_dash="dash", line_color="#999", line_width=2,
              annotation_text="Par (1.0)", annotation_font_color="#999")
fig.update_layout(
    height=380, margin=dict(l=0, r=160, t=10, b=0),
    xaxis=dict(title='Capture Index', range=[0, 2.0], gridcolor='#eee'),
    yaxis=dict(autorange='reversed'),
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig, use_container_width=True)

st.markdown(f"""
<div class="verdict">
    <h3>The Verdict</h3>
    <div class="big">{AVG_WITH/AVG_WITHOUT:.1f}x</div>
    <p>Even after removing brand bias, placement multiplies app presence by <strong>3.1x</strong><br>
    Avg. WITH Placement: <strong>{AVG_WITH:.2f}</strong> | Avg. WITHOUT: <strong>{AVG_WITHOUT:.2f}</strong></p>
</div>
""", unsafe_allow_html=True)

st.markdown("#### The gap visualised: Market Share vs. LG Presence")
apps_short = ['Netflix', 'Prime Video', 'Disney+', 'Mediaset Inf.', 'Atresplayer']
fig2 = go.Figure()
fig2.add_trace(go.Bar(
    x=apps_short, y=MKT_PEN, name='Market Penetration',
    marker_color=C['blue'], text=[f'{v:.1f}%' for v in MKT_PEN],
    textposition='outside', textfont=dict(size=11)
))
fig2.add_trace(go.Bar(
    x=apps_short, y=LG_PEN, name='LG TV Penetration',
    marker_color='#E67E22', text=[f'{v:.1f}%' for v in LG_PEN],
    textposition='outside', textfont=dict(size=11)
))
fig2.update_layout(
    barmode='group', height=400,
    margin=dict(l=0, r=0, t=10, b=0),
    yaxis_title='Penetration (%)',
    legend=dict(orientation='h', y=1.08, x=0.5, xanchor='center'),
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
)
fig2.add_annotation(
    x=3, y=max(MKT_PEN[3], LG_PEN[3]) + 5,
    text="Gap = lost<br>potential", showarrow=True,
    arrowhead=2, arrowcolor=C['not_placed'], font=dict(color=C['not_placed'], size=11)
)
st.plotly_chart(fig2, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="insight-card">
        <h4>Mediaset Infinity</h4>
        <p><strong>3.4M users</strong> in Spain (8.7% market penetration),
        but only <strong>4.2%</strong> of LG TVs. Losing <strong>54%</strong> of its potential.</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="insight-card">
        <h4>Atresplayer</h4>
        <p><strong>3.6M users</strong> in Spain (9.2% market penetration),
        but only <strong>3.6%</strong> of LG TVs. Losing <strong>59%</strong> of its potential.</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# CHAPTER 4: THE OPPORTUNITY
# ============================================================
st.markdown("""
<div class="chapter">
    <span class="num">Chapter 4</span>
    <h2>The Opportunity: What Placement Would Unlock</h2>
</div>
""", unsafe_allow_html=True)

st.markdown("If local partners achieved the same Capture Index as placed apps, here is what would happen:")

for app_name, cur, con, opt in [
    ('Mediaset Infinity', 226_400, 468_060, 627_200),
    ('Atresplayer', 192_300, 494_960, 663_046)
]:
    st.markdown(f"#### {app_name}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Current", f"{cur:,.0f}", "No Placement", delta_color="off")
    col2.metric("Conservative", f"{con:,.0f}", f"+{con-cur:,.0f} (+{(con-cur)/cur*100:.0f}%)")
    col3.metric("Optimistic", f"{opt:,.0f}", f"+{opt-cur:,.0f} (+{(opt-cur)/cur*100:.0f}%)")

apps_l = ['Mediaset Infinity', 'Atresplayer']
fig = go.Figure()
for sc, vals, color in [
    ('Current', [226400, 192300], C['not_placed']),
    ('Conservative (Index=1.0)', [468060, 494960], C['gold']),
    ('Optimistic (Index=1.34)', [627200, 663046], C['placed'])
]:
    fig.add_trace(go.Bar(
        y=apps_l, x=vals, name=sc, orientation='h', marker_color=color,
        text=[f'{v:,.0f}' for v in vals], textposition='outside',
        textfont=dict(size=12)
    ))
fig.update_layout(
    barmode='group', height=300,
    margin=dict(l=0, r=140, t=10, b=0),
    xaxis_title='Unique Devices (App UD)',
    yaxis=dict(autorange='reversed'),
    legend=dict(orientation='h', y=-0.25, x=0.5, xanchor='center'),
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig, use_container_width=True)

# ============================================================
# CHAPTER 5: THE PRICE
# ============================================================
st.markdown("""
<div class="chapter">
    <span class="num">Chapter 5</span>
    <h2>The Price: What is Fair for Spain?</h2>
</div>
""", unsafe_allow_html=True)

st.markdown("""
Global platforms pay **EUR 300K-400K/year**. But Spain is not the UK or the US.
We applied **4 valuation methods** and a **25% Spain market discount**.
""")

tab1, tab2 = st.tabs(["Valuation Methods", "Why the Discount?"])

with tab1:
    methods_data = [
        ("Method 1 - Cost per Incremental Device", "EUR 46K - EUR 76K", 46, 76, C['blue'],
         "EUR 350K / 1.88M incremental = EUR 0.19/device. Applied to +242K incremental devices."),
        ("Method 2 - Ad Revenue Value (AVOD)", "EUR 140K - EUR 210K", 140, 210, C['placed'],
         "23.2M incremental sessions x EUR 20 CPM = EUR 1.4M. Fee = 10-15% of incremental revenue."),
        ("Method 3 - Premium Subscription Conversion", "EUR 140K - EUR 210K", 140, 210, C['purple'],
         "24.2K new subs x EUR 3.99 x 12 = EUR 1.16M in sub revenue. Fee = 12-18%."),
        ("Method 4 - Market Proportionality", "EUR 85K - EUR 120K", 85, 120, '#E67E22',
         "Global apps: 14M users = EUR 350K = EUR 0.025/user. Mediaset 3.4M x EUR 0.025 x 1.35 = EUR 115K.")
    ]

    fig = go.Figure()
    for name, range_str, lo, hi, color, _ in methods_data:
        fig.add_trace(go.Bar(
            y=[name], x=[hi - lo], base=[lo], orientation='h',
            marker_color=color, showlegend=False,
            text=f'EUR {lo}K - EUR {hi}K', textposition='inside',
            textfont=dict(color='white', size=12)
        ))
    fig.add_vrect(x0=70, x1=190, fillcolor=C['lg'], opacity=0.07, line_width=0)
    fig.add_vline(x=70, line_dash="dot", line_color=C['lg'], line_width=1)
    fig.add_vline(x=190, line_dash="dot", line_color=C['lg'], line_width=1)
    fig.add_annotation(x=130, y=-0.4, text="Recommended range: EUR 70K - EUR 190K",
                       showarrow=False, font=dict(color=C['lg'], size=12))
    fig.update_layout(
        height=300, margin=dict(l=0, r=0, t=10, b=40),
        xaxis=dict(title='EUR K / year', range=[0, 260]),
        yaxis=dict(autorange='reversed'),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Detail by method")
    for name, range_str, lo, hi, color, desc in methods_data:
        st.markdown(f"""
        <details style="border-left:4px solid {color};">
            <summary>{name} = {range_str}/year</summary>
            <p>{desc}</p>
        </details>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown("""
    <table class="vs-table">
        <tr><th>Factor</th><th>Spain</th><th>UK</th><th>US</th></tr>
        <tr><td>Pay-TV Penetration</td><td class="bad">&lt;45%</td><td>~65%</td><td>~85%</td></tr>
        <tr><td>AVOD/FAST Weekly Reach</td><td><strong>75%</strong> (#1 in EU)</td><td>~45%</td><td>~50%</td></tr>
        <tr><td>SVoD ARPU</td><td class="bad">~EUR 8.2/month</td><td>~EUR 11-12</td><td>~EUR 13-15</td></tr>
        <tr><td>Telco Bundle Dependency</td><td class="bad">41.3%</td><td>~25%</td><td>~15%</td></tr>
        <tr><td>Password Sharing</td><td>13.2%</td><td>~10%</td><td>~8%</td></tr>
        <tr><td>Local Partner Model</td><td>AVOD + EUR 3-4 premium</td><td colspan="2">SVoD EUR 8-16/month</td></tr>
    </table>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="quote-box">
        <strong>Conclusion:</strong> Lower pay-TV adoption, AVOD dominance, lower ARPU, and bundle dependency
        justify a <strong>25% discount</strong> vs. raw valuation and <strong>50-70% discount</strong> vs. global pricing.
    </div>
    """, unsafe_allow_html=True)

st.markdown("#### Recommended Pricing Tiers")
st.markdown("""
<table class="vs-table">
    <tr><th>Tier</th><th>Includes</th><th>Price/Year</th><th>Rationale</th></tr>
    <tr>
        <td><strong>Entry</strong></td><td>Launcher only</td>
        <td class="good"><strong>EUR 70K - EUR 110K</strong></td>
        <td>1st year proof of concept. Trigger competitive dynamics.</td>
    </tr>
    <tr>
        <td><strong>Target</strong></td><td>Launcher</td>
        <td><strong>EUR 110K - EUR 150K</strong></td>
        <td>Fee = 8-11% of incremental ad revenue (EUR 1.4M+).</td>
    </tr>
    <tr>
        <td><strong>Premium</strong></td><td>Launcher + OOBE + Home Reco + Banner</td>
        <td><strong>EUR 150K - EUR 190K</strong></td>
        <td>Maximum visibility at ~50% of global price.</td>
    </tr>
    <tr>
        <td>Ref: Global</td><td>Full package</td>
        <td>EUR 300K - EUR 400K</td>
        <td>What Netflix/Disney+/Prime pay. Ceiling.</td>
    </tr>
</table>
""", unsafe_allow_html=True)

st.markdown("""
<div class="cta-box">
    <h3>Partner ROI: Even at EUR 150K/year the incremental ad revenue is EUR 1.4M+ = ROI of 9:1</h3>
    <p>The Launcher Placement pays for itself nearly 10 times over.</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# CHAPTER 6: THE STRATEGY
# ============================================================
st.markdown("""
<div class="chapter">
    <span class="num">Chapter 6</span>
    <h2>The Strategy: How to Close the Deal</h2>
</div>
""", unsafe_allow_html=True)

st.markdown("#### The Domino Effect")
st.markdown("""
Mediaset (Telecinco, Cuatro) and Atresmedia (Antena 3, La Sexta) compete for the **same audience**.
If one gets placement, the other faces an **immediate, measurable disadvantage**.
Present to both simultaneously. The **first mover** wins.
""")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="insight-card" style="border-left-color: #E67E22;">
        <h4 style="color: #E67E22;">Pitch to Mediaset Infinity</h4>
        <p>
        +23% YoY growth in digital users<br>
        3.4M users but only 4.2% LG penetration (losing 54%)<br>
        FIFA Club World Cup rights = maximize reach<br>
        ROI 9:1 at EUR 150K<br>
        Warning: If Atresplayer signs first, you lose ground permanently
        </p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="insight-card" style="border-left-color: #3498DB;">
        <h4 style="color: #3498DB;">Pitch to Atresplayer</h4>
        <p>
        Best visitors since May 2024 (3.2M, +20% YoY)<br>
        3.6M users but only 3.6% LG penetration (losing 59%)<br>
        Most national premieres of any platform<br>
        ROI 8-10:1 at EUR 110-150K<br>
        Warning: If Mediaset enters Launcher, you lose share
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("#### Timeline")
timeline = [
    ("Jun", "June 2026", "Send formal proposal to both partners with this analysis."),
    ("Jul", "July 2026", "Negotiation meetings. Present weighted data and growth scenarios."),
    ("Aug", "August 2026", "Close at least one deal before LaLiga and fall content season."),
    ("Q4", "Q4 2026", "Measure results vs. projections. Build success case for partner #2."),
    ("Q1", "Q1 2027", "Both partners placed. Renegotiate upward. Target DAZN, Movistar+ next.")
]
for dot, title, desc in timeline:
    st.markdown(f"""
    <div class="timeline-item">
        <div class="timeline-dot">{dot}</div>
        <div class="timeline-content">
            <strong>{title}</strong>
            <p>{desc}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# GLOSSARY
# ============================================================
st.markdown("""
<div class="chapter">
    <span class="num">Reference</span>
    <h2>Glossary and Definitions</h2>
</div>
""", unsafe_allow_html=True)

# Acronyms
acr_rows = ""
for acr, defn in [
    ('ARPU', 'Average Revenue Per User.'),
    ('AVOD', 'Advertising-based Video On Demand - free streaming funded by ads.'),
    ('CPM', 'Cost Per Mille - cost per 1,000 ad impressions.'),
    ('CTV', 'Connected TV - internet-connected television.'),
    ('DIAL', 'Discovery and Launch - protocol for casting from phone to TV.'),
    ('FAST', 'Free Ad-Supported Streaming TV.'),
    ('GIP', 'Global Input Priority - auto-launches last-used app on power-on.'),
    ('OOBE', 'Out-Of-Box Experience - first-time TV setup flow.'),
    ('ROI', 'Return On Investment.'),
    ('SVoD', 'Subscription Video On Demand.'),
    ('TDT', 'Television Digital Terrestre - Spain free-to-air system.'),
    ('UD', 'Unique Devices.'),
    ('webOS', 'LG Smart TV operating system (since 2014).'),
    ('YoY', 'Year-over-Year comparison.')
]:
    acr_rows += f"<tr><td><strong>{acr}</strong></td><td style='text-align:left;'>{defn}</td></tr>"

st.markdown(f"""
<details>
    <summary>Acronyms and Abbreviations</summary>
    <table class="vs-table" style="margin-top:0.8rem;">
        <tr><th style="width:120px;">Acronym</th><th>Definition</th></tr>
        {acr_rows}
    </table>
</details>
""", unsafe_allow_html=True)

# Key Metrics
met_rows = ""
for met, defn in [
    ('App Access', 'Total app launches. 1 device x 10 opens = 10 App Access.'),
    ('App UD', 'Unique devices that launched an app. 1 device x 10 opens = 1 UD.'),
    ('Capture Index', 'LG Penetration / Market Penetration. Above 1.0 = over-performance.'),
    ('Remote Hot Key', 'Dedicated physical button on remote for an app.'),
    ('Launcher', 'Horizontal app strip on webOS home screen.'),
    ('GIP', 'Auto-launch of last-used app on TV power-on.'),
    ('Home Reco', 'Recommended content cards on home screen shelves.'),
    ('DIAL', 'App launch from phone/tablet to TV.'),
    ('Incremental Devices', 'Projected UD with placement minus current UD.')
]:
    met_rows += f"<tr><td><strong>{met}</strong></td><td style='text-align:left;'>{defn}</td></tr>"

st.markdown(f"""
<details>
    <summary>Key Metrics and KPIs</summary>
    <table class="vs-table" style="margin-top:0.8rem;">
        <tr><th style="width:160px;">Metric</th><th>Definition</th></tr>
        {met_rows}
    </table>
</details>
""", unsafe_allow_html=True)

# Industry Terms
term_rows = ""
for term, defn in [
    ('Launcher Placement', 'Paid agreement to pre-install an app on the Launcher Bar by default.'),
    ('Hot Key', 'Physical branded button on remote (e.g., Netflix button).'),
    ('Home Screen Shelves', 'Content recommendation rows above the Launcher Bar.'),
    ('Magic Remote', 'LG pointer remote with mic, scroll wheel and hot keys.'),
    ('Pay-TV', 'Subscription TV (cable/satellite/IPTV).'),
    ('FTA / TDT', 'Free TV via antenna.'),
    ('Telco Bundle', 'Streaming bundled with telecom packages.'),
    ('Revenue Share', 'Partner pays percentage of revenue instead of fixed fee.'),
    ('First Mover Advantage', 'Competitive edge from being first to secure placement.'),
    ('Installed Base', 'Total active LG Smart TVs in a market (Spain: 5.38M).')
]:
    term_rows += f"<tr><td><strong>{term}</strong></td><td style='text-align:left;'>{defn}</td></tr>"

st.markdown(f"""
<details>
    <summary>Industry and Technical Terms</summary>
    <table class="vs-table" style="margin-top:0.8rem;">
        <tr><th style="width:180px;">Term</th><th>Definition</th></tr>
        {term_rows}
    </table>
</details>
""", unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding: 1rem; color: #999; font-size: 0.85rem;">
    LG Electronics Spain | Marketing and Media Department | June 2026 | Confidential<br>
    Data: LG webOS Analytics Jan-May 2026 | GfK DAM 2025 | JustWatch | CNMC | Futuresource
</div>
""", unsafe_allow_html=True)
