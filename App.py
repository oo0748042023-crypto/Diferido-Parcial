import streamlit as st
from textblob import TextBlob
import pandas as pd

# Función para clasificar el sentimiento basado en la polaridad
def clasificar_sentimientos_textblob(polaridad):
    if polaridad > 0:
            return "Positivo"
    elif polaridad < 0:
        return "Negativo"
    else:
        return "Neutral"
    
#CONFIGURACIÓN DE STREAMLIT
st.title("Analisis de sentimiento Textual (Textblob)")
st.subheader("Demostracion 1: \nAnalisis en Tiempo Real")
st.write("Ingrese una frase para analizar el sentimiento inmediato.")

#SECCIÓN 1: ANÁLISIS EN TIEMPO REAL
texto = st.text_area("Ingrese el texto aqui: ", key="input_text")

if st.button("Analisar sentimiento"):
    analizador = TextBlob(texto)
    polaridad = analizador.sentiment.polarity
    sentimiento = clasificar_sentimientos_textblob(polaridad)
    
    # Muestra el resultado con formato de color
    if sentimiento == "positivo":
        st.success(f"Sentimiento: {sentimiento}")
    elif sentimiento == "Negativo":
        st.error(f"Sentimiento: {sentimiento}")
    else:
        st.warning(f"Sentimiento: {sentimiento}")
        
    st.write(f"**Polaridad Calculada:** `{polaridad:.4f}`")
    st.caption("La Polaridad se mide de -1.0 (Muy Negativo) a 1.0 (Muy Positivo).")
    
st.markdown("---")

#SECCIÓN 2: EVALUACIÓN DE DATASET (EL PLUS PARA TU NOTA)
st.subheader("Demostracion 2: Evaluacion del Databaset CSV")
st.write("Este módulo carga el dataset etiquetado para calcular la precisión del modelo TextBlob.")

try:
    # Carga el archivo CSV del dataset
    df = pd.read_csv("Opiniones_Restaurante.xlsx - FrasesEtiquetas.csv")
    st.dataframe(df.head())
    
    if st.button("Evaluar Precisión de TextBlob", key="eval_button"):
        
        st.info("Calculando la polaridad y sentimiento para cada frase del CSV...")
        
        # 1. Calcula la polaridad y sentimiento usando TextBlob para cada frase
        df['Polaridad_TextBlob'] = df['Frase'].apply(lambda x: TextBlob(x).sentiment.polarity)
        df['Sentimiento_TextBlob'] = df['Polaridad_TextBlob'].apply(clasificar_sentimientos_textblob)
        
        # 2. Renombra la columna manual para compararla
        df.rename(columns={'Etiqueta': 'Etiqueta_Manual'}, inplace=True)
        
        # 3. Elimina los casos "Neutrales" para una comparación directa (Positivo vs. Negativo)
        df_filtrado = df[df['Etiqueta_Manual'].isin(['Positivo', 'Negativo'])]
        
        # 4. Compara las etiquetas
        aciertos = (df_filtrado['Etiqueta_Manual'] == df_filtrado['Sentimiento_TextBlob']).sum()
        total = len(df_filtrado)
        precision = (aciertos / total) * 100
        
        st.success(f"¡Precisión Calculada!")
        st.metric(label="Precisión de TextBlob (vs. Etiquetas Manuales)", 
                  value=f"{precision:.2f} %",
                  delta=f"{aciertos} de {total} frases clasificadas correctamente")

except FileNotFoundError:
    st.error("Archivo CSV no encontrado. Asegúrate de que 'Opiniones_Restaurante.xlsx - FrasesEtiquetas.csv' esté en la misma carpeta que 'App.py'.")

# Footer (Opcional)
st.markdown("---")
st.caption("Realizado por: [Milton Ortiz] | Análisis de Sistemas Expertos")

##Realizado por Milton Isabel Ortiz Ortiz - OO0748042023
## Regional San Miguel
##Parcial 1 Diferido