import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="LG Launcher Placement Analysis - Spain",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem; font-weight: 700; color: #A50034;
        text-align: center; margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem; color: #666; text-align: center; margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #A50034 0%, #D4004B 100%);
        padding: 1.2rem; border-radius: 12px; color: white; text-align: center;
        box-shadow: 0 4px 15px rgba(165,0,52,0.3);
    }
    .metric-card h2 { font-size: 2rem; margin: 0; }
    .metric-card p { font-size: 0.85rem; margin: 0.3rem 0 0 0; opacity: 0.9; }
    .highlight-box {
        background: #FFF3F5; border-left: 4px solid #A50034;
        padding: 1rem 1.5rem; border-radius: 0 8px 8px 0; margin: 1rem 0;
    }
    .green-box {
        background: #F0FFF4; border-left: 4px solid #2D8A4E;
        padding: 1rem 1.5rem; border-radius: 0 8px 8px 0; margin: 1rem 0;
    }
    div[data-testid="stMetric"] {
        background-color: #F8F9FA; padding: 1rem; border-radius: 10px;
        border: 1px solid #E9ECEF;
    }
</style>
""", unsafe_allow_html=True)

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

COLORS = {
    'placed': '#2D8A4E', 'not_placed': '#C0392B', 'lg_red': '#A50034',
    'remote': '#FF6B6B', 'launcher': '#4ECDC4', 'gip': '#45B7D1',
    'home': '#FFA07A', 'other': '#C0C0C0'
}

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### 📺 Launcher Placement Analysis")
    st.markdown("**Spain | Jan-May 2026**")
    st.markdown("---")
    section = st.radio("Navigate to:", [
        "🏠 Executive Summary",
        "🌍 Market Context",
        "📊 Channel Mix Analysis",
        "🎯 Capture Index",
        "📈 Impact Projection",
        "💰 Valuation & Pricing",
        "🤝 Negotiation Strategy",
        "📖 Glossary"
    ])
    st.markdown("---")
    st.caption("LG Electronics Spain\nMarketing & Media Dept.\nJune 2026 | Confidential")

# ============================================================
# EXECUTIVE SUMMARY
# ============================================================
if section == "🏠 Executive Summary":
    st.markdown('<p class="main-header">Strategic Analysis: Launcher Placement Value</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">LG Smart TVs — Spain | January-May 2026</p>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class="metric-card"><h2>3.1x</h2><p>Placement Multiplier<br>(brand-adjusted)</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="metric-card"><h2>-56%</h2><p>Lost Potential<br>(non-placed apps)</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="metric-card"><h2>€70K-190K</h2><p>Recommended Price<br>(Spain-adjusted)</p></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class="metric-card"><h2>9:1 ROI</h2><p>Partner Return<br>(at target price)</p></div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Key Findings")

    findings = {
        "🔄 3.1x Multiplier": "Even after removing the brand effect, placement multiplies an app's presence on LG TVs by 3.1x (Capture Index: 1.34 with vs. 0.43 without).",
        "📉 Lost Potential": "Mediaset Infinity loses 54% and Atresplayer loses 59% of their potential presence on LG TVs solely due to lack of placement.",
        "🔀 Channel Diversification": "Placed apps access 4-5 traffic channels; non-placed apps depend 93%+ on a single channel (organic Launcher).",
        "📈 Growth Projection": "With placement, Mediaset could grow from ~226K to ~468K-627K unique devices (+107% to +177%).",
        "💰 Fair Price": "€70K-190K/year for local partners (25% Spain market discount), compared to €300K-400K paid by global platforms."
    }
    for title, desc in findings.items():
        with st.expander(title):
            st.write(desc)

    st.markdown("---")
    st.subheader("Apps Analysed")
    df_apps = pd.DataFrame({
        'App': APPS,
        'Placement': ['Yes' if p else 'No' for p in PLACEMENT],
        'Users Spain': [f'{u/1e6:.1f}M' for u in MARKET_USERS],
        'App UD (Jan 2026)': [f'{u:,.0f}' for u in APP_UD_TOTAL],
        'Capture Index': [f'{c:.2f}' for c in CAP_IDX]
    })
    st.dataframe(df_apps, use_container_width=True, hide_index=True)

# ============================================================
# MARKET CONTEXT
# ============================================================
elif section == "🌍 Market Context":
    st.header("🌍 Spanish Streaming Market Context")

    tab1, tab2, tab3 = st.tabs(["📺 LG TV Base", "🎬 Streaming Landscape", "🇪🇸 Spain vs Anglo-Saxon"])

    with tab1:
        col1, col2, col3 = st.columns(3)
        col1.metric("LG TVs in Spain", "5.38M", "Active Smart TVs")
        col2.metric("Smart TV Penetration", "64%", "14x growth since 2013")
        col3.metric("HDMI Usage Decline", "-43%", "EU5 since 2016")
        st.info("📊 Source: LG Ad Solutions, February 2025")

    with tab2:
        st.metric("Paid Streaming Households", "63.1%", "of internet households (CNMC Q2 2025)")
        df_mkt = pd.DataFrame({
            'Platform': APPS,
            'Users Spain': [f'{u/1e6:.1f}M' for u in MARKET_USERS],
            'Market Share (JustWatch Q4 2025)': ['23%', '18%', '17%', '2%', '<2%'],
            'LG Placement': ['Yes' if p else 'No' for p in PLACEMENT],
            'Hot Key': ['Yes' if p else 'No' for p in PLACEMENT]
        })
        st.dataframe(df_mkt, use_container_width=True, hide_index=True)

    with tab3:
        st.subheader("Why a 25% Spain Market Discount is Justified")
        comparison = pd.DataFrame({
            'Factor': ['Pay-TV Penetration', 'FAST/AVoD Weekly Reach', 'SVoD ARPU (monthly)',
                       'Bundle Dependency', 'Password Sharing', 'Local Partner Model'],
            'Spain': ['<45%', '75% (highest in EU)', '~€8.2/month',
                      '41.3% via telco bundles', '13.2%', 'AVOD/Free + €3-4 premium'],
            'UK': ['~65%', '~45%', '~€11-12/month', '~25%', '~10%', 'SVoD €8-16/month'],
            'US': ['~85%', '~50%', '~€13-15/month', '~15%', '~8%', 'SVoD €10-18/month']
        })
        st.dataframe(comparison, use_container_width=True, hide_index=True)
        st.markdown("""
        <div class="highlight-box">
            <strong>Conclusion:</strong> A 25% discount vs. raw valuation (and 50-70% discount vs. global app pricing)
            is appropriate for local Spanish partners given the structural differences in the market.
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# CHANNEL MIX ANALYSIS
# ============================================================
elif section == "📊 Channel Mix Analysis":
    st.header("📊 Channel Mix Analysis")

    tab1, tab2, tab3 = st.tabs(["App Access %", "App UD %", "Absolute Reach"])

    with tab1:
        st.subheader("App Access — Channel Distribution (Avg. Jan-May 2026)")
        fig = go.Figure()
        channels_data = [
            ('Remote Hot Key', AA_REMOTE, COLORS['remote']),
            ('Launcher', AA_LAUNCHER, COLORS['launcher']),
            ('GIP', AA_GIP, COLORS['gip']),
            ('Home Reco', AA_HOME, COLORS['home']),
            ('Other', AA_OTHER, COLORS['other'])
        ]
        for name, data, color in channels_data:
            fig.add_trace(go.Bar(
                y=APPS, x=data, name=name, orientation='h',
                marker_color=color,
                text=[f'{v:.1f}%' if v > 2 else '' for v in data],
                textposition='inside', textfont=dict(color='white', size=11)
            ))
        fig.update_layout(
            barmode='stack', height=400, margin=dict(l=0, r=0, t=30, b=0),
            xaxis_title='% of Total App Access',
            legend=dict(orientation='h', y=-0.15),
            yaxis=dict(autorange='reversed')
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        **Key Observations:**
        - Non-placed apps depend **93%+** on Launcher as their sole access channel
        - Placed apps diversify across **3-5 channels**: Remote Hot Key (~38-44%), Launcher (~26-46%), GIP (up to 33%)
        - Search (Text + Voice + Command) accounts for **<1%** of traffic for ALL apps
        """)

    with tab2:
        st.subheader("App UD — Unique Devices by Channel (Avg. Jan-May 2026)")
        channels_ud = {
            'Remote Hot Key': UD_REMOTE, 'Launcher': UD_LAUNCHER,
            'GIP': UD_GIP, 'Home Reco': UD_HOME, 'Other': UD_OTHER
        }
        color_map = {
            'Remote Hot Key': COLORS['remote'], 'Launcher': COLORS['launcher'],
            'GIP': COLORS['gip'], 'Home Reco': COLORS['home'], 'Other': COLORS['other']
        }
        rows = []
        for ch_name, ch_data in channels_ud.items():
            for i, app in enumerate(APPS):
                rows.append({'App': app, 'Channel': ch_name, 'Percentage': ch_data[i]})
        df_ud = pd.DataFrame(rows)
        fig2 = px.bar(
            df_ud, y='App', x='Percentage', color='Channel', orientation='h',
            barmode='group', color_discrete_map=color_map,
            text=df_ud['Percentage'].apply(lambda x: f'{x:.1f}%' if x > 2 else '')
        )
        fig2.update_layout(
            height=500, margin=dict(l=0, r=0, t=30, b=0),
            yaxis=dict(autorange='reversed'), xaxis_title='% of Unique Devices',
            legend=dict(orientation='h', y=-0.15)
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.info("A single device can use multiple channels, so percentages do not sum to 100%.")

    with tab3:
        st.subheader("Absolute Reach — Unique Devices via Launcher (January 2026)")
        bar_colors = [COLORS['placed'] if p else COLORS['not_placed'] for p in PLACEMENT]
        fig3 = go.Figure(go.Bar(
            y=APPS, x=UD_LAUNCHER_JAN, orientation='h',
            marker_color=bar_colors,
            text=[f'{v:,.0f}' for v in UD_LAUNCHER_JAN],
            textposition='outside', textfont=dict(size=12)
        ))
        fig3.update_layout(
            height=400, margin=dict(l=0, r=120, t=30, b=0),
            xaxis_title='Unique Devices (App UD)',
            yaxis=dict(autorange='reversed')
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("🟢 = With Placement | 🔴 = Without Placement")

# ============================================================
# CAPTURE INDEX
# ============================================================
elif section == "🎯 Capture Index":
    st.header("🎯 Weighted Analysis: Isolating Placement from Brand Effect")

    with st.expander("📐 Methodology", expanded=True):
        st.markdown("""
        **Capture Index** = LG TV Penetration (%) / Market Penetration (%)

        | Concept | Formula |
        |---|---|
        | **LG Penetration** | App UD / LG TV Base (5.38M) |
        | **Market Penetration** | Platform Users / Adult Population (~39M) |
        | **Index = 1.0** | App captures on LG exactly what its market share predicts |
        | **Index > 1.0** | Over-performance — placement amplifies presence |
        | **Index < 1.0** | Under-performance — app loses relative presence |
        """)

    col1, col2, col3 = st.columns(3)
    col1.metric("Avg. WITH Placement", f"{AVG_WITH:.2f}", f"+{(AVG_WITH-1)*100:.0f}%")
    col2.metric("Avg. WITHOUT Placement", f"{AVG_WITHOUT:.2f}", f"{(AVG_WITHOUT-1)*100:.0f}%")
    col3.metric("Multiplier", f"{AVG_WITH/AVG_WITHOUT:.1f}x", "Placement effect")

    bar_colors = [COLORS['placed'] if c >= 1 else COLORS['not_placed'] for c in CAP_IDX]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=APPS, x=CAP_IDX, orientation='h', marker_color=bar_colors,
        text=[f'{c:.2f} ({"+" if c>=1 else ""}{(c-1)*100:.0f}%)' for c in CAP_IDX],
        textposition='outside', textfont=dict(size=12)
    ))
    fig.add_vline(x=1.0, line_dash="dash", line_color="#333", annotation_text="Par (1.0)")
    fig.update_layout(
        height=400, margin=dict(l=0, r=150, t=30, b=0),
        xaxis_title='Capture Index', xaxis_range=[0, 2.0],
        yaxis=dict(autorange='reversed')
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Market vs. LG TV Penetration")
    df_pen = pd.DataFrame({
        'App': APPS * 2,
        'Penetration (%)': MKT_PEN + LG_PEN,
        'Type': ['Market Penetration'] * 5 + ['LG TV Penetration'] * 5
    })
    fig2 = px.bar(
        df_pen, y='App', x='Penetration (%)', color='Type', orientation='h', barmode='group',
        color_discrete_map={'Market Penetration': '#3498DB', 'LG TV Penetration': '#E67E22'},
        text=df_pen['Penetration (%)'].apply(lambda x: f'{x:.1f}%')
    )
    fig2.update_layout(height=400, yaxis=dict(autorange='reversed'), legend=dict(orientation='h', y=-0.15))
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Detailed Results")
    df_res = pd.DataFrame({
        'App': APPS,
        'Placement': ['Yes' if p else 'No' for p in PLACEMENT],
        'Total App UD': [f'{u:,.0f}' for u in APP_UD_TOTAL],
        'LG Penetration': [f'{p:.1f}%' for p in LG_PEN],
        'Users Spain': [f'{u/1e6:.1f}M' for u in MARKET_USERS],
        'Market Penetration': [f'{p:.1f}%' for p in MKT_PEN],
        'Capture Index': [f'{c:.2f}' for c in CAP_IDX],
        'Differential': [f'{"+" if (c-1)*100>0 else ""}{(c-1)*100:.0f}%' for c in CAP_IDX]
    })
    st.dataframe(df_res, use_container_width=True, hide_index=True)

# ============================================================
# IMPACT PROJECTION
# ============================================================
elif section == "📈 Impact Projection":
    st.header("📈 Impact Projection for Local Partners")

    current = {'Mediaset Infinity': 226_400, 'Atresplayer': 192_300}
    conservative = {'Mediaset Infinity': 468_060, 'Atresplayer': 494_960}
    optimistic = {'Mediaset Infinity': 627_200, 'Atresplayer': 663_046}

    for app_name in ['Mediaset Infinity', 'Atresplayer']:
        st.subheader(f"📱 {app_name}")
        cur = current[app_name]
        con = conservative[app_name]
        opt = optimistic[app_name]
        col1, col2, col3 = st.columns(3)
        col1.metric("Current (No Placement)", f"{cur:,.0f}", "Baseline")
        col2.metric("Conservative (Index=1.0)", f"{con:,.0f}", f"+{con-cur:,.0f} (+{(con-cur)/cur*100:.0f}%)")
        col3.metric("Optimistic (Index=1.34)", f"{opt:,.0f}", f"+{opt-cur:,.0f} (+{(opt-cur)/cur*100:.0f}%)")

    apps_local = ['Mediaset Infinity', 'Atresplayer']
    scenarios = ['Current', 'Conservative', 'Optimistic']
    values = [[226400, 468060, 627200], [192300, 494960, 663046]]
    colors_sc = ['#C0392B', '#F39C12', '#2D8A4E']

    fig = go.Figure()
    for j, sc in enumerate(scenarios):
        fig.add_trace(go.Bar(
            y=apps_local, x=[values[i][j] for i in range(2)],
            name=sc, orientation='h', marker_color=colors_sc[j],
            text=[f'{values[i][j]:,.0f}' for i in range(2)],
            textposition='outside'
        ))
    fig.update_layout(
        barmode='group', height=350, xaxis_title='Unique Devices (App UD)',
        yaxis=dict(autorange='reversed'), legend=dict(orientation='h', y=-0.2)
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# VALUATION & PRICING
# ============================================================
elif section == "💰 Valuation & Pricing":
    st.header("💰 Launcher Placement Valuation")

    st.info("Global platforms (Netflix, Disney+, Prime Video) pay **€300K-400K/year**. Local partners need adjusted pricing.")

    tab1, tab2, tab3 = st.tabs(["📊 4 Methodologies", "🇪🇸 Spain Discount", "🎯 Recommended Pricing"])

    with tab1:
        methods = [
            ("Method 1: Cost per Incremental Device", "€46K - €76K", 46, 76,
             "Implicit cost: €350K / 1.88M incremental devices = €0.19/device. Applied to Mediaset's +242K incremental."),
            ("Method 2: Ad Revenue Value (AVOD)", "€140K - €210K", 140, 210,
             "242K incremental devices x 8 sessions x 12 months x 3.5 ads x €20 CPM = €1.4M. Fee = 10-15%."),
            ("Method 3: Premium Subscription Conversion", "€140K - €210K", 140, 210,
             "242K x 10% conversion x €3.99/month x 12 = €1.16M in sub revenue. Fee = 12-18%."),
            ("Method 4: Market Proportionality", "€85K - €120K", 85, 120,
             "Global apps: 14M users -> €350K -> €0.025/user. Mediaset 3.4M x €0.025 x 1.35 adj = ~€115K.")
        ]
        for name, range_str, lo, hi, explanation in methods:
            with st.expander(f"**{name}** -> {range_str}/year"):
                st.write(explanation)

        fig = go.Figure()
        method_names = [m[0] for m in methods]
        lows = [m[2] for m in methods]
        highs = [m[3] for m in methods]
        colors_m = ['#3498DB', '#2ECC71', '#9B59B6', '#E67E22']
        for i in range(4):
            fig.add_trace(go.Bar(
                y=[method_names[i]], x=[highs[i]-lows[i]], base=[lows[i]],
                orientation='h', marker_color=colors_m[i], name=method_names[i],
                text=f'€{lows[i]}K - €{highs[i]}K', textposition='inside',
                textfont=dict(color='white', size=11), showlegend=False
            ))
        fig.update_layout(
            height=250, xaxis_title='EUR K / year',
            margin=dict(l=0, r=0, t=10, b=0),
            yaxis=dict(autorange='reversed')
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Spain Market Discount: -25%")
        df_disc = pd.DataFrame({
            'Methodology': ['Cost per Incremental Device', 'Ad Revenue Value', 'Premium Sub Conversion',
                           'Market Proportionality', 'Weighted Average'],
            'Raw Range': ['€46K-€76K', '€140K-€210K', '€140K-€210K', '€85K-€120K', '€103K-€154K'],
            'After 25% Discount': ['€35K-€57K', '€105K-€158K', '€105K-€158K', '€64K-€90K', '€77K-€116K']
        })
        st.dataframe(df_disc, use_container_width=True, hide_index=True)

        st.markdown("""
        **Discount justification:**
        - Pay-TV penetration: Spain <45% vs UK ~65%, US ~85%
        - AVOD dominance: 75% consume free content weekly (highest in EU)
        - SVoD ARPU: ~€8.2/month vs UK ~€11-12, US ~€13-15
        - Bundle dependency: 41.3% via telco bundles
        - Local partner model: AVOD/freemium, not premium SVoD
        """)

    with tab3:
        st.subheader("Recommended Pricing Range (Spain-Adjusted)")
        df_price = pd.DataFrame({
            'Tier': ['Entry (1st Year)', 'Target (Steady State)', 'Premium (Full Bundle)', 'Ref: Global Apps'],
            'Range': ['€70K-€110K/year', '€110K-€150K/year', '€150K-€190K/year', '€300K-€400K/year'],
            'Includes': ['Launcher only', 'Launcher', 'Launcher + OOBE + Home Reco + Banner', 'Full package'],
            'Rationale': ['Close 1st local partner. Proof of concept.',
                         'Fee = 8-11% of incremental ad revenue.',
                         'Max visibility at ~50% of global price.',
                         'What Netflix/Disney+/Prime pay. Ceiling.']
        })
        st.dataframe(df_price, use_container_width=True, hide_index=True)

        st.markdown("""
        <div class="green-box">
            <strong>💰 Partner ROI:</strong> Even at €150K/year, the incremental ad revenue potential is
            <strong>€1.4M+</strong> → <strong>ROI = 9:1</strong>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# NEGOTIATION STRATEGY
# ============================================================
elif section == "🤝 Negotiation Strategy":
    st.header("🤝 Recommended Negotiation Strategy")

    tab1, tab2, tab3, tab4 = st.tabs(["🔄 Domino Effect", "📦 Product Tiers", "🎯 Partner Arguments", "📅 Timeline"])

    with tab1:
        st.subheader("Competitive Dynamics: The Domino Effect")
        st.write("""
        **Mediaset** (Telecinco, Cuatro) and **Atresmedia** (Antena 3, La Sexta) are direct competitors
        for the same generalist audience in Spain. If one secures Launcher Placement, the other faces
        an immediate, measurable competitive disadvantage.
        """)
        st.markdown("""
        <div class="highlight-box">
            <strong>Recommendation:</strong> Present to both simultaneously, making it clear that slots are limited.
            The <strong>"first mover"</strong> gains a significant and lasting competitive advantage.
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        df_tiers = pd.DataFrame({
            'Tier': ['Basic', 'Standard', 'Premium'],
            'Includes': ['Launcher Placement', 'Launcher + OOBE', 'Launcher + OOBE + Home Reco + Banner'],
            'Price': ['€70K-€110K/year', '€130K-€170K/year', '€170K-€210K/year'],
            'Best For': ['Year 1 proof of concept', 'Capture users from first TV setup',
                        'Maximum visibility at ~50% global price']
        })
        st.dataframe(df_tiers, use_container_width=True, hide_index=True)

    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📺 Mediaset Infinity")
            st.markdown("""
            - **+23% YoY** digital users (2025)
            - 3.4M users but only **4.2% LG penetration** — losing >50% potential
            - **FIFA Club World Cup** rights maximize reach
            - **ROI: 9:1** (€150K fee vs €1.4M incremental revenue)
            - If Atresplayer signs first, Mediaset loses ground permanently
            """)
        with col2:
            st.subheader("📺 Atresplayer")
            st.markdown("""
            - Best visitors since May 2024 (**3.2M Jan 2026, +20% YoY**)
            - 3.6M users, only **3.6% LG penetration** — most disadvantaged (Index 0.41)
            - **Most national premieres** of any platform
            - **ROI: 8-10:1** (€110-150K fee vs €1.2-1.5M revenue)
            - If Mediaset enters Launcher, Atresplayer loses share
            """)

    with tab4:
        st.subheader("Recommended Timeline")
        timeline = pd.DataFrame({
            'When': ['June 2026', 'July 2026', 'August 2026', 'Q4 2026', 'Q1 2027'],
            'Action': [
                'Send formal proposal to both partners',
                'Negotiation meetings with weighted data & growth scenarios',
                'Close at least one deal before LaLiga season',
                'Measure results vs. projections. Build success case.',
                'Both partners placed. Target DAZN, Movistar+ next.'
            ]
        })
        st.dataframe(timeline, use_container_width=True, hide_index=True)

# ============================================================
# GLOSSARY
# ============================================================
elif section == "📖 Glossary":
    st.header("📖 Glossary & Definitions")

    tab1, tab2, tab3 = st.tabs(["🔤 Acronyms", "📏 Metrics & KPIs", "🏭 Industry Terms"])

    with tab1:
        st.subheader("A.1 Acronyms & Abbreviations")
        acronyms = {
            'ARPU': 'Average Revenue Per User — avg revenue generated per user over a given period.',
            'AVOD': 'Advertising-based Video On Demand — free streaming funded by ads (e.g., Pluto TV).',
            'CPA': 'Cost Per Acquisition — pricing model where advertiser pays per completed action.',
            'CPM': 'Cost Per Mille — cost per 1,000 ad impressions.',
            'CTV': 'Connected TV — any TV connected to the internet for streaming.',
            'DIAL': 'Discovery and Launch protocol — allows phones/tablets to discover and launch apps on a TV.',
            'EU5': 'Europe Big 5 — UK, Germany, France, Italy, Spain.',
            'FAST': 'Free Ad-Supported Streaming TV — linear-style free channels (e.g., Pluto TV, Samsung TV Plus).',
            'GIP': 'Global Input Priority — LG webOS feature that auto-launches the last-used app on power-on.',
            'HDMI': 'High-Definition Multimedia Interface — physical cable for external devices.',
            'HQ / EHQ': 'Headquarters (Seoul) / European Headquarters (UK).',
            'KPI': 'Key Performance Indicator.',
            'OOBE': 'Out-Of-Box Experience — initial TV setup flow with app recommendations.',
            'ROI': 'Return On Investment — ratio of profit to cost.',
            'SVoD': 'Subscription Video On Demand — paid streaming (Netflix, Disney+, etc.).',
            'TDT': "Television Digital Terrestre — Spain's free-to-air digital TV system.",
            'UD': 'Unique Devices — number of distinct TV sets that performed an action.',
            'webOS': "LG's proprietary Smart TV operating system (since 2014).",
            'YoY': 'Year-over-Year — comparison between same period in consecutive years.'
        }
        df_acr = pd.DataFrame({'Acronym': acronyms.keys(), 'Definition': acronyms.values()})
        st.dataframe(df_acr, use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("A.2 Key Metrics & KPIs")
        metrics = {
            'App Access': 'Total app launches on LG TVs. One device opening Netflix 10x = 10 App Access.',
            'App UD': 'Unique Devices that launched an app at least once. 10 opens = 1 App UD.',
            'App Access - Remote Hot Key': 'Launches via dedicated physical button on remote.',
            'App Access - Launcher': 'Launches via clicking icon in the webOS Launcher Bar.',
            'App Access - Text Search': 'Launches from typing in universal search.',
            'App Access - Voice Search': 'Launches from voice query via Magic Remote mic.',
            'App Access - Voice Command': 'Direct voice instruction (e.g., "Open Netflix").',
            'App Access - GIP': 'Auto-launch via Global Input Priority on power-on.',
            'App Access - DIAL': 'Launch from external device (phone casting).',
            'App Access - Home Reco': 'Launch from Home screen recommended content cards.',
            'Capture Index': 'LG Penetration / Market Penetration. >1.0 = over-performance.',
            'LG TV Penetration': 'App UD / LG Base (5.38M).',
            'Market Penetration': 'Platform Users / Adult Population (~39M).',
            'Incremental Devices': 'Projected App UD (with placement) minus Current App UD.'
        }
        df_met = pd.DataFrame({'Metric': metrics.keys(), 'Definition': metrics.values()})
        st.dataframe(df_met, use_container_width=True, hide_index=True)

    with tab3:
        st.subheader("A.3 Industry & Technical Terms")
        terms = {
            'Launcher / Launcher Bar': 'Horizontal strip of app icons at bottom of webOS home screen.',
            'Launcher Placement': 'Paid agreement to pre-install and pin an app on the Launcher by default.',
            'Home Screen Shelves': 'Horizontal rows of recommended content above the Launcher Bar.',
            'Hot Key': 'Dedicated physical button on remote branded with an app logo.',
            'LG Content Store': 'Built-in app marketplace on LG webOS TVs.',
            'Magic Remote': "LG pointer-style remote with mic, scroll wheel & hot keys.",
            'Pay-TV': 'Subscription TV services (cable/satellite/IPTV).',
            'Free-to-Air (FTA)': 'Free TV via antenna (TDT in Spain, Freeview in UK).',
            'Telco Bundle': 'Streaming included in telecom packages (e.g., Movistar Fusion).',
            'Revenue Share': 'Partner pays % of revenue to TV manufacturer instead of fixed fee.',
            'First Mover Advantage': 'Benefit of being the first local partner to secure placement.',
            'Installed Base': 'Total active LG Smart TVs in a market (Spain: 5.38M).'
        }
        df_terms = pd.DataFrame({'Term': terms.keys(), 'Definition': terms.values()})
        st.dataframe(df_terms, use_container_width=True, hide_index=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption("📺 LG Electronics Spain | Marketing & Media Department | June 2026 | Confidential")
