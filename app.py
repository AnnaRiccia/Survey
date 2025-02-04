import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import plotly.io as pio

# Classi importate
from corr import Correlazione
from func import funz, GraficoInfrastruttura, GraficoRelazioni, GraficoFigure
from key import key


pio.templates.default = "plotly"
st.set_page_config(page_title="Digital Transformation Dashboard", layout="wide")
df = pd.read_excel('cleaned_data.xlsx')

# Stato iniziale per il tab e la sottocategoria
if 'selected_tab' not in st.session_state:
    st.session_state.selected_tab = "Analisi Descrittiva"
if 'selected_subcategory' not in st.session_state:
    st.session_state.selected_subcategory = "Intervistato"

# Funzione per aggiornare il tab selezionato
def select_tab(tab):
    st.session_state.selected_tab = tab
    st.session_state.selected_subcategory = "Intervistato"  # Resetta la sottocategoria al valore predefinito

# Sidebar: stile e tab
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #2E2E2E;  /* Grigio scuro */
        color: white;               /* Colore del testo */
    }
    .stSidebar button {
        background-color: #525252; /* Pulsanti grigi */
        color: white;
    }
    .stSidebar button:hover {
        background-color: #FF6600; /* Colore hover */
    }

    /* Modifica la dimensione dell'etichetta radio */
    div[data-baseweb="radio"] label {
        font-size: 24px !important;  /* Aumenta la dimensione del testo */
        color: white !important;  /* Colore bianco per l'etichetta */
    }

    div[data-baseweb="radio"] div[data-state="checked"] label {
        color: #FF6600 !important;  /* Colore per l'opzione selezionata */
    }
    </style>
    """, unsafe_allow_html=True
)
# Funzione per selezionare la tab corrente
def select_tab(tab):
    st.session_state.selected_tab = tab

# Sidebar: sezione per il tab
st.sidebar.title("Navigazione")
tabs = ["Analisi Descrittiva", "Analisi Dimensioni Chiave", "Analisi Correlazionale", 'Autoanalisi']

# Selezione del tab
for tab in tabs:
    if st.sidebar.button(tab, key=tab):
        select_tab(tab)

# Contenuto principale
st.title("Digital Transformation Analysis Dashboard")
st.markdown("---")

# Aggiungi la selezione della sottocategoria direttamente nel corpo principale
if st.session_state.selected_tab == "Analisi Descrittiva":
    st.markdown("<h3 style='color: black; font-size: 36px; font-weight: bold;'>Seleziona una sottocategoria:</h3>", unsafe_allow_html=True)

    # Lista delle categorie
    subcategories = [
        "Intervistato", "Maturità Digitale", "Figure con Competenze Digitali", "Infrastrutture Digitali", "Relazioni e Valore economico", 
        "Transizione Digitale", "Soddisfazione e miglioramenti"
    ]

    # Modifica lo stile del radio button
    st.markdown(
        """
        <style>
        div[data-baseweb="radio"] label {
            font-size: 24px !important;  /* Aumenta la dimensione del testo delle opzioni */
            font-weight: bold !important; /* Rende il testo delle opzioni più evidente */
            color: white !important;  /* Colore bianco per l'etichetta */
        }

        div[data-baseweb="radio"] div[data-state="checked"] label {
            color: #FF6600 !important;  /* Colore per l'opzione selezionata */
            font-weight: bold !important;  /* Rende il testo dell'opzione selezionata più visibile */
        }

        .st-radio input[type="radio"] {
            transform: scale(1.3);  /* Ingrossa i radio button */
        }
        </style>
        """, unsafe_allow_html=True
    )
    
    # Selezione della sottocategoria con st.radio
    selected_subcategory = st.radio(
        " ",
        subcategories,
        index=subcategories.index(st.session_state.get("selected_subcategory", subcategories[0])),
        key="subcategory_radio",
        help="Seleziona una sottocategoria per visualizzare i dati pertinenti."
    )

    # Aggiorna la sottocategoria selezionata in session_state
    if selected_subcategory != st.session_state.get("selected_subcategory"):
        st.session_state.selected_subcategory = selected_subcategory

# Funzione per creare una sezione con un grafico
def create_section(title, plot_function, df, explanation=None):
    col_left, col_center, col_right = st.columns([1, 4, 1])
    with col_center:
        st.markdown(f"### {title}", unsafe_allow_html=True)
        plot_function(df)  # Richiama la funzione passata come parametro
        if explanation:
            st.markdown(f" {explanation}", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
################################################################################# MOSTRA METRICHE #################################################################################


def display_metrics_and_simplify_maturity(df):
    # Funzione per semplificare la maturità digitale
    def semplifica_maturita(x):
        if pd.isna(x):
            return "Non specificato"
        elif "totalmente Digital Oriented" in x:
            return "Totalmente Digital"
        elif "relativamente digitale" in x:
            return "Relativamente Digital"
        elif "progetto pilota" in x:
            return "Fase Pilota"
        else:
            return "Nessuna Trasformazione"
    
    # Applicare la funzione di semplificazione sulla colonna 'maturita_digitale'
    df['maturita_semplificata'] = df['maturita_digitale'].apply(semplifica_maturita)
    
    # Creiamo le colonne per le metriche
    col1, col2, col3, col4, col5= st.columns(5)
    
    # Metriaca 1: Numero totale aziende
    with col3:
        st.metric("Numero totale aziende", len(df))
    
    # Metriaca 2: Media soddisfazione
    with col4:
        # Convertiamo la colonna 'soddisfazione' in numerico per evitare errori di tipo
        df['soddisfazione'] = pd.to_numeric(df['soddisfazione'], errors='coerce')
        st.metric("Media soddisfazione", round(df['soddisfazione'].mean(), 2))



################################################################################# ANALISI DESCRITTVA #################################################################################

if st.session_state.selected_tab == "Analisi Descrittiva":

# INTERVISTATO

    if st.session_state.selected_subcategory == "Intervistato":
        st.markdown("### Analisi descrittiva - Intervistato")
        create_section(
        title='Distribuzione Anni di Esperienza degli intervistati',
        plot_function=funz.plot_fasce_anni,
        df=df,
        explanation= '- Questi dati suggeriscono una varietà di esperienze tra i partecipanti.'
        )
        create_section(
        title='Percentuale Intervistati con mansioni in ambito informatico',
        plot_function=funz.plot_role_distribution,
        df=df,
        explanation= """- Il fatto che il 30% degli intervistati ricopra un ruolo informatico in azienda evidenzia che una parte significativa del personale 
        è direttamente
         coinvolta nella gestione, implementazione e manutenzione delle tecnologie digitali."""
        )
        display_metrics_and_simplify_maturity(df)

# MATURITà DIGITALE


    elif st.session_state.selected_subcategory == "Maturità Digitale":
        st.markdown("### Analisi descrittiva - Maturità Digitale")
        create_section(
        title='Quale delle seguenti affermazioni meglio descrive il livello di maturità digitale presente in azienda?',
        plot_function=funz.analyze_digital_maturity,
        df=df,
        explanation= """- Devo aggiungere descrizione colonna"""
        )
        create_section(
        title='In quale fase del processo di trasformazione digitale si trova l\'azienda?',
        plot_function=funz.analyze_fase_trans,
        df=df,
        explanation=           """
                - Devo aggiungere descrizione colonna AC"""
        )
        create_section(
        title='Quale percentuale del budget operativo è stata allocata per le iniziative di trasformazione digitale nell’azienda nel 2023?',
        plot_function=funz.analyze_budget_trans,
        df=df,
        explanation=            """
                - Devo aggiungere descrizione colonna AA"""
        )
        display_metrics_and_simplify_maturity(df)

# FIGURE CON COMPETENZE DIGITALI

    elif st.session_state.selected_subcategory == "Figure con Competenze Digitali":
        st.markdown("### Analisi descrittiva - Figure con Competenze Digitali")
        grafico3= GraficoFigure(df)
        create_section(
        title='Quali strategie sta adottando l’azienda per attrarre e sviluppare personale con competenze digitali avanzate?',
        plot_function=funz.plot_strategie_talent,
        df=df,
        explanation=           """
            - Aggiungo Spiegazione
            """
        )
        create_section(
        title='In azienda sono presenti figure con conoscenze digitali?',
        plot_function=grafico3.plot_cdh_conoscenze,
        df=df,
        explanation=           """
            - Nel complesso, la maggior parte delle aziende sembra riconoscere la presenza di figure con competenze digitali, 
            con una discreta percentuale che afferma di avere risorse altamente qualificate. 
            Tuttavia, c'è anche una porzione significativa di aziende che non ha espresso un'opinione chiara o che non ha risposto,
            il che potrebbe suggerire un livello di incertezza o di sfida nel riconoscere e valutare adeguatamente le competenze digitali all'interno delle proprie strutture.
            """
        )
        
        create_section(
        title='In azienda sono presenti figure con competenze tecniche?',
        plot_function=grafico3.plot_cdh_competenze_tecniche,
        df=df,
        explanation=            """
                -  la maggior parte delle aziende è consapevole dell'importanza delle competenze tecniche e ha fatto progressi nel dotarsi di figure adeguate.
             Tuttavia, ci sono ancora aziende che devono sviluppare o misurare meglio le competenze tecniche presenti per affrontare le sfide digitali.
            """
        )
        
        create_section(
        title=' In azienda sono presenti figure con abilità analitiche e decisionali?',
        plot_function=grafico3.plot_cdh_abilita_analitiche,
        df=df,
        explanation="""
                 - Molte aziende stanno facendo progressi nel dotarsi di figure con competenze analitiche e decisionali,
                ma c'è ancora una parte significativa di aziende che non ha una visione chiara di queste competenze
                """
        )
        
        create_section(
        title=' In azienda sono presenti figure con capacità di innovazione?',
        plot_function=grafico3.plot_cdh_innovazione,
        df=df,
        explanation=            """
                - Molte aziende stanno facendo progressi nel dotarsi di figure con competenze analitiche e decisionali,
                ma c'è ancora una parte significativa di aziende che non ha una visione chiara di queste competenze
                """
        )
        
        create_section(
        title='Viene fornita una formazione continua?',
        plot_function=grafico3.plot_cdh_formazione,
        df=df,
        explanation="""
                - I dati mostrano una tendenza generalmente favorevole alla formazione continua, sebbene non emergano segnali di consenso unanime. 
                Questo indica che, mentre molte aziende riconoscono il valore della formazione continua,
                potrebbero esserci barriere pratiche o una percezione limitata del suo impatto diretto.
            """
        )
        display_metrics_and_simplify_maturity(df)
   
 
# INFRASTRUTTURE DIGITALLI
    
    elif st.session_state.selected_subcategory == "Infrastrutture Digitali":
        st.markdown("### Analisi descrittiva - Infrastrutture digitali")
        grafico = GraficoInfrastruttura(df)

        create_section(
        title=' Sono presenti in azienda risorse tecnologiche e strutture organizzative che consentano la gestione e l\'elaborazione delle informazioni digitali?',
        plot_function=funz.plot_infr,
        df=df,
        explanation=
            """  
                - Il dato che il 94% circa delle aziende abbia risposto "sì"
                 suggerisce che la stragrande maggioranza delle imprese riconosce l'importanza delle risorse digitali
                 e si è dotata delle infrastrutture necessarie per gestire il flusso di informazioni nel contesto attuale. "
            """
        )
        
        create_section(
        title='In azienda sono presenti hardware per l\'elaborazione e l\'archiviazione dei dati?',
        plot_function=grafico.plot_hardware,
        df=df,
        explanation=
            """  
            - La maggior parte delle aziende è ben equipaggiata con hardware per gestire i dati, ma il 16.4% di risposte mancanti evidenzia possibili lacune nella comunicazione.
            """
        )
        create_section(
        title='In azienda sono presenti software per l\'elaborazione, l\'analisi e la gestione delle informazioni digitali?',
        plot_function=grafico.plot_software,
        df= df,
        explanation=
            """
            - La maggior parte delle aziende è dotata di software per la gestione digitale, ma c'è ancora una piccola parte che potrebbe migliorare o non essere consapevole delle proprie capacità.
            """
        )
        create_section(
        title='In azienda sono presenti servizi cloud per l\'elaborazione e l\'archiviazione dei dati?',
        plot_function=grafico.plot_cloud,
        df= df,
        explanation= 
            """
            -  I servizi cloud non sono ancora completamente integrati nelle infrastrutture aziendali. C'è una divisione tra aziende molto soddisfatte e altre che mostrano incertezza o insoddisfazione.
            """
        )
        create_section(
        title='In azienda sono presenti servizi per la sicurezza informatica?',
        plot_function=grafico.plot_sicurezza,
        df=df,
        explanation= 
            
            """
            -  La sicurezza informatica sembra essere un punto di forza per molte aziende, ma resta il bisogno di approfondire la consapevolezza e migliorare la protezione per una minoranza di organizzazioni.
            """
        )
        display_metrics_and_simplify_maturity(df)
        
# RELAZIONI E VALORE ECONOMICO

    elif st.session_state.selected_subcategory == "Relazioni e Valore economico":
        st.markdown("### Analisi descrittiva - Relazioni e valore economico")
        grafico1 = GraficoRelazioni(df)
        create_section(
        title='Le persone hanno sviluppato relazioni capaci di creare valore economico e di favorire l\'innovazione attraverso tecnologie digitali?',
        plot_function=funz.plot_Rel,
        df = df,
        explanation= 
    
            """
            """
        )
        create_section(
        title='In azienda esistono interazioni efficaci tra le risorse digitali?',
        plot_function=grafico1.plot_cdh_interazione,
        df=df,
        explanation= 
     
            """  
            """
        )
        create_section(
        title='In azienda sono presenti piattaforme digitali per la collaborazione?',
        plot_function=grafico1.plot_cdh_piattaforme,
        df=df,
        explanation= 
     
            """  
            """
        )
        create_section(
        title='In azienda i processi aziendali sono digitalizzati?',
        plot_function=grafico1.plot_cdh_processi,
        df=df,
        explanation= 
     
            """  
            """
        )
        display_metrics_and_simplify_maturity(df)



# TRANSIZIONE DIGITALE


    elif st.session_state.selected_subcategory == "Transizione Digitale":
        st.markdown("### Analisi descrittiva - Transizione Digitale")
        create_section(
        title='All\'interno della tua azienda, è stato intrapreso un processo di Trasformazione Digitale?',
        plot_function=funz.plot_trans,
        df=df,
        explanation= 
     
            """  
            """
        )
        create_section(
        title='Nella tua azienda quand\'è che si è iniziato a pensare in maniera strutturata alla trasformazione digitale?',
        plot_function=funz.inizio_trans,
        df=df,
        explanation= 
     
            """  
            """
        )
        create_section(
        title='Quali stimoli hanno portato all\'attivazione di un processo di trasformazione digitale?',
        plot_function=funz.plot_stimoli_trans_funnel,
        df=df,
        explanation= 
     
            """  
            """
        )
        create_section(
        title='In che modo l’azienda sta responsabilizzando i dipendenti a partecipare attivamente alla trasformazione digitale?',
        plot_function=funz.plot_resp_dipendenti_funnel,
        df=df,
        explanation= 
     
            """  
            """
        )
        create_section(
        title='In che misura i leader aziendali sono coinvolti nelle iniziative di trasformazione digitale della tua azienda?',
        plot_function=funz.plot_coinvolgimento_leader,
        df=df,
        explanation= 
     
            """  
            """
        )
        create_section(
        title='In quali processi della tua azienda vengono utilizzate le risorse digitali?',
        plot_function=funz.plot_processi_digit,
        df=df,
        explanation= 
     
            """  
            """
        )
        create_section(
        title='Quali sono state le criticità riscontrate durante il processo di trasformazione digitale?',
        plot_function=funz.plot_criticita,
        df=df,
        explanation= 
     
            """  
            """
        )
        display_metrics_and_simplify_maturity(df)


##### SODDISFAZIONE E MIGLIORAMENTI
    
    elif st.session_state.selected_subcategory == "Soddisfazione e miglioramenti":
        st.markdown("### Analisi descrittiva - Soddisfazione e miglioramenti")
        st.markdown("    ")
        create_section(
        title='Qual è il grado di soddisfazione del vertice aziendale correlato al processo di trasformazione digitale?',
        plot_function=funz.analyze_soddisfazione,
        df=df,
        explanation= 
            """  
            - Aggiungo spiegazione
            """
        )
        create_section(
        title= 'In che modo la trasformazione digitale ha influenzato l\'efficienza aziendale?',
        plot_function=funz.analyze_impatto_efficienza,
        df=df,
        explanation= 
            """  
                - Aggiungo spiegazione
            """)  
        create_section(
        title='Miglioramenti apportati dal processo di trasformazione digitale',
        plot_function=funz.analyze_milgioramenti,
        df=df,
        explanation= 
            """  
            - Aggiungo spiegazione
            """
        )
        display_metrics_and_simplify_maturity(df)

#################################################################################     ANALISI DIMENSIONE CHIAVE    #################################################################################

elif st.session_state.selected_tab == "Analisi Dimensioni Chiave":
    create_section(
        title='Maturità Digitale e Soddisfazione',
        plot_function=key.hist_soddisfazione_maturita,
        df=df,
        explanation= 
            """  
                    - Aggiungo spiegazione
            """)  
    create_section(
        title='Maturità Digitale e Infrastrutture Digitali',
        plot_function=key.visualizza_maturita_infrastrutture,
        df=df,
        explanation= 
            """  
                   - Ogni livello di maturità digitale possiede un gruppo di barre.
                   - Ogni barra rappresenta l'average score delle infrastrutture (hardware, software, cloud, sicurezza)
                   - I colori aiutano a visualizzare immediatamente la densità delle aziende in ciascun gruppo.
            """)  
    
    create_section(
            title='Maturità Digitale e Presenza Figure Competenti ',
            plot_function=key.visualizza_maturita_figure,
            df=df,
            explanation= 
                """  
                    - Aggiungo spiegazione 
                """)   
    
    create_section(
            title='Periodo di Inizio Transizione Digitale e Maturità Digitale Raggiunta ',
            plot_function=key.analizza_relazione_inizio_maturita_heatmap,
            df=df,
            explanation= 
                """  
                    - Aggiungo spiegazione
                """)
    create_section(
            title='Grado di Coinvolgimento del Leader e Maturità Digitale Raggiunta ',
            plot_function=key.analizza_maturita_leader,
            df=df,
            explanation= 
                """  
                    - Aggiungo spiegazione  
                """)
    display_metrics_and_simplify_maturity(df)


################################################################################# ANALISI CORRELAZIONALE #################################################################################

elif st.session_state.selected_tab == "Analisi Correlazionale":
    create_section(
        title='Correlazione tra Soddisfazione e Budget Investito',
        plot_function=Correlazione.correlazione1_budget,
        df=df,
        explanation= 
            """  
                    - Aggiungo spiegazione
            """)  
    create_section(
        title= 'Correlazione tra Anni di Esperienza e Maturità Digitale',
        plot_function=Correlazione.heatmap_anni_maturita,
        df=df,
        explanation= 
            """  
                    - Aggiungo spiegazione
            """) 
    create_section(
        title= 'Correlazione tra Budget (% sul fatturato) e Criticità Riscontrate',
        plot_function=Correlazione.plot_criticita_budget,
        df=df,
        explanation= 
            """  
                    - Aggiungo spiegazione
            """)  
    create_section(
        title= 'Correlazione tra Impatto sull\'Efficienza e Budget Investito',
        plot_function=Correlazione.cor_budget_efficienza,
        df=df,
        explanation= 
            """  
                    - Aggiungo spiegazione 
            """)  
    display_metrics_and_simplify_maturity(df)

    
################################################################################# Autoanalisi #################################################################################
elif st.session_state.selected_tab == "Autoanalisi":
    st.markdown('Ci lavoro poi a casa')



