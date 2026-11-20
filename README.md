# Simulación de Filósofos Comensales (Deadlock)

Simulación de eventos discretos del problema de los filósofos comensales.
Compara tres políticas: **ingenua**, **jerarquía de recursos** y **camarero (N-1)**.

Curso: Modelos y Simulación — UNMSM, FISI.

## Contenido

| Archivo | Qué es |
|---|---|
| `index.html` | Simulador web interactivo (sin dependencias) |
| `simulacion_filosofos.py` | Simulación en Python con SimPy |
| `experimentos.py` | Genera `resultados.json` y los gráficos del informe |
| `Informe_Simulacion_Filosofos_Comensales.pdf` | Informe del trabajo |

## Cómo usarlo

**Simulador web:** abre `index.html` en el navegador (o la página de GitHub Pages).

**Python:**

```bash
pip install -r requirements.txt
python simulacion_filosofos.py
```
