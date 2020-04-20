# CPai Setup Guide

CPai is composed of 4 parts:

1. Dialogflow service provided by Google
2. Backend written in Python/Flask
3. Client written in Javascript(Node) - this is another backend that hosts Google Client for interacting with Dialogflow
4. Frontend written in Javascript(Vue)

## Frontend setup guide

The frontend can be built and _statically hosted_ on the web. The build environment tested was Ubuntu 18.04 LTS running on AWS EC2 instance (the same setup used for client and backend).

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

4. Install "yarn" (this setup installed v1.22) and restart the terminal.

````sh
curl -o- -L https://yarnpkg.com/install.sh | bash

1. Replace the urls for backend and client in `frontend/store/index.js`:

```js
16:         clientUrl: "http://localhost:3000/",
17:         backendUrl: "http://localhost:5000/",
````

5. Build the frontend

```sh
yarn install
yarn build
```

6. Upload the content inside `dist` folder to your choice of webserver.
