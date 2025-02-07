import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import plotly.io as pio
import pandas as pd
pio.templates.default = "plotly"
import plotly.express as px
import numpy as np

@staticmethod
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

# # # intervistato ----------------------------
class funz:
    @staticmethod
    def plot_infr(df):
        # Conta la presenza di competenze digitali
        infr_counts = df['presenza_infrastrutture'].value_counts()

        # Crea un oggetto fig
        fig = go.Figure()

        # Aggiungi il grafico a torta
        fig.add_trace(
            go.Pie(
                labels=infr_counts.index, 
                values=infr_counts.values,
                marker=dict(
                    colors=['#2e8b57', '#8fbc8f', '#66cdaa' ]  # Colori per la torta (es. sfumature di blu)
                ),
                textinfo='percent+label',  # Mostra percentuale e etichetta
                textposition='outside',  # Posiziona il testo fuori dalla torta
                pull=[0.1, 0.1],  # Sposta leggermente le sezioni
                showlegend=False
            )
        )

        # Aggiungi titolo e layout
        fig.update_layout(
            title=" ",
            title_x=0.5,  # Centra il titolo orizzontalmente
            height=500, 
            width=1000,  # Imposta la larghezza del grafico
            template='plotly_white'
        )

        # Mostra il grafico su Streamlit
        st.plotly_chart(fig)
    @staticmethod
    def plot_fasce_anni(df):
        # Conta le frequenze di ciascuna fascia di anni
        df['fascia_anni'] = df['Anni'].apply(categorizza_anni)
        counts = df['fascia_anni'].value_counts()

        # Crea un subplot con 1 riga e 2 colonne (grafico a torta e grafico a barre)
        fig = make_subplots(
            rows=1, cols=2, 
            subplot_titles=(' ', ' '),
            specs=[[{'type': 'pie'}, {'type': 'bar'}]]
        )

        # Aggiungi il grafico a torta con colori personalizzati
        fig.add_trace(
            go.Pie(
                labels=counts.index, 
                values=counts.values, 
                name='Da quanto tempo lavori presso questa azienda?',
                marker=dict(
                    colors=['#a8c8f8', '#74aaff', '#4687e1', '#1d5b9b', '#134c6b']),
                textinfo='percent+label',  # Mostra percentuale e etichetta
                textposition='outside',   # Posiziona il testo fuori dalla torta
                pull=[0.1, 0.1, 0.1, 0.1, 0.1],  # Leggero distacco per ogni fetta
                showlegend=False  # Nascondi la legenda per il grafico a torta
            ),
            row=1, col=1
        )

        # Aggiungi il grafico a barre con la legenda nascosta
        fig.add_trace(
            go.Bar(
                x=counts.index, 
                y=counts.values, 
                name="Distribuzione fasce di anni",
                marker=dict(color='#4687e1'),  # Colore personalizzato per le barre
                showlegend=False  # Nascondi la legenda per il grafico a barre
            ),
            row=1, col=2
        )

        # Aggiorna la disposizione per migliorare la visualizzazione
        fig.update_layout(
            showlegend=True,
            height=500, 
            width=1000,
            template="plotly",
            bargap=0.1,  # Modifica la larghezza delle barre
            bargroupgap=0.1
        )

        st.plotly_chart(fig, theme= None, use_container_width=True)
        

    @staticmethod
    def plot_role_distribution(df):

        # Definire i ruoli con conoscenze informatiche approfondite
        it_roles = [
            'IT Manager', 'CIO', 'CFO', 'Coordinatore Data Unit', 'Chief Information Officer', 'Responsabile IT',
            'R&D Manager', 'Quality Assurance, Organization & Sustainability', 'ICT Manager', 'AMMINISTRATORE DI SISTEMA',
            'QHSE & IT Manager', 'Innovation Manager', 'Co-founder e CTO', 'IT Manager', 'Direttore Innovation', 'Executive Assistant'
        ]

        # Filtra i ruoli nel dataframe
        df['Ruolo Informatico'] = df['ruolo'].apply(lambda x: 'Ruolo informatico' if x in it_roles else 'Altro ruolo')

        # Conta il numero di ruoli informatici e non
        role_counts = df['Ruolo Informatico'].value_counts()

        # Crea un grafico a torta per la distribuzione dei ruoli
        pie_fig = go.Pie(
            labels=role_counts.index,
            values=role_counts.values,
            textinfo='percent+label',
            marker=dict(colors=['#1d5b9b', '#a8c8f8'])  # Aggiunta di sfumature di blu
        )

        # Creare la lista dei ruoli informatici
        it_role_list = df[df['Ruolo Informatico'] == 'Ruolo informatico']['ruolo'].unique()

        # Crea un grafico con la lista dei ruoli informatici
        role_text = "<br>".join(it_role_list)

        # Creare un subplot con il grafico a torta e la lista dei ruoli
        fig = make_subplots(
            rows=1, cols=2,
            column_widths=[0.5, 0.5],  # Impostare una larghezza di colonna pari
            specs=[[{'type': 'pie'}, {'type': 'table'}]],  # Pie chart e tabella
        )

        # Aggiungi il grafico a torta
        fig.add_trace(pie_fig, row=1, col=1)

        # Aggiungi una tabella con i ruoli informatici
        fig.add_trace(
            go.Table(
                header=dict(values=["Ruoli Informatici"]),
                cells=dict(values=[it_role_list])
            ),
            row=1, col=2
        )

        # Aggiorna il layout per migliorare la visualizzazione
        fig.update_layout(
            title_text=" ",
            height=500,
            width=1000,
            showlegend=False
        )

        # Mostra il grafico su Streamlit
        st.plotly_chart(fig, use_container_width=True)

    
    @staticmethod
    def plot_Rel(df):
        # Conta la presenza di competenze digitali
        infr_counts = df['ecosistema_valore'].value_counts()

        # Crea un oggetto fig
        fig = go.Figure()

        # Aggiungi il grafico a torta
        fig.add_trace(
            go.Pie(
                labels=infr_counts.index, 
                values=infr_counts.values,
                marker=dict(
                    colors=['#9370DB', '#1E90FF', '#006D5B']  # Colori per la torta (es. sfumature di blu)
                ),
                textinfo='percent+label',  # Mostra percentuale e etichetta
                textposition='outside',  # Posiziona il testo fuori dalla torta
                pull=[0.1, 0.1],  # Sposta leggermente le sezioni
                showlegend=False
            )
        )

        # Aggiungi titolo e layout
        fig.update_layout(
            title=" ",
            title_x=0.5,  # Centra il titolo orizzontalmente
            height=500, 
            width=1000,  # Imposta la larghezza del grafico
            template='plotly_white'
        )

        # Mostra il grafico su Streamlit
        st.plotly_chart(fig)


# # #  maturità digitale ---------------------
    @staticmethod
    def analyze_digital_maturity(df):
        # Mappatura dei valori
        values = {
            'Siamo un\'azienda relativamente digitale; alcuni processi aziendali sono stati digitalizzati con l\'introduzione di tecnologie digitali': 'Relativamente digitale',
            'È stato avviato qualche progetto pilota di trasformazione digitale che al momento è ancora in corso': 'Qualche progetto avviato',
            'Siamo un\'azienda totalmente Digital Oriented; tutti i nostri processi sono supportati dall\'utilizzo di tecnologie digitali': 'Totalmente Digital Oriented',
            'Al momento non è in corso un processo di trasformazione digitale né è stato avviato e concluso in passato': 'Non digitalizzato',
            'È stato avviato qualche progetto pilota di trasformazione digitale che è stato interrotto e non portato a compimento': 'Qualche progetto interrotto'
        }

        # Sostituzione dei valori con la mappatura
        df['maturita_digitale'] = df['maturita_digitale'].replace(values)

        # Conta i livelli di maturità digitale
        maturity_levels = df['maturita_digitale'].value_counts()

        # Calcola le percentuali
        total = maturity_levels.sum()
        percentages = (maturity_levels / total) * 100

            # Creazione del layout con i subplot
        fig = make_subplots(
            rows=1, cols=2, 
            specs=[[{'type': 'pie'}, {'type': 'bar'}]],
            horizontal_spacing=0.2
        )

        # Aggiunta del grafico a torta
        fig.add_trace(
            go.Pie(
                labels=maturity_levels.index, 
                values=maturity_levels.values,
                marker=dict(
                    colors=['#f8a8a8', '#f07474', '#e14444', '#b93333', '#7d1c1c']
                ),
                textinfo='percent+label',  # Mostra percentuali e etichette
                textposition='outside',  # Posiziona il testo fuori dalla torta
                pull=[0.1] * len(maturity_levels)  # Distacco per ogni fetta
            ),
            row=1, col=1
        )

        # Aggiunta del grafico a barre
        fig.add_trace(
            go.Bar(
                x=maturity_levels.index, 
                y=maturity_levels.values, 
                text=percentages.round(1).astype(str) + '%',  # Testo con percentuali
                textposition='auto',  # Testo sopra le barre
                marker=dict(
                    color=['#f8a8a8', '#f07474', '#e14444', '#b93333', '#7d1c1c'][:len(maturity_levels)]
                )
            ),
            row=1, col=2
        )

        # Personalizzazione del layout generale
        fig.update_layout(
            height=500, 
            width=1000,
            showlegend=False,  # Mostra legenda per entrambi i grafici
            bargap=0.1,  # Spaziatura tra le barre
            paper_bgcolor="#f5f5f5",  # Sfondo dell'area esterna al grafico
            plot_bgcolor="#eaeaea",  # Sfondo dell'area del grafico
            margin=dict(l=40, r=40, t=0, b=40),  # Margini
            template="plotly"  # Tema di default
        )


        st.plotly_chart(fig, theme=None, use_container_width=True)

    #################################################################################### FIGURE COMPETENZE TECNICHE ####################################################################################
    @staticmethod
    def plot_strategie_talent(df):
        """
        Visualizza un grafico a torta per le strategie talent, in base alle risposte.
        
        Args:
            df (pd.DataFrame): DataFrame contenente i dati delle strategie talent.
        """
        # Dizionario con le chiavi e i valori iniziali
        dizionario = {
            'Nessuna delle precedenti': 0,
            "Reclutamento di nuovi talenti con competenze digitali ": 0,
            "Formazione continua e sviluppo professionale": 0,
            "Collaborazioni con università e istituti di ricerca ": 0,
            "Programmi di mentoring e coaching ": 0,
            "Organizzazione di hackathon e conferenze tecnologiche ": 0
        }

        # Copia il dizionario iniziale per non modificarlo direttamente
        for risposta in df['strategie_talent'].fillna(''):
            for key in dizionario.keys():
                if key in risposta:
                    dizionario[key] += 1

        # Calcolo delle percentuali
        totale = sum(dizionario.values())
        percentuali = [(val / totale) * 100 if totale > 0 else 0 for val in dizionario.values()]

        # Formatta le percentuali con il simbolo %
        percentuali_formattate = [f"{p:.2f}%" for p in percentuali]

        # Creazione del grafico a torta
        fig = go.Figure(data=[go.Pie(
            labels=list(dizionario.keys()),  # Converti le chiavi del dizionario in una lista
            values=percentuali,  # Le percentuali di occorrenza per ciascuna strategia
            textinfo='percent+label',  # Mostra percentuale e etichetta
            textposition='outside',  # Testo fuori dalla torta
            pull=[0.1] * len(dizionario),  # Aggiungi distacco a ciascuna fetta
            marker=dict(colors=['#ffcc66', '#ff9933', '#ff6600', '#cc3300', '#990000']),
            showlegend=False
        )])

        # Personalizzazione del layout
        fig.update_layout(
            title='   ',
            height=500,
            width=800,
            paper_bgcolor="#f5f5f5",
            plot_bgcolor="#eaeaea",
            margin=dict(l=40, r=40, t=40, b=40),
            template="plotly"
        )

        # Mostra il grafico in Streamlit
        st.plotly_chart(fig, use_container_width=True)

######################################################################### transizione digitale #####################################################################################################################
    @staticmethod
    def plot_trans(df):
        # Conta la presenza di competenze digitali
        infr_counts = df['trans_digitale'].value_counts()

        # Crea un oggetto fig
        fig = go.Figure()

        # Aggiungi il grafico a torta
        fig.add_trace(
            go.Pie(
                labels=infr_counts.index, 
                values=infr_counts.values,
                marker=dict(
                    colors=['#f8a8a8', '#f07474', '#e14444']  # Colori per la torta (es. sfumature di blu)
                ),
                textinfo='percent+label',  # Mostra percentuale e etichetta
                textposition='outside',  # Posiziona il testo fuori dalla torta
                pull=[0.1, 0.1],  # Sposta leggermente le sezioni
                showlegend=False
            )
        )

        # Aggiungi titolo e layout
        fig.update_layout(
            title=" ",
            title_x=0.5,  # Centra il titolo orizzontalmente
            height=500, 
            width=1000,  # Imposta la larghezza del grafico
            template='plotly_white'
        )

        # Mostra il grafico su Streamlit
        st.plotly_chart(fig)

    ################################################################################ inizio transizione ##################################################################################################################
    @staticmethod
    def inizio_trans(df):
        df['inizio_trans'].fillna('Nessuna risposta', inplace=True)  # Rimpiazziamo NaN con 'Nessuna risposta'

        # Conta la distribuzione delle risposte
        distribution_counts = df['inizio_trans'].value_counts()

        # Calcola le percentuali
        total = distribution_counts.sum()
        percentages = (distribution_counts / total) * 100

        # Crea un subplot con 1 riga e 2 colonne (grafico a torta e grafico a barre)
        fig = make_subplots(
            rows=1, cols=2, 
            specs=[[{'type': 'pie'}, {'type': 'bar'}]],  # Pie chart e Bar chart
            column_widths=[0.48, 0.48],  # Imposta la larghezza delle colonne
            horizontal_spacing=0.2  # Spazio orizzontale tra i grafici
        )

        # Aggiungi il grafico a torta
        fig.add_trace(
            go.Pie(
                labels=distribution_counts.index,
                values=distribution_counts.values,
                textinfo='percent+label',  # Mostra percentuale
                textposition='outside',  # Testo fuori dalle fette
                pull=[0.1] * len(distribution_counts),  # Spazio tra le fette
                marker=dict(
                    colors=['#f8a8a8', '#f07474', '#e14444', '#b93333', '#7d1c1c']  # Gradazione di colori
                ),
                showlegend=True  # Mostra la legenda
            ),
            row=1, col=1
        )

        # Aggiungi il grafico a barre
        fig.add_trace(
            go.Bar(
                x=distribution_counts.index,  # Etichette (le risposte)
                y=distribution_counts.values,  # Conteggi
                text=percentages.round(1).astype(str) + '%',  # Percentuali come testo
                textposition='outside',  # Posiziona il testo fuori dalle barre
                marker=dict(
                    color=['#f8a8a8', '#f07474', '#e14444', '#b93333', '#7d1c1c'][:len(distribution_counts)]  # Colori specifici
                ),
                showlegend=False  # Nascondi la legenda per il grafico a barre
            ),
            row=1, col=2
        )

        # Aggiungi titolo e layout
        fig.update_layout(
            title="  ",
            title_x=0.5,  # Centra il titolo orizzontalmente
            height=500, 
            width=1000,  # Imposta la larghezza del grafico
            template='plotly_white'
        )

        st.plotly_chart(fig, theme=None, use_container_width=True)



    ##################################################################################################### stimoli trans ###########################################################################################

    @staticmethod
    def plot_stimoli_trans_funnel(df):
        # Rimpiazziamo i NaN con 'Nessuna risposta' direttamente nella colonna
        df['stimoli_trans'] = df['stimoli_trans'].fillna('Nessuna risposta')

        # Sostituiamo il testo lungo con la versione abbreviata
        df['stimoli_trans'] = df['stimoli_trans'].replace(
            'Stimoli da associazioni di categoria/centri di ricerca/ istituzioni universitarie', 
            'Stimoli da associazioni e centri di ricerca'
        )

        # Mappa le risposte per abbreviarne e contarne la frequenza
        dizionario_stimoli = {
            'Business partner a seguito di attività di formazione e aggiornamento': 0,
            'Competitors': 0,
            'Sollecitazioni interne': 0,
            'Stimoli da associazioni e centri di ricerca': 0,  # Risposta accorciata
            'Nessuna risposta': 0,
        }

        # Popolazione del dizionario con i conteggi
        for x in df['stimoli_trans']:
            for key in dizionario_stimoli.keys():
                if key in x:
                    dizionario_stimoli[key] += 1

        # Creazione del DataFrame con i conteggi
        df_stimoli = pd.DataFrame(list(dizionario_stimoli.items()), columns=['Stimoli', 'Conteggi'])

        # Lista dei colori personalizzati
        colors = ['#f8a8a8', '#f07474', '#e14444', '#b93333', '#7d1c1c']

        # Creazione del grafico a barre con i colori personalizzati
        fig = px.bar(df_stimoli, 
                    x='Stimoli', 
                    y='Conteggi', 
                    color='Stimoli',  
                    color_discrete_sequence=colors,  # Applica i colori definiti
                    text='Conteggi', 
                    title="   ",
                    width=500, 
                    height=500)
        fig.update_layout(showlegend=False)
        # Mostra il grafico
        st.plotly_chart(fig, theme=None, use_container_width=True)

    ########################################################## COINVOGLIEMNTO LEADER ###################################################################
    @staticmethod
    def plot_coinvolgimento_leader(df):
        # Mappatura dei valori numerici in descrizioni comprensibili
        mappa_coinvolgimento = {
            0: 'Per niente coinvolto',
            2: 'Poco coinvolto',
            3: 'Parzialmente coinvolto',
            4: 'Molto coinvolto',
            5: 'Pienamente coinvolto'
        }

        # Sostituiamo i valori numerici con le descrizioni
        df['coinvolgimento_leader'] = df['coinvolgimento_leader'].map(mappa_coinvolgimento)

        # Conta le occorrenze per ciascun valore nella colonna 'coinvolgimento_leader'
        coinvolgimento_counts = df['coinvolgimento_leader'].value_counts().sort_index()

        # Colori personalizzati
        colors=['#f8a8a8', '#f07474', '#e14444', '#b93333', '#7d1c1c']

        # Calcolare le percentuali
        total = coinvolgimento_counts.sum()
        percentages = (coinvolgimento_counts / total) * 100

        # Creazione del layout con i subplot
        fig = make_subplots(
            rows=1, cols=2, 
            specs=[[{'type': 'pie'}, {'type': 'bar'}]],  # Colonna 1: torta, colonna 2: barre
            horizontal_spacing=0.2  # Spazio tra i due grafici
        )

        # Aggiunta del grafico a torta
        fig.add_trace(
            go.Pie(
                labels=coinvolgimento_counts.index.astype(str), 
                values=coinvolgimento_counts.values,
                marker=dict(
                    colors=colors[:len(coinvolgimento_counts)]  # Colori personalizzati
                ),
                textinfo='percent+label',  # Mostra percentuali e etichette
                textposition='outside',  # Posiziona il testo fuori dalla torta
                pull=[0.1] * len(coinvolgimento_counts)  # Distacco per ogni fetta
            ),
            row=1, col=1
        )

        # Aggiunta del grafico a barre
        fig.add_trace(
            go.Bar(
                x=coinvolgimento_counts.index.astype(str), 
                y=coinvolgimento_counts.values, 
                text=percentages.round(1).astype(str) + '%',  # Testo con percentuali
                textposition='auto',  # Testo sopra le barre
                marker=dict(
                    color=colors[:len(coinvolgimento_counts)]  # Colori personalizzati
                )
            ),
            row=1, col=2
        )

        # Personalizzazione del layout generale
        fig.update_layout(
            height=500, 
            width=500,
            showlegend=False,  # Mostra legenda per entrambi i grafici
            bargap=0.1,  # Spaziatura tra le barre
            paper_bgcolor="#f5f5f5",  # Sfondo dell'area esterna al grafico
            plot_bgcolor="#eaeaea",  # Sfondo dell'area del grafico
            margin=dict(l=40, r=40, t=0, b=40),  # Margini
            template="plotly"  # Tema di default
        )

        # Visualizza il grafico in Streamlit
        st.plotly_chart(fig, theme=None, use_container_width=True)
############################################################################################### responsabilità dipendenti ######################################################################
    @staticmethod
    def plot_resp_dipendenti_funnel(df):
        # Rimpiazziamo i NaN con 'Nessuna risposta' direttamente nella colonna
        df['resp_dipendenti'] = df['resp_dipendenti'].fillna('Nessuna risposta')

        # Mappa le risposte per abbreviarne e contarne la frequenza
        dizionario_resp_dipendenti = {
            'Assegnazione di obiettivi individuali': 0,
            'Creazione di un senso condiviso di responsabilità': 0,
            'Promozione della collaborazione interfunzionale': 0,
            'Definizione di ruoli chiari': 0,
            'Incentivi per l\'innovazione e il miglioramento continuo': 0,
            'Nessuna risposta': 0
        }

        # Popolazione del dizionario con i conteggi
        for x in df['resp_dipendenti']:
            for key in dizionario_resp_dipendenti.keys():
                if key in x:
                    dizionario_resp_dipendenti[key] += 1

        # Creazione del DataFrame con i conteggi
        df_resp_dipendenti = pd.DataFrame(list(dizionario_resp_dipendenti.items()), columns=['Stimoli', 'Conteggi'])

        # Lista dei colori personalizzati
        colors = ['#f8a8a8', '#f07474', '#e14444', '#b93333', '#7d1c1c']

        # Creazione del grafico a barre con i colori personalizzati
        fig = px.bar(df_resp_dipendenti, 
                    x='Stimoli', 
                    y='Conteggi', 
                    color='Stimoli',  
                    color_discrete_sequence=colors,  # Applica i colori definiti
                    text='Conteggi', 
                    title="  ",
                    width=800, 
                    height=800)
        fig.update_layout(showlegend=False)
        # Mostra il grafico
        st.plotly_chart(fig, theme=None, use_container_width=True)
############################################################################ cosa #############################################################################################################################################
    @staticmethod
    def analyze_fase_trans(df):
        # Mappatura dei valori
        values = {
            'Adozione e Utilizzo di Risorse Digitali': 'Adozione e utilizzo',
            'Analisi e mappatura dei processi esistenti': 'Analisi dei processi',
            'Definizione della strategia e degli obiettivi': 'Definizione strategia',
            'Progettazione e pianificazione': 'Pianificazione e progettazione',
            'nan': 'Nessuna risposta'
        }

        # Sostituzione dei valori con la mappatura
        df['fase_trans'] = df['fase_trans'].replace(values)

        # Conta i livelli di fase di transizione
        fase_levels = df['fase_trans'].value_counts()

        # Calcola le percentuali
        total = fase_levels.sum()
        percentages = (fase_levels / total) * 100

        # Creazione del layout con i subplot
        fig = make_subplots(
            rows=1, cols=2, 
            specs=[[{'type': 'pie'}, {'type': 'bar'}]],  # Definisce i grafici
            horizontal_spacing=0.2
        )

        # Aggiunta del grafico a torta
        fig.add_trace(
            go.Pie(
                labels=fase_levels.index, 
                values=fase_levels.values,
                marker=dict(
                    colors=['#f8a8a8', '#f07474', '#e14444', '#b93333', '#7d1c1c']  # Colori personalizzati
                ),
                textinfo='percent+label',  # Mostra percentuali e etichette
                textposition='outside',  # Posiziona il testo fuori dalla torta
                pull=[0.1] * len(fase_levels)  # Distacco per ogni fetta
            ),
            row=1, col=1
        )

        # Aggiunta del grafico a barre
        fig.add_trace(
            go.Bar(
                x=fase_levels.index, 
                y=fase_levels.values, 
                text=percentages.round(1).astype(str) + '%',  # Testo con percentuali
                textposition='auto',  # Testo sopra le barre
                marker=dict(
                    color=['#f8a8a8', '#f07474', '#e14444', '#b93333', '#7d1c1c'][:len(fase_levels)]
                )
            ),
            row=1, col=2
        )

        # Personalizzazione del layout generale
        fig.update_layout(
            height=500, 
            width=800,
            showlegend=False,  # Nascondi la legenda
            bargap=0.1,  # Spaziatura tra le barre
            paper_bgcolor="#f5f5f5",  # Sfondo dell'area esterna al grafico
            plot_bgcolor="#eaeaea",  # Sfondo dell'area del grafico
            margin=dict(l=40, r=40, t=0, b=40),  # Margini
            template="plotly"  # Tema di default
        )

        # Mostra il grafico
        st.plotly_chart(fig, theme=None, use_container_width=True)
############################################################################ cosa #############################################################################################################################################

    @staticmethod
    def analyze_budget_trans(df):
        # Mappatura dei valori
        values = {
            '11%-20%': '11%-20% del budget',
            '21%-30%': '21%-30% del budget',
            '5%-10%': '5%-10% del budget',
            'Meno del 5%': 'Meno del 5% del budget',
            'Non so': 'Non so',
            'Più del 30%': 'Più del 30% del budget',
            'nan': 'Nessuna risposta'  # Mappa 'nan' come 'Nessuna risposta'
        }
        # Sostituzione dei valori con la mappatura
        df['budget_trans'] = df['budget_trans'].replace(values)

        # Conta i livelli di budget
        budget_levels = df['budget_trans'].value_counts()

        # Calcola le percentuali
        total = budget_levels.sum()
        percentages = (budget_levels / total) * 100

        # Creazione del layout con i subplot
        fig = make_subplots(
            rows=1, cols=2, 
            specs=[[{'type': 'pie'}, {'type': 'bar'}]],  # Definisce i grafici
            horizontal_spacing=0.2
        )

        # Aggiunta del grafico a torta
        fig.add_trace(
            go.Pie(
                labels=budget_levels.index, 
                values=budget_levels.values,
                marker=dict(
                    colors=['#f8a8a8', '#f07474', '#e14444', '#b93333', '#7d1c1c', '#b33d3d']  # Colori personalizzati
                ),
                textinfo='percent+label',  # Mostra percentuali e etichette
                textposition='outside',  # Posiziona il testo fuori dalla torta
                pull=[0.1] * len(budget_levels)  # Distacco per ogni fetta
            ),
            row=1, col=1
        )

        # Aggiunta del grafico a barre
        fig.add_trace(
            go.Bar(
                x=budget_levels.index, 
                y=budget_levels.values, 
                text=percentages.round(1).astype(str) + '%',  # Testo con percentuali
                textposition='auto',  # Testo sopra le barre
                marker=dict(
                    color=['#f8a8a8', '#f07474', '#e14444', '#b93333', '#7d1c1c', '#b33d3d'][:len(budget_levels)]
                )
            ),
            row=1, col=2
        )

        # Personalizzazione del layout generale
        fig.update_layout(
            height=500, 
            width=1000,
            showlegend=False,  # Nascondi la legenda
            bargap=0.1,  # Spaziatura tra le barre
            paper_bgcolor="#f5f5f5",  # Sfondo dell'area esterna al grafico
            plot_bgcolor="#eaeaea",  # Sfondo dell'area del grafico
            margin=dict(l=40, r=40, t=0, b=40),  # Margini
            template="plotly"  # Tema di default
        )

        # Mostra il grafico
        st.plotly_chart(fig, theme=None, use_container_width=True)
#################################################################################################################################################################################################################################

    @staticmethod
    def plot_processi_digit(df):
        # Rimpiazziamo i NaN con 'Nessuna risposta' direttamente nella colonna
        df['processi_digit'] = df['processi_digit'].fillna('Nessuna risposta')

        # Mappa le risposte per abbreviarne e contarne la frequenza
        dizionario_processi_digit = {
            'Consegna del Prodotto e del Servizio (Produzione, consegna del servizio, Gestione dell\'ambiente operativo, Gestione della manutenzione e del supporto)': 'Consegna Servizio',
            'Gestione della Catena di Approvvigionamento (Pianificazione della catena di approvvigionamento, Approvvigionamento, Produzione, Logistica e distribuzione)': 'Catena di Approvv.',
            'Gestione Ambientale, Sanità e Sicurezza (Pianificazione della salute e della sicurezza, Gestione della salute e della sicurezza sul lavoro, Gestione della salute ambientale e dei sistemi di sicurezza)': 'Sicurezza e Ambiente',
            'Gestione e Amministrazione dell\'Organizzazione': 'Amministrazione',
            'Marketing e Vendite': 'Marketing e Vendite',
            'Sviluppo del Prodotto e del Servizio': 'Sviluppo Prodotto',
            'Nessuna risposta': 'Nessuna risposta'
        }

        # Popolazione del dizionario con i conteggi
        dizionario_abbreviato = {abbreviazione: 0 for abbreviazione in dizionario_processi_digit.values()}

        for x in df['processi_digit']:
            for key, abbreviazione in dizionario_processi_digit.items():
                if key in x:
                    dizionario_abbreviato[abbreviazione] += 1

        # Creazione del DataFrame con i conteggi
        df_processi_digit = pd.DataFrame(list(dizionario_abbreviato.items()), columns=['Processi Digitali', 'Conteggi'])

        # Lista dei colori personalizzati
        colors = ['#f8a8a8', '#f07474', '#e14444', '#b93333', '#7d1c1c', '#f5b7b7']

        # Creazione del grafico a barre con i colori personalizzati
        fig = px.bar(df_processi_digit, 
                    x='Processi Digitali', 
                    y='Conteggi', 
                    color='Processi Digitali',  
                    color_discrete_sequence=colors,  # Applica i colori definiti
                    text='Conteggi', 
                    title="  ",
                    width=500, 
                    height=500)

        # Rimuovi la legenda
        fig.update_layout(showlegend=False)

        # Mostra il grafico
        st.plotly_chart(fig, theme=None, use_container_width=True)
#################################################################################################################################################################################################################################

    @staticmethod
    def plot_criticita(df):


        # Passaggio 1: Rimpiazzo delle stringhe nella colonna 'criticita'
        df['criticita'] = df['criticita'].str.replace(
            r'Inadeguata analisi dei Business Case, la quale ha portato a sottovalutare alcune criticità o non cogliere determinate opportunità.',
            'Inadeguata analisi dei Business Case', regex=True
        )
        df['criticita'] = df['criticita'].str.replace(
            r'Problematiche emerse durante la fase di implementazione, come ad esempio un non adeguato ingaggio degli attori coinvolti.',
            'Problematiche emerse durante la fase di implementazione', regex=True
        )
        df['criticita'] = df['criticita'].str.replace(
            r'Inadeguato allineamento tra strategia e attività svolta.',
            'Inadeguato allineamento tra strategia e attività svolta', regex=True
        )

        # Passaggio 2: Inizializzazione del dizionario per conteggiare le criticità
        dizionario1 = {
            'Inadeguata analisi dei Business Case': 0,
            'Problematiche emerse durante la fase di implementazione': 0,
            'Inadeguato allineamento tra strategia e attività svolta': 0,
            'Governance del progetto non adeguata': 0
        }

        # Passaggio 3: Conteggio delle occorrenze per ogni tipo di criticità
        for risposta in df['criticita'].fillna(''):  # Rimpiazziamo NaN con stringa vuota
            for key in dizionario1.keys():
                if key in risposta:
                    dizionario1[key] += 1

        # Passaggio 4: Creazione delle liste per il grafico
        criticita = list(dizionario1.keys())
        conteggi = list(dizionario1.values())

        # Creazione del DataFrame per il grafico
        df_criticita = pd.DataFrame({
            'Criticità': criticita,
            'Conteggi': conteggi
        })

        # Passaggio 5: Creazione del grafico a barre con Plotly
        colors = ['#f8a8a8', '#f07474', '#e14444', '#b93333']

        fig = px.bar(df_criticita, 
                    x='Criticità', 
                    y='Conteggi', 
                    color='Criticità',  
                    color_discrete_sequence=colors,  # Applica i colori definiti
                    text='Conteggi', 
                    title="Distribuzione delle criticità",
                    width=400, 
                    height=500)
        fig.update_layout(showlegend=False)




        st.plotly_chart(fig, theme=None, use_container_width=True)

############################################################################################## SODDISFAZIONE E MIGLIORAMENTI ######################################################################################################
    @staticmethod
    def analyze_soddisfazione(df):
        """
        Analizza la colonna 'soddisfazione' e visualizza un grafico a torta basato sui valori unici,
        escludendo i valori NaN e mappando i valori numerici in descrizioni.
        
        Args:
            df (pd.DataFrame): DataFrame contenente i dati.
        """
        
        # Verifica se la colonna 'soddisfazione' esiste nel DataFrame
        if 'soddisfazione' not in df.columns:
            st.error("Colonna 'soddisfazione' non trovata nel DataFrame.")
            return

        # Mappatura dei valori numerici a descrizioni
        satisfaction_map = {
            1.0: "Per niente soddisfatto",
            2.0: "Poco soddisfatto",
            3.0: "Soddisfatto",
            4.0: "Molto soddisfatto",
            5.0: "Pienamente soddisfatto"
        }
        
        # Estrai i valori unici dalla colonna 'soddisfazione', escludendo i NaN
        soddisfazione_values = df['soddisfazione'].dropna()

        # Mappatura dei valori numerici a descrizioni
        mapped_values = soddisfazione_values.map(satisfaction_map)
        
        # Conta le occorrenze di ciascun valore
        value_counts = mapped_values.value_counts()

        # Creazione del grafico a torta
        fig = go.Figure(data=[go.Pie(
            labels=value_counts.index,  # Etichette con le descrizioni
            values=value_counts.values,
            marker=dict(colors=['#FAD02E', '#F28D35', '#D83367', '#1F4068', '#5B84B1'] * (len(value_counts) // 5 + 1)),
            textinfo='percent+label',  # Mostra percentuale e etichetta
            textposition='outside',  # Testo fuori dalla torta
            pull=[0.1] * len(value_counts)  # Distacco delle fette
        )])

        # Personalizzazione del layout
        fig.update_layout(
            height=500,
            width=800,
            title="   ",
            paper_bgcolor="#f5f5f5",
            plot_bgcolor="#eaeaea",
            margin=dict(l=40, r=40, t=40, b=40),
            template="plotly"
        )

        # Mostra il grafico in Streamlit
        st.plotly_chart(fig, use_container_width=True)



    @staticmethod
    def analyze_impatto_efficienza(df):
        """
        Analizza una colonna in cui ogni cella può contenere più valori separati da virgola,
        conta le occorrenze di ogni valore e visualizza solo il risultato con un grafico a barre.
        
        Args:
            df (pd.DataFrame): DataFrame contenente i dati.
        """
        
        # Verifica se la colonna 'impatto_efficienza' esiste nel DataFrame
        if 'impatto_efficienza' not in df.columns:
            st.error("Colonna 'impatto_efficienza' non trovata nel DataFrame.")
            return

        # Crea una lista di tutti i valori unici separati da virgola
        all_values = []

        # Estrai tutti i valori separati da virgola e aggiungili alla lista
        for entry in df['impatto_efficienza']:
            if isinstance(entry, str):  # Verifica che l'entry sia una stringa
                values = entry.split(',')
                all_values.extend([v.strip() for v in values])  # Rimuove spazi indesiderati
            else:
                continue

        # Conta le occorrenze di ciascun valore
        value_counts = pd.Series(all_values).value_counts()

        # Creazione del grafico a barre
        fig = go.Figure(data=[go.Bar(
            x=value_counts.index, 
            y=value_counts.values,
            text=value_counts.values,  # Mostra il conteggio sopra le barre
            textposition='auto',  # Posiziona il testo sopra le barre
            marker=dict(color=['#FAD02E', '#F28D35', '#D83367', '#1F4068', '#5B84B1'] * (len(value_counts) // 5 + 1))  # Colori dinamici
        )])

        # Personalizzazione del layout
        fig.update_layout(
            height=500, 
            width=800,
            title="   ",  # Titolo del grafico
            paper_bgcolor="#f5f5f5",
            plot_bgcolor="#eaeaea", 
            margin=dict(l=40, r=40, t=40, b=40),
            template="plotly"
        )

        # Mostra il grafico in Streamlit
        st.plotly_chart(fig, use_container_width=True)
    @staticmethod
    def analyze_milgioramenti(df):
        """
        Analizza una colonna in cui ogni cella può contenere più valori separati da virgola,
        conta le occorrenze di ogni valore e visualizza solo il risultato con un grafico a torta.
        
        Args:
            df (pd.DataFrame): DataFrame contenente i dati.
        """
        
        # Verifica se la colonna 'miglioramenti' esiste nel DataFrame
        if 'miglioramenti' not in df.columns:
            st.error("Colonna 'miglioramenti' non trovata nel DataFrame.")
            return

        # Crea una lista di tutti i valori unici separati da virgola
        all_values = []

        # Estrai tutti i valori separati da virgola e aggiungili alla lista
        for entry in df['miglioramenti']:
            if isinstance(entry, str):  # Verifica che l'entry sia una stringa
                values = entry.split(',')
                all_values.extend([v.strip() for v in values])  # Rimuove spazi indesiderati
            else:
                continue

        # Conta le occorrenze di ciascun valore
        value_counts = pd.Series(all_values).value_counts()

        # Creazione del grafico a torta
        fig = go.Figure(data=[go.Pie(
            labels=value_counts.index, 
            values=value_counts.values,
            marker=dict(colors=['#FAD02E', '#F28D35', '#D83367', '#1F4068', '#5B84B1'] * (len(value_counts) // 5 + 1)),  # Colori dinamici
            textinfo='percent+label', 
            textposition='outside', 
            pull=[0.1] * len(value_counts)  # Aggiunge un po' di distacco per ogni fetta
        )])

        # Personalizzazione del layout
        fig.update_layout(
            height=500, 
            width=800,
            title="  ",  # Titolo del grafico
            showlegend=False, 
            paper_bgcolor="#f5f5f5",
            plot_bgcolor="#eaeaea", 
            margin=dict(l=40, r=40, t=40, b=40),
            template="plotly"
        )

        # Mostra il grafico in Streamlit
        st.plotly_chart(fig, use_container_width=True)


class GraficoFigure:
    def __init__(self, df):
        """
        Inizializza la classe con il dataframe.
        """
        self.df = df  # Memorizza il dataframe nell'istanza
        
        # Dizionario per mappare le risposte
        self.mappa_risposte = {
            "Molto D'accordo": 4,
            "D'accordo": 3,
            "Neutrale": 2,
            "In disaccordo": 1,
            np.nan: 0  # Se np.nan è una risposta, mappiamola a 0
        }
    @staticmethod
    def plot_graph(self, column_name):
        """
        Genera un grafico a torta e a barre per una colonna specifica del dataframe.
        """
        df = self.df  # Usa il dataframe memorizzato nell'istanza
        df[column_name] = df[column_name].map(self.mappa_risposte)
        competency_counts = df[column_name].value_counts()

        # Mappa inversa per visualizzare le risposte originali
        response_map_inverse = {
            4: "Molto D'accordo",
            3: "D'accordo",
            2: "Neutrale",
            1: "In disaccordo",
            0: "Nessuna risposta"
        }

        competency_counts.index = competency_counts.index.map(response_map_inverse)
        total = competency_counts.sum()
        percentages = (competency_counts / total) * 100

        # Creazione del grafico
        fig = make_subplots(
            rows=1, cols=2, 
            specs=[[{'type': 'pie'}, {'type': 'bar'}]],
            column_widths=[0.48, 0.48],
            horizontal_spacing=0.2
        )

        fig.add_trace(
            go.Pie(
                labels=competency_counts.index, 
                values=competency_counts.values,
                texttemplate='%{label}<br><b>%{percent}</b>',
                textposition='outside',
                pull=[0.1] * len(competency_counts),
                showlegend=False
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Bar(
                x=competency_counts.index,
                y=competency_counts.values,
                text=percentages.round(1).astype(str) + '%',
                textposition='auto'
            ),
            row=1, col=2
        )

        return fig

    # Metodi specifici per ogni colonna (richiamano plot_graph)
    def plot_cdh_conoscenze(self):
        st.plotly_chart(self.plot_graph(self, "cdh_conoscenze"), use_container_width=True)

    def plot_cdh_competenze_tecniche(self):
        st.plotly_chart(self.plot_graph(self, 'cdh_competenze_tecniche'), use_container_width=True)

    def plot_cdh_abilita_analitiche(self):
        st.plotly_chart(self.plot_graph(self, 'cdh_abilita_analitiche'), use_container_width=True)

    def plot_cdh_innovazione(self):
        st.plotly_chart(self.plot_graph(self, 'cdh_innovazione'), use_container_width=True)

    def plot_cdh_formazione(self):
        st.plotly_chart(self.plot_graph(self, 'cdh_formazione'), use_container_width=True)



#################################################################################### INFRASTRUTTURE DIGITALI ####################################################################################


class GraficoInfrastruttura:
    def __init__(self, df):
        self.df = df
        self.mappa_risposte = {
            'Molto D\'accordo': 4,
            'D\'accordo': 3,
            'Neutrale': 2,
            'In disaccordo': 1,
            np.nan: 0  # Se np.nan è una risposta, mappiamola a 0
        }
                # Mappa inversa per visualizzare le risposte originali
        self.mappa_risposte_inversa = {
            4: "Molto D\'accordo",
            3: "D\'accordo",
            2: "Neutrale",
            1: "In disaccordo",
            0: "Nessuna risposta"
        }
        self.colori = ['#228B22', '#8fbc8f', '#66cdaa', '#2e8b57', '#006400']

    def plot_graph(self, column_name):
        self.df[column_name] = self.df[column_name].map(self.mappa_risposte)
        competency_counts = self.df[column_name].value_counts()
        competency_counts.index = competency_counts.index.map(self.mappa_risposte_inversa)

        total = competency_counts.sum()
        percentages = (competency_counts / total) * 100

        fig = make_subplots(
            rows=1, cols=2, 
            specs=[[{'type': 'pie'}, {'type': 'bar'}]],
            column_widths=[0.48, 0.48],
            horizontal_spacing=0.2
        )

        fig.add_trace(
            go.Pie(
                labels=competency_counts.index, 
                values=competency_counts.values,
                marker=dict(colors=self.colori),
                texttemplate='%{label}<br><b>%{percent}</b>',
                textposition='outside',
                pull=[0.1] * len(competency_counts),
                showlegend=False
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Bar(
                x=competency_counts.index,
                y=competency_counts.values,
                marker=dict(color=self.colori[:len(competency_counts)]),
                text=percentages.values.round(1).astype(str) + '%',
                textposition='outside',
                showlegend=False
            ),
            row=1, col=2
        )

        fig.update_layout(
            title=" ",
            title_x=0.5,
            height=500, 
            width=1000,
            template='plotly_white'
        )

        return fig

    def plot_hardware(self):
        st.plotly_chart(self.plot_graph('infr_hardware'), use_container_width=True, key='hardware_button')

    def plot_software(self):
        st.plotly_chart(self.plot_graph('infr_software'), use_container_width=True, key='software_button')

    def plot_cloud(self):
        st.plotly_chart(self.plot_graph('infr_cloud'), use_container_width=True, key='cloud_button')

    def plot_sicurezza(self):
        st.plotly_chart(self.plot_graph('infr_sicurezza'), use_container_width=True, key='sicurezza_button')

###################################################### ECOSISTEMA RELAZIONI #########################################################################################################

class GraficoRelazioni:
    def __init__(self, df):
        self.df = df
        self.mappa_risposte = {
            'Molto D\'accordo': 4,
            'D\'accordo': 3,
            'Neutrale': 2,
            'In disaccordo': 1,
            np.nan: 0  # Se np.nan è una risposta, mappiamola a 0
        }
        self.mappa_risposte_inversa = {
                4: 'Molto D\'accordo',
                3: 'D\'accordo',
                2: 'Neutrale',
                1: 'In disaccordo',
                0: 'Nessuna risposta'
            }
        self.colori = ['#228B22', '#8fbc8f', '#66cdaa', '#2e8b57', '#006400']

# Funzione generica per creare grafici a torta e a barre per una colonna
    def plot_graph2(self, column_name):
            self.df[column_name] = self.df[column_name].map(self.mappa_risposte)
            competency_counts = self.df[column_name].value_counts()

            # Riorganizza l'indice e applica la mappa inversa per ottenere le etichette originali
            competency_counts.index = competency_counts.index.map(self.mappa_risposte_inversa)

            # Calcola la percentuale di ciascun valore
            total = competency_counts.sum()
            percentages = (competency_counts / total) * 100

            # Crea un subplot con 1 riga e 2 colonne (grafico a torta e grafico a barre)
            fig = make_subplots(
                rows=1, cols=2, 
                specs=[[{'type': 'pie'}, {'type': 'bar'}]],  # Usa 'bar' per il grafico a barre
                column_widths=[0.48, 0.48],  # Imposta la larghezza delle colonne (più vicine)
                horizontal_spacing=0.2  # Riduce la distanza orizzontale tra i grafici
            )

            # Aggiungi il grafico a torta
            fig.add_trace(
                go.Pie(
                    labels=competency_counts.index, 
                    values=competency_counts.values,
                    marker=dict(
                        colors=['#9370DB', '#1E90FF', '#006D5B', '#6A5ACD', '#4B0082']  # Gradazione di colori
                    ),
                    texttemplate='%{label}<br><b>%{percent}</b>',  # Mostra percentuale e etichetta
                    textposition='outside',  # Posiziona il testo fuori dalle fette
                    pull=[0.1] * len(competency_counts),  # Aggiungi un po' di spazio tra le fette
                    showlegend=False  # Nascondi la legenda
                ),
                row=1, col=1
            )
            # Aggiungi il grafico a barre con asse Y e X invertiti
            fig.add_trace(
                go.Bar(
                    x=competency_counts.index,  # Etichette ordinate
                    y=competency_counts.values,  # Conteggi ordinati
                    text=percentages.values.round(1).astype(str) + '%',  # Mostra la percentuale sopra le barre
                    textposition='outside',  # Posiziona il testo sopra le barre
                    marker=dict(
                        color=['#9370DB', '#1E90FF', '#006D5B', '#6A5ACD', '#4B0082'][:len(competency_counts)],  # Applica i colori nell'ordine specificato
                    ),
                    showlegend=False,  # Nascondi la legenda per il grafico a barre
                ),
                row=1, col=2
            )

            # Aggiungi titolo e layout
            fig.update_layout(
                title=" ",  # Non inserire alcun titolo
                title_x=0.5,  # Centra il titolo orizzontalmente
                height=500, 
                width=1000,  # Imposta la larghezza del grafico
                template='plotly_white',
                xaxis=dict(title='Conteggio', showgrid=True),  # Aggiungi l'asse X
                yaxis=dict(title='Risposte', showgrid=True),  # Aggiungi l'asse Y
            )

            return fig

        # Funzione per il grafico delle interazioni digitali
    def plot_cdh_interazione(self):
            """
            Genera il grafico per la colonna 'eco_interazione' in formato a torta e a barre.
            """
            st.plotly_chart(self.plot_graph2('eco_interazione'), use_container_width=True, key='eco_interazione')

        # Funzione per il grafico delle piattaforme digitali
    def plot_cdh_piattaforme(self):
            """
            Genera il grafico per la colonna 'eco_piattaforme' in formato a torta e a barre.
            """
            st.plotly_chart(self.plot_graph2('eco_piattaforme'), use_container_width=True, key='eco_piattaforme')

        # Funzione per il grafico dei processi digitalizzati
    def plot_cdh_processi(self):
            """
            Genera il grafico per la colonna 'eco_processi' in formato a torta e a barre.
            """
            st.plotly_chart(self.plot_graph2('eco_processi'), use_container_width=True, key='eco_processi')
