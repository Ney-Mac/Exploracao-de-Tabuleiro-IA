import random


class Agente:
    def __init__(self, nome, modelo, dados_treino, rotulos_treino, encoder):
        self.nome = nome
        self.modelo = modelo
        self.encoder = encoder
        self.vivo = True
        self.flag = False
        self.posicao = self.set_posicao()
        self.treinar(dados_treino, rotulos_treino)
        self.qt_tesouros = 0

    def add_tesouro(self, ambiente):
        self.qt_tesouros += 1
        ambiente.tesouros_achados += 1

    def usar_tesouro(self):
        self.qt_tesouros -= 1

    @staticmethod
    def set_posicao():
        linha = random.randint(0, 9)
        coluna = random.randint(0, 9)
        return linha, coluna

    def treinar(self, dados_treino, rotulos_treino):
        self.modelo.fit(dados_treino, rotulos_treino)
        print('Agente ', self.nome, ' Treinado')

    def testar(self, X_test):
        return self.modelo.predict(X_test)

    def predizer(self, dados):
        dados_encode = self.encoder.fit_transform(dados)
        return self.modelo.predict(dados_encode.reshape(1, -1))

    def get_celulas_vizinhas(self, ambiente):
        linha, coluna = self.posicao

        cima = ambiente.matriz_compartilhada[linha - 1][coluna] if (linha - 1 >= 0) else '-'
        baixo = ambiente.matriz_compartilhada[linha + 1][coluna] if (linha + 1 < ambiente.tamanho) else '-'
        esquerda = ambiente.matriz_compartilhada[linha][coluna - 1] if (coluna - 1 >= 0) else '-'
        direita = ambiente.matriz_compartilhada[linha][coluna + 1] if (coluna + 1 < ambiente.tamanho) else '-'

        return [esquerda, direita, cima, baixo]

    def mover(self, ambiente):
        linha, coluna = self.posicao
        celulas_vizinhas = self.get_celulas_vizinhas(ambiente)

        movimento = self.predizer(celulas_vizinhas)[0]

        nova_posicao = (
            (linha + 1, coluna) if movimento == 'Baixo' else (
                (linha - 1, coluna) if movimento == 'Cima' else (
                    (linha, coluna + 1) if movimento == 'Direita' else
                    (linha, coluna - 1)
                )
            )
        )
        self.posicao = nova_posicao

        print(f'\nAgente {self.nome} moveu-se para {movimento}')
        self.interagir(ambiente)

    def interagir(self, ambiente):
        linha, coluna = self.posicao
        celula_atual = ambiente.matriz_base[linha][coluna]

        print(f'Agente {self.nome} encontrou {celula_atual}')

        if celula_atual == 'B':
            if self.qt_tesouros == 0:
                print(f'Agente {self.nome} morreu')
                self.vivo = False
            else:
                self.usar_tesouro()
        elif celula_atual == 'T':
            self.add_tesouro(ambiente)
        elif celula_atual == 'F':
            self.flag = True

        self.enviar_informacao(ambiente)

    def enviar_informacao(self, ambiente):
        linha, coluna = self.posicao
        info = ambiente.matriz_base[linha][coluna]
        ambiente.partilhar_informacao(linha, coluna, info)
