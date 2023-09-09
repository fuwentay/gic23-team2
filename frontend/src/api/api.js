export async function get(url, body, setLoadingCallback = null) {
    const requestOptions = {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        // body: JSON.stringify(body),
    };

    return await fetchJson(url, requestOptions, setLoadingCallback);
}

export async function post(url, body, setLoadingCallback = null) {
    const requestOptions = {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body),
    };

    return await fetchJson(url, requestOptions, setLoadingCallback);
}

export async function postFile(url, file, setLoadingCallback = null) {
    const formData = new FormData();
    formData.append("file", file);
    const requestOptions = {
        method: "POST",
        files: file,
        body: formData,
    };

    return await fetchJson(url, requestOptions, setLoadingCallback);
}

async function fetchJson(url, requestOptions, setLoadingCallback) {
    if (setLoadingCallback != null) setLoadingCallback(true);
    const res = await fetch(url, requestOptions);
    const json = await res.json();
    if (setLoadingCallback != null) setLoadingCallback(false);
    return json;
}