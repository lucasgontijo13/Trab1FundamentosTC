
import xml.etree.ElementTree as ET

from collections import deque
from copy import deepcopy
from itertools import combinations


class AFD:

    def __init__(self, Alfabeto):
        Alfabeto = str(Alfabeto)
        self.estados = set()
        self.alfabeto = Alfabeto
        self.transicoes = dict()
        self.incial = None
        self.finais = set()

    # Funções aprendidas na video aula mas nao utilizadas
    def limpaAfd(self):
        self.__deuErro = False
        self.__estadoAtual = self.incial

    # Funções aprendidas na video aula mas nao utilizadas
    def criaEstado(self,id,inicial=False,final=False):
        id = str(id)
        if id in self.estados:
            return False
        if inicial:
            self.incial = id
        if final:
            self.finais = self.finais.union({id})
        return True

    # Funções aprendidas na video aula mas nao utilizadas
    def criaTransicao(self,origem,destino,simbolo):
        origem = str(origem)
        destino = str(destino)
        simbolo = str(simbolo)

        if not origem in self.estados:
            return False

        if not destino in self.estados:
            return False

        if len(simbolo) != 1 or not simbolo in self.alfabeto:
            return False

        self.transicoes[(origem,simbolo)] = destino
        return True

    # Funções aprendidas na video aula mas nao utilizadas
    def mudaEstadoInicial(self,id):
        if not id in self.estados:
            return
        self.inicial = id

    # Funções aprendidas na video aula mas nao utilizadas
    def mudaEstadoFinal(self, id, final):
        if not id in self.estados:
            return
        if final:
            self.final = self.finais.union({id})
        else:
            self.final = self.finais.difference({id})

    # Funções aprendidas na video aula mas nao utilizadas
    def move(self, cadeia):
        for simbolo in cadeia:
            if not simbolo in self.alfabeto:
                self.__deuErro = True
                break
            if(self.__estadoAtual, simbolo) in self.transicoes.keys():
                novoEstado = self.transicoes[(self.__estadoAtual, simbolo)]
                self.__estadoAtual = novoEstado
            else:
                self.__deuErro = True
                break
        return self.__estadoAtual

    # Funções aprendidas na video aula mas nao utilizadas
    def deuErro(self):
        return self.__deuErro

    # Funções aprendidas na video aula mas nao utilizadas
    def estadoAtual(self):
        return self.__estadoAtual

    # Funções aprendidas na video aula mas nao utilizadas
    def estadoFinal(self, id):
        return id in self.finais

    def __str__(self):
        s = 'AFD:\n'

        # Estados
        s += '  Estados (E):\n'
        s += '   { ' + ', '.join(str(e) for e in self.estados) + ' }\n'

        # Alfabeto
        s += '  Alfabeto (A):\n'
        s += '   { ' + ', '.join(str(a) for a in self.alfabeto) + ' }\n'

        # Transições
        s += '  Transições (T):\n'
        for (e, a), d in self.transicoes.items():
            s += f'   ({e}, "{a}") --> {d}\n'

        # Estado inicial
        s += f'  Estado Inicial (i): {self.incial}\n'

        # Estados Finais
        s += '  Estados Finais (F):\n'
        s += '   { ' + ', '.join(str(e) for e in self.finais) + ' }\n'

        return s




    # ===== SUPORTE AFD EM JFLAP =====

    def carregar_afd_de_jflap(caminho_arquivo):
        tree = ET.parse(caminho_arquivo)
        root = tree.getroot()
        automato = root.find('automaton')

        estados = {}
        alfabeto = set()
        transicoes_temp = []

        inicial = None
        finais = set()

        # 1) Ler os estados
        for state in automato.findall('state'):
            id_xml = state.get('id')  # atributo id do XML (string)
            nome = state.get('name')  # nome legível do estado
            estados[id_xml] = nome  # mapeia id → nome

            if state.find('initial') is not None:
                inicial = nome              # marca estado inicial
            if state.find('final') is not None:
                finais.add(nome)           # adiciona a estados finais

        if inicial is None:

            return None
        if not finais:

            return None

        # 2) Ler transições
        for trans in automato.findall('transition'):
            origem_id = trans.find('from').text  # id numérico do estado de origem
            destino_id = trans.find('to').text  # id numérico do estado de destino
            simbolo = trans.find('read').text or ""  # símbolo lido (pode ser vazio)

            origem = estados[origem_id]  # converte id → nome
            destino = estados[destino_id]  # converte id → nome
            alfabeto.add(simbolo)  # coleta todos os símbolos usados
            transicoes_temp.append((origem, simbolo, destino))

        # 3) Criar o objeto AFD
        afd = AFD(alfabeto)         # inicializa com o alfabeto extraído
        for id_estado in estados.values():
            afd.estados.add(id_estado)          # adiciona cada estado
        afd.incial = inicial  # define o inicial
        afd.finais = finais  # define o conjunto de finais

        # 4) Adicionar transições (já validadas)
        for origem, simbolo, destino in transicoes_temp:
            afd.criaTransicao(origem, destino, simbolo)

        return afd

    def salvar_afd_em_jflap(afd, caminho_arquivo):
        estrutura = ET.Element('structure')
        tipo = ET.SubElement(estrutura, 'type')
        tipo.text = 'fa'
        automato = ET.SubElement(estrutura, 'automaton')

        # Mapeia cada nome de estado para um ID numérico (string)
        id_map = {estado: str(i) for i, estado in enumerate(sorted(afd.estados))}


        for estado in afd.estados:
            state_el = ET.SubElement(automato, 'state', id=id_map[estado], name=str(estado))
            if estado == afd.incial:
                ET.SubElement(state_el, 'initial')
            if estado in afd.finais:
                ET.SubElement(state_el, 'final')

        for (origem, simbolo), destino in afd.transicoes.items():
            trans_el = ET.SubElement(automato, 'transition')
            ET.SubElement(trans_el, 'from').text = id_map[origem]
            ET.SubElement(trans_el, 'to').text = id_map[destino]
            ET.SubElement(trans_el, 'read').text = simbolo

        tree = ET.ElementTree(estrutura)
        tree.write(caminho_arquivo, encoding='utf-8', xml_declaration=True)

    # ===== Funções de manipulação do AFD =====
    def minimizar_hopcroft(self):
        """
        Minimização de AFD pelo algoritmo de Hopcroft.
        Se já estiver minimizado, exibe mensagem e retorna o próprio AFD.
        """
        # Estado completo: garante que para cada estado e símbolo haja transição (pode levar a None)
        # Partições iniciais: finais e não-finais
        Q = set(self.estados)
        F = set(self.finais)
        P = [F, Q - F]
        # Remover partições vazias
        P = [block for block in P if block]
        # Worklist
        W = [block.copy() for block in P]

        while W:
            A = W.pop()
            for c in self.alfabeto:
                # Conjunto de estados que vão para A pelo símbolo c
                X = {q for q in Q if self.transicoes.get((q, c)) in A}
                new_P = []
                for Y in P:
                    inter = Y & X
                    diff = Y - X
                    if inter and diff:
                        new_P.append(inter)
                        new_P.append(diff)
                        # Atualizar worklist
                        if Y in W:
                            W.remove(Y)
                            W.append(inter)
                            W.append(diff)
                        else:
                            # adiciona menor bloco primeiro
                            W.append(inter if len(inter) <= len(diff) else diff)
                    else:
                        new_P.append(Y)
                P = new_P

        # Se cada estado está em seu próprio bloco, já está minimizado
        if len(P) == len(Q):
            print("✅ O AFD já está minimizado pelo critério de Hopcroft.")
            return self

        # Construir novo AFD minimizado
        novo = AFD(self.alfabeto)
        # Mapear cada bloco a um representante de nome
        bloco_map = {}
        for i, block in enumerate(P):
            nome_bloco = f'q{i}'
            bloco_map[frozenset(block)] = nome_bloco
            novo.estados.add(nome_bloco)
            if self.incial in block:
                novo.incial = nome_bloco
            if block & F:
                novo.finais.add(nome_bloco)

        # Criar transições
        for block in P:
            rep = next(iter(block))
            origem = bloco_map[frozenset(block)]
            for c in self.alfabeto:
                dst = self.transicoes.get((rep, c))
                if dst is not None:
                    # encontrar bloco de destino
                    for b in P:
                        if dst in b:
                            destino = bloco_map[frozenset(b)]
                            novo.transicoes[(origem, c)] = destino
                            break
        print("✅ AFD minimizado com sucesso pelo algoritmo de Hopcroft.")
        return novo


    # ===== Teste de equivalência entre dois AFDs =====
    def testar_equivalencia(self, afd1, afd2):
        # Unifica o alfabeto
        sigma = set(afd1.alfabeto) | set(afd2.alfabeto)
        visited = set()
        queue = deque()

        # Estado inicial do par
        queue.append((afd1.incial, afd2.incial))
        visited.add((afd1.incial, afd2.incial))

        while queue:
            q1, q2 = queue.popleft()
            # Verifica discrepância de aceitação
            in1 = q1 in afd1.finais
            in2 = q2 in afd2.finais
            if in1 != in2:
                return False
            # Explora próxima transição para cada símbolo
            for a in sigma:
                next1 = afd1.transicoes.get((q1, a))
                next2 = afd2.transicoes.get((q2, a))
                # Se ambos levam ao estado "morto" (None), continua
                if next1 is None and next2 is None:
                    continue
                pair = (next1, next2)
                if pair not in visited:
                    visited.add(pair)
                    queue.append(pair)
        return True

    def estados_equivalentes(self):

        # Refina partições até estabilizar para identificar classes de equivalência
        estados = sorted(self.estados)
        alfabeto = list(self.alfabeto)

        # Partição inicial: finais x não-finais
        blocos = [set(self.finais), set(estados) - set(self.finais)]
        mudou = True
        while mudou:
            mudou = False
            novos_blocos = []
            for bloco in blocos:
                # Agrupa estados por assinatura de transições
                assinatura_map = {}
                for q in bloco:
                    assinatura = []
                    for a in alfabeto:
                        destino = self.transicoes.get((q, a))
                        # Identifica índice do bloco do estado destino
                        idx = None
                        for i, b in enumerate(blocos):
                            if destino in b:
                                idx = i
                                break
                        assinatura.append(idx)
                    assinatura = tuple(assinatura)
                    assinatura_map.setdefault(assinatura, set()).add(q)

                # Sebloco precisar ser dividido
                if len(assinatura_map) > 1:
                    mudou = True
                novos_blocos.extend(assinatura_map.values())

            blocos = novos_blocos

        # Coleta pares de estados equivalentes em cada bloco com tamanho >= 2
        equivalentes = []
        for bloco in blocos:
            if len(bloco) > 1:
                for p, q in combinations(sorted(bloco), 2):
                    equivalentes.append((p, q))
        return equivalentes



    def copiar(afd):
        return deepcopy(afd)

    def completar_afd(self, afd):
        from copy import deepcopy
        comp = deepcopy(afd)

        # Reconstrói sigma apenas com os símbolos que realmente aparecem nas transições
        sigma = {simbolo for (_, simbolo) in comp.transicoes.keys()}

        # Detectar transições faltantes sobre sigma
        faltantes = []
        for estado in comp.estados:
            for simbolo in sigma:
                if (estado, simbolo) not in comp.transicoes:
                    faltantes.append((estado, simbolo))

        # Se faltar alguma, criar estado morto e completá-las
        if faltantes:
            dead = '__dead__'
            comp.estados.add(dead)
            # dead -> dead em todo símbolo
            for simbolo in sigma:
                comp.transicoes[(dead, simbolo)] = dead
            # ligar cada transição faltante ao estado morto
            for (origem, simbolo) in faltantes:
                comp.transicoes[(origem, simbolo)] = dead

        return comp

    # ===== Operações entre AFDs =====



    def produto_afds(self, afd1, afd2, criterio_final):
        # criterio_final: função que recebe (f1, f2) e diz se (q1,q2) é final
        afd1 = self.completar_afd(afd1)
        afd2 = self.completar_afd(afd2)

        sigma = set(afd1.alfabeto) | set(afd2.alfabeto)
        novo = AFD(sigma)
        # criar estados produto
        for q1 in afd1.estados:
            for q2 in afd2.estados:
                nome = f"({q1},{q2})"
                is_final = criterio_final(q1 in afd1.finais, q2 in afd2.finais)
                novo.estados.add(nome)
                if afd1.incial == q1 and afd2.incial == q2:
                    novo.incial = nome
                if is_final:
                    novo.finais.add(nome)
        # transições
        for q1 in afd1.estados:
            for q2 in afd2.estados:
                for a in sigma:
                    t1 = afd1.transicoes.get((q1, a))
                    t2 = afd2.transicoes.get((q2, a))
                    dest = None
                    if t1 is not None and t2 is not None:
                        dest = f"({t1},{t2})"
                    else:
                        continue  # transições incompletas ignoradas
                    novo.transicoes[(f"({q1},{q2})", a)] = dest
        return novo

    def complemento_afd(self, afd):
        comp = self.completar_afd(afd)
        comp.finais = comp.estados - comp.finais
        return comp

    def uniao_afds(self, afd1, afd2):
        return self.produto_afds(afd1, afd2, lambda f1, f2: f1 or f2)

    def intersecao_afds(self, afd1, afd2):
        return self.produto_afds(afd1, afd2, lambda f1, f2: f1 and f2)

    def diferenca_afds(self, afd1, afd2):
        comp2 = self.complemento_afd(afd2)
        return self.intersecao_afds(afd1, comp2)



