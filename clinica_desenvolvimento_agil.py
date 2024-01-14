import datetime

class ConsultaDataHoraOcupadaException(Exception):
    pass

class ConsultaDataAnteriorException(Exception):
    pass


class ClinicaConsultas:
    def __init__(self):
        self.pacientes_cadastrados = []
        self.agendamentos_cadastrados = []

    def exibir_menu(self):
        print("===== Menu Principal =====")
        print("1. Cadastrar paciente")
        print("2. Marcações de consultas")
        print("3. Cancelamento de consultas")
        print("4. Sair")

    def paciente_ja_cadastrado(self, telefone):
        for paciente in self.pacientes_cadastrados:
            if paciente["telefone"] == telefone:
                return True
        return False

    def cadastrar_paciente(self):
        nome = input("Nome para cadastro: ")
        telefone = int(input("Por favor insira seu número de telefone: "))

        if self.paciente_ja_cadastrado(telefone):
            print("Paciente já cadastrado!")
            return

        paciente = {"nome": nome, "telefone": telefone}
        self.pacientes_cadastrados.append(paciente)

        print("Paciente cadastrado com sucesso")
    

    def verificar_disponibilidade_consulta(self, data_hora):
        for consulta in self.agendamentos_cadastrados:
            if consulta["data_hora"] == data_hora:
                return False
        return True

    def verificar_data_atual(self, data):
        data_atual = datetime.datetime.now().date()
        if data < data_atual:
            raise ConsultaDataAnteriorException("Não é possível marcar consultas retroativas.")

    def marcar_consulta(self):
        try:
            for indice, item in enumerate(self.pacientes_cadastrados, start=1):
                print(f"{indice}, {item}")
            nome_paciente = input("Digite a numeração correspondente ao paciente no qual você deseja marcar a consulta: ")

            data_str = input("Digite a data da consulta (YYYY-MM-DD): ")
            data_consulta = datetime.datetime.strptime(data_str, "%Y-%m-%d").date()

            self.verificar_data_atual(data_consulta)

            hora_str = input("Digite a hora da consulta (HH:MM): ")
            hora_consulta = datetime.datetime.strptime(hora_str, "%H:%M").time()

            data_hora = datetime.datetime.combine(data_consulta, hora_consulta)

            if not self.verificar_disponibilidade_consulta(data_hora):
                raise ConsultaDataHoraOcupadaException("Data e hora já ocupadas!")

            consulta = {"paciente": nome_paciente, "data_hora": data_hora}
            self.agendamentos_cadastrados.append(consulta)

            print("Consulta marcada com sucesso.")

        except ValueError:
            print("Formato de data ou hora inválido. Use o formato YYYY-MM-DD para a data e HH:MM para a hora.")
        except ConsultaDataHoraOcupadaException as e:
            print(f"Erro: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def cancelar_consulta(self):
        for indice, item in enumerate(self.agendamentos_cadastrados, start=1):
            print(f"{indice}, {item}")

        if self.agendamentos_cadastrados:
            try:
                indice_cancelar = int(input("Digite o número da consulta que deseja cancelar: "))
                if 1 <= indice_cancelar <= len(self.agendamentos_cadastrados):
                    consulta_cancelar = self.agendamentos_cadastrados.pop(indice_cancelar - 1)
                    print("Consulta cancelada com sucesso")
                else:
                    print("Número de consulta inválido.")
            except ValueError:
                print("Entrada inválida. Digite um número válido.")
        else:
            print("Não há consultas marcadas para cancelar.")

if __name__ == "__main__":
    clinica = ClinicaConsultas()

    while True:
        clinica.exibir_menu()

        escolha = input("Digite o número da opção desejada: ")

        if escolha == "1":
            clinica.cadastrar_paciente()
        elif escolha == "2":
            clinica.marcar_consulta()
        elif escolha == "3":
            clinica.cancelar_consulta()
        elif escolha == "4":
            print("Saindo do programa. Até logo!")
            break
