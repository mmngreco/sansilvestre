"""Dowload dataset from Marca API."""
from concurrent import futures

import pandas as pd
from pathlib import Path
from tqdm import tqdm


URL = "https://www.marca.com/Servicios/SanSilvestre/Controlador"


def get_df(page: int) -> pd.DataFrame:
    """Download and convert to dataframe.

    Parameters
    ----------
    page : int
        Page number to download.

    Returns
    -------
    out : pandas.DataFrame
    """
    url = f"{URL}?ano=2021&pagina={page}"
    out = pd.read_html(url)
    return out[0]


def download() -> pd.DataFrame:
    """Download the dataset from URL.

    Download all pages from URL and merge it in a DataFrame.

    Returns
    -------
    out : pandas.DataFrame
    """
    max_page = 1092  # HACK: Previoulsy checked manually.
    df_pages = []

    with futures.ThreadPoolExecutor() as executor:
        pages = range(max_page + 1)
        res = executor.map(get_df, pages)

        for df in tqdm(res, total=max_page):
            df_pages.append(df)


    data = pd.concat(df_pages, axis=0)
    return data


def save(filename:str = "data.pkl") -> None:
    """Save data to a pickle in './asset/filename'.
    Parameters
    ----------
    filename : str, optional
    """
    file = Path(__file__).parent / "asset" / filename
    data = download()
    data.to_pickle(file)


if __name__ == "__main__":
    save()
