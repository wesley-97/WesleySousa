import tkinter as tk
from tkinter import messagebox, simpledialog

class Peca:
    def __init__(self, id, peso, cor, comprimento):
        self.id = id
        self.peso = peso
        self.cor = cor
        self.comprimento = comprimento
        self.aprovada, self.motivo_reprovacao = self.avaliar_peca()

    def avaliar_peca(self):
        motivos = []
        if not (95 <= self.peso <= 105):
            motivos.append('Peso fora do padrão')
        if self.cor not in ['azul', 'verde']:
            motivos.append('Cor fora do padrão')
        if not (10 <= self.comprimento <= 20):
            motivos.append('Comprimento fora do padrão')
        if motivos:
            return False, '; '.join(motivos)
        return True, 'Aprovada'

class Caixa:
    def __init__(self, capacidade=10):
        self.capacidade = capacidade
        self.pecas = []
        self.fechada = False

    def adicionar_peca(self, peca):
        if not self.fechada and len(self.pecas) < self.capacidade:
            self.pecas.append(peca)
            if len(self.pecas) == self.capacidade:
                self.fechada = True
                return True
        return False

class SistemaProducao:
    def __init__(self):
        self.pecas_cadastradas = []
        self.pecas_aprovadas = []
        self.pecas_reprovadas = []
        self.caixas = [Caixa()]

    def cadastrar_peca(self, id, peso, cor, comprimento):
        peca = Peca(id, peso, cor, comprimento)
        self.pecas_cadastradas.append(peca)
        if peca.aprovada:
            self.pecas_aprovadas.append(peca)
            caixa_aberta = [cx for cx in self.caixas if not cx.fechada][0]
            caixa_fechou = caixa_aberta.adicionar_peca(peca)
            if caixa_fechou:
                self.caixas.append(Caixa())
        else:
            self.pecas_reprovadas.append(peca)
        return peca.aprovada, peca.motivo_reprovacao

    def listar_pecas(self, aprovadas=True):
        return self.pecas_aprovadas if aprovadas else self.pecas_reprovadas

    def remover_peca(self, id):
        for p in self.pecas_cadastradas:
            if p.id == id:
                self.pecas_cadastradas.remove(p)
                if p.aprovada:
                    self.pecas_aprovadas.remove(p)
                    for cx in self.caixas:
                        if p in cx.pecas:
                            cx.pecas.remove(p)
                            cx.fechada = False if len(cx.pecas) < cx.capacidade else cx.fechada
                            break
                else:
                    self.pecas_reprovadas.remove(p)
                return True
        return False

    def listar_caixas_fechadas(self):
        return [i+1 for i, cx in enumerate(self.caixas) if cx.fechada]

    def gerar_relatorio(self):
        motivos = {}
        for p in self.pecas_reprovadas:
            motivos[p.motivo_reprovacao] = motivos.get(p.motivo_reprovacao, 0) + 1
        return {
            'total_aprovadas': len(self.pecas_aprovadas),
            'total_reprovadas': len(self.pecas_reprovadas),
            'motivos_reprovacao': motivos,
            'caixas_utilizadas': sum(1 for cx in self.caixas if cx.fechada)
        }

class AppMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Controle de Produção")
        self.sistema = SistemaProducao()
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack()

        tk.Button(frame, text="1. Cadastrar nova peça", width=30, command=self.cadastrar_peca).pack(pady=2)
        tk.Button(frame, text="2. Listar peças aprovadas", width=30, command=lambda: self.listar_pecas(True)).pack(pady=2)
        tk.Button(frame, text="3. Listar peças reprovadas", width=30, command=lambda: self.listar_pecas(False)).pack(pady=2)
        tk.Button(frame, text="4. Remover peça cadastrada", width=30, command=self.remover_peca).pack(pady=2)
        tk.Button(frame, text="5. Listar caixas fechadas", width=30, command=self.listar_caixas).pack(pady=2)
        tk.Button(frame, text="6. Gerar relatório final", width=30, command=self.gerar_relatorio).pack(pady=2)
        tk.Button(frame, text="7. Sair", width=30, command=self.root.quit).pack(pady=2)

    def cadastrar_peca(self):
        id = simpledialog.askstring("Cadastro", "Informe o ID da peça:")
        if not id:
            return
        try:
            peso = float(simpledialog.askstring("Cadastro", "Informe o peso (g):"))
            cor = simpledialog.askstring("Cadastro", "Informe a cor (azul ou verde):")
            comprimento = float(simpledialog.askstring("Cadastro", "Informe o comprimento (cm):"))
        except (ValueError, TypeError):
            messagebox.showerror("Erro", "Entrada inválida. Use números para peso e comprimento.")
            return
        aprovada, motivo = self.sistema.cadastrar_peca(id, peso, cor, comprimento)
        messagebox.showinfo("Resultado", f"Peça {'aprovada' if aprovada else 'reprovada'}: {motivo}")

    def listar_pecas(self, aprovadas):
        titulo = "Peças Aprovadas" if aprovadas else "Peças Reprovadas"
        pecas = self.sistema.listar_pecas(aprovadas)
        texto = ""
        for p in pecas:
            texto += f"ID: {p.id} | Peso: {p.peso}g | Cor: {p.cor} | Comprimento: {p.comprimento}cm"
            if not aprovadas:
                texto += f" | Motivo: {p.motivo_reprovacao}"
            texto += "\n"
        if not texto:
            texto = "Nenhuma peça encontrada."
        self.show_text_window(titulo, texto)

    def remover_peca(self):
        id = simpledialog.askstring("Remover", "Informe o ID da peça para remover:")
        if not id:
            return
        removido = self.sistema.remover_peca(id)
        if removido:
            messagebox.showinfo("Remoção", "Peça removida com sucesso.")
        else:
            messagebox.showwarning("Remoção", "Peça não encontrada.")

    def listar_caixas(self):
        caixas = self.sistema.listar_caixas_fechadas()
        texto = f"Caixas fechadas: {caixas}" if caixas else "Nenhuma caixa fechada."
        self.show_text_window("Caixas Fechadas", texto)

    def gerar_relatorio(self):
        rel = self.sistema.gerar_relatorio()
        texto = (f"Total de peças aprovadas: {rel['total_aprovadas']}\n"
                 f"Total de peças reprovadas: {rel['total_reprovadas']}\n"
                 f"Motivos de reprovação:\n")
        for mot, qtd in rel['motivos_reprovacao'].items():
            texto += f"  - {mot}: {qtd}\n"
        texto += f"Caixas utilizadas: {rel['caixas_utilizadas']}"
        self.show_text_window("Relatório Final", texto)

    def show_text_window(self, titulo, texto):
        janela = tk.Toplevel(self.root)
        janela.title(titulo)
        text_area = tk.Text(janela, width=60, height=20)
        text_area.pack(padx=10, pady=10)
        text_area.insert(tk.END, texto)
        text_area.config(state='disabled')  # Impede edição do texto

if __name__ == "__main__":
    root = tk.Tk()
    app = AppMenu(root)
    root.mainloop()