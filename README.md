# cpAI_EECS_498

## How to run frontend

### Install "yarn"

```sh
curl -o- -L https://yarnpkg.com/install.sh | bash
```

### 1. Run the client

```sh
cd client
yarn install
```

Then run the following (copy/paste them into your terminal)

```
export GOOGLE_APPLICATION_CREDENTIALS="cpAI-24a315a29ddb.json"
export CPAI_CLIENT_SECRET="rZBCihS0FEG84jnHGh8XD9Z5lGWg0GQe"
```

Finally to run:

```
yarn start
```

### 2. run the actual frontend (on another terminal window)

```
yarn install
yarn serve
```

Then go to http://localhost:8080/
(use chrome)
