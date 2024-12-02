# Jogo da Memória com Tkinter

Trabalho final da disciplina Computação 2 da UFRJ, desenvolvido por Bernardo Welsing, Gabriel, e Leticia. O objetivo é criar um jogo da memória funcional com integração a banco de dados e interface gráfica em Python.

## Funcionalidades

- Escolha de níveis de dificuldade: Fácil (4x4), Médio (5x5) e Difícil (6x6).
- Banco de dados SQLite para registrar vitórias dos jogadores.
- Carta inválida no modo médio para manter pares.
- Exibição temporária de todas as cartas no início do jogo.
- Contadores de tempo e tentativas durante o jogo.

## Uso

1. Insira seu nome na tela inicial e confirme.
2. Escolha o nível de dificuldade.
3. Combine os pares com o menor número de tentativas possível.
4. O progresso é salvo automaticamente no banco de dados.

## Casos de Teste

O projeto inclui testes básicos para funcionalidades principais, como:

- Atualizar tentativas.
- Verificar vitória.
- Resetar o estado das cartas.
