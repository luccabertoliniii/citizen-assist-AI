# Citizen Assist AI – Gerenciamento de Serviços Públicos

## Sobre o projeto

O Citizen Assist AI é um protótipo de sistema desenvolvido em Python para organizar informações sobre serviços públicos e facilitar o acesso a orientações destinadas aos cidadãos.

O sistema permite cadastrar, consultar, atualizar, excluir, pesquisar, ordenar e analisar serviços relacionados às áreas de saúde, documentação, educação, assistência social e serviços urbanos.

O projeto foi desenvolvido com foco na aplicação prática de estruturas de dados e algoritmos, utilizando uma interface interativa via terminal.

## Principais funcionalidades

- Cadastro de serviços públicos.
- Listagem dos serviços cadastrados.
- Consulta de serviços por ID.
- Atualização de informações.
- Exclusão de registros com confirmação.
- Pesquisa por título ou categoria.
- Ordenação alfabética dos serviços.
- Análise da quantidade de serviços por categoria.
- Validação das informações inseridas pelo usuário.

## Tecnologias utilizadas

- Python 3
- Programação orientada a objetos (POO)
- Estruturas de dados
- Lista simplesmente encadeada
- Busca sequencial
- Selection Sort
- Operações CRUD
- Análise de complexidade Big-O

## Modelagem dos dados

Cada serviço cadastrado possui seis atributos:

| Atributo | Descrição |
|---|---|
| ID | Identificador numérico, positivo e único |
| Título | Nome do serviço |
| Categoria | Área de atendimento |
| Descrição | Finalidade do serviço |
| Requisitos | Documentos e condições necessárias |
| Local | Local de atendimento |

## Estrutura de dados

O sistema utiliza uma lista simplesmente encadeada, implementada manualmente, sem utilizar listas nativas do Python como estrutura principal de armazenamento.

A implementação é dividida em três classes:

- **Servico:** representa os dados de cada serviço.
- **No:** armazena um objeto Servico e uma referência para o próximo nó.
- **ListaEncadeada:** gerencia os registros e as operações realizadas sobre a estrutura.

Representação da estrutura:

    Início → [Serviço A] → [Serviço B] → [Serviço C] → None

Cada nó possui uma referência para o próximo elemento, permitindo operações de inserção, busca, percurso e remoção.

## Algoritmos implementados

### Busca sequencial

Utilizada para localizar serviços por ID, título ou categoria, percorrendo os nós da lista encadeada.

As pesquisas por título e categoria permitem correspondências parciais e não diferenciam letras maiúsculas de minúsculas.

### Selection Sort

Algoritmo de ordenação implementado manualmente para organizar os serviços em ordem alfabética.

O algoritmo percorre os registros, identifica o menor título e realiza a troca dos objetos armazenados nos nós, preservando a estrutura de referências da lista encadeada.

A implementação não utiliza as funções nativas sort() ou sorted() do Python.

## Análise de complexidade

| Operação | Complexidade temporal |
|---|---|
| Inserção | O(n) |
| Busca por ID | O(n) |
| Busca por título ou categoria | O(n) |
| Listagem | O(n) |
| Atualização | O(n) |
| Exclusão | O(n) |
| Selection Sort | O(n²) |
| Análise de registros | O(n) em média |

A análise considera o custo computacional das operações conforme a quantidade de registros armazenados.

## Validação e tratamento de erros

O sistema possui mecanismos de validação para evitar inconsistências durante sua utilização:

- Bloqueio de IDs duplicados.
- Validação de números inteiros positivos.
- Tratamento de entradas inválidas.
- Bloqueio de campos obrigatórios vazios.
- Verificação da existência de registros.
- Confirmação antes da exclusão de serviços.
- Tratamento de opções inválidas no menu.

## Como executar

É necessário possuir o Python 3 instalado.

O projeto utiliza apenas recursos da biblioteca padrão do Python, não sendo necessária a instalação de dependências externas.

Abra o terminal na pasta do projeto e execute:

```bash
python main.py
```

## Cenários de teste

O plano de testes contempla:

- Listagem de uma estrutura vazia.
- Cadastro de múltiplos serviços.
- Tentativas de cadastro com IDs duplicados.
- Inserção de dados inválidos.
- Consulta de registros inexistentes.
- Pesquisa por título e categoria.
- Atualização e exclusão de registros.
- Ordenação alfabética.
- Análise de registros por categoria.

## Limitações e melhorias futuras

Atualmente, os dados são armazenados em memória e são perdidos após o encerramento do programa.

O sistema não possui integração com órgãos públicos, banco de dados, autenticação ou interface gráfica.

Possíveis melhorias incluem:

- Implementação de armazenamento persistente.
- Integração com banco de dados.
- Desenvolvimento de uma interface gráfica.
- Implementação de filtros avançados.
- Aprimoramento do mecanismo de pesquisa.

## Conhecimentos aplicados

O desenvolvimento deste projeto permitiu aplicar conhecimentos de programação orientada a objetos, estruturas de dados, algoritmos de busca e ordenação, análise de complexidade computacional, validação de dados e desenvolvimento de sistemas interativos.

---

Projeto acadêmico desenvolvido durante a Global Solution de 2026 da FIAP.
