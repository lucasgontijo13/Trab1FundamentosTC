

Trabalho de Fundamentos Teóricos da Computação AFD
---

## 📘 `main.py` — Menu Interativo para Manipulação de AFDs (.jff)

Este script Python fornece um menu interativo no terminal para importar, visualizar, manipular e salvar Autômatos Finitos Determinísticos (AFDs), com suporte a arquivos `.jff` do JFLAP.

### ✅ Funcionalidades principais

1. **Importar AFD** de arquivos `.jff`.
2. **Salvar AFD** modificado em novo arquivo `.jff`.
3. **Visualizar o AFD** no terminal.
4. **Copiar um AFD** existente.
5. **Minimizar o AFD** usando o algoritmo de Hopcroft.
6. **Verificar equivalência** entre dois AFDs.
7. **Identificar estados equivalentes** dentro de um AFD.
8. **Realizar operações entre AFDs**:

   * União
   * Interseção
   * Diferença
   * Complemento

### 📂 Requisitos

* Python 3.x
* Interface `AFD.py` com implementação das operações sobre AFDs
* Biblioteca `tkinter` (inclusa por padrão no Python)
* Arquivos de entrada no formato `.jff` (compatíveis com o JFLAP)

### ▶️ Como usar

Execute o script via terminal:

```bash
python main.py
```

Use as opções numéricas para navegar entre as operações. Os arquivos `.jff` podem ser escolhidos via janelas do sistema operacional.


---

```python
import xml.etree.ElementTree as ET
from collections import deque
from copy import deepcopy
from itertools import combinations
```

1. **Importação de módulos**

   * `xml.etree.ElementTree as ET`: permite ler e escrever arquivos XML (usado para JFLAP).
   * `deque` de `collections`: estrutura de fila dupla, usada na busca em largura (equivalência de AFDs).
   * `deepcopy` de `copy`: faz cópia completa (recursiva) de objetos, usada para duplicar AFDs sem vínculo ao original.
   * `combinations` de `itertools`: gera todas as combinações de tamanhos fixos de uma lista, usada para listar pares de estados equivalentes.

---

```python
class AFD:
```

Define a classe `AFD` (Autômato Finito Determinístico).

---

### Construtor e atributos iniciais

```python
    def __init__(self, Alfabeto):
        Alfabeto = str(Alfabeto)
        self.estados = set()
        self.alfabeto = Alfabeto
        self.transicoes = dict()
        self.incial = None
        self.finais = set()
```

1. `def __init__(self, Alfabeto):` — método chamado ao criar um AFD.
2. `Alfabeto = str(Alfabeto)` — garante que o alfabeto seja tratado como string (cada caractere é um símbolo).
3. `self.estados = set()` — conjunto de nomes de estados.
4. `self.alfabeto = Alfabeto` — string cujos caracteres são os símbolos do autômato.
5. `self.transicoes = dict()` — mapa de transições: chave `(estado_origem, símbolo)` → `estado_destino`.
6. `self.incial = None` — nome do estado inicial (a definir).
7. `self.finais = set()` — conjunto de estados finais.

---

### Método de inicialização de execução

```python
    def limpaAfd(self):
        self.__deuErro = False
        self.__estadoAtual = self.incial
```

* Zera a flag de erro (`__deuErro`) e posiciona o autômato no estado inicial (`__estadoAtual`).

---

### Criação de estados

```python
    def criaEstado(self, id, inicial=False, final=False):
        id = str(id)
        if id in self.estados:
            return False
        if inicial:
            self.incial = id
        if final:
            self.finais = self.finais.union({id})
        return True
```

1. Recebe um identificador `id` (converte pra string).
2. Se o `id` já existir, retorna `False`.
3. Se `inicial=True`, marca esse estado como inicial.
4. Se `final=True`, adiciona ao conjunto de finais.
5. Retorna `True` se criou com sucesso.

---

### Criação de transições

```python
    def criaTransicao(self, origem, destino, simbolo):
        origem = str(origem)
        destino = str(destino)
        simbolo = str(simbolo)

        if not origem in self.estados:
            return False
        if not destino in self.estados:
            return False
        if len(simbolo) != 1 or not simbolo in self.alfabeto:
            return False

        self.transicoes[(origem, simbolo)] = destino
        return True
```

Valida origem, destino (devem existir) e símbolo (um caractere do alfabeto). Se ok, registra a transição e retorna `True`.

---

### Mudança de estado inicial e final `(mudaEstadoInicial, mudaEstadoFinal)`

```python
    def mudaEstadoInicial(self, id):
        if not id in self.estados:
            return
        self.inicial = id

    def mudaEstadoFinal(self, id, final):
        if not id in self.estados:
            return
        if final:
            self.final = self.finais.union({id})
        else:
            self.final = self.finais.difference({id})
```

* `mudaEstadoInicial`: altera o estado inicial, se existir.
* `mudaEstadoFinal`: adiciona (`final=True`) ou remove (`final=False`) um estado dos finais.

---

### Execução de uma cadeia `(move, deuErro, estadoAtual, estadoFinal)`

```python
    def move(self, cadeia):
        for simbolo in cadeia:
            if not simbolo in self.alfabeto:
                self.__deuErro = True
                break
            if (self.__estadoAtual, simbolo) in self.transicoes:
                self.__estadoAtual = self.transicoes[(self.__estadoAtual, simbolo)]
            else:
                self.__deuErro = True
                break
        return self.__estadoAtual

    def deuErro(self):
        return self.__deuErro

    def estadoAtual(self):
        return self.__estadoAtual

    def estadoFinal(self, id):
        return id in self.finais
```

1. `move`: lê cada símbolo da string; se não existir transição ou símbolo inválido, marca erro. Retorna o estado em que parou.
2. `deuErro`: indica se houve erro na leitura.
3. `estadoAtual`: retorna o estado atual.
4. `estadoFinal`: verifica se um dado `id` é estado final.

---

### Representação do AFD em string

```python
    def __str__(self):
        s = 'AFD:\n'
        ...
        return s
```

Monta uma descrição em texto com estados, alfabeto, transições, inicial e finais, para imprimir com `print(afd)`.

---

### `carregar_afd_de_jflap` Buscar arquivo XML JFLAP para memória:

1. **Leitura e parsing do arquivo XML**

   ```python
   tree = ET.parse(caminho_arquivo)
   root = tree.getroot()
   automato = root.find('automaton')
   ```

   * `ET.parse(caminho_arquivo)`: carrega o arquivo JFLAP (XML) cujo caminho foi passado como parâmetro.
   * `getroot()`: obtém o elemento raiz do documento XML.
   * `find('automaton')`: dentro da raiz, localiza o nó `<automaton>`, que envolve a definição do autômato.

2. **Coleta de estados, inicial e finais**

   ```python
   estados = {}
   alfabeto = set()
   transicoes_temp = []
   inicial = None
   finais = set()
   for state in automato.findall('state'):
       id_xml = state.get('id')
       nome = state.get('name')
       estados[id_xml] = nome

       if state.find('initial') is not None:
           inicial = nome
       if state.find('final') is not None:
           finais.add(nome)
   ```

   * Cria-se um dicionário `estados` que mapeia o atributo `id` de cada `<state>` para um nome legível (`name`).
   * Variáveis auxiliares:

     * `alfabeto`: conjunto de símbolos usados nas transições (ainda vazio).
     * `transicoes_temp`: lista temporária onde guardaremos tuplas de transição.
     * `inicial`: nome do estado inicial (inicia como `None`).
     * `finais`: conjunto de nomes de estados finais (inicia vazio).
   * Para cada `<state>`:

     * Lê `id` e `name` e registra em `estados`.
     * Se houver um elemento `<initial>` dentro do `<state>`, marca esse `nome` como estado inicial.
     * Se houver um `<final>`, adiciona esse `nome` ao conjunto de finais.
Claro! Seguindo o estilo descritivo e numerado que você usou no README anterior, aqui está a **seção atualizada** para documentar a verificação de estado inicial e final ao carregar o AFD:

---


3. **Verifica se existe estado inicial e final**

   ```python
   if inicial is None:
       print("AFD sem estado inicial.")
       return None

   ```

   * **Estado inicial**: a função verifica se pelo menos um estado possui a tag `<initial>`. Se nenhum for encontrado, a função **cancela o carregamento** e exibe:

     ```
     AFD sem estado inicial.
     ```

---

4. **Leitura das transições**

   ```python
   for trans in automato.findall('transition'):
       origem_id = trans.find('from').text
       destino_id = trans.find('to').text
       simbolo = trans.find('read').text or ""

       origem = estados[origem_id]
       destino = estados[destino_id]
       alfabeto.add(simbolo)
       transicoes_temp.append((origem, simbolo, destino))
   ```

   * Para cada `<transition>`:

     1. Lê o ID do estado de origem e do estado de destino (`<from>` e `<to>`).
     2. Lê o símbolo em `<read>`; se for `None`, assume a cadeia vazia (`""`).
     3. Converte os IDs em nomes usando o dicionário `estados`.
     4. Adiciona o símbolo ao `alfabeto`.
     5. Armazena a transição como tupla `(origem, simbolo, destino)` em `transicoes_temp`.

5. **Construção do objeto AFD e adição de transições**

   ```python
   afd = AFD(alfabeto)
   for id_estado in estados.values():
       afd.estados.add(id_estado)
   afd.incial = inicial
   afd.finais = finais

   for origem, simbolo, destino in transicoes_temp:
       afd.criaTransicao(origem, destino, simbolo)

   return afd
   ```

   * Cria uma instância de `AFD`, inicializando-a com o alfabeto coletado.
   * Adiciona todos os nomes de estados ao conjunto `afd.estados`.
   * Define o estado inicial (`afd.incial`) e o conjunto de finais (`afd.finais`).
   * Percorre `transicoes_temp` e, para cada tupla, chama `afd.criaTransicao(origem, destino, simbolo)` para registrar a transição no autômato.
   * Finalmente, retorna o autômato completamente construído.

---

Função `salvar_afd_em_jflap`:

1. **Criação da estrutura XML básica**

   ```python
   estrutura = ET.Element('structure')
   tipo = ET.SubElement(estrutura, 'type')
   tipo.text = 'fa'
   automato = ET.SubElement(estrutura, 'automaton')
   ```

   * `ET.Element('structure')` cria o nó raiz `<structure>`.
   * Em seguida, um filho `<type>` é criado e recebe o texto `"fa"` (denotando “finite automaton”).
   * Por fim, criamos o nó `<automaton>` dentro de `<structure>`, onde iremos inserir estados e transições.

2. **Mapeamento de nomes de estado para IDs numéricos**

   ```python
   id_map = {estado: str(i) for i, estado in enumerate(sorted(afd.estados))}
   ```

   * Pega o conjunto `afd.estados`, ordena-o (para garantir consistência) e enumera, gerando pares `(índice, estado)`.
   * Converte o índice em string e mapeia cada `estado` ao seu `id` numérico em `id_map[estado]`.

3. **Geração dos nós `<state>`**

   ```python
   for estado in afd.estados:
       state_el = ET.SubElement(automato, 'state',
                                id=id_map[estado],
                                name=str(estado))
       if estado == afd.incial:
           ET.SubElement(state_el, 'initial')
       if estado in afd.finais:
           ET.SubElement(state_el, 'final')
   ```

   * Para cada `estado` em `afd.estados`:

     1. Cria um nó `<state>` em `<automaton>`, com atributos `id="..."` e `name="..."`.
     2. Se for o estado inicial (`estado == afd.incial`), adiciona um filho vazio `<initial>`.
     3. Se estiver no conjunto de finais (`estado in afd.finais`), adiciona um filho vazio `<final>`.

4. **Geração dos nós `<transition>`**

   ```python
   for (origem, simbolo), destino in afd.transicoes.items():
       trans_el = ET.SubElement(automato, 'transition')
       ET.SubElement(trans_el, 'from').text = id_map[origem]
       ET.SubElement(trans_el, 'to').text = id_map[destino]
       ET.SubElement(trans_el, 'read').text = simbolo
   ```

   * `afd.transicoes` é um dicionário cujas chaves são tuplas `(origem, simbolo)` e valores são `destino`.
   * Para cada par:

     1. Cria um nó `<transition>`.
     2. Dentro dele, cria `<from>` com o texto igual ao ID numérico do estado de origem.
     3. Cria `<to>` com o ID do estado de destino.
     4. Cria `<read>` com o símbolo da transição.

5. **Escrita do arquivo JFLAP**

   ```python
   tree = ET.ElementTree(estrutura)
   tree.write(caminho_arquivo,
              encoding='utf-8',
              xml_declaration=True)
   ```

   * Empacota todo o elemento raiz (`estrutura`) na `ElementTree`.
   * Escreve em disco no caminho especificado (`caminho_arquivo`), usando `utf‑8` e incluindo a declaração XML (`<?xml version="1.0" encoding="utf-8"?>`).

---


Função `minimizar_hopcroft`:

---

### 1. Preparação e partições iniciais

```python
Q = set(self.estados)
F = set(self.finais)
P = [F, Q - F]
P = [block for block in P if block]
W = [block.copy() for block in P]
```

1. **Conjuntos fundamentais**

   * `Q` é o conjunto de todos os estados do AFD.
   * `F` é o conjunto de estados finais.

2. **Partições iniciais**

   * `P` começa com duas “blocos” (partições): o bloco dos finais `F` e o bloco dos não‑finais `Q – F`.
   * Linhas seguintes removem quaisquer blocos vazios (caso `F` seja vazio ou todos sejam finais).

3. **Worklist**

   * `W` (lista de trabalho) recebe cópias dos blocos de `P`. Essa lista controla quais blocos ainda podem causar refinamentos.

---

### 2. Loop principal de refinamento

```python
while W:
    A = W.pop()
    for c in self.alfabeto:
        X = {q for q in Q if self.transicoes.get((q, c)) in A}
        new_P = []
        for Y in P:
            inter = Y & X
            diff  = Y - X
            if inter and diff:
                new_P += [inter, diff]
                # ajustar worklist conforme Y
            else:
                new_P.append(Y)
        P = new_P
```

1. **Extrair bloco alvo**

   * Retira (`pop`) um bloco `A` de `W`.

2. **Para cada símbolo do alfabeto**

   * Calcula `X`, o conjunto de todos os estados que, ao ler `c`, transitam para algum estado de `A`.

     ```python
     X = { q ∈ Q | δ(q, c) ∈ A }
     ```

3. **Refinar cada bloco `Y` em `P`**

   * Para o bloco `Y`, computa:

     * `inter = Y ∩ X` (estados de `Y` que vão para `A` lendo `c`)
     * `diff  = Y \ X` (estados de `Y` que **não** vão para `A`).
   * Se ambos forem não‑vazios, `Y` é dividido em dois blocos menores (`inter` e `diff`).

     * Substitui `Y` por esses dois em `new_P`.
     * Atualiza a worklist `W`:

       * Se `Y` já estava em `W`, retira-o e coloca `inter` e `diff`.
       * Caso contrário, adiciona apenas o menor dos dois blocos (heurística de Hopcroft).

4. **Atualiza `P`**

   * Ao final de processar todos os símbolos e blocos, `P` torna‑se a nova lista de partições refinadas.

Esse laço continua até que não haja mais blocos em `W` para processar — isto é, até que nenhuma partição possa ser refinada.

---

### 3. Verificação de minimização imediata

```python
if len(P) == len(Q):
    print("✅ O AFD já está minimizado pelo critério de Hopcroft.")
    return self
```

* Se ao final cada estado ficou isolado em seu próprio bloco (|P| = |Q|), não houve fusão de estados — o autômato já era mínimo e é retornado sem alterações.

---

### 4. Construção do novo AFD mínimo

```python
novo = AFD(self.alfabeto)
bloco_map = {}
for i, block in enumerate(P):
    nome_bloco = f'q{i}'
    bloco_map[frozenset(block)] = nome_bloco
    novo.estados.add(nome_bloco)
    if self.incial in block:
        novo.incial = nome_bloco
    if block & F:
        novo.finais.add(nome_bloco)
```

1. **Instância vazia**

   * Cria `novo`, um AFD com o mesmo alfabeto.

2. **Mapeamento de blocos → novo nome de estado**

   * Cada partição `block` em `P` vira um único estado no AFD mínimo.
   * Gera um nome genérico `q0, q1, …` e guarda em `bloco_map`.
   * Adiciona esse nome ao conjunto `novo.estados`.
   * Se o bloco conter o antigo estado inicial, marca o novo estado como inicial.
   * Se contiver algum estado final, marca o novo como final.

---

### 5. Transferindo transições

```python
for block in P:
    rep = next(iter(block))
    origem = bloco_map[frozenset(block)]
    for c in self.alfabeto:
        dst = self.transicoes.get((rep, c))
        if dst is not None:
            for b in P:
                if dst in b:
                    destino = bloco_map[frozenset(b)]
                    novo.transicoes[(origem, c)] = destino
                    break
```

1. **Escolha de representante**

   * Para cada bloco, pega-se arbitrariamente um elemento `rep` (por exemplo, o primeiro).

2. **Definição de transições**

   * Para cada símbolo `c`, vê-se para onde `rep` iria no AFD original.
   * Descobre-se a qual bloco esse destino pertence e cria-se a transição correspondente no AFD mínimo, entre os nomes de bloco (`origem`, `destino`).

---

### 6. Conclusão

```python
print("✅ AFD minimizado com sucesso pelo algoritmo de Hopcroft.")
return novo
```

* Informa sucesso e retorna o novo autômato, minimizado segundo o algoritmo de Hopcroft.

---




Função `Testar_equivalencia`:

---

### 1. Unificação do alfabeto e inicialização

```python
sigma = set(afd1.alfabeto) | set(afd2.alfabeto)
visited = set()
queue = deque()
```

* **Alfabeto unificado (`sigma`)**
  Cria o conjunto de todos os símbolos que aparecem em ao menos um dos dois AFDs, garantindo que exploraremos transições de ambos.
* **Conjunto `visited`**
  Guarda pares de estados já processados para evitar revisitar.
* **Fila `queue`**
  Será usada para uma busca em largura (BFS) no “produto” dos dois autômatos.

---

### 2. Estado inicial do par

```python
queue.append((afd1.incial, afd2.incial))
visited.add((afd1.incial, afd2.incial))
```

* Empacota o estado inicial de cada AFD em uma tupla `(q1, q2)` e insere na fila.
* Marca esse par como visitado.

---

### 3. Loop principal de BFS

```python
while queue:
    q1, q2 = queue.popleft()
    # ...
```

* Enquanto houver pares de estados na fila:

  1. Remove o próximo par `(q1, q2)` para processar.

---

### 4. Verificação de discrepância de aceitação

```python
in1 = q1 in afd1.finais
in2 = q2 in afd2.finais
if in1 != in2:
    return False
```

* Checa se exatamente um dos dois estados é de aceitação.
* Se um autômato aceita e o outro rejeita naquela configuração, concluímos que **não** são equivalentes e retornamos `False` imediatamente.

---

### 5. Exploração de transições

```python
for a in sigma:
    next1 = afd1.transicoes.get((q1, a))
    next2 = afd2.transicoes.get((q2, a))
    if next1 is None and next2 is None:
        continue
    pair = (next1, next2)
    if pair not in visited:
        visited.add(pair)
        queue.append(pair)
```

Para cada símbolo `a` no alfabeto unificado:

1. Obtém o estado de destino em cada AFD (`next1`, `next2`).
2. Se **ambos** não tiverem transição (`None`), ignora – ambos “morreram” no mesmo símbolo.
3. Caso contrário, forma o par `(next1, next2)`.
4. Se esse par ainda não foi visitado, marca‑o e enfileira para processamento futuro.

---

### 6. Conclusão

```python
return True
```

* Se o laço terminar sem encontrar discrepância de aceitação, todos os pares de estados foram compatíveis.
* Retorna `True`, indicando que os dois AFDs reconhecem exatamente a mesma linguagem.

---

**Em suma**, o método faz uma busca em largura nos pares de estados dos dois AFDs, verificando simultaneamente:

1. Se em alguma configuração um aceita e o outro não.
2. Se, para cada símbolo, seguem transições “paralelas” sem criar distinção.

Se nunca encontrar uma diferença no critério de aceitação, conclui que os autômatos são equivalentes.





Função `estados_equivalentes`:

---

### 1. Inicialização de dados e partições

```python
estados  = sorted(self.estados)
alfabeto = list(self.alfabeto)

# Partição inicial: estado finais x não‑finais
blocos = [ set(self.finais), set(estados) - set(self.finais) ]
mudou  = True
```

1. **Ordena** a lista de estados e converte o alfabeto em lista para índice fixo.
2. **Define** a partição inicial em dois blocos:

   * Estados finais
   * Estados não‑finais
3. `mudou` sinaliza se na última iteração houve alguma divisão de bloco.

---

### 2. Loop de refinamento das partições

```python
while mudou:
    mudou      = False
    novos_blocos = []
    for bloco in blocos:
        assinatura_map = {}
        ...
        novos_blocos.extend(assinatura_map.values())
    blocos = novos_blocos
```

* **Enquanto** houver divisão de blocos (`mudou == True`):

  1. Reinicia `mudou = False` e prepara `novos_blocos`.
  2. Para cada `bloco` na partição atual, cria-se um mapeamento por “assinatura” de transições.
  3. Ao fim, substitui `blocos` por `novos_blocos`.

---

### 3. Cálculo da “assinatura” de cada estado

Dentro do loop de cada bloco:

```python
for q in bloco:
    assinatura = []
    for a in alfabeto:
        destino = self.transicoes.get((q, a))
        # Descobre em que bloco o destino está
        idx = next((i for i, b in enumerate(blocos) if destino in b), None)
        assinatura.append(idx)
    assinatura = tuple(assinatura)
    assinatura_map.setdefault(assinatura, set()).add(q)
```

* Para cada estado `q` em um bloco:

  1. Percorre cada símbolo `a`.
  2. Obtém o estado destino `destino = δ(q, a)` (ou `None` se não existir).
  3. Identifica o **índice** do bloco atual onde `destino` reside (ou `None`).
  4. Constrói uma tupla `assinatura` de índices de bloco — dois estados com a mesma tupla têm comportamento idêntico nas próximas transições.
  5. Agrupa os estados em `assinatura_map[assinatura]`.

---

### 4. Divisão de blocos conforme assinaturas

```python
if len(assinatura_map) > 1:
    mudou = True
novos_blocos.extend(assinatura_map.values())
```

* Se um bloco gerou mais de uma assinatura distinta, ele é **dividido** em sub‑blocos.
* Marca `mudou = True` para indicar que precisamos de outra rodada de refinamento.
* Todos os sub‑blocos (cada valor de `assinatura_map`) vão para `novos_blocos`.

---

### 5. Extração de pares de estados equivalentes

Após estabilizar as partições (nenhum bloco é dividido):

```python
equivalentes = []
for bloco in blocos:
    if len(bloco) > 1:
        for p, q in combinations(sorted(bloco), 2):
            equivalentes.append((p, q))
return equivalentes
```

* Para cada bloco com pelo menos dois estados, gera todas as combinações de pares `(p, q)` dentro do bloco.
* Retorna a lista de todos esses pares — são estados que partilham o mesmo comportamento e, portanto, são equivalentes.

---

**Resumo**:

1. Começa com dois blocos (finais vs. não‑finais).
2. Repetidamente, subdivide cada bloco agrupando estados pela “assinatura” de para quais blocos transitam em cada símbolo.
3. Para cada bloco que se estabiliza (não se subdivide), coleta pares de estados se houver mais de um estado no bloco.
4. Ao final, retorna todos os pares de estados que permanecem juntos em algum bloco — estes são equivalentes.




Pensou por dois segundos


---

Função `completar_afd` – Totalização do AFD

---

### 1. Clonagem do AFD original

```python
from copy import deepcopy
comp = deepcopy(afd)
```

* Gera uma **cópia profunda** de `afd`, preservando o original inalterado.
* `comp` servirá como base para tornar o autômato total (com todas as transições definidas).

---

### 2. Reconstrução do alfabeto efetivo

```python
sigma = {simbolo for (_, simbolo) in comp.transicoes.keys()}
```

* Extrai de `comp.transicoes` apenas os símbolos realmente usados nas chaves `(estado, símbolo)`.
* Ignora eventuais símbolos inúteis ou não referenciados.

---

### 3. Detecção de transições faltantes

```python
faltantes = []
for estado in comp.estados:
    for simbolo in sigma:
        if (estado, simbolo) not in comp.transicoes:
            faltantes.append((estado, simbolo))
```

* Percorre **cada** par `(estado, símbolo)` em `comp.estados × σ`:

  * Se não existir a transição, registra em `faltantes`.
* Isso identifica as “lacunas” que impedem o AFD de ser total.

---

### 4. Criação do estado “morto” e fechamento de transições

```python
if faltantes:
    dead = '__dead__'
    comp.estados.add(dead)
    for simbolo in sigma:
        comp.transicoes[(dead, simbolo)] = dead
    for (origem, simbolo) in faltantes:
        comp.transicoes[(origem, simbolo)] = dead
```

* **Se** houver algum par faltante:

  1. Adiciona `__dead__` a `comp.estados`.
  2. Garante auto‑laços em `dead` para **todo** símbolo de `σ`.
  3. Direciona cada transição faltante para `dead`.
* Após isso, `comp` é um AFD **total**.

---

### 5. Retorno do AFD totalizado

```python
return comp
```

* `comp` está pronto para ser usado por outras operações (sem lacunas).

---

Função `complemento_afd` – Complemento via totalização

---

### 1. Totalização e inversão de finais

```python
comp = self.completar_afd(afd)
comp.finais = comp.estados - comp.finais
return comp
```

1. Chama `completar_afd` para garantir que não haja transições faltantes.
2. Inverte o conjunto de estados finais:

   * Novos finais = todos os estados **que não** eram finais.
3. Retorna o complemento de `afd`, pronto para reconhecer a linguagem inversa.

---

Função `produto_afds` – Produto de dois AFDs totalizados

---

### 1. Totalização prévia dos autômatos

```python
afd1 = self.completar_afd(afd1)
afd2 = self.completar_afd(afd2)
sigma = set(afd1.alfabeto) | set(afd2.alfabeto)
novo = AFD(sigma)
```

* Garante que ambos `afd1` e `afd2` estejam completos.
* Unifica alfabetos e instancia o autômato produto `novo`.

---

### 2. Criação dos estados produto

```python
for q1 in afd1.estados:
    for q2 in afd2.estados:
        nome     = f"({q1},{q2})"
        is_final = criterio_final(q1 in afd1.finais,
                                  q2 in afd2.finais)
        novo.estados.add(nome)
        if afd1.incial == q1 and afd2.incial == q2:
            novo.incial = nome
        if is_final:
            novo.finais.add(nome)
```

* Cada estado de `novo` é um par `(q1, q2)`.
* O estado inicial é o par de iniciais originais.
* Finais definidos pelo `criterio_final(in1, in2)`.

---

### 3. Construção das transições do produto

```python
for q1 in afd1.estados:
    for q2 in afd2.estados:
        for a in sigma:
            t1 = afd1.transicoes.get((q1, a))
            t2 = afd2.transicoes.get((q2, a))
            if t1 is None or t2 is None:
                continue
            dest = f"({t1},{t2})"
            novo.transicoes[(f"({q1},{q2})", a)] = dest
return novo
```

* Para cada `(q1,q2)×a`, verifica movimentos em ambos os AFDs.
* Se ambos existirem, cria a transição para o par de destinos.
* Retorna o AFD produto que segue o critério de aceitação desejado.

---

**Resumo das mudanças**:

* **`completar_afd`**: isolada para totalizar qualquer AFD.
* **`complemento_afd`**: agora usa `completar_afd` antes de inverter finais.
* **`produto_afds`**: totaliza ambos os AFDs antes de gerar estados e transições.





---

## 1. União de AFDs

```python
def uniao_afds(self, afd1, afd2):
    return self.produto_afds(afd1, afd2, lambda f1, f2: f1 or f2)
```

1. **Chamada ao produto de autômatos**
   Você delega a construção do autômato “produto” dos dois AFDs ao método `produto_afds`.
2. **Critério de aceitação**
   Passa como parâmetro uma função anônima (`lambda f1, f2: f1 or f2`) que retorna `True` se **pelo menos um** dos componentes for de aceitação.
3. **Semântica**
   O autômato resultante reconhece exatamente a **união** das linguagens:

   $$
   L(\text{união}) \;=\; \{ w \mid w \in L(afd1) \;\lor\; w \in L(afd2) \}.
   $$

---

## 2. Interseção de AFDs

```python
def intersecao_afds(self, afd1, afd2):
    return self.produto_afds(afd1, afd2, lambda f1, f2: f1 and f2)
```

1. **Reuso de `produto_afds`**
   Novamente usa o construtor de produto de autômatos.
2. **Critério de aceitação**
   A função passada (`lambda f1, f2: f1 and f2`) retorna `True` apenas se **ambos** os componentes forem finais.
3. **Semântica**
   O produto reconhece a **interseção**:

   $$
   L(\text{interseção}) \;=\; \{ w \mid w \in L(afd1) \;\land\; w \in L(afd2) \}.
   $$

---

## 3. Diferença de AFDs

```python
def diferenca_afds(self, afd1, afd2):
    comp2 = self.complemento_afd(afd2)
    return self.intersecao_afds(afd1, comp2)
```

1. **Complemento de `afd2`**
   Chama `self.complemento_afd(afd2)` para obter um AFD que aceita exatamente as cadeias **não** aceitas por `afd2`.
2. **Interseção com `afd1`**
   Em seguida, computa a interseção entre `afd1` e esse complemento.
3. **Semântica**
   Isso produz a **diferença** de linguagens:

   $$
   L(\text{diferença}) \;=\; \{ w \mid w \in L(afd1) \;\land\; w \notin L(afd2)\}.
   $$

---

### Observações gerais

* **Reuso de código**: ao centralizar a construção do autômato produto em `produto_afds`, você evita duplicar lógica para união e interseção.
* **Critérios como funções**: passar o critério de aceitação como callback (`lambda f1,f2: …`) torna a API flexível, permitindo estender a operadores como diferença simétrica, por exemplo, sem reescrever o produto.
* **Modularidade**: a diferença é implementada em termos de complemento e interseção, refletindo diretamente a identidade de conjuntos $\,A \setminus B = A \cap B^c$.

Esse conjunto de métodos cobre as operações clássicas de teoria de linguagens regulares, possibilitando compor AFDs para representar união, interseção e diferença de linguagens de forma clara e reaproveitável.




