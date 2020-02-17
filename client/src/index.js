import express from "express";
const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Imports the Google Cloud client library.
const { Storage } = require("@google-cloud/storage");

const dialogflow = require("dialogflow");
const uuid = require("uuid");

/**
 * Send a query to the dialogflow agent, and return the query result.
 * @param {string} projectId The project to be used
 */
async function runQuery(projectId, query) {
    // A unique identifier for the given session
    const sessionId = uuid.v4();

    // Create a new session
    const sessionClient = new dialogflow.SessionsClient();
    const sessionPath = sessionClient.sessionPath(projectId, sessionId);

    // The text query request.
    const request = {
        session: sessionPath,
        queryInput: {
            text: {
                // The query to send to the dialogflow agent
                text: "What is earned income credit?",
                // The language used by the client (en-US)
                languageCode: "en-US"
            }
        }
    };

    // Send request and log result
    const responses = await sessionClient.detectIntent(request);
    console.log("Detected intent");
    const result = responses[0].queryResult;
    console.log(`  Query: ${result.queryText}`);
    console.log(`  Response: ${result.fulfillmentText}`);
    if (result.intent) {
        console.log(`  Intent: ${result.intent.displayName}`);
    } else {
        console.log(`  No intent matched.`);
    }

    return result.fulfillmentText;
}

async function gCloudConnect() {
    // Instantiates a client. If you don't specify credentials when constructing
    // the client, the client library will look for credentials in the
    // environment.
    const storage = new Storage();

    try {
        // Makes an authenticated API request.
        const results = await storage.getBuckets();

        const [buckets] = results;

        console.log("Buckets:");
        buckets.forEach(bucket => {
            console.log(bucket.name);
        });
    } catch (err) {
        console.error("ERROR:", err);
    }
}

async function helloWorld(req, res) {
    res.send("Hello World!");
}
app.get("/", helloWorld);

async function query(req, res) {
    await gCloudConnect();
    const response = await runQuery("cpai-dweaie");
    console.log(response);
    res.send(response);
}
app.post("/query", query);

app.listen(3000, () => console.log("node client on port 3000!"));
