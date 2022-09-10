import pandas as pd

import numpy as np

import streamlit as st

from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures

tahminet = False


def tahmindum(marka, atg, model, yt, vites, ccm, kasatip, km):
    dc = {"Marka": marka,

          "Arac Tip Grubu": atg,

          "Model Yıl": model,

          "Yakıt Turu": yt,

          "Vites": vites,

          "CCM": ccm,

          "Kasa Tipi": kasatip,

          "Km": km,

          "Fiyat": 0}

    dfdum = pd.read_csv("car.csv")

    dfdum = dfdum.append(dc, ignore_index=True)

    dfdum = dfdum.drop(columns=["İlan Tarihi", "Arac Tip", "Beygir Gucu",

                                "Renk", "Kimden", "Durum", "Fiyat"], axis=1)

    dfdum = pd.get_dummies(dfdum, columns=["Marka", "Arac Tip Grubu", "Yakıt Turu", "Vites", "CCM",

                                           "Kasa Tipi"], drop_first=True)

    tahminsatir = dfdum.iloc[[-1]]

    return tahminsatir


def tahminreg(model, satir):
    sonuc = model.predict(satir)

    return sonuc


def regresyon(tablo, modelsec, train, randomstate, derece=3):
    tablo = pd.get_dummies(tablo, columns=["Marka", "Arac Tip Grubu", "Yakıt Turu",

                                           "Vites", "CCM", "Kasa Tipi"], drop_first=True)

    y = tablo[['Fiyat']]

    x = tablo.drop(columns=["Fiyat", "Renk", "İlan Tarihi", "Arac Tip", "Beygir Gucu",

                            "Kimden", "Durum"])

    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=train,

                                                        random_state=randomstate)

    if modelsec == "Linear Regression":

        reg = LinearRegression()

    elif modelsec == "Ridge":

        reg = Ridge()

    elif modelsec == "Lasso":

        reg = Lasso()

    elif modelsec == "ElasticNet":

        reg = ElasticNet()
    elif modelsec == "Polinomal":
        poly = PolynomialFeatures(derece)
        polx = poly.fit_transform(x)

    global model

    model = reg.fit(x_train, y_train)

    skor = model.score(x_test, y_test)

    st.write("Skorunuz", skor)


df = pd.read_csv('car.csv')

st.dataframe(df)

modeltip = st.sidebar.selectbox("Model Seçiniz", ["Model", "Linear Regression",

                                                  "Ridge", "Lasso", "ElasticNet", "Polinomal(coming soon"])

if modeltip != "Model":

    train = st.sidebar.slider("Train Size", min_value=0, max_value=100,

                              value=80, step=1)

    st.sidebar.write("Train size değeriniz yüzde", train,

                     "test size değeriniz yüzde", 100 - train)

    train = train / 100

    rs = st.sidebar.number_input("Random State Giriniz", value=25)

    hesap = st.sidebar.button("Skoru Hesapla")

    tahminbuton = st.sidebar.checkbox("Tahmin Oluştur")

    if tahminbuton:

        markalar = list(df['Marka'].unique())

        markalar.insert(0, "Marka Seçiniz")

        marka = st.sidebar.selectbox("Marka Seçiniz", markalar)

        if marka != "Marka Seçiniz":
            a = df[df['Marka'] == marka]

            aractg = st.sidebar.selectbox("Model Seçiniz", a['Arac Tip Grubu'].unique())

        modelyil = st.sidebar.number_input("Model Yılı")

        yakit = st.sidebar.selectbox("Yakıt Türü", df["Yakıt Turu"].unique())

        vites = st.sidebar.selectbox("Vites", df["Vites"].unique())

        kasa = st.sidebar.selectbox("Kasa Tipi", df["Kasa Tipi"].unique())

        ccm = st.sidebar.selectbox("Motor Hacmi", df["CCM"].unique())

        km = st.sidebar.number_input("KM")

        tahminet = st.sidebar.button("Tahmin Et")

    if hesap:
        regresyon(df, modeltip, train, rs)

    if tahminet:
        regresyon(df, modeltip, train, rs)

        # st.write(tahmindum(marka,aractg,modelyil,yakit,vites,ccm,kasa,km))

        st.write("Fiyat Tahmini", tahminreg(model, tahmindum(marka, aractg, modelyil,

                                                             yakit, vites, ccm, kasa, km)))