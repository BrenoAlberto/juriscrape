# TJ API e Crawler

Os dois serviços são eficientes e personalizáveis, projetados para manipular um grande volume de processos judiciais. Possuem capacidade robusta de gerenciar e lidar com múltiplas solicitações de processos simultaneamente sem comprometer a velocidade ou o uso de recursos.

## Instalação e Execução

0. Clone os repositórios:

```shell
    gh repo clone BrenoAlberto/tribunal-de-justica-api
    gh repo clone BrenoAlberto/tribunal-de-justica-crawlers
```

Para executar o projeto, você pode utilizar o Docker:

```shell
docker compose up
```

Se não possuir Docker, siga os passos abaixo:

1. Entre no diretório `tribunal-de-justica-crawlers` e instale as dependências:

```shell
cd tribunal-de-justica-crawlers
npm install
npm run build
npm run start
```

2. Repita o processo no diretório `tribunal-de-justica-api`:

```shell
cd tribunal-de-justica-api
npm install
npm run build
npm run start
```

3. Lembre-se de alterar a URL do MongoDB no arquivo `.env` do projeto `tribunal-de-justica-api`.

## Componentes Notáveis

### PageManager & PreloadedFirstDegreePageManager

Estes componentes pré-carregam determinadas páginas com contextos isolados para uso do crawler. Você pode configurar o número de páginas a serem pré-carregadas de acordo com as necessidades do seu projeto.

### CaseProcessor

Esta é uma fila de processamento em segundo plano que lida constantemente com um número pré-determinado de crawlers simultaneamente. Devido à limitação de informações sobre os rate limiting dos Tribunais de Justiça, defini como padrão o número de 10 processos simultâneos. Este valor pode ser ajustado. A cada 2 segundos, uma rotina é executada para verificar se há novos dados disponíveis para serem adicionados ao banco de dados.

Essas variáveis podem ser customizadas no arquivo `tribunal-de-justica-crawlers/src/setup.ts`.

## Uso da API

### Solicitação de Processos

Para usar a API, você pode fazer uma requisição POST para o endpoint `/fetch-court-cases`. Esta requisição retorna uma lista com os números dos processos e seus respectivos status de rastreamento:

```shell
curl --location 'localhost:3000/fetch-court-cases' \
--header 'Content-Type: application/json' \
--data '{
    "caseNumbers": [
        "0710802-55.2018.8.02.0001",
        ...
        "0050996-50.2021.8.06.0122"
    ]
}'
```

### Resposta da API

A API retornará um array JSON com o número do processo e o respectivo status de rastreamento para cada processo:

```json
[
    {
        "caseNumber": "0710802-55.2018.8.02.0001",
        "crawlStatus": "scheduling"
    },
    ...
    {
        "caseNumber": "0050996-50.2021.8.06.0122",
        "crawlStatus": "available"
    }
]
```

Quando os processos estiverem com status "available", você pode buscar os dados de processos específicos usando o endpoint `/get-court-cases`:

```shell
curl --location 'localhost:3000/get-court-cases' \
--header 'Content-Type: application/json' \
--data '{
   

 "caseNumbers": [
        "0070337-91.2008.8.06.0001",
        "0710802-55.2018.8.02.0001"
    ]
}'
```
