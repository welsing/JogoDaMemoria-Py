import tkinter as tk
from tkinter import font, messagebox
from logica import LogicaJogo, BancoDeDados, Jogador
import time


class InterfaceJogo:
    """Classe responsável pela interface do Jogo de Memória"""

    ESTILOS = {
        "bg_primario": "#1c1c1c",
        "bg_secundario": "#4a8db7",
        "bg_erro": "#d9534f",
        "fg_branco": "white",
        "fg_primario": "#ffcc00",
        "fonte_titulo": ("Helvetica", 24, "bold"),
        "fonte_media": ("Helvetica", 16, "bold"),
        "fonte_padrao": ("Helvetica", 12, "bold"),
        "fonte_pequena": ("Helvetica", 10, "italic"),
    }

    CORES = {
        1: "#FF0000",  # Vermelho
        2: "#0000FF",  # Azul
        3: "#00FF00",  # Verde
        4: "#FFFF00",  # Amarelo
        5: "#FF00FF",  # Magenta
        6: "#00FFFF",  # Ciano
        7: "#800000",  # Marrom escuro
        8: "#808000",  # Verde oliva
        9: "#800080",  # Roxo
        10: "#008080",  # Azul petróleo
        11: "#FFA500",  # Laranja
        12: "#A52A2A",  # Marrom
        13: "#8B4513",  # Marrom sela
        14: "#2E8B57",  # Verde marinho
        15: "#000080",  # Azul marinho
        16: "#FFD700",  # Ouro
        17: "#DC143C",  # Carmesim
        18: "#696969",  # Cinza escuro
    }


    def __init__(self, janela):
        self.janela = janela
        self.db = BancoDeDados()
        self.jogador = None
        self.logica_jogo = None
        self.tempo_inicio = None
        self.primeiro_clique = None
        self.botao_primeiro_clique = None
        self.tabuleiro = {}
        self.configurar_janela()
        self.criar_tela_entrada()


    def configurar_janela(self):
        """Configura as propriedades da janela principal"""
        self.janela.title("Jogo de Memória")
        self.janela.geometry("650x700")
        self.janela.configure(bg=self.ESTILOS["bg_primario"])
        self.janela.resizable(False, False)


    def criar_tela_entrada(self):
        """Cria a tela de entrada onde o jogador insere seu nome"""
        self.tela_entrada = tk.Frame(self.janela, bg=self.ESTILOS["bg_primario"])

        label_nome = tk.Label(self.tela_entrada, text="Digite seu nome:", font=self.ESTILOS["fonte_media"], fg=self.ESTILOS["fg_branco"], bg=self.ESTILOS["bg_primario"])
        self.entrada_nome = tk.Entry(self.tela_entrada, font=("Helvetica", 12), width=20, justify="center", bg="#1e3d59", fg=self.ESTILOS["fg_branco"])
        botao_confirmar = tk.Button(self.tela_entrada, text="Confirmar", font=self.ESTILOS["fonte_padrao"], command=self.confirmar_nome, bg=self.ESTILOS["bg_secundario"], fg=self.ESTILOS["fg_branco"])

        label_nome.pack(pady=(200, 0))
        self.entrada_nome.pack(pady=5)
        botao_confirmar.pack(pady=5)
        self.tela_entrada.pack()

        label_projeto2 = tk.Label(self.tela_entrada, text="by: Gabriel, Leticia e Bernardo", font=self.ESTILOS["fonte_pequena"], fg="#808080", bg=self.ESTILOS["bg_primario"])
        label_projeto2.pack(side="bottom", pady=(300, 20))


    def confirmar_nome(self):
        """Confirma o nome do jogador e mostra a tela inicial"""
        nome = nome = self.entrada_nome.get().strip().capitalize()
        if nome:
            self.carregar_jogador(nome)
            self.tela_entrada.pack_forget()
            self.criar_tela_inicial()


    def carregar_jogador(self, nome):
        """Carrega ou cria o jogador usando a classe Jogador"""
        self.jogador = Jogador(nome, self.db)


    def criar_tela_inicial(self):
        """Cria a tela inicial com saudação e botões de dificuldade"""
        self.tela_inicial = tk.Frame(self.janela, bg=self.ESTILOS["bg_primario"])
        self.tela_inicial.pack(expand=True)

        label_titulo = tk.Label(self.tela_inicial, text="JOGO DA\nMEMÓRIA", font=self.ESTILOS["fonte_titulo"], fg=self.ESTILOS["fg_primario"], bg=self.ESTILOS["bg_primario"])
        label_titulo.pack(pady=(20, 10))

        label_saudacao = tk.Label(self.tela_inicial, text=f"Bem-vindo(a), {self.jogador.nome}!", font=("Helvetica", 14, "bold"), fg=self.ESTILOS["fg_branco"], bg=self.ESTILOS["bg_primario"])
        label_saudacao.pack(pady=10)

        label_vitorias = tk.Label(self.tela_inicial, text=f"Vitórias: {self.jogador.vitorias}", font=self.ESTILOS["fonte_padrao"], fg=self.ESTILOS["fg_branco"], bg=self.ESTILOS["bg_primario"])
        label_vitorias.pack(anchor="ne", padx=10, pady=10)

        botoes_frame = tk.Frame(self.tela_inicial, bg=self.ESTILOS["bg_primario"])
        botao_facil = tk.Button(botoes_frame, text="Fácil", font=self.ESTILOS["fonte_padrao"], command=lambda: self.iniciar_jogo(4, 15), bg=self.ESTILOS["bg_secundario"], fg=self.ESTILOS["fg_branco"])
        botao_medio = tk.Button(botoes_frame, text="Médio", font=self.ESTILOS["fonte_padrao"], command=lambda: self.iniciar_jogo(5, 25), bg=self.ESTILOS["bg_secundario"], fg=self.ESTILOS["fg_branco"])
        botao_dificil = tk.Button(botoes_frame, text="Difícil", font=self.ESTILOS["fonte_padrao"], command=lambda: self.iniciar_jogo(6, 40), bg=self.ESTILOS["bg_secundario"], fg=self.ESTILOS["fg_branco"])

        botao_facil.pack(side="left", padx=5)
        botao_medio.pack(side="left", padx=5)
        botao_dificil.pack(side="left", padx=5)
        botoes_frame.pack(pady=20)

        botao_sair = tk.Button(self.tela_inicial, text="Sair", font=self.ESTILOS["fonte_padrao"], command=self.janela.quit, bg=self.ESTILOS["bg_erro"], fg=self.ESTILOS["fg_branco"])
        botao_sair.pack(pady=20)

        label_projeto = tk.Label(self.tela_inicial, text="projeto final comp2", font=self.ESTILOS["fonte_pequena"], fg="#808080", bg=self.ESTILOS["bg_primario"])
        label_projeto.pack(side="bottom", pady=(0, 20))


    def criar_tela_jogo(self):
        """Cria a tela do jogo"""
        self.tela_inicial.pack_forget()
        self.tela_jogo_frame = tk.Frame(self.janela, bg=self.ESTILOS["bg_primario"])
        self.tela_jogo_frame.pack(expand=True, fill="both")

        # Contador de tempo no topo
        self.label_tempo = tk.Label(
            self.tela_jogo_frame,
            text="Tempo: 0s",
            font=self.ESTILOS["fonte_padrao"],
            fg=self.ESTILOS["fg_branco"],
            bg=self.ESTILOS["bg_primario"],
        )
        self.label_tempo.pack(pady=(10, 0))
        

        # Contador de tentativas
        self.label_tentativas = tk.Label(
            self.tela_jogo_frame,
            text=f"Tentativas restantes: {self.logica_jogo.tentativas_restantes}",
            font=self.ESTILOS["fonte_padrao"],
            fg=self.ESTILOS["fg_branco"],
            bg=self.ESTILOS["bg_primario"],
        )
        self.label_tentativas.pack(pady=(10, 0))

        # Cria o tabuleiro
        tabuleiro_frame = tk.Frame(self.tela_jogo_frame, bg=self.ESTILOS["bg_primario"])
        tabuleiro_frame.pack(expand=True)

        for linha in range(self.logica_jogo.tamanho):
            for coluna in range(self.logica_jogo.tamanho):
                valor = self.logica_jogo.tabuleiro[linha, coluna]

                if valor == 0:  # Carta inválida
                    botao_carta = tk.Label(
                        tabuleiro_frame,
                        text="X",
                        width=6,
                        height=3,
                        font=("Helvetica", 10, "bold"),
                        fg="#ffffff",
                        bg="#333333",
                    )
                else:
                    botao_carta = tk.Button(
                        tabuleiro_frame,
                        text="",  # Não mostra números
                        width=6,
                        height=3,
                        font=("Helvetica", 10, "bold"),
                        bg=self.ESTILOS["bg_secundario"],
                        fg=self.ESTILOS["fg_branco"],
                        command=lambda l=linha, c=coluna: self.ao_clicar(l, c),
                    )

                botao_carta.grid(row=linha, column=coluna, padx=5, pady=5)
                self.tabuleiro[(linha, coluna)] = botao_carta
                
        self.atualizar_tempo()

        # Botão de voltar
        botao_voltar = tk.Button(
            self.tela_jogo_frame,
            text="Voltar",
            font=self.ESTILOS["fonte_padrao"],
            command=lambda: self.voltar_para_tela_inicial(self.tela_jogo_frame),
            bg=self.ESTILOS["bg_erro"],
            fg=self.ESTILOS["fg_branco"],
        )
        botao_voltar.pack(pady=20)

        # Revela todas as cartas por 2 segundos no início
        self.revelar_todas_cartas_temporariamente()


    def revelar_todas_cartas_temporariamente(self):
        """Revela todas as cartas no início do jogo por 2 segundos e oculta as válidas."""
        # Bloqueia todos os botões enquanto estão revelados
        self.alterar_estado_botoes("disabled")

        for linha in range(self.logica_jogo.tabuleiro.shape[0]):  # Número de linhas
            for coluna in range(self.logica_jogo.tabuleiro.shape[1]):  # Número de colunas
                valor = self.logica_jogo.tabuleiro[linha, coluna]
                botao = self.tabuleiro.get((linha, coluna))
                if botao:
                    if valor == 0:  # Carta inválida
                        botao.config(text="X", bg="#333333", state="disabled")  # Sempre visível
                    else:
                        botao.config(bg=self.CORES[valor], text="")  # Revela a cor

        # Após 2 segundos, oculta as cartas válidas e permite interação
        def ocultar_cartas():
            for linha in range(self.logica_jogo.tabuleiro.shape[0]):
                for coluna in range(self.logica_jogo.tabuleiro.shape[1]):
                    valor = self.logica_jogo.tabuleiro[linha, coluna]
                    botao = self.tabuleiro.get((linha, coluna))
                    if botao:
                        if valor == 0:  # Carta inválida
                            botao.config(text="X", bg="#333333", state="disabled")  # Mantém visível
                        else:
                            botao.config(
                                text="",  # Remove qualquer texto
                                bg=self.ESTILOS["bg_secundario"],  # Retorna à cor padrão
                                state="normal"  # Reativa os botões para cliques
                            )

        self.janela.after(2000, ocultar_cartas)


    def iniciar_jogo(self, tamanho, tentativas):
        """Inicializa a lógica"""
        print(f"Iniciando jogo para o jogador: {self.jogador.nome}")  # Log para debug
        self.logica_jogo = LogicaJogo(tamanho, tentativas)
        self.criar_tela_jogo()
        self.tempo_inicio = time.time()  # Inicializa o temporizador
        self.jogador.vitorias = self.db.obter_vitorias(self.jogador.nome)  # Atualiza vitórias
        print(f"Vitórias carregadas: {self.jogador.vitorias}")  # Log para debug
 
    def ao_clicar(self, linha, coluna):
        """
        Ação ao clicar em uma carta:
        - Primeiro clique:
            * Revela a carta selecionada e a mantém visível.
            * Armazena sua posição para comparação futura.
        - Segundo clique:
            * Revela a segunda carta selecionada.
            * Verifica se as duas cartas formam um par:
                - Se formam, mantém ambas visíveis e desativa os botões.
                - Se não formam, oculta as cartas após breve intervalo.
        - Atualiza as tentativas restantes e verifica condições de vitória ou derrota:
            * Se as tentativas acabam antes de encontrar todos os pares, exibe derrota.
            * Se todos os pares forem encontrados, exibe vitória.
        - Caso a carta clicada seja inválida ou já revelada, ignora o clique. """
        
        pos = (linha, coluna)
        # Desabilitar clique repetido ou carta já revelada
        if not self.tabuleiro[pos]["state"] == "normal" or self.logica_jogo.carta_revelada(pos):
            return

        botao = self.tabuleiro[pos]

        if self.primeiro_clique is None:
            # Primeiro clique
            resultado = self.logica_jogo.processar_clique(pos)
            botao.config(bg=self.CORES[int(resultado["valor"])], state="disabled")  # Exibir cor correspondente
            self.primeiro_clique = pos
            self.botao_primeiro_clique = botao
        else:
            # Segundo clique
            self.alterar_estado_botoes("disabled")  # Desativar todos os botões temporariamente

            resultado = self.logica_jogo.processar_clique(self.primeiro_clique, pos)
            botao.config(bg=self.CORES[resultado["valor"]], state="disabled")  # Exibir cor correspondente

            if resultado["par"]:
                # Par correto
                botao.config(bg="#5cb85c")  # Cor para pares corretos
                self.botao_primeiro_clique.config(bg="#5cb85c")
                if resultado["fim"]:
                    self.verificar_e_exibir_vitoria()
                else:
                    self.alterar_estado_botoes("normal")  # Reativar botões após processar o par
            else:
                # Não é par: ocultar novamente após 1 segundo
                pos1 = self.primeiro_clique
                self.janela.after(1000, lambda: [self.esconder_cartas(pos1, pos), self.alterar_estado_botoes("normal")])

            # Atualizar exibição do número de tentativas restantes
            self.label_tentativas.config(text=f"Tentativas restantes: {self.logica_jogo.tentativas_restantes}")

            # Verificar se as tentativas acabaram
            if self.logica_jogo.tentativas_restantes <= 0:
                self.exibir_derrota()

            # Resetar cliques
            self.primeiro_clique = None
            self.botao_primeiro_clique = None


    def atualizar_tempo(self):
        """Atualiza o contador de tempo na tela do jogo"""
        if self.tempo_inicio is not None:
            tempo_passado = int(time.time() - self.tempo_inicio)
            self.label_tempo.config(text=f"Tempo: {tempo_passado}s")
        # Garante que o método seja chamado novamente após 1 segundo
        self.janela.after(1000, self.atualizar_tempo)

    def alterar_estado_botoes(self, estado: str):
        """Ativa ou desativa todos os botões do tabuleiro"""
        for botao in self.tabuleiro.values():
            botao.config(state=estado)


    def esconder_cartas(self, pos1, pos2):
        """Esconde as cartas após tentativa errada"""
        botao1 = self.tabuleiro[pos1]
        botao2 = self.tabuleiro[pos2]
        if botao1 and botao2:
            botao1.config(bg=self.ESTILOS["bg_secundario"], state="normal")
            botao2.config(bg=self.ESTILOS["bg_secundario"], state="normal")
        self.logica_jogo.resetar_cartas(pos1, pos2)


    def reiniciar_jogo(self):
        """Reinicia o jogo e retorna à tela inicial"""
        # Remove todos os widgets da janela
        for widget in self.janela.winfo_children():
            widget.destroy()
        # Reinstancia a interface
        self.__init__(self.janela)


    def voltar_para_tela_inicial(self, tela_atual):
        """Retorna para a tela inicial a partir de outra tela"""
        tela_atual.pack_forget()  # Oculta a tela atual
        self.criar_tela_inicial()  # Recria a tela inicial


    def verificar_e_exibir_vitoria(self):
        """Verifica se o jogador venceu e exibe mensagem de vitória"""
        if self.logica_jogo.verificar_vitoria():
            self.db.registrar_vitoria(self.jogador.nome)  # Registra vitória no banco
            self.jogador.vitorias = self.db.obter_vitorias(self.jogador.nome)  # Atualiza vitórias
            messagebox.showinfo("Vitória", "Parabéns! Você encontrou todos os pares!")
            self.voltar_para_tela_inicial(self.tela_jogo_frame)


    def exibir_derrota(self):
        """Exibe mensagem de derrota e reinicia o jogo"""
        messagebox.showwarning("Derrota", "Você perdeu! Suas tentativas acabaram.")
        self.voltar_para_tela_inicial(self.tela_jogo_frame)


