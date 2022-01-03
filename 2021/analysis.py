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
from utils import load_data, plot_hist, get_mine, plot_grid, TIEMPOS, RITMOS
import matplotlib as mpl

mpl.use('Qt5Cairo');

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
#

mine[RITMOS].iloc[0]

#
data[RITMOS].mean()

#
data[RITMOS].std()

# # Plot

plt.ion()
kw = {'xlabel': 'Minutos / Kilómetro', 'ylabel': 'Porcentaje (%)'}

#

plot_hist(RITMOS[0], data, title=RITMOS[0], **kw)

#

plot_hist(RITMOS[1], data, title=RITMOS[1], **kw)

#

plot_hist(RITMOS[2], data, title=RITMOS[2], **kw)

#

plot_hist(RITMOS[3], data, title=RITMOS[3], **kw)

#

plot_grid(data)


mine[TIEMPOS].iloc[0]
categ_mine = mine["Categ."].item()
data.query(" `Categ.` == @categ_mine ")
data.groupby("Categ.").mean()[RITMOS].sort_values(RITMOS[-1])
data.groupby("Categ.").std()[RITMOS]

# Andando

len(data[data["Ritmo Min/Km. 10"] > 13])

