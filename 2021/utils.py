import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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
    min, sec = x.replace("/km", "").replace('"', "").split("'")
    out = pd.Timedelta(minutes=int(min), seconds=int(sec)).total_seconds() / 60
    return out


def get_mine(data):
    return data.query("Nombre=='Maximiliano Greco'")


def plot_hist(
    x,
    data,
    title="San Silvestre",
    xlabel="Minutos",
    ylabel="%",
    decorate=True,
):
    """Plot histogram.

    Parameters
    ----------
    x : str
    """
    fig = plt.figure(figsize=(15, 8))

    data[x].hist(figure=fig, bins=20, density=True)

    if decorate:
        mine = get_mine(data)
        plt.axvline(data[x].mean(), color="red", linewidth=3, label="Media")
        plt.axvline(
            data[x].median(),
            color="red",
            linestyle="--",
            linewidth=3,
            label="Mediana",
        )
        plt.axvline(
            mine[x].item(), color="black", linewidth=3, label="Mi tiempo"
        )

    plt.title(title, fontsize=40)
    plt.legend(fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)

    plt.tight_layout()
    plt.show()


def plot_pace(data):

    from utils import load_data

    data = load_data()
    x = ["Km. 2,5 (Minutos)", "Km. 5 (Minutos)", "Km. 7,5 (Minutos)"]
    df = data[x].melt()
    pal = sns.cubehelix_palette(3, rot=-0.25, light=0.7)
    g = sns.FacetGrid(
        df, row="variable", hue="variable", aspect=8, height=1.5, palette=pal
    )

    g.map(
        sns.kdeplot,
        "value",
        bw_adjust=0.5,
        clip_on=False,
        fill=True,
        alpha=1,
        linewidth=1.5,
    )
    g.map(sns.kdeplot, "value", clip_on=False, color="w", lw=2, bw_adjust=0.5)

    g.refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False)

    def label(x, color, label):
        ax = plt.gca()
        ax.text(
            1,
            0.2,
            label,
            fontweight="bold",
            color=color,
            ha="right",
            va="center",
            transform=ax.transAxes,
        )

    g.map(label, "value")

    g.figure.subplots_adjust(hspace=-0.25)
    g.set_titles("")
    g.set(yticks=[], ylabel="")
    g.despine(bottom=True, left=True)
    plt.tight_layout()
    plt.show()


def load_data():

    data = pd.read_pickle("./asset/data.pkl")
    data = data.reset_index(drop=True)

    data["Tiempo Km. 2,5 (Minutos)"] = data["Km. 2,5"].apply(delta2min)
    data["Tiempo Km. 5 (Minutos)"] = data["Km. 5"].apply(delta2min)
    data["Tiempo Km. 7,5 (Minutos)"] = data["Km. 7,5"].apply(delta2min)
    data["Tiempo Km. 10 (Minutos)"] = data["Tiempo"].apply(delta2min)

    data["Ritmo Km. (Minutos)"] = data["Ritmo Km."].apply(ritmo2minutes)

    data["Ritmo Min/Km. 2,5"] = data["Tiempo Km. 2,5 (Minutos)"] / 2.5
    data["Ritmo Min/Km. 5"] = data["Tiempo Km. 5 (Minutos)"] / 5
    data["Ritmo Min/Km. 7,5"] = data["Tiempo Km. 7,5 (Minutos)"] / 7.5
    data["Ritmo Min/Km. 10"] = data["Tiempo Km. 10 (Minutos)"] / 10

    return data
