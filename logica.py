
import sqlite3
import numpy as np
import random


class Jogador:
    """Classe que representa o jogador"""

    def __init__(self, nome, db):
        self.nome = nome
        self.db = db
        self.vitorias = db.obter_vitorias(nome)


class LogicaJogo:
    """Classe responsável pela lógica do Jogo de Memória"""

    def __init__(self, tamanho, tentativas):
        self.tamanho = tamanho
        self.tentativas_restantes = tentativas
        self.tabuleiro, self.estado_cartas = self.iniciar_jogo()


    def iniciar_jogo(self):
        """
        Cria e embaralha o tabuleiro do jogo:
        - Gera pares de cartas de acordo com o tamanho do tabuleiro:
            * Para 4x4 (fácil) e 6x6 (difícil): todos os pares são válidos.
            * Para 5x5 (médio): inclui uma carta inválida na posição central.
        - Passos:
            1. Cria uma lista com os pares de cartas.
            2. Adiciona uma carta inválida (valor 0) no modo médio.
            3. Embaralha as cartas e as organiza no formato da matriz.
        - Retorno:
            * Tabuleiro: Matriz NumPy representando as cartas.
            * Estado das cartas: Matriz de booleanos indicando cartas reveladas. """
        
        num_celulas = self.tamanho * self.tamanho
        num_pares = (num_celulas - 1) // 2 if self.tamanho == 5 else num_celulas // 2

        # Gera os pares de cartas
        cartas = list(range(1, num_pares + 1)) * 2

        if self.tamanho == 5:
            # Remove dois pares para ajustar ao espaço da carta inválida
            cartas = cartas[:24]

        # Embaralha as cartas
        random.shuffle(cartas)

        # Constrói o tabuleiro
        tabuleiro = np.zeros((self.tamanho, self.tamanho), dtype=int)
        idx = 0
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                if (i, j) == (2, 2) and self.tamanho == 5:  # Carta inválida na posição central
                    tabuleiro[i, j] = 0
                else:
                    tabuleiro[i, j] = cartas[idx]
                    idx += 1

        estado_cartas = np.full(tabuleiro.shape, False)  # Todas as cartas começam ocultas
        return tabuleiro, estado_cartas


    def verificar_par(self, pos1, pos2):
        """Verifica se duas posições formam um par"""
        if self.tabuleiro[pos1] == self.tabuleiro[pos2]:
            self.estado_cartas[pos1] = True
            self.estado_cartas[pos2] = True
            return True
        else:
            return False
        

    def processar_clique(self, pos1, pos2=None):
        """Processa os cliques no jogo e retorna o estado atualizado"""
        if pos2 is None:
            # Primeiro clique: apenas retornar o valor da carta
            return {"valor": self.tabuleiro[pos1], "par": None, "fim": False}

        # Segundo clique: verificar se é um par
        if self.verificar_par(pos1, pos2):
            # Par encontrado
            fim = self.verificar_vitoria()
            return {"valor": self.tabuleiro[pos2], "par": True, "fim": fim}
        else:
            # Não é um par, reduzir tentativas
            self.atualizar_tentativas()
            return {"valor": self.tabuleiro[pos2], "par": False, "fim": self.tentativas_restantes <= 0}


    def carta_revelada(self, pos):
        """Verifica se a carta já foi revelada"""
        return self.estado_cartas[pos]


    def verificar_vitoria(self):
        """Verifica se todas as cartas válidas foram descobertas."""
        for linha in range(self.tabuleiro.shape[0]):
            for coluna in range(self.tabuleiro.shape[1]):
                if self.tabuleiro[linha, coluna] != 0:  # Ignora a carta inválida
                    if not self.estado_cartas[linha, coluna]:  # Se ainda não foi revelada
                        return False
        return True


    def atualizar_tentativas(self):
        """Decrementa o número de tentativas e verifica se ainda há tentativas restantes"""
        self.tentativas_restantes -= 1
        return self.tentativas_restantes > 0


    def resetar_cartas(self, pos1, pos2):
        """Reseta o estado das cartas se não formarem um par"""
        self.estado_cartas[pos1] = False
        self.estado_cartas[pos2] = False


class BancoDeDados:
    def __init__(self, db_path="jogadores.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._inicializar_tabela()


    def _inicializar_tabela(self):
        """Inicializa a tabela de jogadores no banco de dados"""
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS jogadores (
                nome TEXT PRIMARY KEY,
                vitorias INTEGER DEFAULT 0
            )"""
        )
        self.conn.commit()


    def carregar_jogador(self, nome):
        """Carrega ou cria um jogador no banco de dados"""
        self.cursor.execute("SELECT vitorias FROM jogadores WHERE nome = ?", (nome,))
        resultado = self.cursor.fetchone()
        if resultado:
            return {"nome": nome, "vitorias": resultado[0]}
        else:
            self.cursor.execute("INSERT INTO jogadores (nome, vitorias) VALUES (?, ?)", (nome, 0))
            self.conn.commit()
            return {"nome": nome, "vitorias": 0}
        

    def registrar_vitoria(self, nome):
        """Incrementa o número de vitórias de um jogador"""
        self.cursor.execute("UPDATE jogadores SET vitorias = vitorias + 1 WHERE nome = ?", (nome,))
        if self.cursor.rowcount == 0:  # Se nenhum registro foi atualizado, insira
            self.cursor.execute("INSERT INTO jogadores (nome, vitorias) VALUES (?, 1)", (nome,))
        self.conn.commit()
        print(f"Vitória registrada para {nome}")  # Log para debug


    def obter_vitorias(self, nome):
        """Obtém o número de vitórias de um jogador"""
        self.cursor.execute("SELECT vitorias FROM jogadores WHERE nome = ?", (nome,))
        resultado = self.cursor.fetchone()
        return resultado[0] if resultado else 0


    def fechar_conexao(self):
        """Fecha a conexão com o banco de dados"""
        self.conn.close()




#CASOS DE TESTES
if __name__ == "__main__":
    # Teste para iniciar_jogo
    print("Teste: iniciar_jogo()")
    jogo = LogicaJogo(tamanho=4, tentativas=10)
    print("Tabuleiro gerado:")
    print(jogo.tabuleiro)
    print("Estado inicial das cartas:")
    print(jogo.estado_cartas)
    ## Resultado esperado:
    # Tabuleiro gerado: Um array 4x4 com números (1 a 8) distribuídos aleatoriamente.
    # Estado inicial das cartas: Uma matriz 4x4 com valores False.
    print("Tabuleiro gerado corretamente:", jogo.tabuleiro.size == 16)    ## Resultado esperado: True
    print("-" * 50)

    # Teste para verificar_par
    print("Teste: verificar_par()")
    jogo.tabuleiro[0, 0] = 1
    jogo.tabuleiro[0, 1] = 1
    print("Par correto (0,0) e (0,1):", jogo.verificar_par((0, 0), (0, 1)))     ## Resultado esperado: True
    jogo.tabuleiro[1, 1] = 2
    print("Par incorreto (0,0) e (1,1):", jogo.verificar_par((0, 0), (1, 1)))     ## Resultado esperado: False
    print("-" * 50)

    # Teste para atualizar_tentativas
    print("Teste: atualizar_tentativas()")
    print("Tentativas antes:", jogo.tentativas_restantes)     ## Resultado esperado: 10
    jogo.atualizar_tentativas()
    print("Tentativas depois:", jogo.tentativas_restantes)     ## Resultado esperado: 9
    print("-" * 50)

    # Teste para verificar_vitoria
    print("Teste: verificar_vitoria()")
    jogo.estado_cartas[:, :] = True  # Simula todas as cartas reveladas
    print("Vitória detectada:", jogo.verificar_vitoria())    ## Resultado esperado:  True
    jogo.estado_cartas[0, 0] = False
    print("Vitória com cartas ocultas:", jogo.verificar_vitoria())    ## Resultado esperado: False
    print("-" * 50)

    # Teste para resetar_cartas
    print("Teste: resetar_cartas()")
    jogo.estado_cartas[0, 0] = True
    jogo.estado_cartas[0, 1] = True
    print("Estado antes do reset:", jogo.estado_cartas)
    ## Resultado esperado: Estado antes do reset: Uma matriz com True nas posições (0,0) e (0,1).
    jogo.resetar_cartas((0, 0), (0, 1))
    print("Estado após o reset:", jogo.estado_cartas)
    ## Resultado esperado: Estado após o reset: Uma matriz com False em todas as posições.
    print("-" * 50)
