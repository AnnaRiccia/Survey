
import pandas as pd
import plotly.express as px
import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit as st

def semplifica_budget(x):
    if pd.isna(x) or x == 'Non so':
        return "Non specificato"
    else:
        return x

def mappa_maturita(df):
    values = {
        'Siamo un’azienda relativamente digitale; alcuni processi aziendali sono stati digitalizzati con l’introduzione di tecnologie digitali': 'Relativamente digitale',
        'È stato avviato qualche progetto pilota di trasformazione digitale che al momento è ancora in corso': 'Qualche progetto avviato',
        'Siamo un’azienda totalmente Digital Oriented; tutti i nostri processi sono supportati dall’utilizzo di tecnologie digitali': 'Totalmente Digital Oriented',
        'Al momento non è in corso un processo di trasformazione digitale né è stato avviato e concluso in passato': 'Non digitalizzato',
        'È stato avviato qualche progetto pilota di trasformazione digitale che è stato interrotto e non portato a compimento': 'Qualche progetto interrotto'
    }
    df['maturita_digitale'] = df['maturita_digitale'].replace(values)
    df['maturita_digitale'].fillna('Nessuna risposta', inplace=True)


def categorizza_anni(anni):
    if anni <= 5:
        return '0-5 anni'
    elif anni <= 10:
        return '6-10 anni'
    elif anni <= 15:
        return '11-15 anni'
    elif anni <= 20:
        return '16-20 anni'
    else:
        return 'Oltre 20 anni'

def heatmap_anni_maturita(df):
    # Mappare maturità digitale
    mappa_maturita(df)
    
    # Categorizzare gli anni
    df['fascia_anni'] = df['Anni'].apply(categorizza_anni)
    
    # Ordinare per fasce di anni
    ordine_anni = ['0-5 anni', '6-10 anni', '11-15 anni', '16-20 anni', 'Oltre 20 anni']
    
    # Creare la tabella pivot
    pivot = pd.crosstab(df['fascia_anni'], df['maturita_digitale'])
    pivot = pivot.reindex(ordine_anni)
    
    # Heatmap per la relazione tra Maturità Digitale e Fascia di Anni
    fig = px.imshow(
        pivot,
        text_auto=True,
        color_continuous_scale = ['#FAD0D0', '#F8A0A0', '#F57272', '#F44D4D', '#D32F2F'],  # Scala di colori
        title='  ',
        labels={'x': 'Maturità Digitale', 'y': 'Fascia Anni Esperienza', 'color': 'Numero di Aziende'}
    )
    
    # Personalizzazione del layout del grafico
    fig.update_layout(
        xaxis=dict(
            title=dict(text='Maturità Digitale', font=dict(size=18, family='Arial', weight='bold')),
            tickfont=dict(size=14, family='Arial', weight='bold'),
            tickangle=45,  # Angolo dei tick per evitare sovrapposizione
            showticklabels=True
        ),
        yaxis=dict(
            title=dict(text='Fascia di Anni', font=dict(size=18, family='Arial', weight='bold')),
            tickfont=dict(size=14, family='Arial', weight='bold'),
            showticklabels=True
        ),
        title={'text': '  ', 'x': 0.5},  # Centra il titolo
        template='plotly_white',  # Tema bianco
        font=dict(size=14),  # Aumenta la dimensione del testo
        width=1500,  # Larghezza ancora più grande
        height=800,  # Altezza maggiore per una visualizzazione chiara
        margin=dict(l=200, r=200, t=150, b=30)  # Margini più ampi per evitare il taglio delle etichette
    )

    # Visualizzare il grafico su Streamlit
    st.plotly_chart(fig, use_container_width=True)



def correlazione1_budget(df):
    df['budget_clean'] = df['budget_trans'].apply(semplifica_budget)

    ordine_budget = ['Meno del 5%', '5%-10%', '11%-20%', '21%-30%', 'Più del 30%', 'Non specificato']

    # Dizionario di mapping per la soddisfazione
    mapping_soddisfazione = {
        5: "Molto soddisfatto",
        4: "Soddisfatto",
        3: "Neutro",
        2: "Insoddisfatto",
        1: "Per niente soddisfatto"
    }

    # Creare la crosstab per la relazione tra 'budget_clean' e 'soddisfazione'
    pivot_budget_sodd = pd.crosstab(df['budget_clean'], df['soddisfazione'])
    pivot_budget_sodd = pivot_budget_sodd.reindex(ordine_budget)

    # Rinomina le colonne secondo il mapping
    pivot_budget_sodd.columns = [mapping_soddisfazione[val] for val in pivot_budget_sodd.columns]

    # **INVERTIAMO L'ASSE X E Y TRASPONENDO LA TABELLA**
    pivot_budget_sodd = pivot_budget_sodd.T

    # Heatmap con assi invertiti
    fig = px.imshow(
        pivot_budget_sodd,
        text_auto=True,  # Aggiunge i valori nella cella
        color_continuous_scale=['#E4F1F9', '#C0D9E2', '#9ACBCF', '#6DB8C0', '#3C9D9A'],  # Scala di colori
        title=' ',
        labels={'x': 'Budget (% sul fatturato)', 'y': 'Livello di Soddisfazione', 'color': 'Numero di Aziende'}
    )

    # Personalizzazione degli assi
    fig.update_layout(
        xaxis=dict(
            title=dict(text='Budget (% sul fatturato)', font=dict(size=16, family='Arial', weight='bold')),  
            tickfont=dict(size=14, family='Arial', weight='bold'),  
        ),
        yaxis=dict(
            title=dict(text='Livello di Soddisfazione', font=dict(size=16, family='Arial', weight='bold')),  
            tickfont=dict(size=14, family='Arial', weight='bold')  
        ),
        title={'text': '   ', 'x': 0.5},  # Centra il titolo
        template='plotly_white',  # Tema bianco
        font=dict(size=14),  # Aumenta la dimensione del testo
        width=800,  # Larghezza estesa per il grafico orizzontale
        height=800  # Altezza contenuta
    )
    
    st.plotly_chart(fig, theme=None, use_container_width=True)


# Funzione per semplificare il budget
def semplifica_budget(x):
    if pd.isna(x) or x == 'Non so':
        return "Non specificato"
    else:
        return x

def plot_criticita_budget(df):
    # Passaggio 1: Rimpiazzo delle stringhe nella colonna 'criticita'
    df['criticita'] = df['criticita'].str.replace(
        r'Inadeguata analisi dei Business Case, la quale ha portato ha sottovalutare alcune criticità o non cogliere determinate opportunità.',
        'Analisi dei Business Case', regex=True
    )
    df['criticita'] = df['criticita'].str.replace(
        r'Problematiche emerse durante la fase di implementazione, come ad esempio un non adeguato ingaggio degli attori coinvolti.',
        'Problematiche Implementazione', regex=True
    )
    df['criticita'] = df['criticita'].str.replace(
        r'Inadeguato allineamento tra strategia e attività svolta.',
        'Allineamento strategia/attività', regex=True
    )
    df['criticita'] = df['criticita'].str.replace(
        r'Governance del progetto non adeguata',
        'Governance progetto.', regex=True
    )


    # Passaggio 2: Separare le risposte multiple (se ce ne sono) in modo che ogni riga abbia una singola criticità
    df_separato = df['criticita'].str.split(',', expand=True).stack().reset_index(level=1, drop=True)
    df_separato.name = 'criticita'
    df = df.drop('criticita', axis=1).join(df_separato)

    # Passaggio 3: Aggiungere la colonna 'budget_clean' con la funzione semplifica_budget
    df['budget_clean'] = df['budget_trans'].apply(semplifica_budget)

    # Passaggio 4: Creare la crosstab per la relazione tra 'budget_clean' e 'criticita'
    pivot_budget_criticita = pd.crosstab(df['criticita'], df['budget_clean'])

    # Passaggio 5: Heatmap per la relazione tra Budget e Criticità
    fig = px.imshow(
        pivot_budget_criticita,
        text_auto=True,  # Aggiunge i valori nella cella
        color_continuous_scale=['#E4F1F9', '#C0D9E2', '#9ACBCF', '#6DB8C0', '#3C9D9A'],  # Scala di colori verdi
        title='  ',
        labels={'x': 'Budget (% sul fatturato)', 'y': 'Tipo di Criticità', 'color': 'Numero di Aziende'}
    )

    # Passaggio 6: Aggiustamenti grafici per l'aspetto del grafico
    fig.update_layout(
        xaxis=dict(
            title=dict(text='Budget (% sul fatturato)', font=dict(size=16, family='Arial', weight='bold')),  # Grassetto per l'asse X
            tickfont=dict(size=14, family='Arial', weight='bold'),  # Grassetto per i tick dell'asse X
            tickangle=0  # Angolatura dell'asse x impostata a 0 (per evitare inclinazioni)
        ),
        yaxis=dict(
            title=dict(text='Tipo di Criticità', font=dict(size=16, family='Arial', weight='bold')),  # Grassetto per l'asse Y
            tickfont=dict(size=14, family='Arial', weight='bold')  # Grassetto per i tick dell'asse Y
        ),
        title={'text': '  ', 'x': 0.5},  # Centra il titolo
        template='plotly_white',  # Tema bianco
        font=dict(size=14),  # Aumenta la dimensione del testo
        width=1500,  # Larghezza estesa per il grafico orizzontale
        height=800  # Altezza contenuta
    )

    # Passaggio 7: Visualizzare il grafico su Streamlit
    st.plotly_chart(fig, use_container_width=True)


def cor_budget_efficienza(df):
    # Esplodiamo la colonna 'impatto_efficienza' in più righe
    df_exploded = df.assign(impatto_efficienza=df['impatto_efficienza'].str.split(',')).explode('impatto_efficienza')

    # Rimuoviamo gli spazi bianchi dai valori
    df_exploded['impatto_efficienza'] = df_exploded['impatto_efficienza'].str.strip()

    # Creiamo una tabella pivot con il conteggio delle occorrenze di ogni impatto_efficienza per budget_trans
    pivot_table = df_exploded.pivot_table(index='budget_trans', columns='impatto_efficienza', aggfunc='size', fill_value=0)

    # Creiamo una colonna con il totale delle occorrenze di ogni impatto_efficienza
    pivot_table["Totale Risposte"] = pivot_table.sum(axis=1)

    # Riordiniamo la tabella dal valore più alto al più basso per dare maggiore rilievo
    pivot_table = pivot_table.sort_values(by="Totale Risposte", ascending=False)

    # Creiamo la heatmap con Plotly
    fig = px.imshow(
        pivot_table.iloc[:, :-1].values,  # Escludiamo la colonna "Totale Risposte" dalla heatmap
        labels=dict(x="Impatto Efficienza", y="Budget Investito", color="Conteggio"),
        color_continuous_scale= ["#E4F1E1", "#C0E0C6", "#9ACFA8", "#6DBE8D", "#3C9D74"],
        x=pivot_table.columns[:-1],  # Escludiamo "Totale Risposte"
        y=pivot_table.index,
        text_auto=True,  # Aggiunge i valori nella cella
    )
    fig.update_layout(
        xaxis=dict(
            title=dict(text="Impatto Efficienza", font=dict(size=16, family='Arial', weight='bold')),  # Grassetto per l'asse X
            tickfont=dict(size=14, family='Arial', weight='bold')
        ),
        yaxis=dict(
            title=dict(text='Budget (% sul fatturato)', font=dict(size=16, family='Arial', weight='bold')),  # Grassetto per l'asse Y
            tickfont=dict(size=14, family='Arial', weight='bold')
        ),
        title={'text': '  ', 'x': 0.5},  # Centra il titolo
        template='plotly_white',  # Tema bianco
        font=dict(size=14),  # Aumenta la dimensione del testo
        width=800,  # Larghezza estesa per il grafico orizzontale
        height=800  # Altezza contenuta
    )

    # Mostriamo la heatmap in Streamlit
    st.plotly_chart(fig, use_container_width=True)
