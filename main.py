import tkinter as tk
from interface import InterfaceJogo
from logica import BancoDeDados

def main():
    """Função principal para inicializar o jogo"""
    # Criar a janela principal
    janela = tk.Tk()
    janela.title("Jogo de Memória")

    # Inicializar a interface do jogo
    interface = InterfaceJogo(janela)

    # Exibir a janela e iniciar o loop principal
    janela.mainloop()


if __name__ == "__main__":
    db = BancoDeDados()
    print(db.carregar_jogador("Teste"))  # Certifica que está carregando jogadores
    main()
