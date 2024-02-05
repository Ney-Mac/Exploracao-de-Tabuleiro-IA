import tkinter as tk


class Interface:
    def __init__(self, ambiente, agentes, abordagem_a, abordagem_b, abordagem_c):
        self.ambiente = ambiente
        self.agentes = agentes

        self.abordagem_a = abordagem_a
        self.abordagem_b = abordagem_b
        self.abordagem_c = abordagem_c

        self.root = tk.Tk()
        self.root.title("Ambiente")

        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        self.desenhar_tabuleiro()

        abordagem_a_button = tk.Button(self.root, text="Abordagem A", command=self.abordagem_A)
        abordagem_a_button.pack(side=tk.LEFT)

        abordagem_b_button = tk.Button(self.root, text="Abordagem B", command=self.abordagem_B)
        abordagem_b_button.pack(side=tk.LEFT)

        abordagem_c_button = tk.Button(self.root, text="Abordagem C", command=self.abordagem_C)
        abordagem_c_button.pack(side=tk.LEFT)

    def desenhar_tabuleiro(self):
        for linha in range(self.ambiente.tamanho):
            for coluna in range(self.ambiente.tamanho):
                x0, y0 = coluna * 40, linha * 40
                x1, y1 = x0 + 40, y0 + 40
                cor = "white"
                if self.ambiente.matriz_base[linha][coluna] == 'B':
                    cor = "brown"
                elif self.ambiente.matriz_base[linha][coluna] == 'T':
                    cor = "yellow"
                elif self.ambiente.matriz_base[linha][coluna] == 'F':
                    cor = "green"

                self.canvas.create_rectangle(x0, y0, x1, y1, fill=cor)

        for agente in self.agentes:
            linha, coluna = agente.posicao
            x0, y0 = coluna * 40, linha * 40
            x1, y1 = x0 + 40, y0 + 40
            self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=agente.nome)

        self.root.update()

    def atualizar_tabuleiro(self):
        self.desenhar_tabuleiro()
    #
    # def executar_simulacao(self):
    #     while self.ambiente.tesouros_achados <= self.ambiente.total_tesouros * 0.5 and len(self.agentes) > 0:
    #         for agente in self.agentes[:]:
    #             if agente.vivo:
    #                 agente.mover(self.ambiente)
    #                 self.atualizar_tabuleiro()
    #                 time.sleep(0.5)
    #             else:
    #                 self.agentes.remove(agente)
    #
    #     print(f'Total de tesouros iniciais: {self.ambiente.total_tesouros}')
    #     print(f'Total de tesouros encontrados: {self.ambiente.tesouros_achados}')

    def abordagem_A(self):
        self.abordagem_a(self.ambiente, self.agentes, self.atualizar_tabuleiro)
    #
    def abordagem_B(self):
        self.abordagem_b(self.ambiente, self.agentes, self.atualizar_tabuleiro)
    #
    def abordagem_C(self):
        self.abordagem_c(self.ambiente, self.agentes, self.atualizar_tabuleiro)