"""Simulación de interbloqueo (deadlock): Filósofos Comensales con SimPy.
Compara tres políticas: ingenua, jerarquía de recursos y camarero (N-1)."""
import random, statistics, sys
import simpy

# ---------- Parámetros por defecto ----------
N_FILOSOFOS = 5
T_PENSAR = 2.0      # tiempo medio pensando (exponencial)
T_COMER = 3.0       # tiempo medio comiendo (exponencial)
T_PAUSA = 1.0       # tiempo medio entre tomar el 1er y el 2do tenedor
T_SIM = 500.0       # duración de cada réplica
REPLICAS = 200
SEMILLA = 42
POLITICAS = ["ingenua", "jerarquia", "camarero"]


def replica(politica, n, t_pensar, t_comer, t_pausa, t_sim, semilla):
    rng = random.Random(semilla)
    env = simpy.Environment()
    tenedores = [simpy.Resource(env, capacity=1) for _ in range(n)]
    camarero = simpy.Resource(env, capacity=n - 1)
    comidas = [0] * n
    esperas = []

    def filosofo(i):
        izq, der = i, (i + 1) % n
        primero, segundo = (izq, der)
        if politica == "jerarquia":
            primero, segundo = min(izq, der), max(izq, der)
        while True:
            yield env.timeout(rng.expovariate(1 / t_pensar))   # PENSAR
            hambre = env.now
            if politica == "camarero":
                asiento = camarero.request()
                yield asiento
            r1 = tenedores[primero].request()
            yield r1
            yield env.timeout(rng.expovariate(1 / t_pausa))    # pausa (clave del deadlock)
            r2 = tenedores[segundo].request()
            yield r2
            esperas.append(env.now - hambre)
            yield env.timeout(rng.expovariate(1 / t_comer))    # COMER
            comidas[i] += 1
            tenedores[primero].release(r1)
            tenedores[segundo].release(r2)
            if politica == "camarero":
                camarero.release(asiento)

    for i in range(n):
        env.process(filosofo(i))

    t_deadlock = None
    while env.peek() < t_sim:
        env.step()
    if env.peek() == float("inf"):          # no quedan eventos: todos bloqueados
        t_deadlock = env.now
    return {"deadlock": t_deadlock is not None, "t_deadlock": t_deadlock,
            "comidas": sum(comidas), "min_comidas": min(comidas),
            "espera": statistics.mean(esperas) if esperas else 0.0}


def experimento(politica, n=N_FILOSOFOS, t_pensar=T_PENSAR, t_comer=T_COMER,
                t_pausa=T_PAUSA, t_sim=T_SIM, replicas=REPLICAS, semilla=SEMILLA):
    rs = [replica(politica, n, t_pensar, t_comer, t_pausa, t_sim, semilla + k)
          for k in range(replicas)]
    dl = [r for r in rs if r["deadlock"]]
    p = len(dl) / replicas
    return {"politica": politica, "n": n, "p_deadlock": p * 100,
            "ic95": 1.96 * (p * (1 - p) / replicas) ** 0.5 * 100,
            "t_deadlock": statistics.mean(r["t_deadlock"] for r in dl) if dl else None,
            "rendimiento": statistics.mean(r["comidas"] for r in rs) / t_sim,
            "espera": statistics.mean(r["espera"] for r in rs),
            "min_comidas": statistics.mean(r["min_comidas"] for r in rs)}


if __name__ == "__main__":
    print(f"N={N_FILOSOFOS} | pensar={T_PENSAR} | comer={T_COMER} | pausa={T_PAUSA} | "
          f"T={T_SIM} | réplicas={REPLICAS}\n")
    for pol in POLITICAS:
        r = experimento(pol)
        td = f"{r['t_deadlock']:.1f}" if r["t_deadlock"] else "-"
        print(f"{pol:10s} deadlock={r['p_deadlock']:5.1f}% (±{r['ic95']:.1f}) "
              f"t_deadlock={td:>6s} comidas/unid.t={r['rendimiento']:.3f} "
              f"espera={r['espera']:.2f}")
