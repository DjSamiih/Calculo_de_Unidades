import builtins as bi
from math import gcd

def is_prime(p: int) -> bool:
    if p < 2: return False
    if p % 2 == 0: return p == 2
    d = 3
    while d * d <= p:
        if p % d == 0: return False
        d += 2
    return True

def prime_factors(n: int):
    f = []
    x = n
    d = 2
    while d * d <= x:
        if x % d == 0:
            f.append(d)
            while x % d == 0: x //= d
        d = 3 if d == 2 else d + 2
    if x > 1: f.append(x)
    return f

def is_primitive_root(a: int, p: int) -> bool:
    if p == 2: return a % p == 1
    if gcd(a, p) != 1: return False
    phi, x, d = p - 1, p - 1, 2
    factors = {}
    while d * d <= x:
        while x % d == 0:
            factors[d] = factors.get(d, 0) + 1
            x //= d
        d += 1 if d == 2 else 2
    if x > 1: factors[x] = factors.get(x, 0) + 1
    for q in factors:
        if pow(a, phi // q, p) == 1: return False
    return True

def modinv(a: int, p: int) -> int:
    return bi.pow(a, -1, p)

def hat_g_counts_n_eq_p(p: int) -> dict[int, int]:
    return {e: 1 for e in range(p)}

def multiply_exponents_modp(expsA: list[int], expsB: list[int], p: int) -> dict[int, int]:
    acc: dict[int, int] = {}
    for a in expsA:
        for b in expsB:
            e = (a + b) % p
            acc[e] = acc.get(e, 0) + 1
    return acc

def add_dicts(a: dict[int, int], b: dict[int, int]) -> dict[int, int]:
    out = a.copy()
    for k, v in b.items():
        out[k] = out.get(k, 0) + v
        if out[k] == 0: del out[k]
    return out

def format_element(exp_to_coef: dict[int, int]) -> str:
    if not exp_to_coef: return "0"
    parts = []
    for e in sorted(exp_to_coef):
        c = exp_to_coef[e]
        mon = "1" if e == 0 else f"g^{e}"
        if c == 1: parts.append(mon)
        elif c == -1: parts.append(f"-{mon}")
        else: parts.append(f"{c}*{mon}")
    s = parts[0]
    for term in parts[1:]:
        if term.startswith("-"): s += " - " + term[1:]
        else: s += " + " + term
    return s

def format_parens_no_caret(exps: list[int]) -> str:
    parts = ["1"] + [f"g{e}" for e in exps[1:]]
    return "(" + " + ".join(parts) + ")"

def box(title: str):
    line = "═" * 38
    print(f"\n╔{line}╗"); print(f"║ {title}"); print(f"╚{line}╝")

def compute_units_n_eq_p(p: int, t: int):
    if not is_prime(p): raise ValueError("p deve ser um número primo.")
    if not (1 <= t <= max(1, p - 1)): raise ValueError("t deve estar em 1..p-1.")
    if not is_primitive_root(t, p): raise ValueError("t deve ser raiz primitiva módulo p.")
    n = p
    r = modinv(t, p)
    tr1 = t * r - 1
    if tr1 % p != 0: raise ValueError("t*r - 1 não é múltiplo de p.")
    k = tr1 // p

    exps_S1 = [0] + [(j * t) % p for j in range(1, r)]
    counts_hat = hat_g_counts_n_eq_p(p)
    minus_k = {e: -k * c for e, c in counts_hat.items() if c}

    i_min, i_max = 1, (p - 3) // 2
    s2_map: dict[int, list[int]] = {}
    for i in range(i_min, i_max + 1):
        base = bi.pow(t, i, p)
        exps_S2 = [0] + [(j * base) % p for j in range(1, t)]
        s2_map[i] = exps_S2

    factorized = []
    s1_str = format_parens_no_caret(exps_S1)
    for i in range(i_min, i_max + 1):
        s2_str = format_parens_no_caret(s2_map[i])
        factorized.append((i, f"u{i} = {s1_str}{s2_str} − {k}ˆg"))

    units = []
    for i in range(i_min, i_max + 1):
        prod_counts = multiply_exponents_modp(exps_S1, s2_map[i], p)
        ui = add_dicts(prod_counts, minus_k)
        units.append((i, ui))

    return {"p": p, "t": t, "n": n, "r": r, "k": k,
            "S1_exps": exps_S1, "S2_exps": s2_map,
            "factorized": factorized, "units": units}

def print_parameters(res: dict):
    box("PARÂMETROS")
    print(f"  • p (primo): {res['p']}")
    print(f"  • t (raiz primitiva mod p): {res['t']}")
    print(f"  • n (ordem do grupo): {res['n']}")
    print(f"  • r: {res['r']}")
    print(f"  • k: {res['k']}")

def print_factorized(res: dict):
    box("TABELA I")
    print(f"Parâmetros: p={res['p']}, t={res['t']}, n={res['n']}, r={res['r']}, k={res['k']}\n")
    for i, line in res["factorized"]:
        print(" ", line)

def print_final_table(res: dict):
    box("TABELA II")
    print(f"Parâmetros: p={res['p']}, t={res['t']}, n={res['n']}, r={res['r']}, k={res['k']}\n")
    for i, ui in res["units"]:
        print(f"  u_{i} = {format_element(ui)}")

def ask_int(prompt, minimum=None, maximum=None, default=None):
    while True:
        s = input(f"{prompt}" + (f" [{default}]" if default is not None else "") + ": ").strip()
        if s == "" and default is not None: return default
        try:
            v = int(s)
            if minimum is not None and v < minimum:
                print(f"mínimo {minimum}"); continue
            if maximum is not None and v > maximum:
                print(f"máximo {maximum}"); continue
            return v
        except Exception:
            print("  • digite um inteiro válido.")

def ask_prime_interactive() -> int:
    while True:
        p = ask_int("Defina p (número primo)", minimum=2)
        if is_prime(p): return p
        print("  • p deve ser primo. Tente novamente.")

def ask_primitive_root_interactive(p: int) -> int:
    while True:
        t = ask_int(f"Defina t (raiz primitiva módulo {p})", minimum=1, maximum=max(1, p - 1))
        if is_primitive_root(t, p): return t
        print(f"  • {t} NÃO é raiz primitiva módulo {p}. Tente novamente.")

def main():
    while True:
        print("\n=== Unidades u_i ===")
        p = ask_prime_interactive()
        t = ask_primitive_root_interactive(p)
        try:
            res = compute_units_n_eq_p(p, t)
        except Exception as exc:
            print(f"\nErro: {exc}")
            retry = input("Tentar novamente desde o início? [S/n]: ").strip().lower()
            if retry not in ("", "s", "sim", "y", "yes"):
                break
            else:
                continue
        print_parameters(res)
        print_factorized(res)
        print_final_table(res)
        again = input("\nDeseja executar novamente? [s/N]: ").strip().lower()
        if again not in ("", "s", "sim", "y", "yes"):
            print("Encerrando."); break

if __name__ == "__main__":
    main()
