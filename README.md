# 🧪 TBDA Project

Aplicação construída com Streamlit para visualização e análise de dados.

## 🗄️ Banco de dados

Este projeto utiliza **MongoDB** como banco de dados.

O seed da base está em:

`db/provedores.json`

## Desafios

Utilizando a base de dados de provedores de Pelotas e o MongoDB, crie 7 arquivos em PHP, Node ou Python, com saída em HTML, para atender os seguintes requisitos:

1. Crie um arquivo para visualizar os dados de acessos em Pelotas para uma data selecionada entre as disponíveis no sistema.

- <b>R: encontra-se na página "Assinantes por data".</b>

2. Há um erro nos registros de 2010 todos os documentos com mais de 20 clientes estão com 1 cliente a menos. Crie uma função para corrigir esse erro.

- <b>R: resolução documentada na seção [Registros de 2010 com quantidade errada](#registros-de-2010-com-quantidade-errada).</b>

3. Crie um gráfico de linha com eixo horizontal de tempo em anos e eixo vertical de número de assinantes para a base de dados fornecida. Adicione um filtro para selecionar um provedor entre os disponíveis e que caso fique em branco selecione todos os provedores.

- <b>R: encontra-se na página "Assinantes por ano"</b>

4. Crie uma tabela contendo o número de cliente de provedores, de grande porte em percentual, versus o número de clientes de pequeno porte a cada ano, para todo o período de amostragem. São considerados provedores de grande porte=2 e de pequeno porte os que possuem porte=3. Crie um filtro que permita definir uma velocidade mínima e máxima e mostre apenas dados com clientes entre essas velocidades.

- <b>R: encontra-se na página "Grande vs pequeno"</b>

5. Faça uma variação do exercício 3 para mostrar os dados em um gráfico de áreas acumuladas por tecnologia de conexão. Modifique o filtro do exercício 3 para permitir a seleção de ,mais de um provedor.

- <b>R: encontra-se na página "Assinantes por tecnologia"</b>

6. Os dados fornecidos possuem registros duplicados. Remova os dados redundantes via programação.

- <b>R: resolução documentada na seção [Registros duplicados](#registros-duplicados)</b>

## Ajuste de dados

### Registros de 2010 com quantidade errada

Há um erro nos registros de 2010 todos os documentos com mais de 20 clientes estão com 1 cliente a menos. Crie uma função para corrigir esse erro. Para resolver, utilizei o seguinte comando:

```js
db.provedores.updateMany(
  {
    mensuracao: {
      $gte: "2010-01-01",
      $lt: "2011-01-01",
    },
  },
  {
    $inc: { qtd: 1 },
  },
);
```

Ao total, 61 documentos foram alterados:

```json
{
  "acknowledged": true,
  "insertedId": null,
  "matchedCount": 61,
  "modifiedCount": 61,
  "upsertedCount": 0
}
```

### Registros duplicados

Os dados fornecidos possuem registros duplicados. Remova os dados redundantes via programação.

```js
const duplicated_providers = db.provedores
  .aggregate([
    {
      $group: {
        _id: {
          grupo: "$grupo",
          empresa: "$empresa",
          cnpj: "$cnpj",
          porte: "$porte",
          faixa: "$faixa",
          velocidade: "$velocidade",
          tecnologia: "$tecnologia",
          meio: "$meio",
          tpessoa: "$tpessoa",
          tproduto: "$tproduto",
          qt: "$qt",
          mensuracao: "$mensuracao",
        },
        ids: { $push: "$_id" },
      },
    },
    {
      $match: {
        "ids.1": { $exists: true },
      },
    },
  ])
  .toArray();

const ids_to_delete = duplicated_providers.map((item) => item.ids.shift());
db.provedores.deleteMany({ _id: { $in: ids_to_delete } });
```

Com isso, 768 dados duplicados foram deletados.

---

## 🚀 Requisitos

- Python 3.12+
- Poetry
- MongoDB

---

## ⚙️ Setup do ambiente

### 1. Instalar Poetry

```bash
pipx install poetry
```

---

> Alternativa com `pip`:

```bash
pip install poetry
```

---

### 2. Instalar dependências do projeto

```bash
poetry install
```

## ▶️ Rodar o projeto

```bash
poetry run streamlit run app.py
```

Depois disso, o app vai abrir automaticamente no navegador:

```
http://localhost:8501
```

---

## 🧠 Dicas

- Você pode usar `poetry shell` para entrar no ambiente
- Ou executar tudo com `poetry run` sem ativar shell
- Para sair do shell do Poetry:

```bash
exit
```

---

## 📁 Estrutura (exemplo)

```
.
├── db/
│   └── provedores.json
├── app.py
└── pyproject.toml
```

## 📌 Observações

Projeto local para análise de dados com Streamlit. Pode ser facilmente adaptado para deploy em cloud (Streamlit Cloud, AWS, etc).
