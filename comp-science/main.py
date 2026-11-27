
from itertools import product


# ==========================================
# CITIZEN ASSIST AI
# Global Solution GS26_2
# Disciplina: Computer Science
# ==========================================


def apresentar_programa():
    """Apresenta o objetivo e o funcionamento do sistema."""

    print("\n" + "=" * 60)
    print("                    CITIZEN ASSIST AI")
    print("          ORIENTADOR DE SERVICOS PUBLICOS")
    print("=" * 60)

    print("""
BEM-VINDO AO CITIZEN ASSIST AI!

O QUE E ESTE PROGRAMA?

O Citizen Assist AI e um prototipo academico desenvolvido
para auxiliar cidadaos na identificacao dos proximos passos
para solicitar atendimento em servicos publicos.

O sistema utiliza logica booleana para analisar tres
condicoes e fornecer orientacoes simples e objetivas.

COMO FUNCIONA?

O programa considera tres informacoes:

A - DOCUMENTACAO:
    Verifica se o cidadao possui todos os documentos
    exigidos para o atendimento.

B - AGENDAMENTO:
    Verifica se o servico exige agendamento previo.

C - DISPONIBILIDADE:
    Verifica se existe horario disponivel para agendamento.

Para cada pergunta, informe:

    1 = SIM
    0 = NAO

O programa identifica todas as pendencias relevantes
e apresenta orientacoes para cada uma delas.

EXPRESSAO LOGICA UTILIZADA:

    S = A AND (NOT B OR C)

S = 1: Pode prosseguir para a proxima etapa.
S = 0: Existem pendencias a resolver.

O programa tambem permite executar testes automaticos
com todas as 8 combinacoes possiveis das entradas.

IMPORTANTE:
Este sistema e apenas um prototipo academico.
Nao representa um canal oficial do governo.
Nao realiza agendamentos nem confirma a concessao
de servicos ou direitos.

As respostas nao sao armazenadas.
Consulte sempre os canais oficiais para confirmar
os requisitos e a disponibilidade dos servicos.
""")

    print("=" * 60)
    input("\nPressione ENTER para acessar o menu principal...")


def expressao_original(a, b, c):
    """Expressao canonica: mintermos 4, 5 e 7."""

    return (
        (a and not b and not c)
        or (a and not b and c)
        or (a and b and c)
    )


def expressao_simplificada(a, b, c):
    """Expressao simplificada pelo mapa de Karnaugh."""

    return a and (not b or c)


def ler_booleano(pergunta):
    """Aceita somente os valores 0 e 1."""

    while True:
        valor = input(pergunta).strip()

        if valor in ("0", "1"):
            return int(valor)

        print("\nEntrada invalida! Digite apenas 0 ou 1.\n")


def obter_orientacao(a, b, c):
    """Identifica todas as pendencias relevantes."""

    resultado = int(expressao_simplificada(a, b, c))

    orientacoes = []

    # Verifica a documentacao
    if a == 0:
        orientacoes.append(
            "DOCUMENTACAO: Sua documentacao esta incompleta. "
            "Consulte os requisitos oficiais e regularize "
            "os documentos necessarios."
        )
    else:
        orientacoes.append(
            "DOCUMENTACAO: Sua documentacao esta completa."
        )

    # Verifica a necessidade de agendamento
    if b == 0:
        orientacoes.append(
            "AGENDAMENTO: O servico nao exige agendamento "
            "previo. Consulte os canais oficiais para "
            "verificar como realizar o atendimento."
        )

    else:
        if c == 0:
            orientacoes.append(
                "AGENDAMENTO: O servico exige agendamento, "
                "mas nao ha horario disponivel. Consulte "
                "novamente os canais oficiais."
            )
        else:
            orientacoes.append(
                "AGENDAMENTO: O servico exige agendamento "
                "e existe horario disponivel para solicitacao."
            )

    # Conclusao da analise
    if resultado == 1:
        orientacoes.append(
            "CONCLUSAO: Voce pode prosseguir para a proxima "
            "etapa do atendimento, conforme as condicoes "
            "informadas."
        )
    else:
        orientacoes.append(
            "CONCLUSAO: Existem pendencias que precisam "
            "ser resolvidas antes de prosseguir."
        )

    return resultado, orientacoes


def consultar_orientacao():
    """Realiza uma consulta interativa."""

    print("\n" + "=" * 50)
    print("CONSULTA DE ORIENTACAO")
    print("=" * 50)

    print("\nResponda utilizando 0 (Nao) ou 1 (Sim).\n")

    a = ler_booleano(
        "A - Possui todos os documentos exigidos? "
    )

    b = ler_booleano(
        "B - O servico exige agendamento? "
    )

    # A disponibilidade so importa se houver agendamento
    if b == 1:
        c = ler_booleano(
            "C - Existe horario disponivel? "
        )
    else:
        c = 0
        print(
            "\nO servico nao exige agendamento. "
            "A disponibilidade de horario nao se aplica."
        )

    resultado, orientacoes = obter_orientacao(a, b, c)

    print("\n" + "-" * 50)
    print("RESULTADO DA CONSULTA")
    print("-" * 50)

    print(f"\nEntradas: A={a}, B={b}, C={c}")
    print(f"Saida logica (S): {resultado}")

    print("\nANALISE DA SITUACAO:\n")

    for orientacao in orientacoes:
        print(f"- {orientacao}\n")

    print("AVISO:")
    print(
        "Este e um prototipo academico, nao um canal oficial. "
        "Nao confirma agendamentos, concessao de servicos "
        "ou direitos."
    )

    print("-" * 50)


def executar_testes():
    """Valida todas as combinacoes da tabela-verdade."""

    print("\n" + "=" * 65)
    print("VALIDACAO AUTOMATICA DA TABELA-VERDADE")
    print("=" * 65)

    print(
        f"{'A':<4}{'B':<4}{'C':<4}"
        f"{'Original':<12}{'Simplificada':<15}"
        f"{'Programa':<12}{'Status'}"
    )

    print("-" * 65)

    total = 0
    aprovados = 0

    for a, b, c in product((0, 1), repeat=3):

        original = int(expressao_original(a, b, c))
        simplificada = int(expressao_simplificada(a, b, c))
        programa, orientacoes = obter_orientacao(a, b, c)

        indice_mintermo = 4 * a + 2 * b + c
        esperado = int(indice_mintermo in (4, 5, 7))

        aprovado = (
            original == simplificada == programa == esperado
        )

        # Verifica se todas as pendencias sao mencionadas
        texto = " ".join(orientacoes)

        if a == 0:
            aprovado = aprovado and (
                "incompleta" in texto
            )

        if b == 1 and c == 0:
            aprovado = aprovado and (
                "nao ha horario disponivel" in texto
            )

        status = "OK" if aprovado else "FALHOU"

        print(
            f"{a:<4}{b:<4}{c:<4}"
            f"{original:<12}{simplificada:<15}"
            f"{programa:<12}{status}"
        )

        total += 1

        if aprovado:
            aprovados += 1

    print("-" * 65)
    print(f"Testes aprovados: {aprovados}/{total}")

    if aprovados == total:
        print("RESULTADO: Todas as combinacoes foram validadas!")
    else:
        print("RESULTADO: Foram encontradas divergencias!")


def exibir_menu():
    """Exibe o menu principal."""

    while True:
        print("\n" + "=" * 45)
        print("           CITIZEN ASSIST AI")
        print("=" * 45)

        print("1 - Consultar orientacao")
        print("2 - Executar testes automaticos")
        print("3 - Sair")

        opcao = input("\nEscolha uma opcao: ").strip()

        if opcao == "1":
            consultar_orientacao()

        elif opcao == "2":
            executar_testes()

        elif opcao == "3":
            print("\nEncerrando o Citizen Assist AI...")
            break

        else:
            print("\nOpcao invalida! Escolha 1, 2 ou 3.")


if __name__ == "__main__":
    apresentar_programa()
    exibir_menu()
