import ApiConnector from "@/assets/utils/axios/factory.js";

export async function createResource(endpoint, data, onSuccess=response=>{}, onError=error=>{}) {
    return new Promise( async (resolve, reject) => {
        ApiConnector.post(endpoint, data).then(
            response => {
                onSuccess(response);
                resolve(response);
            }
        ).catch(error => {
            onError(error);
            reject(error);
        });
    });
}

export async function readResource(endpoint, onSuccess=response=>{}, onError=error=>{}) {
    return new Promise( async (resolve, reject) => {
        ApiConnector.get(endpoint).then(
            response => {
                onSuccess(response);
                resolve(response);
            }
        ).catch(error => {
            onError(error);
            reject(error);
        });
    });
}

export async function updateResource(endpoint, data, onSuccess=response=>{}, onError=error=>{}) {
    return new Promise( async (resolve, reject) => {
        ApiConnector.patch(endpoint, data).then(
            response => {
                onSuccess(response);
                resolve(response);
            }
        ).catch(error => {
            onError(error);
            reject(error);
        });
    });
}

export async function deleteResource(endpoint, onSuccess=response=>{}, onError=error=>{}) {
    return new Promise( async (resolve, reject) => {
        ApiConnector.delete(endpoint).then(
            response => {
                onSuccess(response);
                resolve(response);
            }
        ).catch(error => {
            onError(error);
            reject(error);
        });
    });
}