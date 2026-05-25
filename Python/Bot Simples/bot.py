"""
Bot Simples - Verificador de Horário
Um bot com interface gráfica que mostra o horário atual quando solicitado.
"""

import tkinter as tk
from tkinter import font
from datetime import datetime
import locale

# Configurar locale para português do Brasil
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil')
    except:
        pass  # Usa padrão se não conseguir configurar


class BotHorario:
    """Classe principal do bot de horário com interface gráfica."""
    
    def __init__(self, root):
        """Inicializa a interface gráfica do bot."""
        self.root = root
        self.root.title("🤖 Bot do Horário")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')
        
        # Configurar ícone da janela (se disponível)
        try:
            self.root.iconbitmap('icone.ico')
        except:
            pass
        
        self._criar_interface()
    
    def _criar_interface(self):
        """Cria os elementos da interface gráfica."""
        
        # Frame principal
        frame_principal = tk.Frame(self.root, bg='#f0f0f0', padx=20, pady=20)
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo_fonte = font.Font(family='Arial', size=16, weight='bold')
        titulo = tk.Label(
            frame_principal,
            text="🤖 Bot do Horário",
            font=titulo_fonte,
            bg='#f0f0f0',
            fg='#333333'
        )
        titulo.pack(pady=(0, 20))
        
        # Área de exibição do horário
        self.label_horario = tk.Label(
            frame_principal,
            text="00:00:00",
            font=('Courier New', 36, 'bold'),
            bg='#ffffff',
            fg='#2c3e50',
            padx=20,
            pady=15,
            relief=tk.RAISED,
            borderwidth=2
        )
        self.label_horario.pack(pady=10, fill=tk.X)
        
        # Área de exibição da data
        self.label_data = tk.Label(
            frame_principal,
            text="",
            font=('Arial', 14),
            bg='#f0f0f0',
            fg='#666666'
        )
        self.label_data.pack(pady=(5, 20))
        
        # Botão para atualizar horário
        botao_fonte = font.Font(family='Arial', size=12, weight='bold')
        botao = tk.Button(
            frame_principal,
            text="🕐 Ver Horário Atual",
            font=botao_fonte,
            command=self._atualizar_horario,
            bg='#3498db',
            fg='white',
            activebackground='#2980b9',
            activeforeground='white',
            padx=20,
            pady=10,
            relief=tk.RAISED,
            borderwidth=2,
            cursor='hand2'
        )
        botao.pack(pady=10)
        
        # Label de instruções
        instrucoes = tk.Label(
            frame_principal,
            text="Clique no botão para ver o horário atual",
            font=('Arial', 9),
            bg='#f0f0f0',
            fg='#999999'
        )
        instrucoes.pack(pady=(20, 0))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto - Clique no botão para começar")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg='#ecf0f1',
            fg='#7f8c8d',
            padx=10,
            pady=5
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Atualizar horário inicial
        self._atualizar_horario()
    
    def _atualizar_horario(self):
        """Atualiza a exibição do horário atual."""
        agora = datetime.now()
        
        # Formatar horário
        horario_str = agora.strftime("%H:%M:%S")
        self.label_horario.config(text=horario_str)
        
        # Formatar data
        try:
            data_str = agora.strftime("%A, %d de %B de %Y")
        except:
            data_str = agora.strftime("%d/%m/%Y - %A")
        
        self.label_data.config(text=data_str)
        
        # Atualizar status
        self.status_var.set(f"Horário atualizado em {horario_str}")
        
        # Mudar cor do botão temporariamente
        self._piscar_botao()
    
    def _piscar_botao(self):
        """Efeito visual de piscar no botão."""
        # Este método poderia ser expandido para criar um efeito visual
        pass


def main():
    """Função principal para iniciar o bot."""
    root = tk.Tk()
    app = BotHorario(root)
    
    # Centralizar janela na tela
    root.update_idletasks()
    largura = root.winfo_width()
    altura = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (largura // 2)
    y = (root.winfo_screenheight() // 2) - (altura // 2)
    root.geometry(f'{largura}x{altura}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()