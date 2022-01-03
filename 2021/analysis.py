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
from utils import load_data, plot_hist, get_mine, plot_pace
import matplotlib as mpl

mpl.use('TkAgg')
mpl.get_backend()

pd.options.display.float_format = '{:,.2f}'.format
np.set_printoptions(precision=2)
# %precision %.2f


# +

data = load_data()
data.head()

#
data.shape
# -
#
#

mine = get_mine(data)
mine

# # Estadísticas

tiempo_all = data["Tiempo Km. 10 (Minutos)"]
tiempo_mine = mine["Tiempo Km. 10 (Minutos)"]

# Cuánto tiempo tardé en completar la carrera?

f"{tiempo_mine.item():.2f} Minutos"

# De media, cuánto tardaron los corredores en completar la carrera ?

f"{tiempo_all.mean():.2f} Minutos"

# En qué percetil está mi tiempo ?

f"{stats.percentileofscore(tiempo_all, tiempo_mine.item()):.2f}%"

# Cuánto tardó el corredor mediano ?

f"{tiempo_all.median():.2f} Minutos"

# Cuánto tardó el corredor que tardó menos que el 80% ?

f"{tiempo_all.quantile(0.2):.2f} Minutos"


# ## Ritmo

ritmos = ["Ritmo Min/Km. 2,5", "Ritmo Min/Km. 5", "Ritmo Min/Km. 7,5", "Ritmo Min/Km. 10"]
mine[ritmos]
data[ritmos].mean()
data[ritmos].std()


# ### Categorías
tiempos = ["Km. 2,5 (Minutos)", "Km. 5 (Minutos)", "Km. 7,5 (Minutos)", "Tiempo (Minutos)"]
mine[ritmos].iloc[0]
categ_mine = mine["Categ."].item()
data.query(" `Categ.` == @categ_mine ")
data.groupby("Categ.").mean()[ritmos].sort_values(ritmos[-1])
data.groupby("Categ.").std()[ritmos]

# Andando

len(data[data["Ritmo Min/Km. 10"] > 13])



# # Plot

# plt.ion()
# plot_hist(
#     "Tiempo (Minutos)",
#     data,
#     title="Distribución del Tiempo en minutos",
#     xlabel="Minutos",
#     ylabel="%",
# )
# plot_hist(
#     "Ritmo Km. (Minutos)",
#     data,
#     title="Distribución del Ritmo ",
#     xlabel="Min/Km",
# )
# plot_hist("Km. 2,5 (Minutos)", data, title="")
# plot_hist("Km. 5 (Minutos)", data, title="")
# plot_hist("Km. 7,5 (Minutos)", data, title="")

#

# Cual fue la evolución de los corredores por cada etapa?

# delta1 = data["Km. 5 (Minutos)"] - data["Km. 2,5 (Minutos)"]
# delta2 = data["Km. 7,5 (Minutos)"] - data["Km. 5 (Minutos)"]
# delta3 = data["Tiempo (Minutos)"] - data["Km. 7,5 (Minutos)"]
#
# delta1.div(2.5).hist(bins=20, alpha=0.5)
# delta2.div(2.5).hist(bins=20, alpha=0.5)
# delta3.div(2.5).hist(bins=20, alpha=0.5)
#
# plt.show()
#
#
# plot_pace(data)

