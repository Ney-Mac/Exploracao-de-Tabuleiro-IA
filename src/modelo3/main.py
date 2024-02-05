import time
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from src.Ambiente import Ambiente
from src.Agente import Agente
from src.Interface import Interface

time_to_sleep = 0.5


def abordagem_a(ambiente, agentes, atualizar_tab):
    for agente in agentes:
        ambiente.set_pos_agente_to_l(agente.posicao[0], agente.posicao[1])

    while ambiente.tesouros_achados <= ambiente.total_tesouros * 0.5 and len(agentes) > 0:
        for agente in agentes[:]:
            if agente.vivo:
                agente.mover(ambiente)
                atualizar_tab()
                time.sleep(time_to_sleep)
            else:
                agentes.remove(agente)
        ambiente.imprimir(agentes)

    if len(agentes) > 0:
        print('*********SUCESSO - Abordagem A********')
        print(f'Total de tesouros iniciais: {ambiente.total_tesouros}')
        print(f'Total de tesouros encontrados: {ambiente.tesouros_achados}')
    else:
        print('*********FALHA - Abordagem A*********')
        print(f'Todos os agentes morreram antes de encontrar ao menos 50% dos tesouros.')


def abordagem_b(ambiente, agentes, atualizar_tab):
    for agente in agentes:
        ambiente.set_pos_agente_to_l(agente.posicao[0], agente.posicao[1])

    while 'N' in [elemento for linha in ambiente.matriz_compartilhada for elemento in linha] and len(agentes) > 0:
        for agente in agentes[:]:
            if agente.vivo:
                agente.mover(ambiente)
                atualizar_tab()
                time.sleep(time_to_sleep)
            else:
                agentes.remove(agente)
        ambiente.imprimir(agentes)

    if len(agentes) > 0:
        print('*********SUCESSO - Abordagem B********')
        print(f'O ambiente foi totalmente explorado e continuam {len(agentes)} vivos')
    else:
        print('*********FALHA - Abordagem B*********')
        print('Todos os agentes morreram antes de explorar o ambiente inteiro')


def abordagem_c(ambiente, agentes, atualizar_tab):
    ambiente.inserir_f()

    for agente in agentes:
        ambiente.set_pos_agente_to_l(agente.posicao[0], agente.posicao[1])

    flag = False
    while not flag and len(agentes) > 0:
        for agente in agentes[:]:
            if agente.vivo:
                agente.mover(ambiente)
            else:
                agentes.remove(agente)
                atualizar_tab()
                time.sleep(time_to_sleep)
            if agente.flag:
                flag = True
                break
        ambiente.imprimir(agentes)

    if flag:
        print('*********SUCESSO - Abordagem C********')
        print('A bandeira foi encontrada')
    else:
        print('*********FALHA - Abordagem C*********')
        print('Todos os agentes morreram antes de encontrar a bandeira')


def main():
    data = pd.read_csv('../dados_treino/dataset.csv', delimiter=',')
    global_encoder = LabelEncoder()

    proporcao = {'B': 0.3, 'T': 0.2}
    ambiente = Ambiente(proporcao)

    # Aplica o encoder para todas as colunas de entrada
    columns_to_encode = ['Esquerda', 'Direita', 'Cima', 'Baixo']
    for column in columns_to_encode:
        data[column] = global_encoder.fit_transform(data[column])

    # Separa os dados em treinamento e teste
    X = data[['Esquerda', 'Direita', 'Cima', 'Baixo']].values
    y = data['Acao'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Criar agentes
    num_agentes = 2
    agentes = []
    for i in range(num_agentes):
        modelo_agente = DecisionTreeClassifier()
        agente = Agente(f'A{i + 1}', modelo_agente, X_train, y_train, global_encoder)
        agentes.append(agente)
    print()

    print('###### Matriz base ##########')
    ambiente.imprimir_matriz_base()
    print('######### Matriz explorada ############')
    ambiente.imprimir(agentes)

    interface = Interface(ambiente, agentes, abordagem_a, abordagem_b, abordagem_c)
    interface.root.mainloop()


main()
