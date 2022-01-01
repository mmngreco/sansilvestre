---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.5
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# San Silvestre 2021

```python
import pandas as pd
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
from utils import load_data, plot_hist
```

```python
pd.options.display.float_format = '{:,.2f}'.format
np.set_printoptions(precision=2)
%precision %.2f

```

```python

data = load_data()
data.head()
```



```python
mine = data.query("Nombre=='Maximiliano Greco'")
mine
```

# Estadísticas


Cuánto tiempo tardé en completar la carrera? 

```python
mine.TiempoMinutos.item()
```

De media, cuánto tardaron los corredores en completar la carrera ? 

```python
float(data.TiempoMinutos.mean())
```

En qué percetil está mi tiempo ?

```python
stats.percentileofscore(data.TiempoMinutos, mine.TiempoMinutos.item())
```

Cuánto tardó el corredor mediano ?

```python
data.TiempoMinutos.median()
```

Cuánto tardó el corredor que tardó menos que el 80% ? 

```python
data.TiempoMinutos.quantile(0.2)
```


```python
ritmos = ["Km. 2,5 Minutos", "Km. 5 Minutos", "Km. 7,5 Minutos", "Ritmo Km. Minutos"]
data[ritmos].describe()
mine[ritmos]
```

# Plot

```python
plot_hist("TiempoMinutos", data, mine)
plot_hist("Ritmo Km. Minutos", data, mine)
plot_hist("Km. 2,5 Minutos", data, mine)
plot_hist("Km. 5 Minutos", data, mine)
plot_hist("Km. 7,5 Minutos", data, mine)
```

