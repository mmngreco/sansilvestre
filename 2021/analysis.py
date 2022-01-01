import pandas as pd
import scipy.stats as stats

pd.options.display.float_format = '{:,.2f}'.format
%precision %.2f

data = pd.read_pickle("./asset/data.pkl")
data["TiempoMinutos"] = data.Tiempo.apply(lambda x: pd.Timedelta(x).total_seconds() / 60)

data.head()
mine = data.query("Nombre=='Maximiliano Greco'")
mine

# Tiempo en minutos
mine.TiempoMinutos.item()

# Percentil
stats.percentileofscore(data.Minutos, mine.TiempoMinutos.item())

# Tiempos
data.TiempoMinutos.mean()
data.TiempoMinutos.median()
data.TiempoMinutos.quantile(0.2)


import matplotlib.pyplot as plt
data.TiempoMinutos.hist(bins=20, density=True)
plt.axvline(mis_minutos, color="green", linewidth=3, label="Mi tiempo")
plt.axvline(data.TiempoMinutos.mean(), color="red", linewidth=3, label="Media")
plt.axvline(data.TiempoMinutos.median(), color="red", linestyle="--", linewidth=3, label="Media")
plt.tight_layout()
plt.show()
