"""Dowload data from Marca API."""
import pandas as pd
from tqdm import tqdm
from time import sleep

error = False
page = -1
max_page = 1092
out = []

for page in tqdm(range(max_page+1)):
    url = f"https://www.marca.com/Servicios/SanSilvestre/Controlador?ano=2021&pagina={page}"
    out += pd.read_html(url)
    sleep(0.01)

data = pd.concat(out)
data.to_pickle("./2021/asset/data.pkl")
