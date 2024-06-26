# THIS README IS VERY OUTDATED - will update soon

## TJ API and Crawler

The two services are efficient and customizable, designed to handle a large volume of court cases. They have a robust capacity to manage and handle multiple simultaneous requests for cases without compromising speed or resource usage.

## Services

### API
https://github.com/BrenoAlberto/juriscrape-api

### Crawlers
https://github.com/BrenoAlberto/juriscrape-crawlers

## Installation and Execution

0. Clone the repositories:

```shell
gh repo clone BrenoAlberto/juriscrape-api
gh repo clone BrenoAlberto/juriscrape-crawlers
```

To run the project, you can use Docker:

```shell
docker compose up
```

If you don't have Docker, follow the steps below:

1. Go to the `juriscrape-crawlers` directory and install the dependencies:

```shell
cd juriscrape-crawlers
npm install
npm run build
npm run start
```

2. Repeat the process in the `juriscrape-api` directory:

```shell
cd juriscrape-api
npm install
npm run build
npm run start
```

3. Remember to change the MongoDB URL in the `.env` file of the `juriscrape-api` project.

## Notable Components

### PageManager & PreloadedFirstDegreePageManager

These components preload certain pages with isolated contexts for crawler use. You can configure the number of pages to be preloaded according to the needs of your project.

### CaseProcessor

This is a background processing queue that constantly handles a predetermined number of simultaneous crawlers. Due to the limited information about the rate limiting of the Courts of Justice, I have set the default number to 10 simultaneous processes. This value can be adjusted. Every 2 seconds, a routine runs to check for new data to be added to the database.

These variables can be customized in the `juriscrape-crawlers/src/setup.ts` file.

## API Usage

### Requesting Cases

To use the API, you can make a POST request to the `/fetch-court-cases` endpoint. This request returns a list of case numbers and their respective tracking statuses:

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

### API Response

The API will return a JSON array with the case number and the respective tracking status for each case:

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

When the cases have the status "available", you can fetch the data of specific cases using the `/get-court-cases` endpoint:

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

### TODO

- [ ] Review the whole project and map necessary improvements.
- [ ] Better logging strategy.
- [ ] Retry strategy for failed requests.
- [ ] Persist the data. Right now the data is stored in the ephemeral k8s pod.
- [ ] Remove custom broker and use a more robust solution.
- [ ] Improve README.md.