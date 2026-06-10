import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.set_page_config(page_title="LG Launcher Placement", page_icon="TV", layout="wide", initial_sidebar_state="collapsed")

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
C = {'placed':'#2D8A4E','not_placed':'#C0392B','lg':'#A50034','remote':'#FF6B6B','launcher':'#4ECDC4','gip':'#45B7D1','home':'#FFA07A','other':'#C0C0C0','dark':'#1a1a2e','gold':'#F39C12','blue':'#3498DB','purple':'#9B59B6'}

CHAPTERS = ["Cover","The Landscape","The Evidence","The Insight","The Opportunity","The Price","The Strategy","Glossary"]
TOTAL = len(CHAPTERS)

# ============================================================
# SESSION STATE
# ============================================================
if "ch" not in st.session_state:
    st.session_state.ch = 0
def go_next():
    if st.session_state.ch < TOTAL - 1: st.session_state.ch += 1
def go_prev():
    if st.session_state.ch > 0: st.session_state.ch -= 1
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

/* Hero */
.hero { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); padding: 4rem 2rem 3rem 2rem; border-radius: 24px; text-align: center; margin-bottom: 2rem; position: relative; overflow: hidden; }
.hero::before { content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle, rgba(165,0,52,0.12) 0%, transparent 50%); }
.hero h1 { color: white; font-size: 2.6rem; font-weight: 800; margin: 0; line-height: 1.25; position: relative; }
.hero .accent { color: #FF6B6B; }
.hero p { color: rgba(255,255,255,0.65); font-size: 1.05rem; margin-top: 1rem; position: relative; line-height: 1.7; }
.hero .tag { display: inline-block; background: rgba(165,0,52,0.3); color: #FF6B6B; padding: 0.3rem 1rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600; margin-bottom: 1.5rem; position: relative; border: 1px solid rgba(165,0,52,0.5); letter-spacing: 1px; }

/* KPI cards */
.kpi-row { display: flex; gap: 1rem; margin: 2rem 0; flex-wrap: wrap; }
.kpi { flex: 1; min-width: 140px; padding: 1.5rem 1rem; border-radius: 16px; text-align: center; }
.kpi-red { background: linear-gradient(135deg, #A50034, #D4004B); color: white; box-shadow: 0 8px 25px rgba(165,0,52,0.25); }
.kpi-dark { background: linear-gradient(135deg, #1a1a2e, #16213e); color: white; box-shadow: 0 8px 25px rgba(26,26,46,0.25); }
.kpi-green { background: linear-gradient(135deg, #2D8A4E, #27ae60); color: white; box-shadow: 0 8px 25px rgba(45,138,78,0.25); }
.kpi-gold { background: linear-gradient(135deg, #F39C12, #e67e22); color: white; box-shadow: 0 8px 25px rgba(243,156,18,0.25); }
.kpi .number { font-size: 2rem; font-weight: 800; margin: 0; }
.kpi .label { font-size: 0.78rem; opacity: 0.85; margin-top: 0.4rem; line-height: 1.4; }

/* Chapter banner */
.ch-banner { background: linear-gradient(135deg, #1a1a2e, #0f3460); padding: 1.8rem 2rem; border-radius: 16px; margin-bottom: 2rem; }
.ch-banner .num { color: #FF6B6B; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 2.5px; margin-bottom: 0.3rem; }
.ch-banner h2 { color: white; font-size: 1.7rem; font-weight: 700; margin: 0; }

/* Cards */
.insight-card { background: #f8f9fa; border-radius: 16px; padding: 1.5rem; margin: 1rem 0; border-left: 5px solid #A50034; transition: transform 0.2s; }
.insight-card:hover { transform: translateX(4px); }
.insight-card h4 { color: #A50034; margin: 0 0 0.5rem 0; font-size: 1rem; }
.insight-card p { color: #444; margin: 0; font-size: 0.92rem; line-height: 1.65; }

/* Verdict */
.verdict { background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%); padding: 2rem; border-radius: 16px; color: white; text-align: center; margin: 2rem 0; }
.verdict h3 { font-size: 1.3rem; margin: 0 0 0.3rem 0; opacity: 0.8; }
.verdict .big { font-size: 3.5rem; font-weight: 800; color: #FF6B6B; }
.verdict p { opacity: 0.75; margin-top: 0.5rem; font-size: 0.9rem; }

/* Boxes */
.quote-box { background: #FFF3F5; border-left: 5px solid #A50034; padding: 1.2rem 1.5rem; border-radius: 0 12px 12px 0; margin: 1.5rem 0; font-style: italic; color: #333; line-height: 1.6; }
.cta-box { background: linear-gradient(135deg, #2D8A4E, #27ae60); padding: 1.5rem 2rem; border-radius: 16px; color: white; text-align: center; margin: 2rem 0; box-shadow: 0 8px 25px rgba(45,138,78,0.25); }
.cta-box h3 { margin: 0; font-size: 1.2rem; }
.cta-box p { margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 0.9rem; }
.teaser { background: #f0f0f5; border-radius: 12px; padding: 1.2rem 1.5rem; text-align: center; margin-top: 2rem; color: #555; font-size: 0.95rem; }
.teaser strong { color: #A50034; }

/* Table */
.vs-table { width: 100%; border-collapse: separate; border-spacing: 0; border-radius: 12px; overflow: hidden; margin: 1rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.07); }
.vs-table th { background: #1a1a2e; color: white; padding: 0.75rem 1rem; font-size: 0.82rem; text-align: center; }
.vs-table td { padding: 0.65rem 1rem; text-align: center; border-bottom: 1px solid #eee; font-size: 0.88rem; }
.vs-table tr:nth-child(even) { background: #f8f9fa; }
.vs-table .good { color: #2D8A4E; font-weight: 700; }
.vs-table .bad { color: #C0392B; font-weight: 700; }

/* Timeline */
.timeline-item { display: flex; gap: 1rem; margin: 1.2rem 0; align-items: flex-start; }
.timeline-dot { min-width: 44px; height: 44px; border-radius: 50%; background: #A50034; color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.8rem; flex-shrink: 0; }
.timeline-content { background: #f8f9fa; padding: 1rem 1.2rem; border-radius: 12px; flex: 1; }
.timeline-content strong { color: #1a1a2e; }
.timeline-content p { color: #555; margin: 0.3rem 0 0 0; font-size: 0.88rem; line-height: 1.5; }

/* Details */
details { background: #f8f9fa; padding: 0.8rem 1.2rem; border-radius: 10px; margin: 0.5rem 0; cursor: pointer; }
details summary { font-weight: 600; font-size: 0.95rem; color: #1a1a2e; list-style: none; }
details summary::before { content: '+ '; color: #A50034; font-weight: 800; font-size: 1.1rem; }
details[open] summary::before { content: '- '; }
details p, details table { margin-top: 0.5rem; }

div[data-testid="stMetric"] { background-color: #F8F9FA; padding: 0.8rem; border-radius: 12px; border: 1px solid #E9ECEF; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### Chapters")
    for i, name in enumerate(CHAPTERS):
        label = f"**{i}. {name}**" if i == ch else f"{i}. {name}"
        if st.button(label, key=f"sb_{i}", use_container_width=True):
            go_to(i)
            st.rerun()
    st.markdown("---")
    st.progress(ch / (TOTAL - 1))
    st.caption(f"Chapter {ch} of {TOTAL-1}")
    st.markdown("---")
    st.caption("LG Electronics Spain\nJune 2026 | Confidential")

# ============================================================
# TOP PROGRESS
# ============================================================
pcol1, pcol2, pcol3 = st.columns([1, 6, 1])
with pcol1:
    st.caption(f"Ch. {ch}/{TOTAL-1}")
with pcol2:
    st.progress(ch / (TOTAL - 1))
with pcol3:
    st.caption(CHAPTERS[ch])


# ############################################################
# CHAPTER 0 — COVER
# ############################################################
if ch == 0:
    st.markdown("""
    <div class="hero">
        <div class="tag">LG ELECTRONICS SPAIN &bull; CONFIDENTIAL &bull; JUNE 2026</div>
        <h1>What happens when your app<br><span class="accent">isn't on the Launcher?</span></h1>
        <p>Every day, 5.38 million LG Smart TVs in Spain wake up and show their users a Launcher Bar.<br>
        Some apps are there by default. Others are not.<br><br>
        This analysis measures the difference — and puts a price on it.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    st.markdown("""
    <div class="kpi-row">
        <div class="kpi kpi-red"><div class="number">3.1x</div><div class="label">Placement Multiplier<br>(brand-adjusted)</div></div>
        <div class="kpi kpi-dark"><div class="number">-56%</div><div class="label">Potential Lost<br>by non-placed apps</div></div>
        <div class="kpi kpi-green"><div class="number">93%+</div><div class="label">Single Channel<br>Dependency</div></div>
        <div class="kpi kpi-gold"><div class="number">EUR 70-190K</div><div class="label">Recommended Price<br>(Spain-adjusted)</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown("")

    st.markdown("""
    This presentation walks you through **7 chapters** of data, insight, and strategy.
    Each chapter builds on the previous one to answer a simple question:

    > **Should local Spanish streaming platforms pay for Launcher Placement on LG TVs — and if so, how much?**

    Use the **Next** button below to begin, or jump to any chapter from the sidebar.
    """)

    st.markdown('<div class="teaser">Next up: <strong>Chapter 1 — The Landscape</strong>. The battlefield where this story takes place.</div>', unsafe_allow_html=True)


# ############################################################
# CHAPTER 1 — THE LANDSCAPE
# ############################################################
elif ch == 1:
    st.markdown("""<div class="ch-banner"><div class="num">Chapter 1 of 7</div><h2>The Landscape: 5.38 Million LG TVs, One Question</h2></div>""", unsafe_allow_html=True)

    st.markdown("""
    Let's start with the basics.

    Spain has **5.38 million active LG Smart TVs**. That is one of the largest connected TV bases in Southern Europe.
    These are not just screens — they are **platforms**. HDMI usage has dropped 43% across the EU5 since 2016.
    The TV itself is now the content hub. And the **Launcher Bar** — that horizontal strip of apps at the bottom
    of every LG TV — is the front door.
    """)

    st.markdown("")

    col1, col2, col3 = st.columns(3)
    col1.metric("LG TVs in Spain", "5.38M", "Active Smart TVs")
    col2.metric("Smart TV Penetration", "64%", "14x growth since 2013")
    col3.metric("HDMI Usage Decline", "-43%", "EU5 since 2016")

    st.markdown("")
    st.markdown("")

    st.markdown("""
    Now here is the crucial part. Not every app gets the same real estate.
    **Three global platforms** — Netflix, Prime Video, and Disney+ — pay between EUR 300K and EUR 400K per year
    for guaranteed Launcher Placement (plus a dedicated button on the remote control).

    **Two major Spanish broadcasters** — Mediaset Infinity and Atresplayer — with millions of users each, **do not**.
    """)

    st.markdown("")

    st.markdown("""
    <table class="vs-table">
        <tr><th>Platform</th><th>Users in Spain</th><th>Launcher Placement</th><th>Remote Hot Key</th></tr>
        <tr><td>Netflix</td><td>14.0M</td><td class="good">Yes</td><td class="good">Yes</td></tr>
        <tr><td>Prime Video</td><td>12.6M</td><td class="good">Yes</td><td class="good">Yes</td></tr>
        <tr><td>Disney+</td><td>6.6M</td><td class="good">Yes</td><td class="good">Yes</td></tr>
        <tr><td>Mediaset Infinity</td><td>3.4M</td><td class="bad">No</td><td class="bad">No</td></tr>
        <tr><td>Atresplayer</td><td>3.6M</td><td class="bad">No</td><td class="bad">No</td></tr>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown("""
    So the question becomes straightforward: **does that placement gap actually matter in the data?**
    Or are the global apps simply bigger brands that would dominate regardless?
    """)

    st.markdown('<div class="teaser">Next: <strong>Chapter 2 — The Evidence</strong>. Let us look at how users actually reach these apps.</div>', unsafe_allow_html=True)


# ############################################################
# CHAPTER 2 — THE EVIDENCE
# ############################################################
elif ch == 2:
    st.markdown("""<div class="ch-banner"><div class="num">Chapter 2 of 7</div><h2>The Evidence: How Users Actually Access Apps</h2></div>""", unsafe_allow_html=True)

    st.markdown("""
    Every time a user opens a streaming app on an LG TV, we can see **which channel** they used to get there:
    the remote's physical button, the Launcher Bar, auto-launch on power-on (GIP), a home screen recommendation, or something else.

    This is where the story gets interesting. When you have placement, users reach your app through **multiple doors**.
    When you don't, there is essentially **one way in** — and the user has to do all the work.
    """)

    st.markdown("")

    view = st.radio("Filter apps:", ["All 5 Apps", "With Placement (Netflix, Prime, Disney+)", "Without Placement (Mediaset, Atresplayer)"], horizontal=True)
    if view.startswith("With"):
        idx = [0, 1, 2]
    elif view.startswith("Without"):
        idx = [3, 4]
    else:
        idx = [0, 1, 2, 3, 4]

    fig = go.Figure()
    for name, data, color in [('Remote Hot Key', AA_R, C['remote']), ('Launcher', AA_L, C['launcher']), ('GIP', AA_G, C['gip']), ('Home Reco', AA_H, C['home']), ('Other', AA_O, C['other'])]:
        fig.add_trace(go.Bar(
            y=[APPS[i] for i in idx], x=[data[i] for i in idx], name=name, orientation='h',
            marker_color=color, text=[f'{data[i]:.1f}%' if data[i] > 2 else '' for i in idx],
            textposition='inside', textfont=dict(color='white', size=11)
        ))
    fig.update_layout(barmode='stack', height=max(220, len(idx)*72), margin=dict(l=0,r=0,t=10,b=0), xaxis_title='% of Total App Access (Avg. Jan-May 2026)', legend=dict(orientation='h', y=-0.22, x=0.5, xanchor='center'), yaxis=dict(autorange='reversed'), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div class="insight-card"><h4>Apps WITH Placement</h4><p>Users arrive through <strong>3 to 5 different channels</strong>. The remote button alone drives 38-44% of opens. The Launcher adds another 26-46%. GIP auto-launch contributes up to 33% for Netflix. The app is everywhere the user looks.</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="insight-card"><h4>Apps WITHOUT Placement</h4><p><strong>93% or more</strong> of all traffic comes from a single channel: the Launcher. No physical button. No auto-launch. No recommendations. The user must remember the app exists, scroll to find it, and actively choose it every single time.</p></div>""", unsafe_allow_html=True)

    st.markdown("")
    st.markdown("")

    st.markdown("""
    The pattern is clear. But there is an obvious objection:
    """)

    st.markdown("""<div class="quote-box">"Of course Netflix gets more traffic — it is the most popular streaming service on the planet. This is not about placement. This is about <strong>brand power</strong>."</div>""", unsafe_allow_html=True)

    st.markdown("""
    Fair point. So how do we separate the brand effect from the placement effect?
    That is exactly what we did in the next chapter.
    """)

    st.markdown('<div class="teaser">Next: <strong>Chapter 3 — The Insight</strong>. We built a metric that removes brand bias entirely.</div>', unsafe_allow_html=True)


# ############################################################
# CHAPTER 3 — THE INSIGHT
# ############################################################
elif ch == 3:
    st.markdown("""<div class="ch-banner"><div class="num">Chapter 3 of 7</div><h2>The Insight: Removing the Brand Bias</h2></div>""", unsafe_allow_html=True)

    st.markdown("""
    To answer the brand vs. placement question, we created a metric called the **Capture Index**.

    The logic is simple: if Netflix has 35.9% of the Spanish adult market, it should naturally capture roughly 35.9%
    of LG TVs too — just by brand gravity. If it captures *more* than that, something is amplifying it.
    If a local app captures *less* than its market share predicts, something is holding it back.
    """)

    st.markdown("")

    st.markdown("""
    <div class="verdict">
        <h3>Capture Index Formula</h3>
        <p style="font-size:1.1rem; margin-top:0.8rem;">LG TV Penetration (%)&nbsp; / &nbsp;Market Penetration (%)</p>
        <p style="font-size:0.85rem; margin-top:1.2rem;">
        Index = 1.0 &rarr; App captures exactly what its brand predicts<br>
        Index &gt; 1.0 &rarr; Something <strong>amplifies</strong> the app beyond its natural weight<br>
        Index &lt; 1.0 &rarr; The app <strong>loses</strong> presence it should otherwise have
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown("Here are the results:")
    st.markdown("")

    bar_colors = [C['placed'] if c >= 1 else C['not_placed'] for c in CI]
    fig = go.Figure()
    fig.add_trace(go.Bar(y=APPS, x=CI, orientation='h', marker_color=bar_colors, text=[f'{c:.2f}  ({"+" if c>=1 else ""}{(c-1)*100:.0f}%)' for c in CI], textposition='outside', textfont=dict(size=13, color=bar_colors)))
    fig.add_vline(x=1.0, line_dash="dash", line_color="#999", line_width=2, annotation_text="Par (1.0)", annotation_font_color="#999")
    fig.update_layout(height=350, margin=dict(l=0,r=160,t=10,b=0), xaxis=dict(title='Capture Index', range=[0,2.0], gridcolor='#eee'), yaxis=dict(autorange='reversed'), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("")

    st.markdown(f"""
    <div class="verdict">
        <h3>The Verdict</h3>
        <div class="big">{AW/AWO:.1f}x</div>
        <p>Even after removing brand bias, placement multiplies an app's presence by <strong>{AW/AWO:.1f}x</strong><br>
        Average WITH placement: <strong>{AW:.2f}</strong>&nbsp; | &nbsp;Average WITHOUT: <strong>{AWO:.2f}</strong></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    st.markdown("#### The gap visualised: what the market gives vs. what LG TVs reflect")
    st.markdown("")

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=APPS, y=MP, name='Market Penetration', marker_color=C['blue'], text=[f'{v:.1f}%' for v in MP], textposition='outside'))
    fig2.add_trace(go.Bar(x=APPS, y=LP, name='LG TV Penetration', marker_color='#E67E22', text=[f'{v:.1f}%' for v in LP], textposition='outside'))
    fig2.update_layout(barmode='group', height=380, margin=dict(l=0,r=0,t=10,b=0), yaxis_title='Penetration (%)', legend=dict(orientation='h', y=1.08, x=0.5, xanchor='center'), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div class="insight-card"><h4>Mediaset Infinity</h4><p><strong>3.4M users</strong> in Spain (8.7% of adults), but only <strong>4.2%</strong> of LG TVs. That is <strong>54% of its potential</strong> simply missing — not because the brand is weak, but because the app lacks visibility.</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="insight-card"><h4>Atresplayer</h4><p><strong>3.6M users</strong> in Spain (9.2% of adults), but only <strong>3.6%</strong> of LG TVs. The most disadvantaged app in our study, <strong>losing 59%</strong> of its potential presence on LG screens.</p></div>""", unsafe_allow_html=True)

    st.markdown("")
    st.markdown("""
    The data is unambiguous. Placement is not just a "nice to have" — it is a **multiplier**.
    So the natural next question is: what would happen if these local apps actually got it?
    """)

    st.markdown('<div class="teaser">Next: <strong>Chapter 4 — The Opportunity</strong>. Interactive projections for Mediaset and Atresplayer.</div>', unsafe_allow_html=True)


# ############################################################
# CHAPTER 4 — THE OPPORTUNITY (INTERACTIVE)
# ############################################################
elif ch == 4:
    st.markdown("""<div class="ch-banner"><div class="num">Chapter 4 of 7</div><h2>The Opportunity: What Placement Would Unlock</h2></div>""", unsafe_allow_html=True)

    st.markdown("""
    Now we move from analysis to projection. If Mediaset Infinity or Atresplayer secured Launcher Placement,
    how many additional devices would they reach?

    Use the slider below to simulate different scenarios. A Capture Index of **1.00** means the app performs
    at par with its market share. The average for placed apps is **1.34** — meaning placement typically
    *over-delivers* by 34%.
    """)

    st.markdown("")

    target_idx = st.slider("Target Capture Index", min_value=0.40, max_value=1.60, value=1.00, step=0.05, format="%.2f", help="1.00 = par with market share. 1.34 = average of placed apps.")

    st.markdown("")

    partner_view = st.radio("Show:", ["Both Partners", "Mediaset Infinity Only", "Atresplayer Only"], horizontal=True)

    partners = {
        'Mediaset Infinity': {'users': 3_400_000, 'current_ud': 226_400},
        'Atresplayer': {'users': 3_600_000, 'current_ud': 192_300}
    }

    if partner_view == "Mediaset Infinity Only":
        show = ['Mediaset Infinity']
    elif partner_view == "Atresplayer Only":
        show = ['Atresplayer']
    else:
        show = ['Mediaset Infinity', 'Atresplayer']

    st.markdown("")

    for name in show:
        p = partners[name]
        mkt_pen = p['users'] / AD * 100
        proj_pen = mkt_pen * target_idx
        proj_ud = int(proj_pen / 100 * LB)
        inc = proj_ud - p['current_ud']
        growth = (inc / p['current_ud'] * 100) if p['current_ud'] > 0 else 0

        st.markdown(f"#### {name}")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Current UD", f"{p['current_ud']:,.0f}", "No Placement", delta_color="off")
        c2.metric("Projected UD", f"{proj_ud:,.0f}", f"+{inc:,.0f}" if inc >= 0 else f"{inc:,.0f}")
        c3.metric("Growth", f"{growth:+,.0f}%", f"Capture Index {target_idx:.2f}")
        c4.metric("New LG Penetration", f"{proj_pen:.1f}%", f"vs {p['current_ud']/LB*100:.1f}% today")
        st.markdown("")

    # Chart
    fig = go.Figure()
    for name in show:
        p = partners[name]
        mkt_pen = p['users'] / AD * 100
        proj_ud = int(mkt_pen * target_idx / 100 * LB)
        fig.add_trace(go.Bar(y=[name + ' (Current)'], x=[p['current_ud']], orientation='h', marker_color=C['not_placed'], text=[f"{p['current_ud']:,.0f}"], textposition='outside', showlegend=False))
        fig.add_trace(go.Bar(y=[name + ' (Projected)'], x=[proj_ud], orientation='h', marker_color=C['placed'], text=[f"{proj_ud:,.0f}"], textposition='outside', showlegend=False))
    fig.update_layout(height=max(200, len(show)*130), margin=dict(l=0,r=140,t=10,b=0), xaxis_title='Unique Devices', yaxis=dict(autorange='reversed'), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("")

    if target_idx >= 1.0:
        st.markdown("""<div class="cta-box"><h3>At this Capture Index, local partners close the gap with their true market potential</h3><p>Every point above 1.0 represents incremental reach that placement delivers beyond brand gravity.</p></div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class="quote-box">At a Capture Index below 1.0, the app is still under-performing relative to its market share. Placement would help close this gap.</div>""", unsafe_allow_html=True)

    st.markdown("")
    st.markdown("The growth potential is significant. But potential is only useful if we can put a fair price on it.")

    st.markdown('<div class="teaser">Next: <strong>Chapter 5 — The Price</strong>. Four valuation methods, one recommendation.</div>', unsafe_allow_html=True)


# ############################################################
# CHAPTER 5 — THE PRICE (INTERACTIVE)
# ############################################################
elif ch == 5:
    st.markdown("""<div class="ch-banner"><div class="num">Chapter 5 of 7</div><h2>The Price: What is Fair for Spain?</h2></div>""", unsafe_allow_html=True)

    st.markdown("""
    Global platforms pay **EUR 300K to EUR 400K per year** for Launcher Placement.
    But Spain is structurally different from the US or UK: lower pay-TV penetration, dominant AVOD consumption,
    lower streaming ARPU, and high telco-bundle dependency.

    We applied **four independent valuation methods** and then adjusted for the Spanish market.
    Explore the result below.
    """)

    st.markdown("")
    st.markdown("#### Interactive Pricing Explorer")
    st.markdown("")

    price = st.slider("Select a price point (EUR K/year)", min_value=50, max_value=300, value=120, step=5)

    if price <= 110:
        tier = "Entry"; tier_c = C['placed']; includes = "Launcher Placement only"; rationale = "First-year proof of concept. Low barrier to trigger competitive dynamics."
    elif price <= 150:
        tier = "Target"; tier_c = C['blue']; includes = "Launcher Placement"; rationale = "Steady-state pricing. Estimated +242K incremental devices, up to EUR 1.4M incremental ad revenue."
    elif price <= 190:
        tier = "Premium"; tier_c = C['purple']; includes = "Launcher + OOBE + Home Reco + Banner"; rationale = "Full visibility package at roughly 50% of what global apps pay."
    else:
        tier = "Above Range"; tier_c = C['gold']; includes = "Approaching global-level package"; rationale = "Nearing what Netflix/Disney+/Prime pay. Maximum anchor."

    discount = round((1 - price / 350) * 100)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Price", f"EUR {price}K/yr")
    col2.metric("Tier", tier)
    col3.metric("vs Global Avg", f"-{discount}%", "below EUR 350K")
    col4.metric("Includes", includes.split("+")[0].strip())

    st.markdown("")

    # Visual position map
    fig = go.Figure()
    fig.add_vrect(x0=70, x1=110, fillcolor=C['placed'], opacity=0.12, line_width=0, annotation_text="Entry", annotation_position="top left", annotation_font_size=10)
    fig.add_vrect(x0=110, x1=150, fillcolor=C['blue'], opacity=0.12, line_width=0, annotation_text="Target", annotation_position="top left", annotation_font_size=10)
    fig.add_vrect(x0=150, x1=190, fillcolor=C['purple'], opacity=0.12, line_width=0, annotation_text="Premium", annotation_position="top left", annotation_font_size=10)
    fig.add_vrect(x0=300, x1=400, fillcolor=C['gold'], opacity=0.08, line_width=0, annotation_text="Global Apps", annotation_position="top left", annotation_font_size=10)
    fig.add_vline(x=price, line_color=C['lg'], line_width=4, annotation_text=f"EUR {price}K", annotation_font_color=C['lg'], annotation_font_size=13)
    fig.update_layout(height=160, margin=dict(l=0,r=0,t=40,b=10), xaxis=dict(title="EUR K / year", range=[0,420]), yaxis=dict(visible=False), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"**Rationale:** {rationale}")
    st.markdown(f"**Package:** {includes}")

    st.markdown("")
    st.markdown("---")
    st.markdown("")

    st.markdown("#### How we arrived at this range")
    st.markdown("")

    methods = [
        ("Method 1 - Cost per Incremental Device", "EUR 46K - EUR 76K", C['blue'], "EUR 350K / 1.88M incremental devices = EUR 0.19 per device. Applied to Mediaset's +242K incremental."),
        ("Method 2 - Ad Revenue Value (AVOD)", "EUR 140K - EUR 210K", C['placed'], "23.2M incremental sessions x EUR 20 CPM = EUR 1.4M in incremental ad revenue. Fee = 10-15% of that value."),
        ("Method 3 - Premium Subscription Conversion", "EUR 140K - EUR 210K", C['purple'], "24.2K new subscribers x EUR 3.99/month x 12 = EUR 1.16M in subscription revenue. Fee = 12-18%."),
        ("Method 4 - Market Proportionality", "EUR 85K - EUR 120K", '#E67E22', "Global apps: 14M users at EUR 350K = EUR 0.025/user. Mediaset 3.4M x 0.025 x 1.35 local adjustment = EUR 115K.")
    ]
    for name, rng, color, desc in methods:
        st.markdown(f"""<details style="border-left:4px solid {color};"><summary>{name} = {rng}/year</summary><p>{desc}</p></details>""", unsafe_allow_html=True)

    st.markdown("")

    st.markdown("""
    <details>
        <summary>Why apply a 25% Spain Market Discount?</summary>
        <table class="vs-table" style="margin-top:0.8rem;">
            <tr><th>Factor</th><th>Spain</th><th>UK</th><th>US</th></tr>
            <tr><td>Pay-TV Penetration</td><td class="bad">&lt;45%</td><td>~65%</td><td>~85%</td></tr>
            <tr><td>AVOD/FAST Weekly Reach</td><td><strong>75%</strong> (#1 in EU)</td><td>~45%</td><td>~50%</td></tr>
            <tr><td>SVoD ARPU</td><td class="bad">~EUR 8.2/mo</td><td>~EUR 11-12</td><td>~EUR 13-15</td></tr>
            <tr><td>Telco Bundle Dependency</td><td class="bad">41.3%</td><td>~25%</td><td>~15%</td></tr>
        </table>
        <p>Lower ARPU, AVOD dominance, and bundle dependency justify a <strong>25% discount</strong> vs. raw valuation.</p>
    </details>
    """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown("Now that we have the data, the insight, and the price — how do we actually close the deal?")

    st.markdown('<div class="teaser">Next: <strong>Chapter 6 — The Strategy</strong>. The playbook for turning analysis into revenue.</div>', unsafe_allow_html=True)


# ############################################################
# CHAPTER 6 — THE STRATEGY
# ############################################################
elif ch == 6:
    st.markdown("""<div class="ch-banner"><div class="num">Chapter 6 of 7</div><h2>The Strategy: How to Close the Deal</h2></div>""", unsafe_allow_html=True)

    st.markdown("""
    The data tells a clear story. Now we need to turn it into action.

    The key dynamic to understand is that **Mediaset and Atresmedia are direct competitors**
    for the same generalist Spanish audience. Telecinco vs. Antena 3. Cuatro vs. La Sexta.
    They fight for the same eyeballs every single day.

    This creates a powerful negotiation lever.
    """)

    st.markdown("")

    st.markdown("""
    <div class="verdict">
        <h3>The Domino Effect</h3>
        <p style="font-size:1rem; margin-top:0.8rem;">If one signs, the other <strong>cannot afford not to</strong>.<br>
        Present to both simultaneously. Make it clear that slots are limited.<br>
        The <strong>first mover</strong> gains a measurable, lasting competitive advantage.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown("#### Tailored Pitch by Partner")
    st.markdown("")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div class="insight-card" style="border-left-color: #E67E22;"><h4 style="color: #E67E22;">Mediaset Infinity</h4><p>
        +23% YoY growth in digital users (2025)<br>
        3.4M users, but only 4.2% LG penetration<br>
        Currently losing 54% of potential reach<br>
        FIFA Club World Cup rights to maximize<br>
        Potential: +242K to +401K incremental devices<br><br>
        <strong>Key message:</strong> "You have the content and the audience. Placement gives you the distribution to match."
        </p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="insight-card" style="border-left-color: #3498DB;"><h4 style="color: #3498DB;">Atresplayer</h4><p>
        Best visitors since May 2024 (3.2M, +20% YoY)<br>
        3.6M users, but only 3.6% LG penetration<br>
        Most disadvantaged: losing 59% of potential<br>
        Most national premieres of any platform<br>
        Potential: +303K to +471K incremental devices<br><br>
        <strong>Key message:</strong> "Your content is premiering nationally. Placement ensures it reaches every LG screen."
        </p></div>""", unsafe_allow_html=True)

    st.markdown("")
    st.markdown("")
    st.markdown("#### Recommended Timeline")
    st.markdown("")

    for dot, title, desc in [
        ("Jun", "June 2026", "Send formal proposal to both partners simultaneously with this analysis as the data backbone."),
        ("Jul", "July 2026", "Negotiation meetings. Walk through weighted data, growth scenarios, and competitive dynamics."),
        ("Aug", "August 2026", "Close at least one deal before LaLiga season and the fall content cycle begin."),
        ("Q4", "Q4 2026", "Measure real results vs. projections. Build a documented success case for partner number two."),
        ("Q1", "Q1 2027", "Both partners placed. Renegotiate upward. Begin outreach to DAZN, Movistar+, and other targets.")
    ]:
        st.markdown(f"""<div class="timeline-item"><div class="timeline-dot">{dot}</div><div class="timeline-content"><strong>{title}</strong><p>{desc}</p></div></div>""", unsafe_allow_html=True)

    st.markdown("")
    st.markdown("")

    st.markdown("""
    <div class="cta-box">
        <h3>The window is now. LaLiga starts in August. Fall content launches in September.</h3>
        <p>Every month without placement is reach that local partners are leaving on the table — and revenue that LG is not capturing.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="teaser">Final section: <strong>Glossary</strong>. Reference definitions for all terms used in this analysis.</div>', unsafe_allow_html=True)


# ############################################################
# CHAPTER 7 — GLOSSARY
# ############################################################
elif ch == 7:
    st.markdown("""<div class="ch-banner"><div class="num">Reference</div><h2>Glossary and Definitions</h2></div>""", unsafe_allow_html=True)

    st.markdown("Click on any section below to expand the full list of definitions.")
    st.markdown("")

    acr_rows = ""
    for a, d in [('ARPU','Average Revenue Per User.'),('AVOD','Advertising-based Video On Demand — free streaming funded by ads.'),('CPM','Cost Per Mille — cost per 1,000 ad impressions.'),('CTV','Connected TV — internet-connected television.'),('DIAL','Discovery and Launch — protocol for casting from phone to TV.'),('FAST','Free Ad-Supported Streaming TV — linear-style free channels.'),('GIP','Global Input Priority — auto-launches last-used app on power-on.'),('OOBE','Out-Of-Box Experience — initial TV setup flow with app recommendations.'),('SVoD','Subscription Video On Demand — paid streaming services.'),('TDT','Television Digital Terrestre — Spain free-to-air digital TV.'),('UD','Unique Devices — number of distinct TVs that performed an action.'),('webOS','LG proprietary Smart TV operating system (since 2014).'),('YoY','Year-over-Year — comparison between same period in consecutive years.')]:
        acr_rows += f"<tr><td><strong>{a}</strong></td><td style='text-align:left;'>{d}</td></tr>"
    st.markdown(f"""<details><summary>Acronyms and Abbreviations</summary><table class="vs-table" style="margin-top:0.8rem;"><tr><th style="width:100px;">Term</th><th>Definition</th></tr>{acr_rows}</table></details>""", unsafe_allow_html=True)

    st.markdown("")

    met_rows = ""
    for m, d in [('App Access','Total app launches on LG TVs. One device opening Netflix 10x = 10 App Access.'),('App UD','Unique Devices that launched an app at least once. 10 opens from 1 device = 1 UD.'),('Capture Index','LG Penetration / Market Penetration. Above 1.0 = over-performance on LG TVs.'),('Remote Hot Key','Launches via the dedicated physical button on the remote control.'),('Launcher','Launches via clicking the app icon in the webOS Launcher Bar.'),('GIP','Auto-launch via Global Input Priority when the TV powers on.'),('Home Reco','Launch from recommended content cards on the home screen.'),('DIAL','Launch triggered from an external device (phone/tablet casting to TV).'),('Incremental Devices','Projected App UD with placement minus current App UD without it.')]:
        met_rows += f"<tr><td><strong>{m}</strong></td><td style='text-align:left;'>{d}</td></tr>"
    st.markdown(f"""<details><summary>Key Metrics and KPIs</summary><table class="vs-table" style="margin-top:0.8rem;"><tr><th style="width:140px;">Metric</th><th>Definition</th></tr>{met_rows}</table></details>""", unsafe_allow_html=True)

    st.markdown("")

    term_rows = ""
    for t, d in [('Launcher Placement','Paid agreement to pre-install and pin an app on the Launcher Bar by default on all LG TVs.'),('Hot Key','Dedicated physical button on the remote control branded with an app logo (e.g., the Netflix button).'),('Home Screen Shelves','Horizontal rows of recommended content displayed above the Launcher Bar.'),('Magic Remote','LG pointer-style remote control with built-in microphone, scroll wheel, and branded hot keys.'),('Pay-TV','Subscription television services delivered via cable, satellite, or IPTV.'),('FTA / TDT','Free-to-air television via antenna. TDT is the Spanish digital terrestrial system.'),('Telco Bundle','Streaming subscriptions included within telecom packages (e.g., Movistar Fusion).'),('Revenue Share','Commercial model where the partner pays a percentage of revenue instead of a fixed annual fee.'),('First Mover Advantage','The competitive edge gained by being the first local partner to secure Launcher Placement.'),('Installed Base','Total number of active LG Smart TVs in a given market. Spain: 5.38 million.')]:
        term_rows += f"<tr><td><strong>{t}</strong></td><td style='text-align:left;'>{d}</td></tr>"
    st.markdown(f"""<details><summary>Industry and Technical Terms</summary><table class="vs-table" style="margin-top:0.8rem;"><tr><th style="width:160px;">Term</th><th>Definition</th></tr>{term_rows}</table></details>""", unsafe_allow_html=True)

    st.markdown("")
    st.markdown("")

    st.markdown("""
    <div style="text-align:center; padding:2rem 1rem; color:#999; font-size:0.85rem; line-height:1.8;">
        LG Electronics Spain | Marketing and Media Department | June 2026 | Confidential<br>
        Data sources: LG webOS Analytics (Jan-May 2026) | GfK DAM 2025 | JustWatch | CNMC | Futuresource | Comscore
    </div>
    """, unsafe_allow_html=True)


# ############################################################
# NAVIGATION
# ############################################################
st.markdown("")
st.markdown("---")

nav1, nav2, nav3 = st.columns([1, 3, 1])
with nav1:
    if ch > 0:
        st.button("Previous Chapter", on_click=go_prev, use_container_width=True)
with nav2:
    label = CHAPTERS[ch]
    next_label = CHAPTERS[ch + 1] if ch < TOTAL - 1 else None
    if next_label:
        st.markdown(f"<p style='text-align:center; color:#aaa; font-size:0.85rem; margin-top:0.5rem;'>You are on <strong>{label}</strong> &nbsp;|&nbsp; Next: <strong>{next_label}</strong></p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p style='text-align:center; color:#aaa; font-size:0.85rem; margin-top:0.5rem;'>You have reached the end. Thank you.</p>", unsafe_allow_html=True)
with nav3:
    if ch < TOTAL - 1:
        st.button("Next Chapter", on_click=go_next, type="primary", use_container_width=True)
