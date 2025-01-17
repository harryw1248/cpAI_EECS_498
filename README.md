# CPai Setup Guide

## CPai Introduction
CPai is a chatbot that uses Conversational Artificial Intelligence and Natural Language Processing to help people fill out their taxes. CPai adjusts the questions it asks based on the information users provides. It aims to minimize the number of questions asked to make filling out taxes easier. CPai can also help explain complicated tax terms and maximize the amount of deductions for a person. This makes CPai an effective tax assistant.   


CPai is composed of 4 parts:

1. Dialogflow service provided by Google
2. Backend written in Python/Flask
3. Client written in Javascript(Node) - this is another backend that hosts Google Client for interacting with Dialogflow
4. Frontend written in Javascript(Vue)

## Import CPai Dialogflow engine

Open the existing agent you would like to export from/import into in DialogFlow
On the left-hand list, go to the top and click on the settings icon next to your agent name

<img src='dialogflow1.png'/>

Click on the Export/Import tab

<img src='dialogflow2.png'/>

If exporting, “Export as zip”, if importing, “Import from zip” and choose `cpai_dialogflow_engine.zip`.

The backend and client can be hosted on any NIX server as long as their dependencies can be installed.
However, in this guide, we will use AWS EC2 instances (Ubuntu).

When your backend is setup, you will need to change your fulfillment link on DialogFlow to match your webhook. For all intents that will need to communicate with the backend, you will need to turn on web fulfillment at the bottom.

## Client Setup Guide

1. Launch a new EC2 instance by choosing Ubuntu Server 18.04 LTS (HVM), SSD Volume Type - ami-0fc20dd1da406780b (64-bit x86).

-   Configure your security group so that SSH and TCP PORT 3000 are allowed.

2. SSH into the newly launched EC2 instance and update the system:

```sh
> sudo apt update; sudo apt -y upgrade;
```

3. Install Node.js (this setup installed v13.13.0, the latest version)

```sh
curl -sL https://deb.nodesource.com/setup_13.x | sudo -E bash -
sudo apt-get install -y nodejs
```

3. Install "yarn" (this setup installed v1.22) and restart the terminal.

```sh
curl -o- -L https://yarnpkg.com/install.sh | bash
```

4. Run the following inside `client` folder

```sh
yarn install
```

5. Export your Google Client Credentials/Secret:
   Please follow and obtain your credentials here: https://cloud.google.com/dialogflow/docs/quick/setup#nodejs

```
export GOOGLE_APPLICATION_CREDENTIALS="cpAI-24a315a29ddb.json"
export CPAI_CLIENT_SECRET="rZBCihS0FEG84jnHGh8XD9Z5lGWg0GQe"
```

6. Export the name of your Dialogflow project:

```
export GCP_PROJECT_ID=<your project id>
```

Finally to run:

```
yarn start
```

## Backend Setup Guide

We tested the backend with both python3.7 and python3.6. For this setup, use the default Python3.6 that ships with Ubuntu18.04.

1. Launch a new EC2 instance by choosing Ubuntu Server 18.04 LTS (HVM), SSD Volume Type - ami-0fc20dd1da406780b (64-bit x86).

-   Configure your security group so that SSH, HTTP (PORT 80) and HTTPS (PORT 443) are allowed.

2. SSH into the newly launched EC2 instance and update the system:

```sh
> sudo apt update; sudo apt -y upgrade;
```

3. Copy `backend` folder into the EC2 instance (rsync or git clone) and run the following commands inside the directory (enter yes to all prompts):

-`poppler-utils` is required for a Python module used for converting PDFs to JPEGs.

```sh
sudo apt install -y gcc
sudo apt install -y python3-pip
sudo apt install -y poppler-utils
pip3 install --upgrade pip
pip3 install wheel
pip3 install -r requirements.txt
export FLASK_APP=app.py
export FLASK_ENV=production
```

4. Run the backend:

```sh
sudo python3 -m flask run --host=0.0.0.0 --port=<target port> > ~/log &
```

Google Dialogflow requires that the backend uses HTTP over TLS. You can either configure your EC2 instance to forward all HTTP requests to HTTPS after running the backend app on port 80 or directly run the python app on port 443. As a work around, you may also run `ngrok` which can forward all external traffic to our EC2 instance over HTTP/TLS.

## Frontend setup guide

The frontend can be built and _statically hosted_ on the web. The build environment tested was Ubuntu 18.04 LTS running on AWS EC2 instance (the same setup used for client and backend) and the following packages need to be installed:

> node.js

> yarn

1. Replace the urls for backend and client in `frontend/store/index.js`:

```js
16:         clientUrl: "http://localhost:3000/",
17:         backendUrl: "http://localhost:5000/",
```

2. Build the frontend

```sh
yarn install
yarn build
```

3. Upload the content inside `dist` folder to your choice of webserver.
