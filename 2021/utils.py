import pandas as pd
import matplotlib.pyplot as plt


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


def plot_hist(x, data, mine):
    """Plot histogram.

    Parameters
    ----------
    x : str
    """
    fig = plt.figure(figsize=(20, 10))

    data[x].hist(figure=fig, bins=20, density=True)
    plt.axvline(mine[x].item(), color="green", linewidth=3, label="Mi tiempo")
    plt.axvline(data[x].mean(), color="red", linewidth=3, label="Media")
    plt.axvline(data[x].median(), color="red", linestyle="--", linewidth=3, label="Media")

    plt.title("San Silvestre: Distribución de tiempo", fontsize=40)
    plt.legend(fontsize=18)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlabel("Minutos", fontsize=20)
    plt.ylabel("%", fontsize=20)

    plt.tight_layout()
    plt.show()


def load_data():

    data = pd.read_pickle("./asset/data.pkl")
    data["TiempoMinutos"] = data.Tiempo.apply(delta2min)
    data["Km. 2,5 Minutos"] = data["Km. 2,5"].apply(delta2min)
    data["Km. 5 Minutos"] = data["Km. 5"].apply(delta2min)
    data["Km. 7,5 Minutos"] = data["Km. 7,5"].apply(delta2min)
    data["Ritmo Km. Minutos"] = data["Ritmo Km."].apply(ritmo2minutes)

    return data
