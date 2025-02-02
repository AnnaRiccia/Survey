import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

def create_radar_chart(df):
    values = {
        'Siamo un’azienda relativamente digitale; alcuni processi aziendali sono stati digitalizzati con l’introduzione di tecnologie digitali': 'Relativamente digitale',
        'È stato avviato qualche progetto pilota di trasformazione digitale che al momento è ancora in corso': 'Qualche progetto avviato',
        'Siamo un’azienda totalmente Digital Oriented; tutti i nostri processi sono supportati dall’utilizzo di tecnologie digitali': 'Totalmente Digital Oriented',
        'Al momento non è in corso un processo di trasformazione digitale né è stato avviato e concluso in passato': 'Non digitalizzato',
        'È stato avviato qualche progetto pilota di trasformazione digitale che è stato interrotto e non portato a compimento': 'Qualche progetto interrotto'
    }
    df['maturita_digitale'].replace(values, inplace=True)

    conversion_map = {
        "Molto D'accordo": 4,
        "D'accordo": 3,
        "Neutrale": 2,
        "In disaccordo": 1
    }

    # Rimuove le righe con maturita_digitale NaN
    df = df.dropna(subset=['maturita_digitale'])

    # Riempi i NaN nelle colonne di infrastruttura con 0
    columns_to_convert = [
        'cdh_conoscenze', 'cdh_competenze_tecniche', 'cdh_abilita_analitiche',
        'cdh_innovazione', 'cdh_formazione', 'infr_hardware', 
        'infr_software', 'infr_cloud', 'infr_sicurezza'
    ]

    for column in columns_to_convert:
        df[column] = df[column].map(conversion_map)
        df[column] = pd.to_numeric(df[column], errors='coerce')  # Assicura che i NaN siano gestiti correttamente
    
    # Gestione di NaN per le infrastrutture
    df[['infr_hardware', 'infr_software', 'infr_cloud', 'infr_sicurezza']] = df[['infr_hardware', 'infr_software', 'infr_cloud', 'infr_sicurezza']].fillna(0)

    # Filtra per la Maturità Digitale
    selected_maturity = st.radio(' ', df['maturita_digitale'].unique())
    df_filtered = df[df['maturita_digitale'] == selected_maturity]
    aggregated_values = []

    for column in columns_to_convert:
        valid_data = df_filtered[column]
        valid_data = valid_data[~valid_data.isna()]  # Escludi i NaN
        if valid_data.empty:
            aggregated_values.append(0)  # Imposta a 0 se non ci sono dati validi
        else:
            aggregated_values.append(valid_data.mean())

    # Crea il radar chart
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=aggregated_values,
        theta=columns_to_convert,
        fill='toself',
        name=f"Media Risposte - {selected_maturity}",
        fillcolor='rgba(216, 51, 103, 0.5)',  # Giallo trasparente
        line=dict(color='#F28D35', width=3)  # Arancione
    ))

    # Personalizzazione grafico
    fig.update_layout(
        title="Radar Chart",
        autosize=True,
        width=1000,
        height=1000,
        font=dict(size=16, color="white"),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        polar=dict(
            bgcolor='#FFE1C4',
            radialaxis=dict(
                visible=True,
                range=[0, 4],
                gridcolor='#5B84B1',
                tickfont=dict(size=14, color='black', family='Arial', weight='bold'),
                tickangle=0
            ),
            angularaxis=dict(
                tickfont=dict(size=14, color='black', family='Arial', weight='bold'),
                gridcolor='#D83367'
            )
        )
    )

    st.plotly_chart(fig)
