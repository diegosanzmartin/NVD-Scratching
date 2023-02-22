import requests
import pandas as pd

# Hacer una solicitud HTTP GET para obtener el JSON de la URL
url = "https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=macOS+Ventura"
response = requests.get(url)

# Obtener el contenido JSON de la respuesta
json_content = response.json()

# Crear un marco de datos a partir del contenido JSON
vulnerabilities = json_content["vulnerabilities"]
data = []
for v in vulnerabilities:
    cve = v["cve"]
    cvss_metric = cve["metrics"]["cvssMetricV31"][0]["cvssData"]
    data.append({
        "CVE": cve["id"],
        "CWE": cve["weaknesses"][0]["description"][0]["value"], 
        "sourceIdentifier": cve["sourceIdentifier"],
        "published": cve["published"],
        "attackVector": cvss_metric["attackVector"],
        "baseScore": cvss_metric["baseScore"] 
    })
df = pd.DataFrame(data)

# Ordenar el marco de datos por la columna baseScore de mayor a menor
df_sorted = df.sort_values("baseScore", ascending=False)

# Imprimir el marco de datos ordenado
print(df_sorted)
#print(df_sorted.head(n=150).to_string(index=False))
