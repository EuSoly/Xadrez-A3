import tkinter as tk
from tkinter import messagebox

class ChessTimer:
    def __init__(self, root, turno_callback):
        self.root = root
        self.turno_callback = turno_callback  # Função para avisar mudança de turno
        self.total_time = 0
        self.time1 = 0
        self.time2 = 0
        self.turn = 1  # 1 para jogador 1 (branco), 2 para jogador 2 (preto)
        self.running = False
        self.after_id = None
        self.jogadas = []

        # Widgets
        self.frame = tk.Frame(self.root)
        self.frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.label_tempo = tk.Label(self.frame, text="Tempo da partida (segundos):")
        self.label_tempo.pack()

        self.entry_tempo = tk.Entry(self.frame)
        self.entry_tempo.pack()

        self.start_button = tk.Button(self.frame, text="Iniciar", command=self.iniciar_partida)
        self.start_button.pack(pady=5)

        self.label1 = tk.Label(self.frame, text="Brancas: 0s", font=("Arial", 16))
        self.label1.pack()

        self.label2 = tk.Label(self.frame, text="Pretas: 0s", font=("Arial", 16))
        self.label2.pack()


        self.registrar_button = tk.Button(self.frame, text="Historico de Jogadas", command=self.registrar_jogada)
        self.registrar_button.pack()

        self.jogada_listbox = tk.Listbox(self.frame, width=40)
        self.jogada_listbox.pack(pady=10)

    def iniciar_partida(self):
        try:
            self.total_time = int(self.entry_tempo.get())
            if self.total_time <= 0:
                raise ValueError
            self.time1 = self.total_time
            self.time2 = self.total_time
            self.turn = 1
            self.jogadas.clear()
            self.jogada_listbox.delete(0, tk.END)
            self.update_labels()
            self.running = True
            self.contar_tempo()
        except ValueError:
            messagebox.showerror("Erro", "Digite um número inteiro positivo para o tempo.")

    def contar_tempo(self):
        if not self.running:
            return

        if self.turn == 1:
            self.time1 -= 1
        else:
            self.time2 -= 1

        self.update_labels()

        if self.time1 <= 0 or self.time2 <= 0:
            self.running = False
            vencedor = "Jogador 2" if self.time1 <= 0 else "Jogador 1"
            messagebox.showinfo("Fim de Jogo", f"Tempo esgotado! {vencedor} venceu.")
            return

        self.after_id = self.root.after(1000, self.contar_tempo)
    def trocar_turno_automatica(self):
        # Alterna o turno no timer também
        self.turn = 2 if self.turn == 1 else 1
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self.contar_tempo()

    def update_labels(self):
        self.label1.config(text=f"Brancas: {self.time1}s {'←' if self.turn == 1 else ''}")
        self.label2.config(text=f"Pretas: {self.time2}s {'←' if self.turn == 2 else ''}")

    def registrar_jogada(self):
        if not self.running:
            return

        jogada = self.entry_jogada.get().strip()
        if jogada:
            jogador = f"Jogador {self.turn}"
            texto = f"{jogador}: {jogada}"
            self.jogadas.append(texto)
            self.jogada_listbox.insert(tk.END, texto)
            self.entry_jogada.delete(0, tk.END)
            self.trocar_turno()
        else:
            messagebox.showwarning("Aviso", "Digite a jogada antes de registrar.")

    def trocar_turno(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self.turn = 2 if self.turn == 1 else 1
        self.update_labels()
        self.contar_tempo()
        if self.turno_callback:
            self.turno_callback(self.turn)  # Notifica mudança de turno

    def troca_turno_automatica(self):
        # Troca de turno feita pelo jogo (exemplo: após movimento)
        self.trocar_turno()


class JogoXadrez:
    def __init__(self, root):
        self.root = root
        self.root.title("Xadrez com Timer")

        self.tamanho_casa = 80
        self.selecionado = None
        self.pecas = {}
        self.estado = {}
        self.turno = "branco"  # "branco" ou "preto"

        # Frame para tabuleiro e timer lado a lado
        self.frame_tabuleiro = tk.Frame(self.root)
        self.frame_tabuleiro.pack(side=tk.LEFT)

        self.canvas = tk.Canvas(self.frame_tabuleiro, width=8*self.tamanho_casa, height=8*self.tamanho_casa)
        self.canvas.pack()

        self.criar_tabuleiro()
        self.colocar_pecas()

        self.canvas.bind("<Button-1>", self.clique)

        # Cria timer e passa callback para mudar turno
        self.timer = ChessTimer(self.root, self.mudar_turno_por_timer)

    def criar_tabuleiro(self):
        for linha in range(8):
            for coluna in range(8):
                x1 = coluna * self.tamanho_casa
                y1 = linha * self.tamanho_casa
                x2 = x1 + self.tamanho_casa
                y2 = y1 + self.tamanho_casa
                cor = "white" if (linha + coluna) % 2 == 0 else "gray"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor)
                
    def posicao_para_notacao(self, pos):
        linha, coluna = pos
        letra = chr(ord('a') + coluna)
        numero = 8 - linha
        return f"{letra}{numero}"

    def colocar_pecas(self):
        pecas_iniciais = {
            # Brancas
            "a1": "♖", "b1": "♘", "c1": "♗", "d1": "♕",
            "e1": "♔", "f1": "♗", "g1": "♘", "h1": "♖",
            "a2": "♙", "b2": "♙", "c2": "♙", "d2": "♙",
            "e2": "♙", "f2": "♙", "g2": "♙", "h2": "♙",

            # Pretas
            "a8": "♜", "b8": "♞", "c8": "♝", "d8": "♛",
            "e8": "♚", "f8": "♝", "g8": "♞", "h8": "♜",
            "a7": "♟", "b7": "♟", "c7": "♟", "d7": "♟",
            "e7": "♟", "f7": "♟", "g7": "♟", "h7": "♟",
        }

        for pos, peca in pecas_iniciais.items():
            col = ord(pos[0]) - ord('a')
            row = 8 - int(pos[1])
            self.adicionar_peca(row, col, peca)

    def adicionar_peca(self, linha, coluna, simbolo):
        x = coluna * self.tamanho_casa + self.tamanho_casa // 2
        y = linha * self.tamanho_casa + self.tamanho_casa // 2
        id_texto = self.canvas.create_text(x, y, text=simbolo, font=("Arial", 36))
        self.pecas[(linha, coluna)] = id_texto
        self.estado[(linha, coluna)] = simbolo

    def clique(self, evento):
        col = evento.x // self.tamanho_casa
        row = evento.y // self.tamanho_casa
        pos = (row, col)

        if self.selecionado:
            origem = self.selecionado
            peca = self.estado.get(origem)
            movimentos = self.movimentos_validos(origem, peca)

            if pos in movimentos:
                # Remove a peça da posição original
                simbolo = self.estado.pop(origem)
                id_peca = self.pecas.pop(origem)
                self.canvas.delete(id_peca)

                # Se já tiver peça na posição destino, remove (captura)
                if pos in self.pecas:
                    self.canvas.delete(self.pecas[pos])
                    self.pecas.pop(pos)
                    self.estado.pop(pos)

                # Adiciona peça na nova posição
                self.adicionar_peca(pos[0], pos[1], simbolo)

                # Registra jogada automaticamente no timer
                origem_not = self.posicao_para_notacao(origem)
                destino_not = self.posicao_para_notacao(pos)
                jogada_texto = f"{origem_not} -> {destino_not}"

                self.timer.jogadas.append(jogada_texto)
                self.timer.jogada_listbox.insert(tk.END, jogada_texto)
                self.timer.entry_jogada.delete(0, tk.END)

                # Troca turno no jogo e no timer
                self.turno = "preto" if self.turno == "branco" else "branco"
                self.timer.trocar_turno_automatica()

            self.selecionado = None
        else:
            if pos in self.estado:
                peca = self.estado[pos]
                if (self.turno == "branco" and peca in "♙♖♘♗♕♔") or \
                (self.turno == "preto" and peca in "♟♜♞♝♛♚"):
                    self.selecionado = pos

    def eh_peca_branca(self, peca):
        return peca in "♙♖♘♗♕♔"

    def eh_peca_preta(self, peca):
        return peca in "♟♜♞♝♛♚"

    def movimentos_validos(self, origem, peca):
        row, col = origem
        movimentos = []

        if peca == "♙":  # Peão branco
            frente = (row - 1, col)
            if frente not in self.estado and 0 <= frente[0] < 8:
                movimentos.append(frente)
                if row == 6:
                    dois_frentes = (row - 2, col)
                    if dois_frentes not in self.estado:
                        movimentos.append(dois_frentes)
            for dc in [-1, 1]:
                ataque = (row - 1, col + dc)
                if ataque in self.estado and self.eh_peca_preta(self.estado[ataque]):
                    movimentos.append(ataque)

        elif peca == "♟":  # Peão preto
            frente = (row + 1, col)
            if frente not in self.estado and 0 <= frente[0] < 8:
                movimentos.append(frente)
                if row == 1:
                    dois_frentes = (row + 2, col)
                    if dois_frentes not in self.estado:
                        movimentos.append(dois_frentes)
            for dc in [-1, 1]:
                ataque = (row + 1, col + dc)
                if ataque in self.estado and self.eh_peca_branca(self.estado[ataque]):
                    movimentos.append(ataque)

        elif peca in ("♖", "♜"):  # Torres
            direcoes = [(-1,0),(1,0),(0,-1),(0,1)]
            for dr, dc in direcoes:
                r, c = row+dr, col+dc
                while 0 <= r < 8 and 0 <= c < 8:
                    if (r,c) not in self.estado:
                        movimentos.append((r,c))
                    else:
                        if (self.turno == "branco" and self.eh_peca_preta(self.estado[(r,c)])) or \
                           (self.turno == "preto" and self.eh_peca_branca(self.estado[(r,c)])):
                            movimentos.append((r,c))
                        break
                    r += dr
                    c += dc

        elif peca in ("♘", "♞"):  # Cavalos
            possibilidades = [
                (row+2,col+1),(row+2,col-1),(row-2,col+1),(row-2,col-1),
                (row+1,col+2),(row+1,col-2),(row-1,col+2),(row-1,col-2)
            ]
            for r,c in possibilidades:
                if 0 <= r < 8 and 0 <= c < 8:
                    if (r,c) not in self.estado or \
                        (self.turno == "branco" and self.eh_peca_preta(self.estado.get((r,c), None))) or \
                        (self.turno == "preto" and self.eh_peca_branca(self.estado.get((r,c), None))):
                        movimentos.append((r,c))

        elif peca in ("♗", "♝"):  # Bispos
            direcoes = [(-1,-1),(-1,1),(1,-1),(1,1)]
            for dr, dc in direcoes:
                r, c = row+dr, col+dc
                while 0 <= r < 8 and 0 <= c < 8:
                    if (r,c) not in self.estado:
                        movimentos.append((r,c))
                    else:
                        if (self.turno == "branco" and self.eh_peca_preta(self.estado[(r,c)])) or \
                           (self.turno == "preto" and self.eh_peca_branca(self.estado[(r,c)])):
                            movimentos.append((r,c))
                        break
                    r += dr
                    c += dc

        elif peca in ("♕", "♛"):  # Rainha
            # Combina movimentos da torre e bispo
            direcoes = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
            for dr, dc in direcoes:
                r, c = row+dr, col+dc
                while 0 <= r < 8 and 0 <= c < 8:
                    if (r,c) not in self.estado:
                        movimentos.append((r,c))
                    else:
                        if (self.turno == "branco" and self.eh_peca_preta(self.estado[(r,c)])) or \
                           (self.turno == "preto" and self.eh_peca_branca(self.estado[(r,c)])):
                            movimentos.append((r,c))
                        break
                    r += dr
                    c += dc

        elif peca in ("♔", "♚"):  # Rei
            possibilidades = [
                (row-1,col-1),(row-1,col),(row-1,col+1),
                (row,col-1),           (row,col+1),
                (row+1,col-1),(row+1,col),(row+1,col+1)
            ]
            for r,c in possibilidades:
                if 0 <= r < 8 and 0 <= c < 8:
                    if (r,c) not in self.estado or \
                        (self.turno == "branco" and self.eh_peca_preta(self.estado.get((r,c), None))) or \
                        (self.turno == "preto" and self.eh_peca_branca(self.estado.get((r,c), None))):
                        movimentos.append((r,c))

        return movimentos

    def mudar_turno_por_timer(self, turno_num):
        # Método chamado pelo timer para mudar o turno do jogo
        self.turno = "branco" if turno_num == 1 else "preto"


if __name__ == "__main__":
    root = tk.Tk()
    jogo = JogoXadrez(root)
    root.mainloop()
