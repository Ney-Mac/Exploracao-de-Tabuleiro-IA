import random
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from Ambiente import Ambiente
from Agente import Agente

def abordagem_A(ambiente, agentes):
    for agente in agentes:
        ambiente.set_pos_agente_to_l(agente.posicao[0], agente.posicao[1])

    print('###### Matriz base ##########')
    ambiente.imprimir_matriz_base()

    print('######### Matriz explorada ############')
    ambiente.imprimir(agentes)

    i = 0
    while ambiente.tesouros_achados <= ambiente.total_tesouros * 0.5:
        for agente in agentes:
            if agente.vivo:
                agente.mover(ambiente)
        ambiente.imprimir(agentes)
        i += 1
        print(i)
        if i == 10: break

def main():
    data = pd.read_csv('./dados_treino/dataset.csv', delimiter=',')
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
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=8)

    # Criar agentes
    num_agentes = 2
    agentes = []
    for i in range(num_agentes):
        modelo_agente = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=2000)
        agente = Agente(f'A{i + 1}', modelo_agente, X_train, y_train, global_encoder)
        agentes.append(agente)
    print()

    abordagem_A(ambiente, agentes)

main()