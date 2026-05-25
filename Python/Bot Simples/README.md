# 🤖 Bot Simples - Verificador de Horário

Um bot simples em Python com interface gráfica que mostra o horário atual quando solicitado.

## 📋 Descrição

Este bot foi criado para automatizar a tarefa de verificar o horário atual. Ele possui uma interface gráfica amigável desenvolvida com tkinter (biblioteca padrão do Python) que exibe:

- Horário atual em formato digital (HH:MM:SS)
- Data completa
- Barra de status com informações de atualização

## ✨ Funcionalidades

- Exibe o horário atual em tempo real
- Mostra a data completa formatada
- Interface gráfica simples e intuitiva
- Barra de status que indica quando o horário foi atualizado
- Janela centralizada na tela

## 🚀 Como Executar

### Pré-requisitos

- Python 3.x instalado no seu computador
- Tkinter (geralmente já vem com a instalação padrão do Python)

### Passos para execução

1. **Verifique se o Python está instalado:**
   ```bash
   python --version
   ```
   ou
   ```bash
   py --version
   ```

2. **Execute o bot:**
   ```bash
   python bot.py
   ```
   ou
   ```bash
   py bot.py
   ```

3. **Use o bot:**
   - Ao abrir, o bot já mostrará o horário atual automaticamente
   - Clique no botão "🕐 Ver Horário Atual" para atualizar o horário
   - A data também será exibida abaixo do horário

## 📁 Estrutura do Projeto

```
Bot Simples/
│
├── bot.py          # Arquivo principal do bot
└── README.md       # Este arquivo de documentação
```

## 🛠️ Tecnologias Utilizadas

- **Python 3.x** - Linguagem de programação
- **Tkinter** - Biblioteca para interface gráfica
- **datetime** - Módulo para manipulação de datas e horários
- **locale** - Módulo para formatação em português do Brasil

## 📝 Funcionamento

O bot funciona da seguinte maneira:

1. Ao ser executado, ele cria uma janela gráfica centralizada na tela
2. Automaticamente exibe o horário atual no momento da abertura
3. Quando o usuário clica no botão "Ver Horário Atual":
   - O horário é atualizado
   - A data é exibida formatada
   - A barra de status mostra o momento da última atualização

## 🔧 Personalização

Se você deseja personalizar o bot, pode modificar:

- **Cores**: Altere os valores hexadecimais nas propriedades `bg` e `fg`
- **Tamanhos**: Modifique os parâmetros `geometry` e `font`
- **Texto**: Altere as strings exibidas nos labels e botões
- **Funcionalidades**: Adicione novos métodos na classe `BotHorario`

## ⚠️ Solução de Problemas

### Python não encontrado
Se você recebeu a mensagem "Python não foi encontrado", é necessário instalar o Python no seu computador:

1. Acesse [python.org](https://www.python.org/downloads/)
2. Baixe a versão mais recente do Python 3
3. Durante a instalação, marque a opção "Add Python to PATH"
4. Após instalar, reinicie o terminal e tente executar novamente

### Erro com locale (formatação em português)
Se a data não estiver aparecendo em português, o bot usará um formato alternativo (dd/mm/aaaa). Isso não afeta o funcionamento do bot.

## 📄 Licença

Este projeto é de código aberto e pode ser modificado livremente.

## 👨‍💻 Autor

Criado por solicitação do usuário para automatizar a tarefa de verificar o horário atual.

---

**Divirta-se usando o Bot do Horário! 🕐**