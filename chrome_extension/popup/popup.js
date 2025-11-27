/**
 * ZenFeed Popup Script
 * Handles popup UI interactions and displays statistics
 */

// Load and display statistics
async function loadStats() {
    try {
        // Get stats from storage instead of content script
        const stats = await chrome.storage.sync.get(['itemsScanned', 'interventionsApplied', 'alternativesShown']);

        document.getElementById('itemsScanned').textContent = stats.itemsScanned || 0;
        document.getElementById('interventions').textContent = stats.interventionsApplied || 0;
        document.getElementById('alternatives').textContent = stats.alternativesShown || 0;
    } catch (error) {
        console.error('Error loading stats:', error);
        // Set defaults on error
        document.getElementById('itemsScanned').textContent = '0';
        document.getElementById('interventions').textContent = '0';
        document.getElementById('alternatives').textContent = '0';
    }
}

// Toggle main ZenFeed functionality
document.getElementById('mainToggle').addEventListener('click', function () {
    this.classList.toggle('active');
    const isActive = this.classList.contains('active');

    chrome.storage.sync.set({ zenfeedActive: isActive });

    // Notify content script (if available)
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs[0]) {
            chrome.tabs.sendMessage(tabs[0].id, {
                action: 'toggleZenFeed',
                enabled: isActive
            }, () => {
                // Ignore errors if content script not ready
                if (chrome.runtime.lastError) {
                    console.log('Content script not ready yet');
                }
            });
        }
    });
});

// Toggle backend analysis
document.getElementById('backendToggle').addEventListener('click', function () {
    this.classList.toggle('active');
    const isActive = this.classList.contains('active');

    chrome.storage.sync.set({ enableBackend: isActive });

    // Notify content script (if available)
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs[0]) {
            chrome.tabs.sendMessage(tabs[0].id, {
                action: 'toggleBackend',
                enabled: isActive
            }, () => {
                // Ignore errors if content script not ready
                if (chrome.runtime.lastError) {
                    console.log('Content script not ready yet');
                }
            });
        }
    });
});

// View full dashboard
document.getElementById('viewDashboard').addEventListener('click', () => {
    chrome.tabs.create({ url: 'dashboard.html' });
});

// Reset statistics
document.getElementById('resetStats').addEventListener('click', () => {
    if (confirm('Reset all statistics?')) {
        chrome.storage.sync.set({
            itemsScanned: 0,
            interventionsApplied: 0,
            alternativesShown: 0
        });

        loadStats();
    }
});

// Load saved settings
chrome.storage.sync.get(['zenfeedActive', 'enableBackend'], (result) => {
    if (result.zenfeedActive !== false) {
        document.getElementById('mainToggle').classList.add('active');
    }

    if (result.enableBackend) {
        document.getElementById('backendToggle').classList.add('active');
    }
});

// Refresh stats every 2 seconds
setInterval(loadStats, 2000);

// Initial load
loadStats();
