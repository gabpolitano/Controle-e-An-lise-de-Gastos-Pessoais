import tkinter as tk
from tkinter import messagebox

# Classe que representa um usuário
class Usuario:
    def __init__(self, nome, cargo, salario):
        self.nome = nome
        self.cargo = cargo
        self.salario = salario
        # Dicionário para armazenar o saldo disponível por mês
        self.saldo_por_mes = {mes: salario for mes in range(1, 13)}

    # Método para atualizar o saldo disponível de um mês após adicionar um gasto
    def atualizar_saldo(self, mes, gasto):
        self.saldo_por_mes[mes] -= gasto

# Classe que representa um gasto
class Gasto:
    def __init__(self, ano, mes, descricao, valor):
        self.ano = ano
        self.mes = mes
        self.descricao = descricao
        self.valor = valor

# Classe para gerenciar os gastos do usuário
class GerenciadorGastos:
    def __init__(self, usuario):
        self.usuario = usuario
        self.gastos = []

    # Método para adicionar um gasto
    def adicionar_gasto(self, ano, mes, descricao, valor):
        self.gastos.append(Gasto(ano, mes, descricao, valor))
        # Atualiza o saldo disponível do usuário após adicionar o gasto
        self.usuario.atualizar_saldo(mes, valor)

    # Método para calcular os totais de gastos por mês
    def calcular_total_gastos(self, ano=None):
        total_por_mes = {}
        detalhes_por_mes = {}

        for gasto in self.gastos:
            if ano is None or gasto.ano == ano:
                total_por_mes.setdefault(gasto.mes, 0)
                total_por_mes[gasto.mes] += gasto.valor

                detalhes_por_mes.setdefault(gasto.mes, [])
                detalhes_por_mes[gasto.mes].append(gasto)

        return total_por_mes, detalhes_por_mes

# Classe para a aplicação de gerenciamento de gastos
class AplicacaoGastos:
    # Dicionário de meses para facilitar a exibição
    MESES = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho",
        7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }

    def __init__(self, root):
        self.root = root
        self.usuario = None
        self.gerenciador = None

        # Criação da interface gráfica
        self.frame = tk.Frame(root)
        self.frame.pack()

        # Entradas de texto para informações do usuário e gastos
        self.labels = ["Nome", "Cargo", "Salário", "Ano", "Mês", "Descrição", "Valor"]
        self.entries = {}

        for i, label_text in enumerate(self.labels):
            label = tk.Label(self.frame, text=label_text + ":")
            label.grid(row=i, column=0, sticky="w")
            entry = tk.Entry(self.frame)
            entry.grid(row=i, column=1)
            self.entries[label_text.lower()] = entry

        # Botões para confirmar usuário, adicionar gasto e calcular
        self.botao_confirmar = tk.Button(self.frame, text="Confirmar Usuário", command=self.iniciar_aplicacao)
        self.botao_confirmar.grid(row=len(self.labels), columnspan=2)

        self.botao_adicionar = tk.Button(self.frame, text="Adicionar Gasto", command=self.adicionar_gasto, state=tk.DISABLED)
        self.botao_adicionar.grid(row=len(self.labels) + 1, columnspan=2)

        self.botao_calcular = tk.Button(self.frame, text="Calcular", command=self.calcular, state=tk.DISABLED)
        self.botao_calcular.grid(row=len(self.labels) + 2, columnspan=2)

        # Rótulo para exibir resultados
        self.resultado_label = tk.Label(self.frame, text="")
        self.resultado_label.grid(row=len(self.labels) + 3, columnspan=2)

    # Método para iniciar a aplicação
    def iniciar_aplicacao(self):
        nome = self.entries["nome"].get()
        cargo = self.entries["cargo"].get()
        salario = self.entries["salário"].get()

        # Validação das entradas do usuário e criação do objeto Usuário
        if not salario.replace('.', '', 1).isdigit():
            messagebox.showerror("Erro", "Por favor, insira um valor numérico válido para o salário.")
            return

        salario = float(salario)

        if nome and cargo and salario > 0:
            self.usuario = Usuario(nome, cargo, salario)
            self.gerenciador = GerenciadorGastos(self.usuario)
            messagebox.showinfo("Usuário Confirmado", "Usuário confirmado, adicione seus gastos mensais, e os calcule!!!")
            self.botao_confirmar.config(state=tk.DISABLED)
            self.botao_adicionar.config(state=tk.NORMAL)
            self.botao_calcular.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos corretamente.")
            return

    # Método para adicionar um gasto
    def adicionar_gasto(self):
        if not self.usuario:
            messagebox.showerror("Erro", "Por favor, insira suas informações antes de adicionar um gasto.")
            return

        ano = self.entries["ano"].get()
        mes = self.entries["mês"].get()
        descricao = self.entries["descrição"].get()
        valor = self.entries["valor"].get()

        # Validação das entradas do gasto e adição do mesmo
        if not ano.isdigit():
            messagebox.showerror("Erro", "Por favor, insira um ano válido.")
            return

        ano = int(ano)

        if mes not in self.MESES.values():
            messagebox.showerror("Erro", "Mês inválido. Por favor, digite o nome completo do mês.")
            return

        mes = [key for key, value in self.MESES.items() if value == mes][0]

        if not valor.replace('.', '', 1).isdigit():
            messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")
            return

        valor = float(valor)

        if valor > self.usuario.saldo_por_mes[mes]:
            messagebox.showerror("Erro", "O valor do gasto excede o saldo disponível para o mês.")
            return

        self.gerenciador.adicionar_gasto(ano, mes, descricao, valor)
        self.entries["ano"].delete(0, tk.END)
        self.entries["mês"].delete(0, tk.END)
        self.entries["descrição"].delete(0, tk.END)
        self.entries["valor"].delete(0, tk.END)

        messagebox.showinfo("Sucesso", "Gasto adicionado com sucesso!")

    # Método para calcular os gastos
    def calcular(self):
        if not self.usuario:
            messagebox.showerror("Erro", "Por favor, insira suas informações antes de calcular os gastos.")
            return

        ano = self.entries["ano"].get()

        if not ano.isdigit():
            messagebox.showerror("Erro", "Por favor, insira um ano válido.")
            return

        ano = int(ano)

        total_por_mes, resumo_detalhado = self.gerenciador.calcular_total_gastos(ano)
        if total_por_mes:
            self.exibir_resultados(total_por_mes, resumo_detalhado)
        else:
            self.resultado_label.config(text="Não há gastos para o ano informado.")

    # Método para exibir os resultados
    def exibir_resultados(self, total_por_mes, resumo_detalhado):
        nova_janela = tk.Toplevel(self.root)
        nova_janela.title("Resumo de Gastos por Mês")

        for mes, total_gasto_mes in total_por_mes.items():
            frame_mes = tk.Frame(nova_janela)
            frame_mes.pack(padx=10, pady=5, anchor="w")

            tk.Label(frame_mes, text=self.MESES[mes], font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2)

            tk.Label(frame_mes, text="Descrição", font=("Arial", 10, "underline")).grid(row=1, column=0)
            tk.Label(frame_mes, text="Valor", font=("Arial", 10, "underline")).grid(row=1, column=1)

            total_mes = 0
            for idx, gasto in enumerate(resumo_detalhado[mes]):
                tk.Label(frame_mes, text=gasto.descricao).grid(row=idx + 2, column=0, sticky="w")
                tk.Label(frame_mes, text=f"R${gasto.valor:.2f}").grid(row=idx + 2, column=1, sticky="w")
                total_mes += gasto.valor

            tk.Label(frame_mes, text=f"Total de Gastos: R${total_gasto_mes:.2f}", font=("Arial", 10, "bold")).grid(row=len(resumo_detalhado[mes]) + 2, columnspan=2, sticky="w")
            tk.Label(frame_mes, text=f"Saldo Disponível para Investir: R${self.usuario.saldo_por_mes[mes]:.2f}", font=("Arial", 10, "bold")).grid(row=len(resumo_detalhado[mes]) + 3, columnspan=2, sticky="w")


def main():
    root = tk.Tk()
    app = AplicacaoGastos(root)
    root.mainloop()

if __name__ == "__main__":
    main()
