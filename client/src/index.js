import express from "express";
import cors from "cors";
import helmet from "helmet";

const app = express();

app.use(helmet());
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Imports the Google Cloud client library.
const { Storage } = require("@google-cloud/storage");

const dialogflow = require("dialogflow");
const uuid = require("uuid");

async function newSession(projectId) {
    // A unique identifier for the given session
    const sessionId = uuid.v4();

    // Create a new session
    const sessionClient = new dialogflow.SessionsClient();
    const sessionPath = sessionClient.sessionPath(projectId, sessionId);

    return { sessionClient, sessionPath };
}

let sessionInfo = null;

/**
 * Send a query to the dialogflow agent, and return the query result.
 */
async function runQuery(sessionInfo, query) {
    let sessionPath = sessionInfo["sessionPath"];
    let sessionClient = sessionInfo["sessionClient"];
    // The text query request.
    const request = {
        session: sessionPath,
        queryInput: {
            text: {
                // The query to send to the dialogflow agent
                text: query,
                // The language used by the client (en-US)
                languageCode: "en-US",
            },
        },
    };

    // Send request and log result
    const responses = await sessionClient.detectIntent(request);
    console.log("Detected intent");
    const result = responses[0].queryResult;
    const responseText = result.fulfillmentMessages[0]["text"]["text"][0];

    let resultFields = result.parameters.fields;
    if (result.intent) {
        console.log(`  Intent: ${result.intent.displayName}`);
    } else {
        console.log(`  No intent matched.`);
    }

    console.log(responseText);
    const responseData = {
        responseText,
        intent: result.intent.displayName,
        params: resultFields,
    };

    return responseData;
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
        buckets.forEach((bucket) => {
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
    res.header("Access-Control-Allow-Origin", "*");
    res.header(
        "Access-Control-Allow-Headers",
        "Origin, X-Requested-With, Content-Type, Accept"
    );

    const response = await runQuery(sessionInfo, req.body.query);
    res.send(response);
}
app.post("/query", query);

app.listen(3000, async function () {
    console.log("node client on port 3000!");
    console.log("ready");
    await gCloudConnect();
    const projectId = process.env.GCP_PROJECT_ID; //cpai-dweaie
    sessionInfo = await newSession(projectId);
    console.log(sessionInfo);
});
