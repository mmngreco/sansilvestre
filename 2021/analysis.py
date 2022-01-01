import pandas as pd
import scipy.stats as stats

pd.options.display.float_format = '{:,.2f}'.format
%precision %.2f

data = pd.read_pickle("./asset/data.pkl")


def delta2min(x):
    """Convert time duration into a minutes.

    Parameters
    ----------
    x : str

    Returns
    -------
    out : float
    """
    return pd.Timedelta(x).total_seconds() / 60

def ritmo2minutes(x):
    """Convert pace to minutes per kilometer.

    Parameter
    ---------
    x : str
        String input with a format like: 2'55"/km.

    Returns
    -------
    out : float
        Minutes per kilometer
    """
    min, sec = x.replace("/km", "").replace('"',"").split("'")
    out = pd.Timedelta(minutes=int(min), seconds=int(sec)).total_seconds() / 60
    return out


data["TiempoMinutos"] = data.Tiempo.apply(delta2min)
data["Km. 2,5 Minutos"] = data["Km. 2,5"].apply(delta2min)
data["Km. 5 Minutos"] = data["Km. 5"].apply(delta2min)
data["Km. 7,5 Minutos"] = data["Km. 7,5"].apply(delta2min)
data["Ritmo Km. Minutos"] = data["Ritmo Km."].apply(ritmo2minutes)

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


ritmos = ["Km. 2,5 Minutos", "Km. 5 Minutos", "Km. 7,5 Minutos", "Ritmo Km. Minutos"]
data[ritmos].describe()
mine[ritmos]


import matplotlib.pyplot as plt
plt.ion()

x = "TiempoMinutos"
def plot_hist(x):
    fig = plt.figure(figsize=(20, 10))
    data.loc[:, x].hist(figure=fig, bins=20, density=True)
    plt.axvline(mine.loc[:, x].item(), color="green", linewidth=3, label="Mi tiempo")
    plt.axvline(data.loc[:, x].mean(), color="red", linewidth=3, label="Media")
    plt.axvline(data.loc[:, x].median(), color="red", linestyle="--", linewidth=3, label="Media")
    plt.tight_layout()
    plt.show()

plot_hist("TiempoMinutos")

plot_hist("Ritmo Km. Minutos")
plot_hist("Km. 2,5 Minutos")
plot_hist("Km. 5 Minutos")
plot_hist("Km. 7,5 Minutos")
