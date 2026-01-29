let previousUrl = ""

// function to send the url to your python server
async function sendUrlToPython(url) {
    const result = await chrome.storage.local.get(['trackingEnabled']);

    if (result.trackingEnabled === false) {
        console.log("Tracking paused by user.");
        return; 
    }

    if (previousUrl && previousUrl !== url) {
        chrome.storage.local.set({ previousUrl: previousUrl });
    }
    previousUrl = url;


    try {
        await fetch("http://localhost:5000/update-url", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: url })
        });
        console.log("Sent:", url);
    } catch (error) {
        console.log("Server likely offline:", error);
    }
}

// user switches tabs
chrome.tabs.onActivated.addListener(async (activeInfo) => {
    try {
        const tab = await chrome.tabs.get(activeInfo.tabId);
        if (tab.url) {
            sendUrlToPython(tab.url);
        }
    } catch (e) { /* ignore errors */ }
});

// listen when user navigates to new url in the same tab
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete' && tab.url) {
        sendUrlToPython(tab.url);
    }
});