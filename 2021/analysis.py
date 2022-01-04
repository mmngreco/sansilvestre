# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py,md
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # San Silvestre 2021

import pandas as pd
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
from utils import load_data, plot_hist, get_mine, plot_grid, TIEMPOS, RITMOS, ritmo2minutes
import matplotlib as mpl
import seaborn as sns
import os
if not "JPY_PARENT_PID" in os.environ:
    mpl.use('Qt5Cairo')
    plt.ion()
pd.options.display.float_format = '{:,.2f}'.format
np.set_printoptions(precision=2)
# %precision %.2f

data = load_data()
data.head()

# # Datos inconsistentes

wrong_time = (
    (data["Tiempo Km. 2,5 (Minutos)"] > data["Tiempo Km. 5 (Minutos)"])
    | (data["Tiempo Km. 2,5 (Minutos)"] > data["Tiempo Km. 7,5 (Minutos)"])
    | (data["Tiempo Km. 5 (Minutos)"] > data["Tiempo Km. 7,5 (Minutos)"])
    | (data["Tiempo Km. 2,5 (Minutos)"] > data["Tiempo Km. 10 (Minutos)"])
    | (data["Tiempo Km. 5 (Minutos)"] > data["Tiempo Km. 10 (Minutos)"])
    | (data["Tiempo Km. 7,5 (Minutos)"] > data["Tiempo Km. 10 (Minutos)"])
    | (data.isnull().any(1))
)

data[wrong_time][["Km. 2,5", "Km. 5", "Km. 7,5", "Tiempo"]]

data = data[~wrong_time]

data.shape

mine = get_mine(data)
mine

# # Estadísticas

tiempo_all = data["Tiempo Km. 10 (Minutos)"]
tiempo_mine = mine["Tiempo Km. 10 (Minutos)"]

# ### Cuánto tiempo tardé en completar la carrera?

f"{tiempo_mine.item():.2f} Minutos"

# ### De media, cuánto tardaron los corredores en completar la carrera ?

f"{tiempo_all.mean():.2f} Minutos"

# ### En qué percetil está mi tiempo ?

f"{stats.percentileofscore(tiempo_all, tiempo_mine.item()):.2f}%"

# ### Cuánto tardó el corredor mediano ?

f"{tiempo_all.median():.2f} Minutos"

# ### Cuánto tardó el corredor que tardó menos que el 80% ?

f"{tiempo_all.quantile(0.2):.2f} Minutos"


# # Ritmo
#

mine[RITMOS].iloc[0]

data[RITMOS].mean()

data[RITMOS].std()

# # Plot

plot_grid(data)


mine[TIEMPOS].iloc[0]
categ_mine = mine["Edad"].item()
data.query("Edad == @categ_mine")
data.groupby("Edad").mean()[RITMOS].sort_values(RITMOS[-1])
data.groupby("Edad").std()[RITMOS]
data.groupby("Edad").count()[RITMOS]
data.groupby("Sexo").mean()[RITMOS].sort_values(RITMOS[-1])
data.groupby("Sexo").count()[RITMOS]
data.groupby(["Sexo", "Edad"]).mean()[TIEMPOS].sort_values(TIEMPOS[-1]).sort_index()
df = data[RITMOS + ["Sexo", "Edad"]].melt(["Sexo", "Edad"])

sns.violinplot(data=df, y="value", hue='Sexo', x="variable", kind='violin', split=True)
plt.tight_layout()


# ## Andando
#
# Cúantas personas realizaron la carrera andando ?
#
# > Ver https://www.healthline.com/health/exercise-fitness/average-walking-speed

len(data[data["Ritmo Min/Km. 10"] > 11.6])


# Cuántas personas no terminaron la carrera?

data["Ritmo Min/Km. 10"].isnull().sum()

# # Categorías
#
# Se establecen las siguientes categorías:
# - Absoluta Popular masculino y femenino *
# - Júnior masculino y femenino
# Nacidos en los años 2002, 2003, 2004 y 2005 (16, 17, 18 y 19 años cumplidos).
# - Promesas masculinas y femeninas
# Nacidos en los años 1999, 2000 y 2001 (20, 21 y 22 años cumplidos).
# - Senior masculino y femenino
# Nacidos entre el año 1987 y 1998.
#
# ## Veteranos masculino y femenino
#
# - M-35 de 35 a 44 años cumplidos (nacidos entre 1977 y 1986).
# - M-45 de 45 a 54 años cumplidos (nacidos entre 1967 y 1976).
# - M-55 de 55 a 64 (nacidos entre el 1957 y 1966).
# - M-65 de 65 en adelante (nacidos en 1956 y anteriores)
# Handbike y sillas de atletismo masculino y femenino
# (*) Esta categoría serán entregados los trofeos el día de la prueba en el
# Estadio de Vallecas al concluir la Carrera Nationale-Nederlanden San
# Silvestre Vallecana Internacional. Se habilitará una salida especial para las
# categorías handbike y sillas de atletismo antes de la salida oficial de las
# 16:20. Se ruega a los participantes de estas categorías hagan uso de esta
# salida con el fin de poder correr mejor al encontrarse el recorrido
# totalmente libre.
# > fuente: https://www.sansilvestrevallecana.com/descargas/ReglamentoPopular.pdf

# ### Cómo evolucionó la carrera (en media) por categorías?

df = data.groupby("Categ.").mean()[TIEMPOS].rank().sort_values(TIEMPOS[-1], ascending=True).T
kw = dict(linewidth=4, markersize=8, marker="o", legend=False, figsize=(12,8))
ax = df.plot(**kw)
t_kw = dict(horizontalalignment='left', verticalalignment='center', fontsize=20)
plt.text(3.1, 0, "Categoría", **t_kw, fontweight="bold")
for c in df.columns:
    plt.text(3.1, df.loc[TIEMPOS[-1], c], c, **t_kw)
ax.invert_yaxis()
ax.set_yticks(range(1, 15))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.ylabel("Posición", fontsize=20)
plt.xticks(range(4), labels=["Km 2,5", "Km 5", "Km 7,5", "Km 10"], rotation=25, fontsize=20)
plt.yticks(fontsize=20)
plt.suptitle("Posiciones por etapas de cada categoría", fontsize=30)
plt.set_cmap("tab20")
plt.tight_layout()
plt.show()



# Los que mas escalaron posiciones

df = data[TIEMPOS].rank().query("`Tiempo Km. 2,5 (Minutos)` - `Tiempo Km. 10 (Minutos)` > 9000")
data.loc[df.index][RITMOS]
df = data.groupby("Categ.", group_keys=False).apply(lambda x: x.head(5))
df = df.set_index("Nombre")[TIEMPOS]
df.loc["Yo"] = mine[TIEMPOS].iloc[0]
df = df.rank().T
# kw = dict(linewidth=4, markersize=8, marker="o", legend=False, figsize=(12,8))
# ax = df.plot(**kw)
# t_kw = dict(horizontalalignment='left', verticalalignment='center', fontsize=20)
# plt.text(3.1, 0, "Categoría", **t_kw, fontweight="bold")
# for c in df.columns:
#     plt.text(3.1, df.loc[TIEMPOS[-1], c], c, **t_kw)
# ax.invert_yaxis()
# ax.set_yticks(range(1, df.shape[1]))
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)
# ax.set_ylabel("Posición", fontsize=20)
# plt.suptitle("Posiciones por etapas de cada categoría", fontsize=30)
# plt.set_cmap("tab20")
# plt.tight_layout()
# plt.show()

import seaborn as sns
df = data.groupby("Categ.").mean()[RITMOS]
sns.heatmap(df, annot=True)
# data.groupby("Categ.").mean()[RITMOS]
