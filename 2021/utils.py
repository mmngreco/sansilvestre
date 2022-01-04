import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

RITMOS = [
    "Ritmo Min/Km. 2,5",
    "Ritmo Min/Km. 5",
    "Ritmo Min/Km. 7,5",
    "Ritmo Min/Km. 10",
]
TIEMPOS = [
    "Tiempo Km. 2,5 (Minutos)",
    "Tiempo Km. 5 (Minutos)",
    "Tiempo Km. 7,5 (Minutos)",
    "Tiempo Km. 10 (Minutos)",
]


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
    fig = plt.figure(figsize=(8, 4))

    data[x].hist(figure=fig, bins=20, density=True, grid=False)

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

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.suptitle(title, fontsize=30)
    plt.legend(fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)

    plt.tight_layout()
    plt.show()


def plot_grid(data, cols=RITMOS):

    data = load_data()
    cols = RITMOS
    df = data[cols].melt()
    outlier = df.value.mean() + df.value.std() * 3
    df = df.query("value < @outlier")
    pal = sns.cubehelix_palette(len(cols), rot=-0.25, light=0.7)
    g = sns.FacetGrid(
        df, row="variable", hue="variable", aspect=5, height=1.5, palette=pal
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

    def mean(x, color, label):
        ax = plt.gca()
        ax.axvline(x.mean(), color="white", label="Average", linewidth=4)
        ax.axvline(x.mean(), color="black", label="Average")
        ax.axvline(
            get_mine(data)[label].item(),
            color="white",
            label="Me",
            linewidth=4,
        )
        ax.axvline(get_mine(data)[label].item(), color="green", label="Me")

    g.map(label, "value")
    g.map(mean, "value")
    get_mine(data)["Ritmo Min/Km. 10"].item()
    g.figure.subplots_adjust(hspace=-0.25)
    g.set_titles("")
    g.set(yticks=[], ylabel="")
    g.set_xlabels("Ritmo (Minutos / Kilómetro)")
    g.despine(bottom=True, left=True)
    plt.suptitle("Ritmo por Etapas", fontsize=30)
    plt.tight_layout()
    plt.show()


def load_data():

    data = pd.read_pickle("./asset/data.pkl")
    data = data.reset_index(drop=True)

    age = ['Júnior', 'Promesa', 'Sénior', '35', '45', '55', '65']
    age_type = pd.CategoricalDtype(categories=age, ordered=True)
    sex_type = pd.CategoricalDtype(categories=["F", "M"], ordered=False)
    data["Edad"] = (
        data["Categ."]
        .apply(
            lambda x: x.replace("-", "")
            .replace("M", "")
            .replace("F", "")
            .strip()
        )
        .astype(age_type)
    )
    data["Sexo"] = (
        data["Categ."]
        .apply(lambda x: "F" if "F" in x else "M")
        .astype(sex_type)
    )

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
