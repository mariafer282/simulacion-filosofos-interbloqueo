import json
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                Image, PageBreak, Preformatted, KeepTogether)

R = json.load(open("resultados.json"))
URL_REPO = "https://github.com/mariafer282/simulacion-filosofos-interbloqueo"
URL_WEB = "https://mariafer282.github.io/simulacion-filosofos-interbloqueo/"
AZUL, ROJO, GRIS = colors.HexColor("#2f6f8f"), colors.HexColor("#b5423a"), colors.HexColor("#f1eee6")

ss = getSampleStyleSheet()
B = ParagraphStyle("B", parent=ss["Normal"], fontName="Helvetica", fontSize=10.5, leading=16, alignment=TA_JUSTIFY, spaceAfter=8)
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=15, textColor=AZUL, spaceBefore=16, spaceAfter=8, keepWithNext=1)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=11.5, textColor=colors.black, spaceBefore=10, spaceAfter=5, keepWithNext=1)
CAP = ParagraphStyle("CAP", parent=B, fontSize=9, leading=12, alignment=TA_CENTER, textColor=colors.HexColor("#555555"))
CEN = ParagraphStyle("CEN", parent=B, alignment=TA_CENTER, spaceAfter=4)
BUL = ParagraphStyle("BUL", parent=B, leftIndent=14, bulletIndent=2, spaceAfter=4)
CODE = ParagraphStyle("CODE", fontName="Courier", fontSize=8, leading=10.5, backColor=GRIS, borderPadding=6, spaceAfter=10)
CELL = ParagraphStyle("CELL", parent=B, fontSize=9, leading=12, alignment=0, spaceAfter=0)
CELLH = ParagraphStyle("CELLH", parent=CELL, fontName="Helvetica-Bold", textColor=colors.white)

def P(t, s=B): return Paragraph(t, s)
def bullets(items): return [Paragraph(i, BUL, bulletText="•") for i in items]
def tabla(datos, anchos, rojo_col=None):
    filas = [[Paragraph(str(c), CELLH) for c in datos[0]]] + [[Paragraph(str(c), CELL) for c in f] for f in datos[1:]]
    t = Table(filas, colWidths=anchos, repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), AZUL), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, GRIS]), ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6), ("LINEBELOW", (0, 0), (-1, -1), 0.3, colors.HexColor("#cccccc"))]))
    return t
def caja(texto):
    t = Table([[Paragraph(texto, CELL)]], colWidths=[16 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), GRIS), ("LINEBEFORE", (0, 0), (0, -1), 3, AZUL),
        ("LEFTPADDING", (0, 0), (-1, -1), 12), ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9)]))
    return t
def f1(x): return f"{x:.1f}"

def pie(c, d):
    c.saveState(); c.setFont("Helvetica", 8); c.setFillColor(colors.grey)
    c.drawCentredString(A4[0] / 2, 1.2 * cm, f"Simulación de Filósofos Comensales  |  página {d.page}"); c.restoreState()

S = []
# ---------------- Portada ----------------
S += [Spacer(1, 1.2 * cm), P("<b>UNIVERSIDAD NACIONAL MAYOR DE SAN MARCOS</b>", CEN),
      P("Facultad de Ingeniería de Sistemas e Informática", CEN), Spacer(1, 2.2 * cm),
      P("<font size=24 color='#2f6f8f'><b>Simulación de Procesos</b></font>", CEN), Spacer(1, 6),
      P("<font size=15>Interbloqueo (deadlock) en el problema de los Filósofos Comensales:<br/>comparación de políticas de asignación de recursos</font>", CEN),
      Spacer(1, 2 * cm)]
S.append(tabla([["Datos del trabajo", ""], ["Asignatura", "Modelos y Simulación"], ["Docente", "Rivas Peña, Marcos Hernan"],
    ["Alumna", "María Fernanda Flores Capcha"], ["Código", "[COMPLETAR CÓDIGO DE MATRÍCULA]"],
    ["Fecha", "19 de noviembre de 2026"], ["Lugar", "Lima, Perú"]], [4 * cm, 12 * cm]))
S += [Spacer(1, 1 * cm), P("<b>Recursos del proyecto</b>", CEN),
      P(f"Simulador web: <link href='{URL_WEB}' color='#2f6f8f'>{URL_WEB}</link>", CEN),
      P(f"Repositorio: <link href='{URL_REPO}' color='#2f6f8f'>{URL_REPO}</link>", CEN), PageBreak()]

# ---------------- 1 Resumen ----------------
S.append(P("1. Resumen", H1))
S.append(P("Este trabajo simula el problema clásico de los <b>filósofos comensales</b>, un modelo de Sistemas Operativos que muestra cómo varios procesos que compiten por recursos compartidos pueden quedar bloqueados para siempre (interbloqueo o <i>deadlock</i>). Se construyó un modelo de eventos discretos, estocástico y dinámico, implementado en Python con SimPy y en un simulador web interactivo, que compara tres políticas: <b>ingenua</b>, <b>jerarquía de recursos</b> y <b>camarero (N-1)</b>."))
b = R["base"]
S.append(P(f"Con 5 filósofos y 300 réplicas por política, la política ingenua terminó en deadlock en <b>{f1(b[0]['p_deadlock'])}%</b> de las réplicas, mientras que las otras dos políticas no presentaron ningún bloqueo. La jerarquía de recursos fue además la de mayor rendimiento ({b[1]['rendimiento']:.3f} comidas por unidad de tiempo, frente a {b[2]['rendimiento']:.3f} del camarero)."))
S.append(caja("<b>En palabras simples:</b> cinco filósofos comparten cinco tenedores y cada uno necesita dos para comer. Si todos agarran a la vez el tenedor de su izquierda, todos esperan el de su derecha y nadie suelta nada: el sistema se congela. La simulación mide qué tan seguido ocurre eso y qué reglas lo evitan."))

# ---------------- 2 Objetivos ----------------
S.append(P("2. Objetivos", H1))
S.append(P("<b>Objetivo general.</b> Evaluar mediante simulación de eventos discretos cómo la política de adquisición de tenedores afecta la probabilidad de deadlock y el rendimiento de un sistema de procesos concurrentes."))
S.append(P("<b>Objetivos específicos.</b>"))
S += bullets(["Modelar filósofos y tenedores como procesos y recursos con exclusión mutua.",
  "Estimar la probabilidad de deadlock con intervalos de confianza al 95% mediante réplicas independientes.",
  "Comparar las políticas ingenua, jerarquía y camarero en deadlock, rendimiento, espera y equidad.",
  "Analizar la sensibilidad del deadlock al tiempo de pausa entre tenedores y al número de filósofos.",
  "Verificar el modelo comparando dos implementaciones independientes (SimPy y JavaScript)."])

# ---------------- 3 Descripción ----------------
S.append(P("3. Descripción del proceso", H1))
S.append(P("Hay N filósofos sentados en una mesa redonda y N tenedores, uno entre cada par de filósofos. Cada filósofo repite el ciclo: <b>pensar, tomar el primer tenedor, pausar, tomar el segundo tenedor, comer y soltar ambos</b>. Un tenedor solo puede usarlo un filósofo a la vez, y los que no consiguen su tenedor esperan en una cola FIFO."))
S.append(Image("fig_modelo.png", 6.2 * cm, 6.2 * cm))
S.append(P("Figura 1. Mesa con 5 filósofos (F0-F4) y 5 tenedores (T0-T4). El filósofo i usa los tenedores Ti y T(i+1) mod N.", CAP))
S.append(P("3.1 Condiciones de Coffman", H2))
S.append(P("Un deadlock ocurre únicamente si se cumplen a la vez cuatro condiciones (Coffman et al., 1971). En esta mesa las cuatro aparecen cuando todos sostienen un tenedor:"))
S.append(tabla([["Condición", "Cómo aparece en la mesa"],
  ["Exclusión mutua", "Un tenedor lo usa un solo filósofo."],
  ["Retención y espera", "Quien tiene un tenedor espera el segundo sin soltar el primero."],
  ["Sin apropiación", "Nadie puede quitarle un tenedor a otro."],
  ["Espera circular", "F0 espera a F1, F1 a F2, ... y F4 espera a F0."]], [4.5 * cm, 11.5 * cm]))
S.append(Spacer(1, 8))
S.append(P("3.2 Políticas comparadas", H2))
S.append(tabla([["Política", "Regla", "Qué condición rompe"],
  ["Ingenua", "Toma primero el tenedor izquierdo y luego el derecho.", "Ninguna: puede haber deadlock."],
  ["Jerarquía (Dijkstra)", "Los tenedores se numeran y siempre se toma primero el de menor número.", "Espera circular."],
  ["Camarero", "Un camarero deja sentarse (a tomar tenedores) como máximo a N-1 filósofos.", "Espera circular: siempre queda un tenedor útil."]],
  [3.6 * cm, 7.4 * cm, 5 * cm]))

# ---------------- 4 Parámetros ----------------
S.append(P("4. Parámetros de entrada", H1))
S.append(tabla([["Parámetro", "Valor inicial", "Rango", "Descripción"],
  ["N (filósofos)", "5", "2 a 30", "Número de filósofos y de tenedores."],
  ["Tiempo medio pensando", "2", "> 0", "Media de la exponencial del tiempo de pensar."],
  ["Tiempo medio comiendo", "3", "> 0", "Media de la exponencial del tiempo de comer."],
  ["Pausa entre tenedores", "1", "> 0", "Media del tiempo entre tomar el 1.º y el 2.º tenedor."],
  ["Duración de la réplica", "500", "mín. 10", "Tiempo simulado de cada corrida."],
  ["Réplicas", "300", "1 a 2000", "Corridas independientes por escenario."],
  ["Semilla base", "42", "entero", "La réplica k usa la semilla 42 + k (reproducible)."]], [4.2 * cm, 2.6 * cm, 2.2 * cm, 7 * cm]))
S.append(Spacer(1, 6))
S.append(P("La <b>pausa entre tenedores</b> es el parámetro clave del modelo: si agarrar el segundo tenedor fuera instantáneo, los filósofos nunca se bloquearían entre sí en la simulación. La pausa representa el tiempo real que hay entre dos solicitudes de recurso y abre la ventana donde aparece el deadlock."))

# ---------------- 5 Modelo ----------------
S.append(P("5. Modelo de simulación", H1))
S.append(P("Es un modelo <b>discreto</b> (el estado cambia en instantes de evento), <b>estocástico</b> (los tiempos son aleatorios) y <b>dinámico</b> (evoluciona en el tiempo). Como en la guía de la asignatura, el reloj salta de un evento al siguiente y los recursos se modelan con <font name='Courier'>simpy.Resource</font> de capacidad 1."))
S += bullets(["<b>Tiempos:</b> pensar, pausar y comer siguen distribuciones exponenciales con las medias indicadas.",
  "<b>Detección de deadlock:</b> si la lista de eventos se vacía antes del tiempo final, ningún proceso puede continuar; ese instante es el tiempo de deadlock.",
  "<b>Réplicas:</b> cada escenario se repite con semillas distintas; la probabilidad de deadlock se estima como proporción, con IC95 = 1,96 · raíz(p(1-p)/n)."])
S.append(P("5.1 Indicadores", H2))
S.append(tabla([["Indicador", "Definición"],
  ["Deadlock (%)", "Porcentaje de réplicas que terminan bloqueadas."],
  ["Tiempo medio al deadlock", "Instante promedio del bloqueo, solo en las réplicas bloqueadas."],
  ["Rendimiento", "Comidas totales por unidad de tiempo simulado (si hay bloqueo, cuenta cero desde ese momento)."],
  ["Espera media", "Tiempo desde que un filósofo tiene hambre hasta que empieza a comer."],
  ["Mínimo de comidas", "Comidas del filósofo menos atendido: mide equidad e inanición."]], [4.5 * cm, 11.5 * cm]))

# ---------------- 6 Implementación ----------------
S.append(P("6. Implementación", H1))
S.append(P("Se desarrollaron dos implementaciones independientes de la misma lógica: <font name='Courier'>simulacion_filosofos.py</font> (SimPy, siguiendo la guía de la asignatura) y <font name='Courier'>index.html</font>, un simulador web en JavaScript sin dependencias que permite cambiar parámetros, comparar las tres políticas y ver el estado final de la mesa. Fragmento central del proceso de cada filósofo:"))
S.append(Preformatted("""def filosofo(i):
    izq, der = i, (i + 1) % n
    primero, segundo = (izq, der)
    if politica == "jerarquia":
        primero, segundo = min(izq, der), max(izq, der)
    while True:
        yield env.timeout(rng.expovariate(1 / t_pensar))   # PENSAR
        if politica == "camarero":
            asiento = camarero.request(); yield asiento
        r1 = tenedores[primero].request(); yield r1
        yield env.timeout(rng.expovariate(1 / t_pausa))    # pausa
        r2 = tenedores[segundo].request(); yield r2
        yield env.timeout(rng.expovariate(1 / t_comer))    # COMER
        tenedores[primero].release(r1); tenedores[segundo].release(r2)
        if politica == "camarero": camarero.release(asiento)""", CODE))

# ---------------- 7 V&V ----------------
S.append(P("7. Verificación y validación", H1))
S.append(P("Para verificar que no hay errores de programación se ejecutó el mismo escenario base (N = 5, 300 réplicas) en las dos implementaciones. Como usan generadores de números aleatorios distintos, no se esperan cifras idénticas, sino resultados estadísticamente compatibles."))
S.append(tabla([["Política", "Deadlock % SimPy", "Deadlock % Web", "Rendim. SimPy", "Rendim. Web"],
  ["Ingenua", f1(b[0]["p_deadlock"]) + " (±" + f1(b[0]["ic95"]) + ")", "60.7", f"{b[0]['rendimiento']:.3f}", "0.218"],
  ["Jerarquía", "0.0", "0.0", f"{b[1]['rendimiento']:.3f}", "0.447"],
  ["Camarero", "0.0", "0.0", f"{b[2]['rendimiento']:.3f}", "0.359"]], [3 * cm, 3.6 * cm, 3.2 * cm, 3.2 * cm, 3 * cm]))
S.append(Spacer(1, 6))
S.append(P("Las diferencias están dentro del intervalo de confianza, por lo que ambas implementaciones representan el mismo modelo. Además se comprobó la coherencia con la teoría: con jerarquía y camarero el deadlock es imposible (0 en todas las réplicas), y con la política ingenua el bloqueo siempre ocurre con todos los filósofos reteniendo un tenedor."))

# ---------------- 8 Resultados ----------------
S.append(P("8. Experimentos y resultados", H1))
S.append(P("8.1 Comparación de políticas (N = 5)", H2))
filas = [["Política", "Deadlock (%)", "IC95", "t medio al deadlock", "Comidas / t", "Espera media", "Mín. comidas"]]
for r in b:
    filas.append([r["politica"].capitalize(), f1(r["p_deadlock"]), f1(r["ic95"]),
                  f1(r["t_deadlock"]) if r["t_deadlock"] else "-", f"{r['rendimiento']:.3f}", f"{r['espera']:.2f}", f1(r["min_comidas"])])
S.append(tabla(filas, [2.6 * cm, 2.3 * cm, 1.7 * cm, 2.8 * cm, 2.3 * cm, 2.3 * cm, 2 * cm]))
S.append(Spacer(1, 8))
S.append(Image("fig_politicas.png", 15 * cm, 6 * cm))
S.append(P("Figura 2. Probabilidad de deadlock (con IC95) y rendimiento por política.", CAP))
S.append(P("8.2 Sensibilidad a la pausa y al número de filósofos", H2))
S.append(Image("fig_sensibilidad.png", 15 * cm, 6 * cm))
S.append(P("Figura 3. Deadlock de la política ingenua al variar la pausa entre tenedores (izquierda) y N (derecha).", CAP))
fp = [["Pausa media", "Deadlock (%)", "N", "Deadlock (%)"]]
for (x, r1), (y, r2) in zip(R["pausa"][:4], R["n"]):
    fp.append([x, f1(r1["p_deadlock"]) + " (±" + f1(r1["ic95"]) + ")", y, f1(r2["p_deadlock"]) + " (±" + f1(r2["ic95"]) + ")"])
S.append(tabla(fp, [3.5 * cm, 4.5 * cm, 3.5 * cm, 4.5 * cm]))
S.append(Spacer(1, 6))
S.append(P("8.3 Políticas con muchos filósofos (N = 12)", H2))
S.append(tabla([["Política", "Deadlock (%)", "Comidas / t", "Espera media"]] +
  [[p.capitalize(), f1(r["p_deadlock"]), f"{r['rendimiento']:.3f}", f"{r['espera']:.2f}"] for p, r in R["n_pol"]],
  [4 * cm, 4 * cm, 4 * cm, 4 * cm]))

# ---------------- 9 Análisis ----------------
S.append(P("9. Análisis de resultados", H1))
S += bullets([
 f"<b>El deadlock es probabilístico, no seguro.</b> Con la política ingenua y N = 5 ocurrió en {f1(b[0]['p_deadlock'])}% de las réplicas, en promedio cerca de t = {b[0]['t_deadlock']:.0f}. Una prueba corta puede no mostrarlo, lo que explica por qué estos errores aparecen en producción y no en pruebas.",
 "<b>La pausa lo vuelve casi inevitable.</b> Con pausa 0,1 no hubo bloqueos en 300 réplicas; con pausa 2 ocurrió en 99%. Cuanto más tiempo se retiene el primer tenedor, más probable es que todos lo retengan a la vez.",
 "<b>Menos filósofos, más riesgo.</b> Con N = 3 el bloqueo fue seguro, y con N = 12 casi desapareció, porque es muy poco probable que los 12 estén a la vez en la misma situación. Esto no significa que la política ingenua sea segura: solo que el riesgo es menor.",
 f"<b>Jerarquía es la mejor política en este modelo.</b> No bloquea y tiene mayor rendimiento ({b[1]['rendimiento']:.3f}) y menor espera ({b[1]['espera']:.2f}), porque permite más filósofos comiendo a la vez.",
 f"<b>El camarero evita el deadlock pero con costo.</b> Limitar a N-1 sentados reduce el paralelismo: rendimiento de {b[2]['rendimiento']:.3f} y espera de {b[2]['espera']:.2f}.",
 "<b>El deadlock destruye el rendimiento.</b> La política ingenua rinde la mitad que jerarquía porque, tras bloquearse, la réplica no produce más comidas."])

# ---------------- 10 Conclusiones ----------------
S.append(P("10. Conclusiones", H1))
S += bullets(["La simulación de eventos discretos permitió estimar con intervalos de confianza un fenómeno raro y difícil de reproducir manualmente: el deadlock.",
  "Evitar el deadlock no requiere más hardware, sino una regla de adquisición de recursos: ordenar los recursos (jerarquía) o limitar la concurrencia (camarero).",
  "La jerarquía de recursos ofreció la mejor combinación de seguridad y rendimiento en todos los escenarios probados.",
  "Ajustar los parámetros (pausa y N) permite al usuario explorar por qué un sistema funciona con pocas pruebas y falla bajo otras condiciones."])
S.append(P("11. Limitaciones y trabajo futuro", H1))
S += bullets(["Los tiempos son exponenciales; en sistemas reales pueden tener otras distribuciones.",
  "Todos los filósofos tienen los mismos parámetros y no hay prioridades ni cancelaciones.",
  "No se modeló la detección y recuperación de deadlock (por ejemplo, abortar un proceso), ni el Algoritmo del Banquero. Son extensiones naturales."])

# ---------------- 12 Referencias ----------------
S.append(P("12. Referencias y recursos", H1))
S += bullets([
 "Dijkstra, E. W. (1971). Hierarchical ordering of sequential processes. <i>Acta Informatica</i>, 1(2), 115-138.",
 "Coffman, E. G., Elphick, M. J., y Shoshani, A. (1971). System deadlocks. <i>ACM Computing Surveys</i>, 3(2), 67-78.",
 "Silberschatz, A., Galvin, P. B., y Gagne, G. <i>Operating System Concepts</i>. Wiley.",
 "Tanenbaum, A. S., y Bos, H. <i>Modern Operating Systems</i>. Pearson.",
 "Documentación de SimPy: https://simpy.readthedocs.io",
 "Guía técnica «Simulación de Procesos y Casos Prácticos en Python» (material de la asignatura).",
 f"Código y simulador: {URL_REPO}"])

SimpleDocTemplate("Informe_Simulacion_Filosofos_Comensales.pdf", pagesize=A4, leftMargin=2.5 * cm, rightMargin=2.5 * cm,
    topMargin=2.3 * cm, bottomMargin=2.3 * cm, title="Simulación de Filósofos Comensales",
    author="María Fernanda Flores Capcha").build(S, onFirstPage=lambda c, d: None, onLaterPages=pie)
