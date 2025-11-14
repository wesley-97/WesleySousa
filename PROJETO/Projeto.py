class Peca:
    def __init__(self, id, peso, cor, comprimento):
        self.id = id
        self.peso = peso
        self.cor = cor.lower()
        self.comprimento = comprimento
        self.resultado, self.motivo = self.avaliar()
        
    def avaliar(self):
        if not (95 <= self.peso <= 105):
            return "reprovada", "Peso fora do padrão"
        if self.cor not in ["azul", "verde"]:
            return "reprovada", "Cor fora do padrão"
        if not (10 <= self.comprimento <= 20):
            return "reprovada", "Comprimento fora do padrão"
        return "aprovada", ""
        
class Caixa:
    def __init__(self, numero):
        self.numero = numero
        self.pecas = []

    def adicionar_peca(self, peca):
        if len(self.pecas) < 10:
            self.pecas.append(peca)
            return True
        return False

    def esta_cheia(self):
        return len(self.pecas) == 10

class Sistema:
    def __init__(self):
        self.pecas = []
        self.aprovadas = []
        self.reprovadas = []
        self.caixas = []
        self.caixa_atual = Caixa(1)

    def cadastrar_peca(self):
        try:
            id = input("ID da peça: ")
            peso = float(input("Peso (g): "))
            cor = input("Cor (azul/verde): ")
            comprimento = float(input("Comprimento (cm): "))
            peca = Peca(id, peso, cor, comprimento)
            self.pecas.append(peca)
            if peca.resultado == "aprovada":
                if not self.caixa_atual.adicionar_peca(peca):
                    self.caixas.append(self.caixa_atual)
                    self.caixa_atual = Caixa(len(self.caixas) + 1)
                    self.caixa_atual.adicionar_peca(peca)
                self.aprovadas.append(peca)
            else:
                self.reprovadas.append(peca)
            print(f"Peça {peca.resultado.upper()}! {peca.motivo}")
        except Exception as e:
            print("Erro ao cadastrar peça:", e)

    def listar_pecas(self):
        print("\n--- Peças Aprovadas ---")
        for p in self.aprovadas:
            print(f"ID: {p.id}, Peso: {p.peso}, Cor: {p.cor}, Comprimento: {p.comprimento}")
        print("\n--- Peças Reprovadas ---")
        for p in self.reprovadas:
            print(f"ID: {p.id}, Peso: {p.peso}, Cor: {p.cor}, Comprimento: {p.comprimento}, Motivo: {p.motivo}")

    def remover_peca(self):
        id = input("Informe o ID da peça a remover: ")
        for lista in [self.aprovadas, self.reprovadas]:
            for p in lista:
                if p.id == id:
                    lista.remove(p)
                    print("Peça removida com sucesso!")
                    return
        print("Peça não encontrada.")

    def listar_caixas_fechadas(self):
        print("\nCaixas fechadas:")
        for caixa in self.caixas:
            print(f"Caixa {caixa.numero}: {[p.id for p in caixa.pecas]}")

    def gerar_relatorio(self):
        print("\n===== Relatório Final =====")
        print(f"Total aprovadas: {len(self.aprovadas)}")
        print(f"Total reprovadas: {len(self.reprovadas)}")
        motivos = {}
        for p in self.reprovadas:
            motivo = p.motivo
            motivos[motivo] = motivos.get(motivo, 0) + 1
        print("Motivos de reprovação:")
        for motivo, qtd in motivos.items():
            print(f"{motivo}: {qtd}")
        caixa_utilizadas = len(self.caixas)
        if self.caixa_atual.pecas:
            caixa_utilizadas += 1
        print(f"Caixas utilizadas: {caixa_utilizadas}")

    def menu(self):
        while True:
            print("\n1. Cadastrar nova peça")
            print("2. Listar peças aprovadas/reprovadas")
            print("3. Remover peça cadastrada")
            print("4. Listar caixas fechadas")
            print("5. Gerar relatório final")
            print("0. Sair")
            opcao = input("Escolha uma opção: ")
            if opcao == "1":
                self.cadastrar_peca()
            elif opcao == "2":
                self.listar_pecas()
            elif opcao == "3":
                self.remover_peca()
            elif opcao == "4":
                self.listar_caixas_fechadas()
            elif opcao == "5":
                self.gerar_relatorio()
            elif opcao == "0":
                break
            else:
                print("Opção inválida!")

if __name__ == "__main__":
    s = Sistema()
    s.menu()
