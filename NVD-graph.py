import requests
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from datetime import datetime

# Realizar petición GET a la URL y obtener el JSON de respuesta
url = "https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=macOS+Ventura"
response = requests.get(url)
json_data = response.json()

# Crear lista de valores para el eje x y el eje y del gráfico
x_values = []
y_values = []
cve_ids = []
for vulnerability in json_data["vulnerabilities"]:
    if "metrics" in vulnerability["cve"]:
        cvss_data = vulnerability["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]
        if "baseScore" in cvss_data and "published" in vulnerability["cve"]:
            base_score = cvss_data["baseScore"]
            published_date = datetime.strptime(vulnerability["cve"]["published"], "%Y-%m-%dT%H:%M:%S.%f")
            x_values.append(published_date)
            y_values.append(base_score)
            cve_ids.append(vulnerability["cve"]["id"])

# Crear mapa de colores que vaya desde verde hasta rojo
colors = LinearSegmentedColormap.from_list("Green to Red", ["green", "red"])

# Crear gráfico con cambio cromático de verde a rojo en función del valor del eje y
plt.scatter(x_values, y_values, c=y_values, cmap=colors)

# Añadir información sobre el cve id de cada punto
for i in range(len(x_values)):
    plt.annotate(cve_ids[i], (x_values[i], y_values[i]), textcoords="offset points", xytext=(0, 10), ha='center')

plt.xlabel("Published Date")
plt.ylabel("Base Score")
plt.title("Vulnerabilities")
plt.show()

