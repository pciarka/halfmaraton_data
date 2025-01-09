import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # type: ignore
st.set_page_config(page_title="Przegląd danych")
st.markdown('## Analiza półmaratonu wrocławskiego 2024')

df=pd.read_csv('halfmarathon_wroclaw_2024__final.csv', sep=';')

#Zmajstrowanie sidebara
with st.sidebar:
    name = st.text_input('Podaj imię biegacza')
    countries = st.multiselect('Wybierz kraj', sorted(df["Kraj"].dropna().unique()))
    age_categories = st.multiselect(
        'Wybierz kategorię wiekową',
        sorted(df['Kategoria wiekowa'].dropna().unique())
    )
    gender = st.radio(
        "Wybierz płeć",
        ["Wszyscy", "Mężczyźni", "Kobiety"],
    )
#Działania pod wpływem sidebara

if name:
    df=df[df['Imię'].str.contains(name, case=False)]

if countries:
    df=df[df["Kraj"].isin(countries)]

if age_categories:
    df=df[df["Kategoria wiekowa"].isin(age_categories)]

if gender:
    df=df[df['Imię'].str.contains(name, case=False)]




c0, c1, c2 = st.columns(3)

with c0:
    st.metric("Liczba zawodników", len(df[df['Płeć']=='M']))

with c1:
    st.metric("Liczba mężczyzn", len(df))   
with c2:
    st.metric("Liczba kobiet", len(df[df['Płeć']=='K'])) 

    # 10 losowych wierszy
x = min(10, len(df))
st.write(f"## {x} losowych wierszy")
st.dataframe(df.sample(x), use_container_width=True, hide_index=True)

# TOP 5 zawodników
st.header("Top 5 zawodników")
top_columns = ["Miejsce", "Numer startowy", "Imię", "Nazwisko", "Miasto", "Kraj", "Czas"]
st.dataframe(
    df.sort_values("Miejsce")[top_columns].head(5),
    hide_index=True,
    use_container_width=True,
)

# Barplot krajów
st.header("Pochodzenie zawodników")
gdf = df.groupby("Kraj", as_index=False).count().rename(columns={"Miejsce": "Liczba zawodników"})
st.bar_chart(gdf, x="Kraj", y="Liczba zawodników")

# Histogram czasu na mecie
st.header("Histogram czasu na mecie")
df["Czas"] = pd.to_datetime(df["Czas"], format='%H:%M:%S', errors="coerce").dt.time

# Tworzenie histogramu przy użyciu seaborn
plt.figure(figsize=(10, 6))
plot = sns.histplot(df["Czas"].apply(lambda x: x.hour * 60 + x.minute + x.second / 60), kde=True)

st.pyplot(plot.figure)

# Macierz korelacji
st.header("Macierz korelacji")
correlation_matrix = df.corr(numeric_only=True)
plt.figure(figsize=(16, 12))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', cbar=True)
st.pyplot(plt.gcf())



# Pogłębiona analiza korelacji
# st.header("Pogłębiona analiza korelacji")
# pairplot_fig=sns.pairplot(df, hue='Płeć', vars=['Rocznik', 'Miejsce', 'Numer startowy'])
# st.pyplot(pairplot_fig)


