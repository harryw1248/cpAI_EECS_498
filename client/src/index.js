import express from "express";
import cors from "cors";
import helmet from "helmet";
/*
import session from "express-session";

const { CPAI_CLIENT_SECRET = CPAI_CLIENT_SECRET } = process.env;
app.use(
    session({
        secret: CPAI_CLIENT_SECRET,
        resave: false,
        saveUninitialized: true,
        cookie: {
            maxAge: 1000 * 60 * 60 * 24 // 24 hours,
        }
    })
);
*/

const app = express();

app.use(helmet());
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

/*
const users = [{ id: 1, username: "cpai", password: "superduper" }];

app.post("/login", (req, res) => {
    const { username, password } = req.body;
    console.log(username, password);
});
*/

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

function checkParams(resultFields, responseData) {
    // TODO rewrite
    if (
        resultFields["given-name"] &&
        resultFields["given-name"]["stringValue"] !== ""
    ) {
        responseData["data"]["given-name"] =
            resultFields["given-name"]["stringValue"];
        console.log(responseData["data"]["given-name"]);
    }
    if (
        resultFields["last-name"] &&
        resultFields["last-name"]["stringValue"] !== ""
    ) {
        responseData["data"]["last-name"] =
            resultFields["last-name"]["stringValue"];
        console.log(responseData["data"]["last-name"]);
    }
    if (
        resultFields["zip-code"] &&
        resultFields["zip-code"]["stringValue"] !== ""
    ) {
        responseData["data"]["zip-code"] =
            resultFields["zip-code"]["stringValue"];
        console.log(responseData["data"]["zip-code"]);
    }
    if (
        resultFields["social_security"] &&
        resultFields["social_security"]["stringValue"] !== ""
    ) {
        responseData["data"]["social_security"] =
            resultFields["social_security"]["stringValue"];
        console.log(responseData["data"]["social_security"]);
    }
    if (
        resultFields["location"] &&
        resultFields["location"]["kind"] === "structValue"
    ) {
        console.log(resultFields["location"]["structValue"]["fields"]);
        responseData["data"]["location"] =
            resultFields["location"]["structValue"]["fields"];
        console.log(responseData["data"]["location"]);
    }
}
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
                languageCode: "en-US"
            }
        }
    };

    // Send request and log result
    const responses = await sessionClient.detectIntent(request);
    console.log("Detected intent");
    const result = responses[0].queryResult;
    const responseText = result.fulfillmentMessages[0]["text"]["text"][0];
    //console.log(`  Query: ${result.queryText}`);
    //console.log(`  Response: ${result.fulfillmentText}`);
    //console.log(result.fulfillmentMessages[0]["text"]["text"][0]);
    //console.log(result);
    let resultFields = result.parameters.fields;
    console.log("parametres:", resultFields);

    if (result.intent) {
        console.log(`  Intent: ${result.intent.displayName}`);
    } else {
        console.log(`  No intent matched.`);
    }

    console.log(responseText);
    const responseData = {
        responseText,
        data: {},
        intent: result.intent.displayName
    };
    checkParams(resultFields, responseData);
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
    res.header("Access-Control-Allow-Origin", "*");
    res.header(
        "Access-Control-Allow-Headers",
        "Origin, X-Requested-With, Content-Type, Accept"
    );

    const response = await runQuery(sessionInfo, req.body.query);
    res.send(response);
}
app.post("/query", query);

app.listen(3000, async function() {
    console.log("node client on port 3000!");
    console.log("ready");
    await gCloudConnect();
    sessionInfo = await newSession("cpai-dweaie");
    console.log(sessionInfo);
});
