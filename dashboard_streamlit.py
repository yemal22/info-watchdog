#!/usr/bin/env python3
"""
Dashboard Streamlit pour InfoWatchdog
Surveillance en temps réel des données collectées dans Airtable
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import sys
from pathlib import Path
import numpy as np
from collections import Counter
import time

# Configuration de la page
st.set_page_config(
    page_title="🐕‍🦺 InfoWatchdog Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ajoute le chemin src pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# CSS personnalisé pour le thème InfoWatchdog
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #2D8A47 0%, #1E88E5 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #2D8A47;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .watchdog-ascii {
        font-family: monospace;
        font-size: 0.8em;
        color: #2D8A47;
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .status-online {
        color: #28a745;
    }
    .status-offline {
        color: #dc3545;
    }
    .source-reddit {
        color: #FF4500;
    }
    .source-rss {
        color: #FFA500;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)  # Cache pendant 5 minutes
def load_airtable_data():
    """Charge les données depuis Airtable avec cache"""
    try:
        from dotenv import load_dotenv
        from airtable import Airtable
        
        load_dotenv()
        
        airtable = Airtable(
            base_id=os.getenv("AIRTABLE_BASE_ID"),
            table_name=os.getenv("AIRTABLE_TABLE_NAME", "Environmental_News"),
            api_key=os.getenv("AIRTABLE_API_KEY")
        )
        
        records = airtable.get_all()
        
        # Conversion en DataFrame
        data = []
        for record in records:
            fields = record.get('fields', {})
            data.append({
                'id': record.get('id'),
                'title': fields.get('Title', ''),
                'url': fields.get('URL', ''),
                'source': fields.get('Source', 'Unknown'),
                'content': fields.get('Content', ''),
                'author': fields.get('Author', ''),
                'published_date': fields.get('Published_Date', ''),
                'collected_date': fields.get('Collected_Date', ''),
                'collector': fields.get('Collector', 'Unknown'),
                'hash': fields.get('Hash', ''),
                'tags': fields.get('Tags', ''),
                'reddit_score': fields.get('Reddit_Score', 0),
                'reddit_comments': fields.get('Reddit_Comments', 0),
                'subreddit': fields.get('Subreddit', '')
            })
        
        df = pd.DataFrame(data)
        
        # Conversion des dates
        if not df.empty:
            df['collected_date'] = pd.to_datetime(df['collected_date'], errors='coerce')
            df['published_date'] = pd.to_datetime(df['published_date'], errors='coerce')
            
        return df
        
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {str(e)}")
        return pd.DataFrame()

def display_watchdog_header():
    """Affiche l'en-tête avec logo ASCII"""
    st.markdown("""
    <div class="main-header">
        <h1 style="color: white; margin: 0;">🐕‍🦺 InfoWatchdog Dashboard 🌍</h1>
        <p style="color: white; margin: 0.5rem 0 0 0;">Environmental News Guardian - Real-time Monitoring</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Logo ASCII dans une colonne
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="watchdog-ascii">
            🐕‍🦺 InfoWatchdog Environmental Guardian 🌍
            ═══════════════════════════════════════════
                 /\   /\     📡 Real-time Dashboard
                (  ◉.◉  )    🌿 Data Analytics
                 \  ω  /     📊 Always Watching
                  ^^^^       🔍 Live Monitoring
        </div>
        """, unsafe_allow_html=True)

def display_metrics(df):
    """Affiche les métriques principales"""
    if df.empty:
        st.warning("Aucune donnée disponible")
        return
    
    # Calculs des métriques
    total_articles = len(df)
    reddit_articles = len(df[df['collector'] == 'reddit'])
    rss_articles = len(df[df['collector'] == 'rss'])
    
    # Articles des 24 dernières heures
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    recent_articles = len(df[df['collected_date'] > yesterday])
    
    # Articles des 7 derniers jours
    week_ago = now - timedelta(days=7)
    week_articles = len(df[df['collected_date'] > week_ago])
    
    # Affichage des métriques
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="📰 Total Articles",
            value=f"{total_articles:,}",
            delta=f"+{recent_articles} (24h)"
        )
    
    with col2:
        st.metric(
            label="🔴 Reddit",
            value=f"{reddit_articles:,}",
            delta=f"{reddit_articles/total_articles*100:.1f}%" if total_articles > 0 else "0%"
        )
    
    with col3:
        st.metric(
            label="🟠 RSS Feeds",
            value=f"{rss_articles:,}",
            delta=f"{rss_articles/total_articles*100:.1f}%" if total_articles > 0 else "0%"
        )
    
    with col4:
        st.metric(
            label="📅 Cette semaine",
            value=f"{week_articles:,}",
            delta=f"{week_articles/total_articles*100:.1f}%" if total_articles > 0 else "0%"
        )
    
    with col5:
        unique_sources = df['source'].nunique()
        st.metric(
            label="🌐 Sources uniques",
            value=f"{unique_sources}",
            delta="Active"
        )

def create_daily_collection_chart(df):
    """Graphique des collectes quotidiennes"""
    if df.empty:
        return
    
    # Grouper par jour
    df_daily = df.groupby(df['collected_date'].dt.date).size().reset_index()
    df_daily.columns = ['date', 'articles']
    
    # Graphique avec Plotly
    fig = px.line(
        df_daily, 
        x='date', 
        y='articles',
        title='📈 Articles collectés par jour',
        labels={'articles': 'Nombre d\'articles', 'date': 'Date'}
    )
    
    fig.update_traces(
        line_color='#2D8A47',
        line_width=3,
        marker_size=8
    )
    
    fig.update_layout(
        template='plotly_white',
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_sources_pie_chart(df):
    """Graphique en secteurs des sources"""
    if df.empty:
        return
    
    source_counts = df['source'].value_counts()
    
    fig = px.pie(
        values=source_counts.values,
        names=source_counts.index,
        title='📊 Répartition par source',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    
    st.plotly_chart(fig, use_container_width=True)

def create_hourly_heatmap(df):
    """Heatmap des collectes par heure et jour"""
    if df.empty:
        return
    
    # Extraction heure et jour de la semaine
    df['hour'] = df['collected_date'].dt.hour
    df['day_name'] = df['collected_date'].dt.day_name()
    
    # Pivot table pour heatmap
    heatmap_data = df.groupby(['day_name', 'hour']).size().unstack(fill_value=0)
    
    # Ordre des jours
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_data = heatmap_data.reindex(day_order)
    
    fig = px.imshow(
        heatmap_data,
        title='🕐 Activité par heure et jour de la semaine',
        labels=dict(x="Heure", y="Jour", color="Articles"),
        aspect="auto",
        color_continuous_scale='Greens'
    )
    
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

def display_recent_articles(df, limit=10):
    """Affiche les articles récents"""
    if df.empty:
        st.info("Aucun article récent")
        return
    
    recent_df = df.nlargest(limit, 'collected_date')
    
    st.subheader("📰 Articles récents")
    
    for _, article in recent_df.iterrows():
        with st.container():
            col1, col2 = st.columns([4, 1])
            
            with col1:
                # Icône selon la source
                icon = "🔴" if article['collector'] == 'reddit' else "🟠"
                
                st.markdown(f"""
                **{icon} [{article['title'][:100]}...]({article['url']})**
                
                📰 *{article['source']}* • 📅 {article['collected_date'].strftime('%d/%m/%Y %H:%M') if pd.notna(article['collected_date']) else 'N/A'}
                """)
                
                if article['collector'] == 'reddit' and article['reddit_score'] > 0:
                    st.caption(f"⬆️ {article['reddit_score']} points • 💬 {article['reddit_comments']} commentaires • r/{article['subreddit']}")
                
            with col2:
                if article['reddit_score'] > 0:
                    st.metric("Score Reddit", article['reddit_score'])
            
            st.divider()

def display_trending_analysis(df):
    """Analyse des tendances"""
    if df.empty:
        return
    
    st.subheader("🔥 Analyse des tendances")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🏆 Top sources (7 derniers jours)**")
        week_ago = datetime.now() - timedelta(days=7)
        recent_df = df[df['collected_date'] > week_ago]
        
        if not recent_df.empty:
            top_sources = recent_df['source'].value_counts().head(10)
            for source, count in top_sources.items():
                st.write(f"• {source}: **{count}** articles")
        else:
            st.info("Pas de données récentes")
    
    with col2:
        st.write("**📈 Top subreddits Reddit**")
        reddit_df = df[df['collector'] == 'reddit']
        
        if not reddit_df.empty:
            top_subreddits = reddit_df['subreddit'].value_counts().head(10)
            for subreddit, count in top_subreddits.items():
                if subreddit:  # Évite les valeurs vides
                    st.write(f"• r/{subreddit}: **{count}** articles")
        else:
            st.info("Pas de données Reddit")

def display_collection_stats(df):
    """Statistiques de collecte"""
    if df.empty:
        return
    
    st.subheader("📊 Statistiques de collecte")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**⏱️ Activité par période**")
        
        # Articles par période
        now = datetime.now()
        periods = {
            "Aujourd'hui": now - timedelta(days=1),
            "Cette semaine": now - timedelta(days=7),
            "Ce mois": now - timedelta(days=30)
        }
        
        for period_name, cutoff_date in periods.items():
            count = len(df[df['collected_date'] > cutoff_date])
            st.metric(period_name, f"{count:,}")
    
    with col2:
        st.write("**🎯 Performance par collecteur**")
        
        collector_stats = df['collector'].value_counts()
        for collector, count in collector_stats.items():
            percentage = (count / len(df)) * 100
            st.write(f"• {collector.title()}: {count:,} ({percentage:.1f}%)")
    
    with col3:
        st.write("**📈 Scores Reddit moyens**")
        
        reddit_df = df[df['collector'] == 'reddit']
        if not reddit_df.empty and reddit_df['reddit_score'].notna().any():
            avg_score = reddit_df['reddit_score'].mean()
            max_score = reddit_df['reddit_score'].max()
            
            st.metric("Score moyen", f"{avg_score:.1f}")
            st.metric("Score maximum", f"{max_score:,}")
        else:
            st.info("Pas de scores Reddit")

def main():
    """Fonction principale du dashboard"""
    display_watchdog_header()
    
    # Sidebar avec contrôles
    with st.sidebar:
        st.markdown("### 🎛️ Contrôles Dashboard")
        
        # Bouton de rafraîchissement
        if st.button("🔄 Actualiser les données", type="primary"):
            st.cache_data.clear()
            st.rerun()
        
        # Sélection de la période
        period_options = {
            "Toutes les données": None,
            "7 derniers jours": 7,
            "30 derniers jours": 30,
            "90 derniers jours": 90
        }
        
        selected_period = st.selectbox(
            "📅 Période d'analyse",
            options=list(period_options.keys()),
            index=1  # 7 derniers jours par défaut
        )
        
        # Auto-refresh
        auto_refresh = st.checkbox("🔄 Actualisation automatique (30s)")
        
        st.markdown("---")
        st.markdown("### 📊 Informations")
        st.info("Dashboard temps réel pour InfoWatchdog. Les données sont mises en cache pendant 5 minutes.")
        
        # Statut de connexion
        st.markdown("### 🌐 Statut")
        st.markdown('<p class="status-online">🟢 Connecté à Airtable</p>', unsafe_allow_html=True)
        
        # Logo ASCII compact
        st.markdown("""
        ```
        🐕‍🦺 InfoWatchdog
        ──────────────────
             /\   /\
            (  ◉.◉  )
             \  ω  /
              ^^^^
        Always Watching 👀
        ```
        """)
    
    # Chargement des données
    with st.spinner("🔍 Chargement des données depuis Airtable..."):
        df = load_airtable_data()
    
    if df.empty:
        st.error("❌ Impossible de charger les données. Vérifiez votre configuration Airtable.")
        st.stop()
    
    # Filtrage par période
    if period_options[selected_period] is not None:
        cutoff_date = datetime.now() - timedelta(days=period_options[selected_period])
        df = df[df['collected_date'] > cutoff_date]
    
    # Affichage des métriques principales
    display_metrics(df)
    
    # Graphiques principaux
    col1, col2 = st.columns(2)
    
    with col1:
        create_daily_collection_chart(df)
    
    with col2:
        create_sources_pie_chart(df)
    
    # Heatmap d'activité
    create_hourly_heatmap(df)
    
    # Sections d'analyse
    col1, col2 = st.columns([2, 1])
    
    with col1:
        display_recent_articles(df, limit=15)
    
    with col2:
        display_trending_analysis(df)
    
    # Statistiques détaillées
    display_collection_stats(df)
    
    # Footer avec informations
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.caption(f"📊 Dernière mise à jour: {datetime.now().strftime('%H:%M:%S')}")
    
    with col2:
        st.caption(f"📰 Total articles analysés: {len(df):,}")
    
    with col3:
        st.caption("🐕‍🦺 InfoWatchdog Environmental Guardian")
    
    # Auto-refresh
    if auto_refresh:
        time.sleep(30)
        st.rerun()

if __name__ == "__main__":
    main()