import random

class Ambiente:
    def __init__(self, proporcao):
        self.tamanho = 10
        self.total_tesouros = 0
        self.tesouros_achados = 0
        self.proporcao = proporcao
        self.matriz_base = self.inicializar()
        self.matriz_compartilhada = self.inicializar_matriz_compartilhada()

    def inicializar_matriz_compartilhada(self):
        return [['N'] * self.tamanho for _ in range(self.tamanho)]

    def inicializar(self):
        matriz = [['L'] * self.tamanho for _ in range(self.tamanho)]
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                r = random.random()
                if r < self.proporcao['B']:
                    matriz[i][j] = 'B'
                elif r < self.proporcao['B'] + self.proporcao['T']:
                    matriz[i][j] = 'T'
                    self.total_tesouros += 1
        return matriz

    def imprimir(self, agentes):
        for agente in agentes:
            valor_agente = self.matriz_compartilhada[agente.posicao[0]][agente.posicao[1]]
            self.matriz_compartilhada[agente.posicao[0]][agente.posicao[1]] = agente.nome

        for linha in self.matriz_compartilhada:
            print("    ".join(linha))

        for agente in agentes:
            self.matriz_compartilhada[agente.posicao[0]][agente.posicao[1]] = valor_agente
        print()

    def imprimir_matriz_base(self):
        for linha in self.matriz_base:
            print("    ".join(linha))
        print()

    def partilhar_informacao(self, linha, coluna, info):
        self.matriz_compartilhada[linha][coluna] = info

    def inserir_f(self):
        linha = random.randint(0, 9)
        coluna = random.randint(0, 9)

        self.matriz_base[linha][coluna] = 'F'

    def set_pos_agente_to_l(self, linha, coluna):
        if(self.matriz_base[linha][coluna] == 'F'):
            new_line = random.randint(0, 9)
            new_column = random.randint(0, 9)

            while(new_line == linha and new_column == coluna):
                new_line = random.randint(0, 9)
                new_column = random.randint(0, 9)

            self.matriz_base[new_line][new_column] = 'F'

        self.matriz_base[linha][coluna] = 'L'
        self.partilhar_informacao(linha, coluna, 'L')
