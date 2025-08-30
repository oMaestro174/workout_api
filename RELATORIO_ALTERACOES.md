# Relatório de Alterações - Desafio Workout API

## Introdução

Este documento detalha as modificações e melhorias implementadas na `workout_api` como parte do desafio proposto. As alterações visam aprimorar a funcionalidade, a robustez e a usabilidade da API, focando em quatro áreas principais:

1.  **Filtragem de Dados:** Adição de filtros na consulta de atletas.
2.  **Customização de Resposta:** Otimização da estrutura de dados retornada.
3.  **Tratamento de Erros:** Manipulação de exceções de integridade de dados.
4.  **Paginação:** Implementação de um sistema de paginação para lidar com grandes volumes de dados.

A seguir, cada uma dessas implementações é detalhada.

---

## 1. Adição de Query Parameters na Rota de Atletas

### O que foi feito?

O endpoint `GET /atletas` foi aprimorado para permitir a filtragem de atletas com base no `nome` e/ou no `cpf`. Isso torna a consulta de dados mais flexível e poderosa.

### Implementação Técnica

Foram adicionados parâmetros de consulta (query parameters) opcionais à função que gerencia a rota. A lógica de consulta ao banco de dados foi atualizada para incluir cláusulas `WHERE` dinâmicas, que são aplicadas somente se os parâmetros forem fornecidos na requisição.

**Exemplo de uso:**

* **Filtrar por nome:**
    ```http
    GET /atletas?nome=Joao
    ```
* **Filtrar por CPF:**
    ```http
    GET /atletas?cpf=12345678900
    ```
* **Filtrar por nome E CPF:**
    ```http
    GET /atletas?nome=Joao&cpf=12345678900
    ```

---

## 2. Customização da Resposta de Retorno (`GET /atletas`)

### O que foi feito?

Para otimizar o tráfego de dados e fornecer uma resposta mais limpa e focada, o endpoint `GET /atletas` agora retorna uma lista simplificada de atletas, contendo apenas os seguintes campos:
* `nome`
* `categoria`
* `centro_treinamento`

### Implementação Técnica

Foi criado um novo schema Pydantic, `AtletaListOut`, que define a estrutura de dados de saída desejada. O `response_model` do endpoint foi atualizado para utilizar este novo schema, garantindo que a API retorne apenas os campos especificados.

**Exemplo de corpo da resposta (`response body`):**

```json
[
  {
    "nome": "Joao",
    "categoria": "Scale",
    "centro_treinamento": "CT King"
  },
  {
    "nome": "Maria",
    "categoria": "RX",
    "centro_treinamento": "CT Bodybuilding"
  }
]
```

---

## 3. Tratamento de Exceção de Integridade (CPF Duplicado)

### O que foi feito?

A API agora é capaz de tratar tentativas de cadastro de atletas com um CPF que já existe na base de dados. Isso garante a integridade dos dados e fornece um feedback claro ao usuário.

### Implementação Técnica

A lógica de criação de atletas, na rota `POST /atletas`, foi encapsulada em um bloco `try...except`. O sistema agora captura a exceção `sqlalchemy.exc.IntegrityError`, que ocorre quando há uma violação de chave única (constraint `unique`) no banco de dados.

Ao capturar essa exceção, a API retorna:
* **Status Code:** `303 See Other` (conforme solicitado nas instruções).
* **Mensagem de Erro:** Um JSON detalhando o conflito.

**Exemplo de resposta de erro:**

```json
{
  "detail": "Já existe um atleta cadastrado com o cpf: 12345678900"
}
```

---

## 4. Adição de Paginação

### O que foi feito?

Para garantir a performance e a escalabilidade da API ao lidar com um grande número de atletas, foi implementado um sistema de paginação no endpoint `GET /atletas`.

### Implementação Técnica

Foi utilizada a biblioteca `fastapi-pagination`, uma solução robusta e bem integrada ao ecossistema FastAPI. A implementação consistiu em:
1.  Instalar e configurar a biblioteca no projeto (`add_pagination(app)`).
2.  Atualizar o `response_model` da rota para `Page[AtletaListOut]`.
3.  Utilizar a função `paginate` para processar e formatar a lista de resultados.

A paginação é controlada pelos query parameters `page` e `size`.

**Exemplo de uso:**

* **Acessar a primeira página, com 20 itens por página:**
    ```http
    GET /atletas?page=1&size=20
    ```

**Exemplo de corpo da resposta (`response body`):**

```json
{
  "items": [
    {
      "nome": "Joao",
      "categoria": "Scale",
      "centro_treinamento": "CT King"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 20,
  "pages": 1
}
```

## Conclusão

As alterações implementadas modernizaram a API, tornando-a mais eficiente, robusta e fácil de usar. Os novos recursos de filtragem, paginação e tratamento de erros aprimoram significativamente a experiência do desenvolvedor e a performance geral da aplicação.
