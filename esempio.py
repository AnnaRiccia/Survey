import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configurazione della pagina
st.set_page_config(page_title="Radar Chart Aziende", layout="wide")
st.title("Analisi Comparativa Aziende")

# Funzione per trovare le aziende più virtuose
def get_top_performers(df, categories, n=1):
    df['score'] = df[categories].mean(axis=1)
    top_performers = df.nlargest(n, 'score')
    return top_performers.drop('score', axis=1)

# Funzione per creare il radar chart con Plotly
def create_radar_chart(categories, values, labels, title):
    fig = go.Figure()
    
    # Lista di colori per differenziare le linee
    colors = ['rgb(31, 119, 180)', 'rgb(255, 99, 71)', 'rgb(60, 179, 113)', 'rgb(147, 112, 219)']
    
    for i, (value, label) in enumerate(zip(values, labels)):
        fig.add_trace(go.Scatterpolar(
            r=value + [value[0]],  # Chiude il poligono
            theta=categories + [categories[0]],  # Chiude il poligono
            name=label,
            line=dict(color=colors[i], width=2),
            fill='toself',
            fillcolor=colors[i],
            opacity=0.1
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )
        ),
        showlegend=True,
        title=dict(
            text=title,
            x=0.5,
            xanchor='center'
        ),
        height=600
    )
    
    return fig

# Dati
data = {
    'azienda': ['azeinda1', 'azeinda2', 'azeinda3', 'azeinda4', 'azeinda5', 
                'azeinda6', 'azeinda7', 'azeinda8', 'azeinda9', 'azeinda10',
                'azeinda11', 'azeinda12', 'azeinda13', 'azeinda14', 'azeinda15',
                'azeinda16', 'azeinda17', 'azeinda18', 'azeinda19', 'azeinda20'],
    'conoscenze': [5, 5, 4, 3, 1, 1, 5, 3, 1, 5, 5, 1, 5, 2, 4, 1, 1, 5, 1, 5],
    'hardware': [5, 3, 5, 5, 5, 1, 1, 4, 2, 4, 1, 2, 1, 5, 3, 3, 5, 1, 1, 4],
    'ecologia': [5, 2, 1, 2, 2, 1, 3, 1, 1, 3, 2, 3, 5, 2, 4, 2, 4, 3, 3, 3],
    'resp_dipendenti': [3, 5, 1, 1, 1, 4, 5, 3, 4, 1, 2, 2, 5, 1, 5, 5, 3, 5, 3, 1],
    'processi_digit': [1, 2, 2, 4, 5, 3, 2, 1, 3, 5, 1, 2, 4, 1, 2, 5, 1, 3, 5, 2],
    'criticità': [5, 2, 2, 1, 3, 1, 1, 1, 2, 5, 5, 5, 5, 2, 3, 4, 5, 3, 3, 1]
}


df = pd.DataFrame(data)
categories = ['conoscenze', 'hardware', 'ecologia', 'resp_dipendenti', 'processi_digit', 'criticità']

# Sidebar per la selezione dell'azienda e tipo di confronto
st.sidebar.header("Seleziona Azienda e Confronto")

# Selezione singola azienda
selected_company = st.sidebar.selectbox(
    "Scegli l'azienda da analizzare",
    options=df['azienda'].tolist()
)

# Tipo di confronto
comparison_type = st.sidebar.multiselect(
    "Scegli il tipo di confronto",
    options=["Media di tutte le aziende", "Azienda più virtuosa"],
    default=["Media di tutte le aziende"]
)

# Preparazione dei dati per il radar chart
values = []
labels = []

# Dati dell'azienda selezionata
company_data = df[df['azienda'] == selected_company]
values.append([company_data[cat].iloc[0] for cat in categories])
labels.append(selected_company)

# Aggiunta dei confronti selezionati
if "Media di tutte le aziende" in comparison_type:
    mean_values = df[categories].mean().tolist()
    values.append(mean_values)
    labels.append("Media settore")

if "Azienda più virtuosa" in comparison_type:
    top_performer = get_top_performers(df, categories)
    top_values = [top_performer[cat].iloc[0] for cat in categories]
    values.append(top_values)
    labels.append(f"Top performer ({top_performer['azienda'].iloc[0]})")

# Creazione e visualizzazione del radar chart
fig = create_radar_chart(categories, values, labels, f"Confronto {selected_company}")
st.plotly_chart(fig, use_container_width=True)

# Tabella dei dati di confronto con formattazione migliorata
st.header("Dati Dettagliati")
comparison_df = pd.DataFrame()

# Aggiungi i dati dell'azienda selezionata
comparison_df = pd.concat([comparison_df, company_data[['azienda'] + categories]])

# Aggiungi la media se selezionata
if "Media di tutte le aziende" in comparison_type:
    mean_df = pd.DataFrame({
        'azienda': ['Media settore'],
        **{cat: [round(df[cat].mean(), 2)] for cat in categories}
    })
    comparison_df = pd.concat([comparison_df, mean_df])

# Aggiungi il top performer se selezionato
if "Azienda più virtuosa" in comparison_type:
    comparison_df = pd.concat([comparison_df, top_performer[['azienda'] + categories]])

st.dataframe(comparison_df, hide_index=True)

# Analisi delle differenze con visualizzazione migliorata
if "Media di tutte le aziende" in comparison_type:
    st.header("Analisi delle Differenze")
    
    # Calcolo delle differenze
    differences = [company_data[cat].iloc[0] - df[cat].mean() for cat in categories]
    
    # Creazione del grafico a barre per le differenze
    fig_diff = go.Figure()
    
    fig_diff.add_trace(go.Bar(
        x=categories,
        y=differences,
        marker_color=['red' if x < 0 else 'green' for x in differences],
        text=[f"{x:.2f}" for x in differences],
        textposition='auto',
    ))
    
    fig_diff.update_layout(
        title="Differenze rispetto alla media del settore",
        yaxis_title="Differenza",
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig_diff, use_container_width=True)

    # Tabella delle differenze
    st.subheader("Dettaglio numerico delle differenze")
    diff_from_mean = pd.DataFrame({
        'Categoria': categories,
        'Differenza dalla media': differences
    })
    st.dataframe(
        diff_from_mean.style.background_gradient(
            cmap='RdYlGn',
            subset=['Differenza dalla media']
        ),
        hide_index=True
    )