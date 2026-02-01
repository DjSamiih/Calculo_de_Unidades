# Cálculo de Unidades
## Descrição do programa

Este repositório contém códigos escritos em *Python* com o objetivo de apoiar cálculos relacionados a **unidades em anéis de grupo integrais**.

Em particular, o arquivo `units.py` implementa o cálculo de unidades da forma:

```math
u_i=\left(\sum_{j=0}^{r-1} g^{tj}\right)\left(\sum_{j=0}^{t-1} g^{j t^i}\right)-k\hat{g}
=
(1+g^t+\cdots+g^{t(r-1)})(1+g^{t^{i}}+\cdots+g^{t^{i(t-1)}})-k\hat{g}.
```

Para executar os cálculos, o usuário fornece apenas:
- o primo _p_;
- uma raiz primitiva _t_ módulo _p_.

As informações de:
- _r_, o menor inteiro positivo tal que
```math
  tr\equiv 1\mod p;
```
- _k_, o inteiro
```math
(rt - 1)/p;
```

são calculadas automaticamente pelo próprio programa.

Ao final, o programa retorna:
- os valores de _p_, _t_, _r_ e _k_ utilizados;
- uma tabela com o resultado parcial das unidades ou seja, a expressão definida sem calcular;
- uma segunda tabela com o resultado final das unidades.

Em complemento, o arquivo `multiply.py` implementa operações auxiliares de **multiplicação** e **potenciação** de elementos (unidades) no anel de grupo, com redução de expoentes módulo _p_.

Na **multiplicação**, dados dois elementos _h_1_ e _h_2_, o programa calcula
```math
h_1\cdot h_2
```

considerando a redução dos expoentes módulo _p_ durante a operação. Para executar o cálculo, o usuário fornece:
- o primo _p_;
- a expressão de _h_1_;
- a expressão de _h_2_.

Na **potenciação**, dado um elemento _h_ e um expoente inteiro 
```math
m \ge 0
```
o programa calcula

```math
h^m
```
<br>

por multiplicações sucessivas (também com redução de expoentes módulo _p_). Para executar o cálculo, o usuário fornece:
- o primo _p_;
- a expressão de _h_;
- o expoente _m_.

Ao final, o programa retorna o resultado final e, se solicitado, as etapas intermediárias do processo.

---

## Execução e testes

Este software foi inicialmente testado utilizando **compiladores online de Python**. Atualmente, **não existe um CLI empacotado**. A execução é feita diretamente a partir dos scripts Python.

### Requisitos
- Python 3.x

### Executar localmente

Clone o repositório (ou baixe os arquivos) e execute o script desejado:

#### `units.py` — Cálculo das unidades \(u_i\)

```bash
python units.py
```

O script solicitará:
- um primo _p_;
- uma raiz primitiva _t_ módulo _p_.

E exibirá:
- parâmetros _p_, _t_, _n_, _r_, _k_;
- **Tabela I** (forma fatorada / resultado parcial);
- **Tabela II** (resultado final).

#### `multiply.py` — Multiplicação e potenciação de unidades

```bash
python multiply.py
```

O script apresenta um menu com as opções:

- **1) Multiplicação**  
  O usuário fornece:
  - o primo _p_;
  - duas expressões _h_1_ e _h_2_ (unidades) a serem multiplicadas.

  O programa calcula
  ```math
  h_1\cdot h_2
  ```
  com **redução de expoentes módulo _p_** e pode exibir o **passo a passo**.

- **2) Potenciação**  
  O usuário fornece:
  - o primo _p_;
  - uma expressão _h_;
  - um expoente inteiro
  ```math
  m \ge 0.
  ```

  O programa calcula
  ```math
  h^m
  ```
  por multiplicações sucessivas, com **redução de expoentes módulo _p_**, e também pode exibir o **passo a passo**.

### Executar em compiladores online

1. Abra um ambiente online de execução de Python.
2. Cole o conteúdo do arquivo `units.py` ou `multiply.py`.
3. Execute.
4. Forneça as entradas solicitadas no console do ambiente.

---

## Formato das expressões (no `multiply.py`)

As expressões são inseridas como combinações lineares de potências de _g_, por exemplo:

- `g^2 - g^3 + g^4`
- `1 + 2*g - g^4`
- `-3 + g - 5*g^7`

---

## Observação acadêmica

Este software foi desenvolvido como **ferramenta auxiliar** para experimentação e verificação computacional em contexto acadêmico.
