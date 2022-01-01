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

```python
tiempo_all = data["Tiempo Minutos"]
tiempo_mine = mine["Tiempo Minutos"]
```

Cuánto tiempo tardé en completar la carrera? 

```python
tiempo_mine.item()
```

De media, cuánto tardaron los corredores en completar la carrera ? 

```python
float(tiempo_all.mean())
```

En qué percetil está mi tiempo ?

```python
stats.percentileofscore(tiempo_all, tiempo_mine.item())
```

Cuánto tardó el corredor mediano ?

```python
tiempo_all.median()
```

Cuánto tardó el corredor que tardó menos que el 80% ? 

```python
tiempo_all.quantile(0.2)
```


## Pace 

```python
ritmos = ["Km. 2,5 Minutos", "Km. 5 Minutos", "Km. 7,5 Minutos", "Ritmo Km. Minutos"]
```

```python
data[ritmos].describe()
```

```python
mine[ritmos]
```

# Plot

```python
plot_hist("Tiempo Minutos", data, mine)
```

```python
plot_hist("Ritmo Km. Minutos", data, mine)
```

```python
plot_hist("Km. 2,5 Minutos", data, mine)
```

```python
plot_hist("Km. 5 Minutos", data, mine)
```

```python
plot_hist("Km. 7,5 Minutos", data, mine)
```



Cual fue la evolución de los corredores por cada etapa? 

```python
delta1 = data["Km. 5 Minutos"] - data["Km. 2,5 Minutos"]
delta2 = data["Km. 7,5 Minutos"] - data["Km. 5 Minutos"]
delta1.hist()
delta2.hist()
plt.show()
```
