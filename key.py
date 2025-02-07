import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import unicodedata
df = pd.read_excel('cleaned_data.xlsx')

class key:
    def __init__(self, df):
        self.df = df

    def mappa_maturita(self):
        values = {
            'Siamo una azienda relativamente digitale; alcuni processi aziendali sono stati digitalizzati con l introduzione di tecnologie digitali': 'Relativamente digitale',
            'È stato avviato qualche progetto pilota di trasformazione digitale che al momento è ancora in corso': 'Qualche progetto avviato',
            'Siamo una azienda totalmente Digital Oriented; tutti i nostri processi sono supportati dall utilizzo di tecnologie digitali': 'Totalmente Digital Oriented',
            'Al momento non è in corso un processo di trasformazione digitale né è stato avviato e concluso in passato': 'Non digitalizzato',
            'È stato avviato qualche progetto pilota di trasformazione digitale che è stato interrotto e non portato a compimento': 'Qualche progetto interrotto'
        }
        
        # Normalizza le stringhe nella colonna 'maturita_digitale'
        self.df['maturita_digitale'] = self.df['maturita_digitale'].apply(lambda x: unicodedata.normalize('NFKD', x) if isinstance(x, str) else x)
        
        self.df['maturita_digitale'] = self.df['maturita_digitale'].replace(values)
        self.df['maturita_digitale'].fillna('Nessuna risposta', inplace=True)
    # Funzione per creare lo scatter plot

    # Funzione per la creazione del grafico
    def hist_soddisfazione_maturita(self):
        # Assicurati che la funzione 'mappa_maturita' sia stata applicata in precedenza
        self.mappa_maturita()  # Applica la mappatura sulla maturità digitale
        pastel_colors = ['#FAD02E', '#F28D35', '#D83367', '#1F4068', '#5B84B1', '#6B4226']
        # Creiamo un istogramma per Soddisfazione e Maturità Digitale insieme
        fig = px.histogram(
            self.df,  # DataFrame con le colonne 'soddisfazione' e 'maturita_digitale'
            x="soddisfazione",  # Asse X per Soddisfazione
            color="maturita_digitale",  # Colori per la maturità digitale
            nbins=5,  # Numero di barre (puoi aggiustarlo se necessario)
            title=" ",
            labels={"soddisfazione": "Livello di Soddisfazione", "maturita_digitale": "Maturità Digitale"},
            template="plotly_white",  # Tema bianco
            histfunc="count",  # Calcola il numero di occorrenze
            color_discrete_sequence=pastel_colors)
        
        # Personalizzazione del layout
        fig.update_layout(
            title={'text': ' ', 'x': 0.5},
            xaxis=dict(
                title="Livello di Soddisfazione",
                title_font=dict(size=14, family='Arial', weight='bold')  # Titolo in grassetto
            ),
            yaxis=dict(
                title="Numero di Aziende",
                title_font=dict(size=14, family='Arial', weight='bold')  # Titolo in grassetto
            ),
            font=dict(size=14),
            width=800,
            height=600
        )

        # Mostriamo il grafico in Streamlit
        st.plotly_chart(fig, use_container_width=True)


#################################################################################################### Maturità Digitale e Infrastrutture Digitali ####################################################################################################
    # Funzione per mappare le risposte
    def mappa_risposte(self):
        mappa_risposte = {
            'Molto D\'accordo': 4,
            'D\'accordo': 3,
            'Neutrale': 2,
            'In disaccordo': 1,
            np.nan: 0  
        }
        
        self.df[['infr_hardware', 'infr_software', 'infr_cloud', 'infr_sicurezza']] = self.df[['infr_hardware', 'infr_software', 'infr_cloud', 'infr_sicurezza']].replace('Nessuna risposta', np.nan)
        
        # Applica la mappatura a tutte le colonne delle infrastrutture
        for col in ['infr_hardware', 'infr_software', 'infr_cloud', 'infr_sicurezza']:
            self.df[col] = self.df[col].map(mappa_risposte)

        # Converte le colonne delle infrastrutture in tipo numerico per evitare problemi con la media
        for col in ['infr_hardware', 'infr_software', 'infr_cloud', 'infr_sicurezza']:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')  # Converte in numerico, sostituendo eventuali errori con NaN
        # Funzione per creare il grafico con intensità del colore basata sul conteggio delle aziende
    def visualizza_maturita_infrastrutture(self):
        # Applica la mappatura delle risposte
        self.mappa_risposte()
        
        # Gestisci i valori NaN nelle colonne delle infrastrutture (li mappiamo a 0)
        self.df[['infr_hardware', 'infr_software', 'infr_cloud', 'infr_sicurezza']] = self.df[['infr_hardware', 'infr_software', 'infr_cloud', 'infr_sicurezza']].fillna(0)

        # Rimuovi le righe dove non ci sono risposte valide per nessuna infrastruttura
        self.df = self.df.dropna(subset=['maturita_digitale'])

        # Filtra per rimuovere "Nessuna risposta" dalla colonna 'maturita_digitale'
        self.df = self.df[self.df['maturita_digitale'] != 'Nessuna risposta']

        # Raggruppa i dati per 'maturita_digitale' e calcola la media per ogni infrastruttura
        infrastrutture = ['infr_hardware', 'infr_software', 'infr_cloud', 'infr_sicurezza']
        data = []

        # Calcoliamo il conteggio delle risposte per ogni livello di maturità digitale
        conteggi = self.df['maturita_digitale'].value_counts().reset_index()
        conteggi.columns = ['maturita_digitale', 'conteggio']

        for infrastruttura in infrastrutture:
            media_infrastruttura = self.df.groupby('maturita_digitale')[infrastruttura].mean().reset_index()
            media_infrastruttura['infrastruttura'] = infrastruttura
            data.append(media_infrastruttura)

        # Unisci tutti i dati
        df_grouped = pd.concat(data, ignore_index=True)

        # Aggiungi i conteggi alle medie delle infrastrutture
        df_grouped = df_grouped.merge(conteggi, on='maturita_digitale', how='left')

        # Crea il layout con 1 subplot
        fig = go.Figure()

        # Aggiungi i grafici per ogni infrastruttura
        for i, infrastruttura in enumerate(infrastrutture):
            df_infrastruttura = df_grouped[df_grouped['infrastruttura'] == infrastruttura]

            fig.add_trace(
                go.Bar(
                    x=df_infrastruttura['maturita_digitale'],  # Maturità Digitale sull'asse X
                    y=df_infrastruttura[infrastruttura],       # Media dei punteggi sull'asse Y
                    name=infrastruttura,
                    marker=dict(
                        color=df_infrastruttura['conteggio'],  # Intensità del colore basata sul conteggio
                        colorscale=['#FAD02E', '#F28D35', '#D83367', '#1F4068', '#5B84B1'],  # Colori specificati
                        colorbar=dict(title="Conteggio Aziende")  # Barra dei colori
                    ),
                    hovertemplate='Infrastruttura: %{text}<br>Maturità Digitale: %{x}<br>Media Punteggi: %{y}<br>Conteggio Aziende: %{marker.color}',
                    text=infrastruttura
                )
            )

        # Aggiorna layout con titoli, etichette e altre personalizzazioni
        fig.update_layout(
            height=600,
            width=800,
            title_text="Distribuzione della Maturità Digitale rispetto alle Infrastrutture Digitali",
            showlegend=False,  # Rimuove la legenda
            barmode='group',  # I grafici saranno raggruppati per ogni livello di maturità digitale
            xaxis_title="Maturità Digitale",
            yaxis_title="Media Punteggi",
            font=dict(size=12)
        )

        # Mostriamo il grafico
        st.plotly_chart(fig, use_container_width=True)



#################################################################################################### Maturità Digitale e Relazioni Digitali ####################################################################################################

    def mappa_risposte1(self):
        mappa_risposte = {
            'Molto D\'accordo': 4,
            'D\'accordo': 3,
            'Neutrale': 2,
            'In disaccordo': 1,
            np.nan: 0  
        }
        
        #
        self.df[['cdh_conoscenze', 'cdh_competenze_tecniche', 'cdh_abilita_analitiche', 'cdh_innovazione', 'cdh_formazione']] = self.df[['cdh_conoscenze', 'cdh_competenze_tecniche', 'cdh_abilita_analitiche', 'cdh_innovazione', 'cdh_formazione']].replace('Nessuna risposta', np.nan)
        
        # Applica la mappatura a tutte le colonne specificate nel dizionario
        for col in ['cdh_conoscenze', 'cdh_competenze_tecniche', 'cdh_abilita_analitiche', 'cdh_innovazione', 'cdh_formazione']:
            self.df[col] = self.df[col].map(mappa_risposte)

        # Converte le colonne in tipo numerico per evitare problemi con la media
        for col in ['cdh_conoscenze', 'cdh_competenze_tecniche', 'cdh_abilita_analitiche', 'cdh_innovazione', 'cdh_formazione']:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')  # Converte in numerico, sostituendo eventuali errori con NaN

    # Funzione per creare il grafico con intensità del colore basata sul conteggio delle aziende
    def visualizza_maturita_figure(self):
        titles_dict = {
            'cdh_conoscenze': "figure conoscenze digitali",
            'cdh_competenze_tecniche': "figure competenze tecniche",
            'cdh_abilita_analitiche': "figure abilità analitiche/decisionali",
            'cdh_innovazione': "figure capacità di innovazione",
            'cdh_formazione': "formazione continua"
        }
        # Applica la mappatura delle risposte
        self.mappa_risposte1()
        
        # Gestisci i valori NaN nelle colonne (li mappiamo a 0)
        self.df[['cdh_conoscenze', 'cdh_competenze_tecniche', 'cdh_abilita_analitiche', 'cdh_innovazione', 'cdh_formazione']] = self.df[['cdh_conoscenze', 'cdh_competenze_tecniche', 'cdh_abilita_analitiche', 'cdh_innovazione', 'cdh_formazione']].fillna(0)

        # Rimuovi le righe dove non ci sono risposte valide per 'maturita_digitale'
        self.df = self.df.dropna(subset=['maturita_digitale'])

        # Filtra per rimuovere "Nessuna risposta" dalla colonna 'maturita_digitale'
        self.df = self.df[self.df['maturita_digitale'] != 'Nessuna risposta']
        self.df = self.df[self.df['maturita_digitale'] != 'Non digitalizzato'] 

        # Raggruppa i dati per 'maturita_digitale' e calcola la media per ogni colonna
        columns = ['cdh_conoscenze', 'cdh_competenze_tecniche', 'cdh_abilita_analitiche', 'cdh_innovazione', 'cdh_formazione']
        data = []

        # Calcoliamo il conteggio delle risposte per ogni livello di maturità digitale
        conteggi = self.df['maturita_digitale'].value_counts().reset_index()
        conteggi.columns = ['maturita_digitale', 'conteggio']

        for col in columns:
            media_col = self.df.groupby('maturita_digitale')[col].mean().reset_index()
            media_col['colonna'] = col
            data.append(media_col)

        # Unisci tutti i dati
        df_grouped = pd.concat(data, ignore_index=True)

        # Aggiungi i conteggi alle medie delle colonne
        df_grouped = df_grouped.merge(conteggi, on='maturita_digitale', how='left')

        # Crea il layout con 1 subplot
        fig = go.Figure()

        # Aggiungi i grafici per ogni colonna
        for i, col in enumerate(columns):
            df_col = df_grouped[df_grouped['colonna'] == col]

            fig.add_trace(
                go.Bar(
                    x=df_col['maturita_digitale'],  # Maturità Digitale sull'asse X
                    y=df_col[col],                   # Media dei punteggi sull'asse Y
                    name=titles_dict[col],           # Usa il titolo dal dizionario
                    marker=dict(
                        color=df_col['conteggio'],   # Intensità del colore basata sul conteggio
                        colorscale=['#FAD02E', '#F28D35', '#D83367', '#1F4068', '#5B84B1'],  # Colori specificati
                        colorbar=dict(title="Conteggio Aziende")  # Barra dei colori
                    ),
                    hovertemplate='Colonna: %{text}<br>Maturità Digitale: %{x}<br>Media Punteggi: %{y}<br>Conteggio Aziende: %{marker.color}',
                    text=titles_dict[col]  # Aggiungi il titolo
                )
            )

        # Aggiorna layout con titoli, etichette e altre personalizzazioni
        fig.update_layout(
            height=600,
            width=800,
            title_text="  ",
            showlegend=False,  # Rimuove la legenda
            barmode='group',  # I grafici saranno raggruppati per ogni livello di maturità digitale
            xaxis_title="Maturità Digitale",
            yaxis_title="Media Punteggi",
            font=dict(size=12)
        )

        # Mostriamo il grafico
        st.plotly_chart(fig, use_container_width=True)



#################################################################################################### Maturità Digitale e Data di transizione ####################################################################################################


    def mappa_maturita(self):
        values = {
            'Siamo un\'azienda relativamente digitale; alcuni processi aziendali sono stati digitalizzati con l\'introduzione di tecnologie digitali': 'Relativamente digitale',
            'È stato avviato qualche progetto pilota di trasformazione digitale che al momento è ancora in corso': 'Qualche progetto avviato',
            'Siamo un\'azienda totalmente Digital Oriented; tutti i nostri processi sono supportati dall\'utilizzo di tecnologie digitali': 'Totalmente Digital Oriented',
            'Al momento non è in corso un processo di trasformazione digitale né è stato avviato e concluso in passato': 'Non digitalizzato',
            'È stato avviato qualche progetto pilota di trasformazione digitale che è stato interrotto e non portato a compimento': 'Qualche progetto interrotto'
        }
        if 'maturita_digitale' in self.df.columns:
            self.df['maturita_digitale'] = self.df['maturita_digitale'].replace(values)
            self.df['maturita_digitale'].fillna('Nessuna risposta', inplace=True)

    def analizza_relazione_inizio_maturita_heatmap(self):
        """
        Crea una heatmap che mostra la relazione tra il livello di maturità digitale 
        e l'anno di inizio della digitalizzazione delle aziende.
        
        Args:
            df (pd.DataFrame): DataFrame contenente le colonne 'inizio_trans' e 'maturita_digitale'.
        """
        
        # Mappa la maturità digitale
        self.mappa_maturita()
        
        # Verifica che le colonne esistano
        if 'inizio_trans' not in self.df.columns or 'maturita_digitale' not in self.df.columns:
            st.error("Le colonne 'inizio_trans' e 'maturita_digitale' non sono presenti nel dataset.")
            return

        # Sostituisci i valori NaN con "Nessuna risposta"
        self.df['inizio_trans'].fillna('Nessuna risposta', inplace=True)

        # Definiamo l'ordine delle categorie per una visualizzazione più chiara
        ordine_inizio_trans = [
            "Prima del 2015 ",
            "Tra il 2015 e il 2019 ",
            "Dal 2020 in poi ",
            "Nessuna risposta"
        ]
        
        ordine_maturita = [
            "Non digitalizzato",
            "Qualche progetto interrotto",
            "Qualche progetto avviato",
            "Relativamente digitale",
            "Totalmente Digital Oriented"
        ]
        
        # Creiamo la tabella di contingenza
        tabella_contingenza = self.df.groupby(["inizio_trans", "maturita_digitale"]).size().reset_index(name="conteggio")

        # Ordiniamo le categorie
        tabella_contingenza["inizio_trans"] = pd.Categorical(tabella_contingenza["inizio_trans"], categories=ordine_inizio_trans, ordered=True)
        tabella_contingenza["maturita_digitale"] = pd.Categorical(tabella_contingenza["maturita_digitale"], categories=ordine_maturita, ordered=True)

        # Creiamo la matrice pivot per la heatmap, riempiendo i valori mancanti con 0
        matrice_heatmap = tabella_contingenza.pivot(index="inizio_trans", columns="maturita_digitale", values="conteggio").reindex(index=ordine_inizio_trans, columns=ordine_maturita).fillna(0)

        # Creiamo la heatmap con gli assi invertiti
        fig = px.imshow(
            matrice_heatmap.values,  # Convertiamo la matrice in array
            labels=dict(x="Maturità Digitale", y="Anno di inizio digitalizzazione", color="Numero di Aziende"),
            text_auto=True,
            x=ordine_maturita,  # Impostiamo le etichette per l'asse X (ora Maturità Digitale)
            y=ordine_inizio_trans,  # Impostiamo le etichette per l'asse Y (ora Anno di inizio digitalizzazione)
            color_continuous_scale=['#FAD02E', '#F28D35', '#D83367', '#1F4068', '#5B84B1']  # Palette personalizzata
        )
        fig.update_layout(
            xaxis=dict(
                title=dict(text='Maturità Digitale', font=dict(size=18, family='Arial', weight='bold')),
                tickfont=dict(size=14, family='Arial', weight='bold'),
                tickangle=45,  # Angolo dei tick per evitare sovrapposizione
                showticklabels=True
            ),
            yaxis=dict(
                title=dict(text='Anno di inizio digitalizzazione', font=dict(size=18, family='Arial', weight='bold')),
                tickfont=dict(size=14, family='Arial', weight='bold'),
                showticklabels=True
            ),
            title={'text': '  ', 'x': 0.5},  # Centra il titolo
            template='plotly_white',  # Tema bianco
            font=dict(size=14),  # Aumenta la dimensione del testo
            width=1500,  # Larghezza ancora più grande
            height=900,  # Altezza maggiore per una visualizzazione chiara
            margin=dict(l=200, r=200, t=150, b=30)  # Margini più ampi per evitare il taglio delle etichette
        )
        # Personalizziamo il layout
        fig.update_layout(
            title=" ",
            xaxis_title="Maturità Digitale",
            yaxis_title="Anno di inizio digitalizzazione",
            coloraxis_colorbar=dict(title="Numero di Aziende"),
            width=1500,
            height=900
        )

        # Mostriamo il grafico in Streamlit
        st.plotly_chart(fig, use_container_width=True)

#################################################################################################### MATURITA E LEADER ####################################################################################################
    def analizza_maturita_leader(self):
        """
        Crea una heatmap che mostra la relazione tra il livello di maturità digitale 
        e il coinvolgimento del leader nell'azienda.
        
        Args:
            df (pd.DataFrame): DataFrame contenente le colonne 'coinvolgimento_leader' e 'maturita_digitale'.
        """
        
        # Mappa la maturità digitale
        self.mappa_maturita(self)
        
        # Verifica che le colonne esistano
        if 'coinvolgimento_leader' not in self.df.columns or 'maturita_digitale' not in self.df.columns:
            st.error("Le colonne 'coinvolgimento_leader' e 'maturita_digitale' non sono presenti nel dataset.")
            return

        # Verifica e correggi i valori di 'coinvolgimento_leader'
        self.df['coinvolgimento_leader'] = pd.to_numeric(self.df['coinvolgimento_leader'], errors='coerce')  # Converte in numerico, NaN per valori non numerici
        self.df['coinvolgimento_leader'] = self.df['coinvolgimento_leader'].fillna(0)  # Rimpiazza NaN con 0
        self.df['coinvolgimento_leader'] = self.df['coinvolgimento_leader'].apply(lambda x: x if 0 <= x <= 5 else 0)  # Rimpiazza valori fuori dall'intervallo [0,5] con 0
        
        # Definiamo l'ordine delle categorie numeriche per una visualizzazione più chiara
        ordine_coinvolgimento_leader = [0, 1, 2, 3, 4, 5]  # Aggiungiamo anche il valore '0' per le risposte mancanti

        # Creiamo una mappatura per l'asse Y con frasi descrittive
        etichette_coinvolgimento = {
            0: "Non coinvolto",
            1: "Minimamente coinvolto",
            2: "Coinvolto moderatamente",
            3: "Coinvolto",
            4: "Molto coinvolto",
            5: "Completamente coinvolto"
        }

        ordine_maturita = [
            "Non digitalizzato",
            "Qualche progetto interrotto",
            "Qualche progetto avviato",
            "Relativamente digitale",
            "Totalmente Digital Oriented"
        ]
        
        # Creiamo la tabella di contingenza
        tabella_contingenza = self.df.groupby(["coinvolgimento_leader", "maturita_digitale"]).size().reset_index(name="conteggio")
        
        # Aggiungi un controllo per verificare se la tabella di contingenza è corretta
        if tabella_contingenza.empty:
            st.warning("La tabella di contingenza è vuota. Verifica i dati di input.")
            return

        # Ordiniamo le categorie
        tabella_contingenza["coinvolgimento_leader"] = pd.Categorical(tabella_contingenza["coinvolgimento_leader"], categories=ordine_coinvolgimento_leader, ordered=True)
        tabella_contingenza["maturita_digitale"] = pd.Categorical(tabella_contingenza["maturita_digitale"], categories=ordine_maturita, ordered=True)

        # Creiamo la matrice pivot per la heatmap, riempiendo i valori mancanti con 0
        matrice_heatmap = tabella_contingenza.pivot(index="coinvolgimento_leader", columns="maturita_digitale", values="conteggio").reindex(index=ordine_coinvolgimento_leader, columns=ordine_maturita).fillna(0)

        # Verifica la matrice heatmap
        if matrice_heatmap.isnull().values.any():
            st.warning("La matrice heatmap contiene valori nulli. Assicurati che i dati siano completi.")

        # Creiamo la heatmap con gli assi invertiti
        fig = px.imshow(
            matrice_heatmap.values,  # Convertiamo la matrice in array
            labels=dict(x="Maturità Digitale", y="Coinvolgimento del Leader", color="Numero di Aziende"),
            text_auto=True,
            x=ordine_maturita,  # Impostiamo le etichette per l'asse X (ora Maturità Digitale)
            y=[etichette_coinvolgimento[x] for x in ordine_coinvolgimento_leader],  # Impostiamo le etichette per l'asse Y (ora Coinvolgimento del Leader)
            color_continuous_scale=['#FAD02E', '#F28D35', '#D83367', '#1F4068', '#5B84B1']  # Palette personalizzata
        )
        fig.update_layout(
            xaxis=dict(
                title=dict(text='Maturità Digitale', font=dict(size=18, family='Arial', weight='bold'))),
            yaxis=dict(
                title=dict(text='Coinvolgimento del Leader', font=dict(size=18, family='Arial', weight='bold'))),
            title={'text': '  ', 'x': 0.5},
            template='plotly_white',  # Tema bianco
            font=dict(size=14),  # Aumenta la dimensione del testo
            width=1500,  # Larghezza maggiore per una visualizzazione chiara
            height=900,  # Altezza maggiore
            margin=dict(l=200, r=200, t=150, b=30)  # Margini più ampi per evitare il taglio delle etichette
        )
        # Personalizziamo il layout
        fig.update_layout(
            title=" ",
            xaxis_title="Maturità Digitale",
            yaxis_title="Coinvolgimento del Leader",
            coloraxis_colorbar=dict(title="Numero di Aziende"),
            width=1500,
            height=900
        )

        # Mostriamo il grafico in Streamlit
        st.plotly_chart(fig, use_container_width=True)
