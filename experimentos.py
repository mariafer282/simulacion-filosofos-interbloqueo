"""Genera los resultados y gráficos del informe."""
import json, math
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from simulacion_filosofos import experimento, POLITICAS

res = {"base": [experimento(p, replicas=300) for p in POLITICAS]}
res["pausa"] = [(x, experimento("ingenua", t_pausa=x, replicas=300)) for x in (0.1, 0.5, 1, 2, 4)]
res["n"] = [(x, experimento("ingenua", n=x, replicas=300)) for x in (3, 5, 8, 12)]
res["n_pol"] = [(p, experimento(p, n=12, replicas=300)) for p in POLITICAS]
json.dump(res, open("resultados.json", "w"), indent=1)

C = {"ingenua": "#b5423a", "jerarquia": "#2f6f8f", "camarero": "#4f8a4b"}
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})

# Fig 2: políticas
fig, ax = plt.subplots(1, 2, figsize=(8, 3.2))
nom = [r["politica"].capitalize() for r in res["base"]]
cols = [C[r["politica"]] for r in res["base"]]
ax[0].bar(nom, [r["p_deadlock"] for r in res["base"]], color=cols,
          yerr=[r["ic95"] for r in res["base"]], capsize=4)
ax[0].set_ylabel("Réplicas con deadlock (%)"); ax[0].set_title("Probabilidad de deadlock")
ax[1].bar(nom, [r["rendimiento"] for r in res["base"]], color=cols)
ax[1].set_ylabel("Comidas por unidad de tiempo"); ax[1].set_title("Rendimiento")
plt.tight_layout(); plt.savefig("fig_politicas.png", dpi=200); plt.close()

# Fig 3: sensibilidad a la pausa y a N
fig, ax = plt.subplots(1, 2, figsize=(8, 3.2))
xs = [x for x, _ in res["pausa"]]
ax[0].errorbar(xs, [r["p_deadlock"] for _, r in res["pausa"]],
               yerr=[r["ic95"] for _, r in res["pausa"]], marker="o", color=C["ingenua"], capsize=3)
ax[0].set_xlabel("Pausa media entre tenedores"); ax[0].set_ylabel("Deadlock (%)")
ax[0].set_title("Política ingenua, N = 5")
xs = [x for x, _ in res["n"]]
ax[1].errorbar(xs, [r["p_deadlock"] for _, r in res["n"]],
               yerr=[r["ic95"] for _, r in res["n"]], marker="o", color=C["ingenua"], capsize=3)
ax[1].set_xlabel("Número de filósofos (N)"); ax[1].set_ylabel("Deadlock (%)")
ax[1].set_title("Política ingenua, pausa = 1")
plt.tight_layout(); plt.savefig("fig_sensibilidad.png", dpi=200); plt.close()

# Fig 1: modelo conceptual
fig, ax = plt.subplots(figsize=(3.6, 3.6)); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(plt.Circle((0, 0), 0.55, color="#e8e2d6"))
for i in range(5):
    a = math.pi / 2 - 2 * math.pi * i / 5
    x, y = 1.25 * math.cos(a), 1.25 * math.sin(a)
    ax.add_patch(plt.Circle((x, y), 0.26, color="#2f6f8f"))
    ax.text(x, y, f"F{i}", color="white", ha="center", va="center", fontweight="bold")
    b = a - math.pi / 5
    tx, ty = 0.85 * math.cos(b), 0.85 * math.sin(b)
    ax.plot([tx * 0.8, tx * 1.12], [ty * 0.8, ty * 1.12], color="#b5423a", lw=3)
    ax.text(1.0 * math.cos(b) * 1.18, 1.0 * math.sin(b) * 1.18, f"T{i}", color="#b5423a",
            ha="center", va="center", fontsize=8)
ax.set_xlim(-1.8, 1.8); ax.set_ylim(-1.8, 1.8)
plt.savefig("fig_modelo.png", dpi=200, bbox_inches="tight"); plt.close()

for r in res["base"]: print(r)
print(res["pausa"]); print(res["n"]); print(res["n_pol"])
