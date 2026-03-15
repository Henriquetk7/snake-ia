# Snake IA - Algoritmo A*

Este projeto implementa o jogo Snake clássico, porém jogado por uma Inteligência Artificial utilizando o Algoritmo de busca estruturada A* (A-Star) e uma interface usando Pygame.

## 🚀 Como rodar o projeto em uma nova máquina

Siga este passo a passo se você acabou de clonar este repositório via `git clone`:

### 1. Entre na pasta do projeto
```bash
cd snake-ia
```

### 2. Crie um Ambiente Virtual Python (Recomendado)
O ambiente virtual previne conflitos de versões de bibliotecas do seu computador.
```bash
python -m venv venv
```

### 3. Ative o Ambiente Virtual
Dependendo do seu sistema operacional, o comando será diferente:

- **No Windows:**
  ```cmd
  venv\Scripts\activate
  ```

- **No Linux ou macOS:**
  ```bash
  source venv/bin/activate
  ```

> Você saberá que deu certo se o termo `(venv)` aparecer no começo da linha de comando do seu terminal.

### 4. Instale as Dependências
Com o ambiente ativado, instale as bibliotecas necessárias listadas no `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 5. Inicie o Jogo
Agora que tudo está configurado, basta rodar o arquivo principal:
```bash
python main.py
```

---

## 🎮 Controles no Jogo

Embora a IA jogue sozinha, você pode controlar a interface e a velocidade:
- `Seta para Cima`: Acelera a velocidade do jogo (Aumenta o FPS)
- `Seta para Baixo`: Diminui a velocidade do jogo (Diminui o FPS)
- `R`: Reinicia a partida
- `ESC`: Fecha o jogo
