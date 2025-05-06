import os
import sys
from gc import disable
import tkinter as tk
from AFD import *
from collections import deque
from tkinter import filedialog

# ===== Funções que abrem o EXPLORER =====

def escolher_arquivo_abrir():
    root = tk.Tk()
    root.withdraw()
    caminho = filedialog.askopenfilename(
        title="Selecione um arquivo JFLAP (.jff)",
        filetypes=[("Arquivos JFLAP", "*.jff")],
    )
    return caminho

def escolher_arquivo_salvar():
    root = tk.Tk()
    root.withdraw()
    caminho = filedialog.asksaveasfilename(
        title="Salvar AFD como...",
        defaultextension=".jff",
        filetypes=[("Arquivos JFLAP", "*.jff")],
    )
    return caminho



# ===== Menu interativo no terminal =====
def menu():
    afds = {}

    while True:
        print("\n===== MENU AFD =====")
        print("1. Importar AFD de arquivo JFLAP (.jff)")
        print("2. Salvar AFD atual em arquivo")
        print("3. Mostrar AFD")
        print("4. Criar cópia do AFD")
        print("5. Minimizar AFD")
        print("6. Verificar equivalência entre AFDs")
        print("7. Verificar estados esquivalentes do AFD")
        print("8. Operação entre AFDs")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome_afd = input("Digite o nome do AFD: ")
            caminho = escolher_arquivo_abrir()
            if caminho and os.path.exists(caminho):
                try:
                    afd = AFD.carregar_afd_de_jflap(caminho)
                    afds[nome_afd] = afd
                    print(f"✅ AFD carregado com sucesso com o nome '{nome_afd}' de:\n{caminho}")
                except Exception as e:
                    print(f"❌ Erro ao carregar AFD:\n{e}")
            else:
                print("⚠️ Nenhum arquivo selecionado ou caminho inválido.")

        elif opcao == "2":
            if not afds:
                print("⚠️ Nenhum AFD carregado ainda.")
                continue
            nome_afd = input(f"Escolha um AFD para salvar {list(afds.keys())}: ")
            if nome_afd in afds:
                caminho = escolher_arquivo_salvar()
                if caminho:
                    try:
                        afds[nome_afd].salvar_afd_em_jflap(caminho)
                        print(f"✅ AFD '{nome_afd}' salvo com sucesso em:\n{caminho}")
                    except Exception as e:
                        print(f"❌ Erro ao salvar AFD:\n{e}")
                else:
                    print("⚠️ Salvamento cancelado.")
            else:
                print("⚠️ AFD não encontrado.")

        elif opcao == "3":
            if not afds:
                print("⚠️ Nenhum AFD carregado.")
                continue
            nome_afd = input(f"Escolha um AFD para mostrar {list(afds.keys())}: ")
            if nome_afd in afds:
                print(afds[nome_afd])
            else:
                print("⚠️ AFD não encontrado.")

        elif opcao == "4":
            if not afds:
                print("⚠️ Nenhum AFD carregado.")
                continue
            nome_afd = input(f"Escolha um AFD para copiar {list(afds.keys())}: ")
            if nome_afd in afds:
                copia = afds[nome_afd].copiar()
                nome_copia = f"{nome_afd}_copia"
                afds[nome_copia] = copia
                print(f"✅ AFD '{nome_afd}' copiado com o nome :{nome_copia}")
            else:
                print("⚠️ AFD não encontrado.")

        elif opcao == "5":
            if not afds:
                print("⚠️ Nenhum AFD carregado.")
                continue
            nome = input(f"Escolha o AFD para minimização Hopcroft {list(afds.keys())}: ")
            if nome not in afds:
                print("⚠️ AFD não encontrado.")
                continue
            novo = afds[nome].minimizar_hopcroft()
            # Se retornar novo objeto diferente, atualiza ou armazena novo
            if novo is not afds[nome]:
                afds[f"{nome}_min"] = novo
            else:
                afds[nome] = novo

        elif opcao == "6":
            if len(afds) < 2:
                print("⚠️ É necessário ter pelo menos dois AFDs carregados para verificar equivalência.")
                continue
            nome1 = input(f"Digite o nome do primeiro AFD {list(afds.keys())}: ")
            nome2 = input(f"Digite o nome do segundo AFD {list(afds.keys())}: ")
            if nome1 not in afds or nome2 not in afds:
                print("⚠️ Um ou ambos os AFDs não foram encontrados.")
                continue
            equivalente = afd.testar_equivalencia(afds[nome1], afds[nome2])
            if equivalente:
                print(f"✅ Os AFDs '{nome1}' e '{nome2}' são equivalentes.")
            else:
                print(f"❌ Os AFDs '{nome1}' e '{nome2}' NÃO são equivalentes.")
        elif opcao == "7":
            if not afds:
                print("⚠️ Nenhum AFD carregado.")
                continue
            nome_afd = input(f"Digite o nome do AFD para verificar estados equivalentes {list(afds.keys())}: ")
            if nome_afd in afds:
                equivalentes = afds[nome_afd].estados_equivalentes()
                if equivalentes:
                    print("✅ Estados equivalentes encontrados:")
                    for par in equivalentes:
                        print(f"  - {par[0]} ≡ {par[1]}")
                else:
                    print("ℹ️ Nenhum par de estados equivalentes encontrado.")
            else:
                print("⚠️ AFD não encontrado.")

        elif opcao == "8":
            if not afds:
                print("⚠️ Nenhum AFD carregado.")
                continue
            # submenu de operações
            print("\n--- OPERACAO ENTRE AFDS ---")
            print("a. Uniao")
            print("b. Intersecao")
            print("c. Diferenca")
            print("d. Complemento")
            print("0. Voltar")
            op = input("Escolha a operacao: ")

            if op == 'a':
                n1 = input(f"Primeiro AFD {list(afds.keys())}: ")
                if n1 not in afds:
                    print(f"❌ AFD '{n1}' não encontrado.")
                    continue
                n2 = input(f"Segundo AFD {list(afds.keys())}: ")
                if n2 not in afds:
                    print(f"❌ AFD '{n2}' não encontrado.")
                    continue
                res = afd.uniao_afds(afds[n1], afds[n2])
                afds[f"{n1}_U_{n2}"] = res
                print(f"✅ AFD resultante '" + f"{n1}_U_{n2}" + "' criado.")

            elif op == 'b':
                n1 = input(f"Primeiro AFD {list(afds.keys())}: ")
                if n1 not in afds:
                    print(f"❌ AFD '{n1}' não encontrado.")
                    continue
                n2 = input(f"Segundo AFD {list(afds.keys())}: ")
                if n2 not in afds:
                    print(f"❌ AFD '{n2}' não encontrado.")
                    continue
                res = afd.intersecao_afds(afds[n1], afds[n2])
                afds[f"{n1}_I_{n2}"] = res
                print(f"✅ AFD resultante '" + f"{n1}_I_{n2}" + "' criado.")

            elif op == 'c':
                n1 = input(f"AFD minuendo {list(afds.keys())}: ")
                if n1 not in afds:
                    print(f"❌ AFD '{n1}' não encontrado.")
                    continue
                n2 = input(f"AFD subtraendo {list(afds.keys())}: ")
                if n2 not in afds:
                    print(f"❌ AFD '{n2}' não encontrado.")
                    continue
                res = afd.diferenca_afds(afds[n1], afds[n2])
                afds[f"{n1}_D_{n2}"] = res
                print(f"✅ AFD resultante '" + f"{n1}_D_{n2}" + "' criado.")

            elif op == 'd':
                n = input(f"AFD para complementar {list(afds.keys())}: ")
                if n not in afds:
                    print(f"❌ AFD '{n}' não encontrado.")
                    continue
                res = afd.complemento_afd(afds[n])
                afds[f"{n}_C"] = res
                print(f"✅ AFD resultante '{n}_C' criado.")

        elif opcao == "0":
            print("Saindo...")
            sys.exit()

        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
