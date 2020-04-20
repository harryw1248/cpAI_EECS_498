koeul
vkraman
risnayak
harrydw
vahluw
gmkang

# CPai


## Overview of the components

CPai is composed of 4 parts.

1. Dialogflow service provided by Google
2. Backend written in Python/Flask
3. Client written in Javascript(Node) - this is another backend that hosts Google Client for interacting with Dialogflow
4. Frontend written in Javascript(Vue)


The frontend can be statically hosted and interacts with both the client (to send and receive utterances/reponses) and backend (for receiving a pdf/image of the tax form being filled on the backend)

The client hosts Google API Client that allows it to pass along utterances and user inputs to the Dialogflow engine.

The backend interacts with the Dialogflow and responds to PDF and image requests made by the frontend.
(it additionally queries the Firebase database storing the explanation for tax-form related terminology).

There is no direct interaction between the client and the backend.

