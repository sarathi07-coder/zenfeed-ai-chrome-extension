/**
 * ZenFeed Background Service Worker
 * 
 * Handles:
 * - Extension lifecycle
 * - Cross-origin requests
 * - Response caching
 * - User preferences
 */

console.log('[ZenFeed Background] Service worker initialized');

// Cache for backend responses
const responseCache = new Map();
const CACHE_DURATION_MS = 5 * 60 * 1000; // 5 minutes

/**
 * Handle extension installation
 */
chrome.runtime.onInstalled.addListener((details) => {
    if (details.reason === 'install') {
        console.log('[ZenFeed Background] Extension installed');

        // Set default preferences
        chrome.storage.sync.set({
            zenfeedActive: true,
            enableBackend: false,
            backendUrl: 'http://localhost:8000',
            minAddictionScoreForBlur: 6,
            minAddictionScoreForNudge: 3
        });

        // Open welcome page
        chrome.tabs.create({
            url: 'popup/popup.html'
        });
    } else if (details.reason === 'update') {
        console.log('[ZenFeed Background] Extension updated');
    }
});

/**
 * Handle messages from content scripts
 */
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'analyzeContent') {
        // Handle backend analysis request
        handleBackendAnalysis(request.data)
            .then(sendResponse)
            .catch(error => {
                console.error('[ZenFeed Background] Analysis error:', error);
                sendResponse({ error: error.message });
            });

        return true; // Keep channel open for async response
    }

    if (request.action === 'clearCache') {
        responseCache.clear();
        sendResponse({ success: true });
    }
});

/**
 * Handle backend analysis with caching
 */
async function handleBackendAnalysis(contentData) {
    // Check cache first
    const cacheKey = JSON.stringify(contentData);
    const cached = responseCache.get(cacheKey);

    if (cached && Date.now() - cached.timestamp < CACHE_DURATION_MS) {
        console.log('[ZenFeed Background] Using cached response');
        return cached.data;
    }

    // Get backend URL from storage
    const settings = await chrome.storage.sync.get(['backendUrl', 'enableBackend']);

    if (!settings.enableBackend) {
        return { error: 'Backend analysis disabled' };
    }

    const backendUrl = settings.backendUrl || 'http://localhost:8000';

    try {
        // Make request to backend
        const response = await fetch(`${backendUrl}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(contentData)
        });

        if (!response.ok) {
            throw new Error(`Backend returned ${response.status}`);
        }

        const data = await response.json();

        // Cache the response
        responseCache.set(cacheKey, {
            data: data,
            timestamp: Date.now()
        });

        // Clean old cache entries
        cleanCache();

        return data;

    } catch (error) {
        console.error('[ZenFeed Background] Backend request failed:', error);
        throw error;
    }
}

/**
 * Clean expired cache entries
 */
function cleanCache() {
    const now = Date.now();
    for (const [key, value] of responseCache.entries()) {
        if (now - value.timestamp > CACHE_DURATION_MS) {
            responseCache.delete(key);
        }
    }
}

/**
 * Periodic cache cleanup
 */
setInterval(cleanCache, 60 * 1000); // Every minute

console.log('[ZenFeed Background] Service worker ready');

