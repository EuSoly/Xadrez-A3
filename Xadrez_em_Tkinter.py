import tkinter as tk
from tkinter import messagebox

#Elizeu Walczuk Ruthes
#Luiz 




class ChessTimer:
    def __init__(self, root, turno_callback, jogo_xadrez_instance):
        self.root = root
        self.turno_callback = turno_callback
        self.jogo_xadrez_instance = jogo_xadrez_instance 
        self.total_time = 0
        self.time1 = 0 
        self.time2 = 0
        self.turn = 1
        self.running = False
        self.after_id = None
        self.jogadas = []

        self.frame = tk.Frame(self.root, bd=2, relief="groove", padx=10, pady=10)
        self.frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.label_tempo = tk.Label(self.frame, text="Tempo da partida (segundos):", font=("Arial", 10, "bold"))
        self.label_tempo.pack(pady=(0,5))

        self.entry_tempo = tk.Entry(self.frame, width=15, justify="center")
        self.entry_tempo.pack(pady=(0,10))
        self.entry_tempo.insert(0, "300")

        self.start_button = tk.Button(self.frame, text="Iniciar Partida", command=self.iniciar_partida,
                                      bg="lime", fg="white", font=("Arial", 10, "bold"), relief="raised", bd=3)
        self.start_button.pack(pady=5, ipadx=10, ipady=5)

        self.reset_button = tk.Button(self.frame, text="Resetar Partida", command=self.resetar_partida,
                                       bg="red", fg="white", font=("Arial", 10, "bold"), relief="raised", bd=3)
        self.reset_button.pack(pady=5, ipadx=10, ipady=5)

        self.label1 = tk.Label(self.frame, text="Brancas: 0s", font=("Arial", 20, "bold"), fg="gray")
        self.label1.pack(pady=15)

        self.label2 = tk.Label(self.frame, text="Pretas: 0s", font=("Arial", 20, "bold"), fg="black")
        self.label2.pack(pady=15)

        self.label_historico = tk.Label(self.frame, text="Histórico de Jogadas:", font=("Arial", 10, "bold"))
        self.label_historico.pack(pady=(10,5))

        self.jogada_listbox = tk.Listbox(self.frame, width=20, height=10, font=("Courier", 10))
        self.jogada_listbox.pack(pady=(0,10))
        self.jogada_listbox.config(relief="sunken", bd=2)
        
        self.pecas_mortas_label = tk.Label(self.frame, text="Peças Capturadas:", font=("Arial", 10, "bold"))
        self.pecas_mortas_label.pack(pady=(10,5))
        self.pecas_mortas_listbox = tk.Listbox(self.frame, width=20, height=10, font=("Courier", 10))
        self.pecas_mortas_listbox.pack(pady=(0,10))
        self.pecas_mortas_listbox.config(relief="sunken", bd=2)

        self.update_labels()

    def iniciar_partida(self):
        """Inicia o timer da partida de xadrez."""
        if self.running:
            messagebox.showwarning("Aviso", "A partida já está em andamento!")
            return

        try:
            self.total_time = int(self.entry_tempo.get())
            if self.total_time <= 0:
                raise ValueError
            
            self.time1 = self.total_time
            self.time2 = self.total_time
            self.turn = 1
            self.jogadas.clear()
            self.jogada_listbox.delete(0, tk.END)
            self.pecas_mortas_listbox.delete(0, tk.END) 
            self.update_labels()
            self.running = True
            self.contar_tempo()
            self.jogo_xadrez_instance.resetar_jogo()
            self.start_button.config(text="Partida em Andamento...", state=tk.DISABLED)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, digite um número inteiro positivo para o tempo da partida.")

    def resetar_partida(self):
        """Reseta o timer e o estado da partida."""
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.running = False
        self.total_time = 0
        self.time1 = 0
        self.time2 = 0
        self.turn = 1
        self.jogadas.clear()
        self.jogada_listbox.delete(0, tk.END)
        self.pecas_mortas_listbox.delete(0, tk.END)
        self.update_labels()
        messagebox.showinfo("Partida Resetada", "A partida foi resetada. Configure o tempo e clique em Iniciar para uma nova partida.")
        self.start_button.config(text="Iniciar Partida", state=tk.NORMAL)
        self.jogo_xadrez_instance.resetar_jogo()

    def contar_tempo(self):
        """Decrementa o tempo do jogador atual e atualiza a interface."""
        if not self.running:
            return

        if self.turn == 1:
            self.time1 -= 1
        else:
            self.time2 -= 1

        self.update_labels()

        if self.time1 <= 0 or self.time2 <= 0:
            self.running = False
            if self.after_id:
                self.root.after_cancel(self.after_id)
                self.after_id = None
            
            vencedor = "Pretas" if self.time1 <= 0 else "Brancas"
            messagebox.showinfo("Fim de Jogo", f"Tempo esgotado! O jogador das {vencedor} venceu por tempo.")
            self.start_button.config(text="Iniciar Partida", state=tk.NORMAL)
            return

        self.after_id = self.root.after(1000, self.contar_tempo)

    def trocar_turno(self):
        """Troca o turno do jogo e reinicia a contagem do tempo para o próximo jogador."""
        if not self.running:
            return

        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        
        self.turn = 2 if self.turn == 1 else 1
        self.update_labels()
        self.contar_tempo()
        
        if self.turno_callback:
            self.turno_callback(self.turn)

    def update_labels(self):
        """Atualiza os rótulos de tempo exibindo o tempo restante e o turno ativo."""
        self.label1.config(text=f"Brancas: {self.time1}s {'←' if self.turn == 1 and self.running else ''}")
        self.label2.config(text=f"Pretas: {self.time2}s {'←' if self.turn == 2 and self.running else ''}")

    def registrar_jogada_ui(self, jogada_texto):
        """Adiciona uma jogada ao listbox de histórico."""
        self.jogadas.append(jogada_texto)
        self.jogada_listbox.insert(tk.END, jogada_texto)
        self.jogada_listbox.see(tk.END)

class JogoXadrez:
    def __init__(self, root):
        self.root = root
        self.root.title("Xadrez com Timer")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)

        self.tamanho_casa = 80
        self.selecionado = None
        self.pecas = {}
        self.estado = {}
        self.turno = "branco"
        self.pecas_mortas = []

        self.highlight_rect_id = None

        self.frame_tabuleiro = tk.Frame(self.root, bd=2, relief="groove")
        self.frame_tabuleiro.pack(side=tk.LEFT, padx=10, pady=10)

        self.canvas = tk.Canvas(self.frame_tabuleiro, width=8*self.tamanho_casa, height=8*self.tamanho_casa, bg="#f0d9b5")
        self.canvas.pack()

        self.criar_tabuleiro()
        self.colocar_pecas()

        self.canvas.bind("<Button-1>", self.clique)

        self.timer = ChessTimer(self.root, self.mudar_turno_por_timer, self)

    def criar_tabuleiro(self):
        """Desenha as casas do tabuleiro de xadrez no canvas."""
        for linha in range(8):
            for coluna in range(8):
                x1 = coluna * self.tamanho_casa
                y1 = linha * self.tamanho_casa
                x2 = x1 + self.tamanho_casa
                y2 = y1 + self.tamanho_casa
                # Cores padrão de xadrez para as casas
                cor = "#f0d9b5" if (linha + coluna) % 2 == 0 else "#b58863"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor, outline="")

    def resetar_jogo(self):
        """Reseta o tabuleiro do jogo para a posição inicial."""
        self.canvas.delete("all")
        self.pecas = {}
        self.estado = {}
        self.selecionado = None
        self.turno = "branco"
        self.highlight_rect_id = None
        self.pecas_mortas = []
        self.criar_tabuleiro()
        self.colocar_pecas()
        self.canvas.bind("<Button-1>", self.clique)
        self.atualizar_pecas_mortas()

    def posicao_para_notacao(self, pos):
        """Converte uma posição (linha, coluna) para notação de xadrez (ex: (0,0) -> 'a8')."""
        linha, coluna = pos
        letra = chr(ord('a') + coluna)
        numero = 8 - linha
        return f"{letra}{numero}"

    def colocar_pecas(self):
        """Coloca as peças de xadrez em suas posições iniciais no tabuleiro."""
        pecas_iniciais = {
            "a1": "♖", "b1": "♘", "c1": "♗", "d1": "♕",
            "e1": "♔", "f1": "♗", "g1": "♘", "h1": "♖",
            "a2": "♙", "b2": "♙", "c2": "♙", "d2": "♙",
            "e2": "♙", "f2": "♙", "g2": "♙", "h2": "♙",

            "a8": "♜", "b8": "♞", "c8": "♝", "d8": "♛",
            "e8": "♚", "f8": "♝", "g8": "♞", "h8": "♜",
            "a7": "♟", "b7": "♟", "c7": "♟", "d7": "♟",
            "e7": "♟", "f7": "♟", "g7": "♟", "h7": "♟",
        }

        for pos_notacao, peca_simbolo in pecas_iniciais.items():
            col = ord(pos_notacao[0]) - ord('a')
            row = 8 - int(pos_notacao[1])
            self.adicionar_peca(row, col, peca_simbolo)

    def adicionar_peca(self, linha, coluna, simbolo):
        """Adiciona uma peça no canvas na posição especificada."""
        x = coluna * self.tamanho_casa + self.tamanho_casa // 2
        y = linha * self.tamanho_casa + self.tamanho_casa // 2
        id_texto = self.canvas.create_text(x, y, text=simbolo, font=("Arial", 40), fill="black")
        self.pecas[(linha, coluna)] = id_texto
        self.estado[(linha, coluna)] = simbolo

    def clique(self, evento):
        """Lida com o evento de clique do mouse no tabuleiro."""
        col = evento.x // self.tamanho_casa
        row = evento.y // self.tamanho_casa
        pos = (row, col)
        
        if not self.timer.running:
            messagebox.showwarning("Aviso", "Por favor, inicie a partida clicando em 'Iniciar Partida' antes de mover as peças.")
            return
    
        if self.selecionado:
            origem = self.selecionado
            peca = self.estado.get(origem)
            
            if self.highlight_rect_id:
                self.canvas.delete(self.highlight_rect_id)
                self.highlight_rect_id = None

            movimentos = self.movimentos_validos(origem, peca)

            if pos in movimentos:
                self.executar_jogada(origem, pos, peca)
                self.turno = "preto" if self.turno == "branco" else "branco"
                self.timer.trocar_turno()
                
            self.selecionado = None
        else:
            if pos in self.estado:
                peca = self.estado[pos]
                if (self.turno == "branco" and self.eh_peca_branca(peca)) or \
                   (self.turno == "preto" and self.eh_peca_preta(peca)):
                    self.selecionado = pos
                    x1 = col * self.tamanho_casa
                    y1 = row * self.tamanho_casa
                    x2 = x1 + self.tamanho_casa
                    y2 = y1 + self.tamanho_casa
                    self.highlight_rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, outline="green", width=4)
                else:
                    messagebox.showwarning("Aviso de Turno", f"É o turno das {self.turno.capitalize()}. Selecione uma peça da sua cor.")
            else:
                pass


    def executar_jogada(self, origem, destino, simbolo_peca):
        """Executa o movimento de uma peça no tabuleiro."""
        self.canvas.delete(self.pecas.pop(origem))
        self.estado.pop(origem)

        if destino in self.pecas:
            peca_capturada = self.estado[destino]
            self.canvas.delete(self.pecas[destino])
            self.pecas.pop(destino)
            self.estado.pop(destino)
            self.pecas_mortas.append(peca_capturada)
            self.atualizar_pecas_mortas()

        self.adicionar_peca(destino[0], destino[1], simbolo_peca)

        # Registra jogada no histórico do timer
        origem_not = self.posicao_para_notacao(origem)
        destino_not = self.posicao_para_notacao(destino)
        jogada_texto = f"{self.turno.capitalize()}: {simbolo_peca} de {origem_not} para {destino_not}"
        self.timer.registrar_jogada_ui(jogada_texto)

        self.verificar_rei_morto()


    def eh_peca_branca(self, peca):
        """Verifica se o símbolo da peça corresponde a uma peça branca."""
        return peca in "♙♖♘♗♕♔"

    def eh_peca_preta(self, peca):
        """Verifica se o símbolo da peça corresponde a uma peça preta."""
        return peca in "♟♜♞♝♛♚"

    def movimentos_validos(self, origem, peca):
        """
        Retorna uma lista de posições válidas para uma peça específica.
        NOTA: Não verifica xeque, xeque-mate, roque, en passant ou promoção.
        """
        row, col = origem
        movimentos = []
        cor_peca = "branco" if self.eh_peca_branca(peca) else "preto"

        def adicionar_movimento_se_valido(r, c):
            if 0 <= r < 8 and 0 <= c < 8:
                if (r,c) not in self.estado:
                    movimentos.append((r,c))
                    return True
                else:
                    peca_alvo = self.estado[(r,c)]
                    if (cor_peca == "branco" and self.eh_peca_preta(peca_alvo)) or \
                       (cor_peca == "preto" and self.eh_peca_branca(peca_alvo)):
                        movimentos.append((r,c))
                    return False
            return False

        if peca == "♙":
            frente = (row - 1, col)
            if frente not in self.estado and 0 <= frente[0] < 8:
                movimentos.append(frente)
                if row == 6:
                    dois_frentes = (row - 2, col)
                    if dois_frentes not in self.estado:
                        movimentos.append(dois_frentes)
            for dc in [-1, 1]:
                ataque = (row - 1, col + dc)
                if 0 <= ataque[1] < 8 and ataque in self.estado and self.eh_peca_preta(self.estado[ataque]):
                    movimentos.append(ataque)

        elif peca == "♟":
            frente = (row + 1, col)
            if frente not in self.estado and 0 <= frente[0] < 8:
                movimentos.append(frente)
                if row == 1:
                    dois_frentes = (row + 2, col)
                    if dois_frentes not in self.estado:
                        movimentos.append(dois_frentes)
            for dc in [-1, 1]:
                ataque = (row + 1, col + dc)
                if 0 <= ataque[1] < 8 and ataque in self.estado and self.eh_peca_branca(self.estado[ataque]):
                    movimentos.append(ataque)

        elif peca in ("♖", "♜"):
            direcoes = [(-1,0),(1,0),(0,-1),(0,1)]
            for dr, dc in direcoes:
                r, c = row+dr, col+dc
                while adicionar_movimento_se_valido(r, c):
                    r += dr
                    c += dc
            
        elif peca in ("♘", "♞"):
            possibilidades = [
                (row+2,col+1),(row+2,col-1),(row-2,col+1),(row-2,col-1),
                (row+1,col+2),(row+1,col-2),(row-1,col+2),(row-1,col-2)
            ]
            for r,c in possibilidades:
                adicionar_movimento_se_valido(r,c)

        elif peca in ("♗", "♝"):
            direcoes = [(-1,-1),(-1,1),(1,-1),(1,1)]
            for dr, dc in direcoes:
                r, c = row+dr, col+dc
                while adicionar_movimento_se_valido(r, c):
                    r += dr
                    c += dc

        elif peca in ("♕", "♛"):
            direcoes = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
            for dr, dc in direcoes:
                r, c = row+dr, col+dc
                while adicionar_movimento_se_valido(r, c):
                    r += dr
                    c += dc

        elif peca in ("♔", "♚"):
            possibilidades = [
                (row-1,col-1),(row-1,col),(row-1,col+1),
                (row,col-1),                 (row,col+1),
                (row+1,col-1),(row+1,col),(row+1,col+1)
            ]
            for r,c in possibilidades:
                adicionar_movimento_se_valido(r,c)

        return movimentos

    def verificar_rei_morto(self):
        """Verifica se algum rei foi capturado e finaliza o jogo."""
        rei_branco_presente = False
        rei_preto_presente = False

        for peca_simbolo in self.estado.values():
            if peca_simbolo == "♔":
                rei_branco_presente = True
            elif peca_simbolo == "♚":
                rei_preto_presente = True

        if not rei_branco_presente:
            self.finalizar_jogo("Pretas")
            return True
        elif not rei_preto_presente:
            self.finalizar_jogo("Brancas")
            return True
        return False

    def finalizar_jogo(self, vencedor_cor):
        """Finaliza o jogo e declara o vencedor."""
        self.timer.running = False
        if self.timer.after_id:
            self.root.after_cancel(self.timer.after_id)
            self.timer.after_id = None
        messagebox.showinfo("Fim de Jogo", f"O rei das {'Brancas' if vencedor_cor == 'Brancas' else 'Pretas'} foi capturado!\nO jogador das {vencedor_cor} venceu a partida!")
        self.canvas.unbind("<Button-1>")
        
        if self.highlight_rect_id:
            self.canvas.delete(self.highlight_rect_id)
            self.highlight_rect_id = None
        self.timer.start_button.config(text="Iniciar Partida", state=tk.NORMAL)


    def mudar_turno_por_timer(self, turno_num):
        """Sincroniza o turno do jogo com o timer."""
        self.turno = "branco" if turno_num == 1 else "preto"
        
    def atualizar_pecas_mortas(self):
        """Atualiza a listbox de peças capturadas."""
        self.timer.pecas_mortas_listbox.delete(0, tk.END)
        brancas_capturadas = [p for p in self.pecas_mortas if self.eh_peca_branca(p)]
        pretas_capturadas = [p for p in self.pecas_mortas if self.eh_peca_preta(p)]
        self.timer.pecas_mortas_listbox.insert(tk.END, "Brancas: " + " ".join(brancas_capturadas))
        self.timer.pecas_mortas_listbox.insert(tk.END, "Pretas: " + " ".join(pretas_capturadas))

if __name__ == "__main__":
    root = tk.Tk()
    jogo = JogoXadrez(root)
    root.mainloop()
