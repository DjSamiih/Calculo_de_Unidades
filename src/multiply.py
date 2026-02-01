import re

# -------------------- user input --------------------
def ask_integer(prompt, minimum=None, maximum=None, default=None):
    while True:
        s = input(prompt + (f" [{default}]" if default is not None else "") + ": ").strip()
        if s == "" and default is not None:
            return default
        try:
            v = int(s)
            if minimum is not None and v < minimum:
                print("mínimo", minimum); continue
            if maximum is not None and v > maximum:
                print("máximo", maximum); continue
            return v
        except Exception:
            print("  • digite um inteiro válido.")

def ask_yesno(prompt, default=False):
    yes = {"s", "sim", "y", "yes"}
    no  = {"n", "nao", "não", "no"}
    suf = " [S/n]" if default else " [s/N]"
    while True:
        s = input(prompt + suf + ": ").strip().lower()
        if s == "" : return default
        if s in yes: return True
        if s in no : return False
        print("  • responda com s/n.")

def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())

# -------------------- parsing & formatting --------------------
def parse_group_ring_element(text: str) -> dict[int, int]:
    s = normalize_spaces(text)
    s = s.replace("−", "-").replace("–", "-").replace("—", "-")
    s = s.replace(" ", "")
    s = s.replace("-", "+-")
    parts = s.split("+")
    exp_to_coef: dict[int, int] = {}
    for part in parts:
        if not part:
            continue
        if part == "1":
            c, e = 1, 0
        elif part == "-1":
            c, e = -1, 0
        else:
            m = re.fullmatch(r"([+-]?\d+)\*?g(?:\^(\d+))?$", part)
            if m:
                c = int(m.group(1))
                e = int(m.group(2)) if m.group(2) is not None else 1
            else:
                m2 = re.fullmatch(r"([+-]?)g(?:\^(\d+))?$", part)
                if m2:
                    c = -1 if m2.group(1) == "-" else 1
                    e = int(m2.group(2)) if m2.group(2) is not None else 1
                else:
                    m3 = re.fullmatch(r"([+-]?\d+)$", part)
                    if m3:
                        c = int(m3.group(1)); e = 0
                    else:
                        raise ValueError(f"termo inválido: {part}")
        exp_to_coef[e] = exp_to_coef.get(e, 0) + c
        if exp_to_coef[e] == 0:
            del exp_to_coef[e]
    return exp_to_coef

def _mono_base(exp: int) -> str:
    if exp == 0: return "1"
    if exp == 1: return "g"
    return f"g^{exp}"

def format_monomial(coef: int, exp: int) -> str:
    base = _mono_base(exp)
    if exp != 0 and coef == 1: return base
    if exp != 0 and coef == -1: return f"-{base}"
    if exp == 0: return f"{coef}"
    return f"{coef}*{base}"

def format_group_ring_element(exp_to_coef: dict[int, int]) -> str:
    if not exp_to_coef:
        return "0"
    parts = []
    for e in sorted(exp_to_coef):
        c = exp_to_coef[e]
        if c == 0: continue
        base = _mono_base(e)
        if e == 0:
            parts.append(str(c))
        else:
            if c == 1: parts.append(base)
            elif c == -1: parts.append(f"-{base}")
            else: parts.append(f"{c}*{base}")
    if not parts: return "0"
    s = parts[0]
    for term in parts[1:]:
        if term.startswith("-"): s += " - " + term[1:]
        else: s += " + " + term
    return s

def format_coef_times_exp(coef: int, exp: int) -> str:
    if exp == 0:
        return f"{coef}"
    base = _mono_base(exp)
    if coef == 1:  return base
    if coef == -1: return f"-{base}"
    return f"{coef}*{base}"

# -------------------- operations --------------------
def multiply_elements_mod_p(A: dict[int, int], B: dict[int, int], prime_p: int):
    contributions = []
    result_exp_to_coef: dict[int, int] = {}
    for exp_a, coef_a in A.items():
        if coef_a == 0: continue
        for exp_b, coef_b in B.items():
            if coef_b == 0: continue
            raw_exp = exp_a + exp_b
            reduced_exp = raw_exp % prime_p
            coef_prod = coef_a * coef_b
            contributions.append((coef_a, exp_a, coef_b, exp_b, raw_exp, reduced_exp, coef_prod))
            result_exp_to_coef[reduced_exp] = result_exp_to_coef.get(reduced_exp, 0) + coef_prod
            if result_exp_to_coef[reduced_exp] == 0:
                del result_exp_to_coef[reduced_exp]
    return contributions, result_exp_to_coef

# -------------------- UI helpers --------------------
def box_ascii(title: str, width=70):
    line = "-" * width
    print(f"\n+{line}+")
    print(f"| {title}")
    print(f"+{line}+")

def show_multiplication_inputs(prime_p, h1_text, h2_text, h1_dict, h2_dict):
    box_ascii("ENTRADAS — MULTIPLICAÇÃO")
    print(f"| p (primo): {prime_p}")
    print(f"| h1 (texto): {h1_text}")
    print(f"| h2 (texto): {h2_text}")
    print(f"| h1 (parse): {format_group_ring_element(h1_dict)}")
    print(f"| h2 (parse): {format_group_ring_element(h2_dict)}")

def show_step_by_step(contributions, prime_p, title="PASSO A PASSO DA MULTIPLICAÇÃO (mod p)"):
    box_ascii(title)
    for ca, ea, cb, eb, raw_e, red_e, cprod in contributions:
        left = format_monomial(ca, ea)
        right = format_monomial(cb, eb)
        raw_term = format_coef_times_exp(cprod, raw_e)
        red_term = format_coef_times_exp(cprod, red_e)
        print(f"| ({left}) x ({right})  =>  {raw_term}  ~=  {red_term}  (mod {prime_p})")

# -------------------- processes --------------------
def run_process_multiplication():
    box_ascii("MULTIPLICAÇÃO h1 · h2")
    prime_p = ask_integer("| Defina p (número primo)", minimum=2)
    h1_text = input("| Digite h1 (ex.: g^2 - g^3 + g^4): ").strip()
    h2_text = input("| Digite h2 (ex.: 1 + 2*g - g^4): ").strip()
    try:
        h1_dict = parse_group_ring_element(h1_text)
        h2_dict = parse_group_ring_element(h2_text)
    except Exception as ex:
        print(f"\n| Erro de parse: {ex}")
        return
    show_multiplication_inputs(prime_p, h1_text, h2_text, h1_dict, h2_dict)
    contributions, result_dict = multiply_elements_mod_p(h1_dict, h2_dict, prime_p)
    if ask_yesno("| Exibir passo a passo?", default=False):
        show_step_by_step(contributions, prime_p)
    box_ascii("RESULTADO FINAL")
    print("|", format_group_ring_element(result_dict))

def run_process_power():
    box_ascii("POTENCIAÇÃO h^m")
    prime_p = ask_integer("| Defina p (número primo)", minimum=2)
    base_text = input("| Digite h (ex.: g^2 - g^3 + g^4): ").strip()
    exponent_m = ask_integer("| Defina m (expoente inteiro >= 0)", minimum=0)
    show_steps = ask_yesno("| Exibir passo a passo?", default=False)
    try:
        base_dict = parse_group_ring_element(base_text)
    except Exception as ex:
        print(f"\n| Erro de parse: {ex}")
        return
    box_ascii("ENTRADAS — POTENCIAÇÃO")
    print(f"| p (primo): {prime_p}")
    print(f"| h (texto): {base_text}")
    print(f"| h (parse): {format_group_ring_element(base_dict)}")
    if exponent_m == 0:
        box_ascii("RESULTADO FINAL")
        print("| 1")
        return
    current_dict = {0: 1}
    for step in range(1, exponent_m + 1):
        contributions, tally = multiply_elements_mod_p(current_dict, base_dict, prime_p)
        if show_steps:
            show_step_by_step(contributions, prime_p, title=f"PASSO {step}: (resultado parcial) x h")
        current_dict = tally
    box_ascii(f"RESULTADO FINAL — h^{exponent_m}")
    print("|", format_group_ring_element(current_dict))

# -------------------- main --------------------
def main():
    while True:
        print("\n+--------------------------------------------------------------------+")
        print("|                   MULTIPLICAÇÃO/POTÊNCIA DE UNIDADES")
        print("+--------------------------------------------------------------------+")
        print("| 1) Multiplicação")
        print("| 2) Potenciação")
        print("| 0) Sair")
        print("+--------------------------------------------------------------------+")
        option = input("| Escolha uma opção: ").strip()
        if option == "1":
            run_process_multiplication()
            input("\n| Pressione Enter para voltar ao menu...")
        elif option == "2":
            run_process_power()
            input("\n| Pressione Enter para voltar ao menu...")
        elif option == "0":
            print("| Encerrando. Até mais!")
            break
        else:
            print("| Opção inválida.")

if __name__ == "__main__":
    main()
