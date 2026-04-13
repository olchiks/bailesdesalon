# 🕺💃 Percepción social de los bailes deportivos de salón: ¿deporte, arte o ambos?

Este repositorio contiene el código y los resultados de un estudio sobre cómo diferentes grupos de personas perciben los bailes deportivos de salón (también conocidos como bailes de competición o *Dance Sport*). El trabajo combina un análisis teórico con una encuesta online (N = 207) y diversos análisis estadísticos.

## 🎯 Objetivo principal

Investigar qué factores (experiencia personal, nivel de conocimiento, fuentes de información, etc.) influyen en que una persona considere los bailes de salón como **deporte**, como **arte** o como una **síntesis de ambos**.

## 📊 Principales resultados

- **89,9%** de los encuestados está de acuerdo en que los bailes de salón son un deporte.
- **84,1%** está de acuerdo en que son una forma de arte.
- **60,9%** elige la opción “en igual medida deporte y arte”.
- La **experiencia personal** se asocia débilmente con la percepción deportiva (ρ = 0,15; p = 0,037), pero **no** influye en la percepción artística.
- El **nivel de conocimiento** sobre bailes de salón se relaciona positivamente con verlos como deporte (ρ = 0,22; p < 0,01).
- La **participación en competiciones** es el factor más fuerte (χ² = 106,8; p < 0,001): el 74% de los competidores los considera totalmente deporte.
- Las **fuentes pasivas de información** (TV, redes sociales, etc.) **no** muestran relación significativa con la percepción.
- Existe una **correlación positiva moderada** entre percibirlos como deporte y como arte (ρ = 0,30; p < 0,001), lo que confirma su naturaleza sintética.

## 📁 Estructura del repositorio
  ├── bailes.R # Código en R: limpieza de datos, correlaciones, tablas y gráficos  
  ├── mapa.py # Código en Python para generar un mapa interactivo de las ciudades de los encuestados  
  ├── mapa_final.html # Mapa interactivo (se puede abrir en el navegador)  
  ├── para_imprimir_las_respuestas.ipynb # Jupyter Notebook para formatear y exportar respuestas individuales a PDF  
  └── README.md # Este archivo  

## 🔒 Nota sobre la privacidad de los datos

**Los datos brutos de la encuesta no se incluyen en este repositorio** porque contienen información personal que podría identificar a los participantes. Solo se han subido los scripts de análisis y los resultados agregados. Si deseas reproducir el análisis, puedes crear un archivo CSV anónimo con la misma estructura de columnas utilizada en `bailes.R`.

## 🛠️ Requisitos técnicos

- **R** (versión ≥ 4.0) con paquetes: `dplyr`, `ggplot2`, `corrplot`, `knitr`.
- **Python** (versión ≥ 3.8) con: `folium`, `pandas`, `math` (para el mapa).
- El notebook `para_imprimir_las_respuestas.ipynb` necesita `pandas`, `weasyprint` o `openpyxl`.


## 📚 Publicación académica

Este trabajo forma parte de un proyecto de investigación de nivel escolar (9º curso, San Petersburgo, Rusia). Los resultados completos y la discusión teórica están disponibles en el informe en ruso (no incluido aquí).


## 📄 Licencia

El código se distribuye bajo licencia MIT. Los datos personales no están disponibles por razones de privacidad.
