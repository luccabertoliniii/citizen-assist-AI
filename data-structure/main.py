# =====================================
# CITIZEN ASSIST AI
# GLOBAL SOLUTION - DSA
# =====================================


class Servico:
    def __init__(self, id, titulo, categoria, descricao, requisitos, local):
        self.id = id
        self.titulo = titulo
        self.categoria = categoria
        self.descricao = descricao
        self.requisitos = requisitos
        self.local = local


class No:
    def __init__(self, servico):
        self.servico = servico
        self.proximo = None


class ListaEncadeada:
    def __init__(self):
        self.inicio = None

    def buscar_id(self, id):
        atual = self.inicio
        while atual is not None:
            if atual.servico.id == id:
                return atual.servico
            atual = atual.proximo
        return None

    def inserir(self, servico):
        if self.buscar_id(servico.id) is not None:
            return False

        novo = No(servico)
        if self.inicio is None:
            self.inicio = novo
        else:
            atual = self.inicio
            while atual.proximo is not None:
                atual = atual.proximo
            atual.proximo = novo
        return True

    def mostrar_servico(self, servico):
        print("----------------------------")
        print("ID:", servico.id)
        print("Titulo:", servico.titulo)
        print("Categoria:", servico.categoria)
        print("Descricao:", servico.descricao)
        print("Requisitos:", servico.requisitos)
        print("Local:", servico.local)

    def listar(self):
        if self.inicio is None:
            print("Nenhum servico cadastrado.")
            return

        atual = self.inicio
        while atual is not None:
            self.mostrar_servico(atual.servico)
            atual = atual.proximo

    def excluir(self, id):
        atual = self.inicio
        anterior = None

        while atual is not None:
            if atual.servico.id == id:
                if anterior is None:
                    self.inicio = atual.proximo
                else:
                    anterior.proximo = atual.proximo
                return True
            anterior = atual
            atual = atual.proximo
        return False

    def buscar_titulo(self, texto):
        atual = self.inicio
        encontrou = False
        while atual is not None:
            if texto.lower() in atual.servico.titulo.lower():
                self.mostrar_servico(atual.servico)
                encontrou = True
            atual = atual.proximo
        return encontrou

    def buscar_categoria(self, texto):
        atual = self.inicio
        encontrou = False
        while atual is not None:
            if texto.lower() in atual.servico.categoria.lower():
                self.mostrar_servico(atual.servico)
                encontrou = True
            atual = atual.proximo
        return encontrou

    def ordenar_por_titulo(self):
        if self.inicio is None:
            return False

        # Selection Sort diretamente nos nos da lista encadeada.
        # Trocamos os servicos guardados nos nos, nao os ponteiros.
        atual = self.inicio
        while atual is not None:
            menor = atual
            comparador = atual.proximo

            while comparador is not None:
                if comparador.servico.titulo.lower() < menor.servico.titulo.lower():
                    menor = comparador
                comparador = comparador.proximo

            atual.servico, menor.servico = menor.servico, atual.servico
            atual = atual.proximo
        return True

    def analisar(self):
        if self.inicio is None:
            print("Nenhum servico cadastrado para analisar.")
            return

        total = 0
        categorias = {}
        atual = self.inicio

        while atual is not None:
            total += 1
            categoria = atual.servico.categoria.strip().lower()
            if categoria in categorias:
                categorias[categoria] += 1
            else:
                categorias[categoria] = 1
            atual = atual.proximo

        print("Total de servicos:", total)
        print("Servicos por categoria:")
        for categoria, quantidade in categorias.items():
            print("-", categoria.title() + ":", quantidade)


def ler_id(mensagem):
    try:
        id = int(input(mensagem).strip())
        if id <= 0:
            print("Erro: o ID deve ser um inteiro positivo.")
            return None
        return id
    except ValueError:
        print("Erro: digite um numero inteiro valido.")
        return None


def ler_campo(nome):
    valor = input(nome + ": ").strip()
    if valor == "":
        print("Erro: o campo", nome, "nao pode ficar vazio.")
        return None
    return valor


def cadastrar(lista):
    print("\n========== CADASTRO DE SERVICO ==========")
    print("Cadastre um SERVICO PUBLICO, nao os dados de um cidadao.")
    print("Exemplo: Emissao de RG, Atendimento na UBS ou Matricula Escolar.")
    print("\nPreencha os campos:")
    print("ID: numero unico para identificar o servico (ex.: 1).")
    print("Titulo: nome do servico (ex.: Emissao de RG).")
    print("Categoria: area a que pertence o servico.")
    print("Descricao: explique o que o servico oferece.")
    print("Requisitos: documentos ou condicoes necessarias.")
    print("Local: onde o cidadao pode buscar atendimento.")
    print("\nCategorias sugeridas: Saude, Documentacao, Educacao,")
    print("Assistencia Social e Servicos Urbanos.")
    print("-----------------------------------------")
    id = ler_id("ID do servico: ")
    if id is None:
        return
    if lista.buscar_id(id) is not None:
        print("Erro: esse ID ja esta cadastrado.")
        return

    titulo = ler_campo("Titulo")
    if titulo is None:
        return
    categoria = ler_campo("Categoria")
    if categoria is None:
        return
    descricao = ler_campo("Descricao")
    if descricao is None:
        return
    requisitos = ler_campo("Requisitos")
    if requisitos is None:
        return
    local = ler_campo("Local de atendimento")
    if local is None:
        return

    servico = Servico(id, titulo, categoria, descricao, requisitos, local)
    if lista.inserir(servico):
        print("\nServico cadastrado com sucesso! Confira os dados:")
        lista.mostrar_servico(servico)
    else:
        print("Erro: ID duplicado.")


def consultar(lista):
    id = ler_id("ID do servico: ")
    if id is None:
        return
    servico = lista.buscar_id(id)
    if servico is None:
        print("Servico nao encontrado.")
    else:
        lista.mostrar_servico(servico)


def atualizar(lista):
    id = ler_id("ID do servico que deseja atualizar: ")
    if id is None:
        return
    servico = lista.buscar_id(id)
    if servico is None:
        print("Servico nao encontrado.")
        return

    print("Digite os novos dados (Enter mantem o valor atual).")
    titulo = input("Titulo [" + servico.titulo + "]: ").strip()
    categoria = input("Categoria [" + servico.categoria + "]: ").strip()
    descricao = input("Descricao [" + servico.descricao + "]: ").strip()
    requisitos = input("Requisitos [" + servico.requisitos + "]: ").strip()
    local = input("Local [" + servico.local + "]: ").strip()

    if titulo != "":
        servico.titulo = titulo
    if categoria != "":
        servico.categoria = categoria
    if descricao != "":
        servico.descricao = descricao
    if requisitos != "":
        servico.requisitos = requisitos
    if local != "":
        servico.local = local
    print("Servico atualizado com sucesso!")


def excluir_servico(lista):
    id = ler_id("ID do servico que deseja excluir: ")
    if id is None:
        return
    servico = lista.buscar_id(id)
    if servico is None:
        print("Servico nao encontrado.")
        return

    lista.mostrar_servico(servico)
    confirmar = input("Confirma a exclusao? (s/n): ").strip().lower()
    if confirmar == "s":
        lista.excluir(id)
        print("Servico excluido com sucesso!")
    else:
        print("Exclusao cancelada.")


def pesquisar(lista):
    print("\n1 - Buscar por titulo")
    print("2 - Buscar por categoria")
    opcao = input("Escolha: ").strip()

    if opcao not in ("1", "2"):
        print("Opcao invalida.")
        return

    texto = input("Digite o termo da busca: ").strip()
    if texto == "":
        print("Erro: informe um termo para buscar.")
        return

    if opcao == "1":
        encontrou = lista.buscar_titulo(texto)
    else:
        encontrou = lista.buscar_categoria(texto)

    if not encontrou:
        print("Nenhum servico encontrado.")


def menu():
    lista = ListaEncadeada()
    print("=========================================")
    print("            CITIZEN ASSIST AI")
    print("=========================================")
    print("Sistema de consulta e gestao de SERVICOS PUBLICOS.")
    print("Cadastre orientacoes sobre atendimentos oferecidos")
    print("a populacao, como saude, documentos e educacao.")
    print("Este sistema NAO cadastra dados de cidadaos.")

    while True:
        print("\n===== CITIZEN ASSIST AI =====")
        print("1 - Cadastrar novo servico publico")
        print("2 - Ver todos os servicos cadastrados")
        print("3 - Consultar servico pelo ID")
        print("4 - Alterar dados de um servico")
        print("5 - Excluir um servico")
        print("6 - Pesquisar servicos por titulo ou categoria")
        print("7 - Ordenar servicos por titulo (A-Z)")
        print("8 - Ver total e quantidade por categoria")
        print("0 - Sair")

        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            cadastrar(lista)
        elif opcao == "2":
            lista.listar()
        elif opcao == "3":
            consultar(lista)
        elif opcao == "4":
            atualizar(lista)
        elif opcao == "5":
            excluir_servico(lista)
        elif opcao == "6":
            pesquisar(lista)
        elif opcao == "7":
            if lista.ordenar_por_titulo():
                print("Servicos ordenados por titulo!")
                lista.listar()
            else:
                print("Nenhum servico para ordenar.")
        elif opcao == "8":
            lista.analisar()
        elif opcao == "0":
            print("Encerrando Citizen Assist AI...")
            break
        else:
            print("Opcao invalida!")


if __name__ == "__main__":
    menu()
