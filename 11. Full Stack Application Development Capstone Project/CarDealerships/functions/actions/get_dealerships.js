/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

const COUCH_URL = "";
const IAM_API_KEY = "";

function main() {
    const authenticator = new IamAuthenticator({ apikey: IAM_API_KEY });
    const cloudant = CloudantV1.newInstance({
        authenticator: authenticator
    });
    
    cloudant.setServiceUrl(COUCH_URL);

    let dealerships = getAllRecords(cloudant, 'dealerships');
    
    return dealerships;
}

function getAllRecords(cloudant, dbname) {
    return new Promise((resolve, reject) => {
        cloudant.postAllDocs({ db: dbname, includeDocs: true, limit: 10 })
            .then((result) => {
                resolve({ result: result.result.rows });
            })
            .catch(err => {
                console.error(err);
                reject({ err: err });
            });
    });
}