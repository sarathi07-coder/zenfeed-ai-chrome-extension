/**
 * ZenFeed Content Script - SMART VERSION
 * 
 * Features:
 * - Works on YouTube HOME PAGE
 * - Analyzes watch history and patterns
 * - Waits 3 minutes to learn behavior
 * - Detects repeated content types
 * - Provides varied productive alternatives
 */

// Configuration
const CONFIG = {
    BACKEND_URL: 'http://localhost:8000',
    SCAN_INTERVAL_MS: 2000,
    LEARNING_PERIOD_MS: 3 * 60 * 1000, // 3 minutes to learn
    ENABLE_BACKEND: true,
    MIN_ADDICTION_SCORE_FOR_BLOCK: 2,
    VARIETY_IN_ALTERNATIVES: true
};

// Smart State - Tracks user behavior
let smartState = {
    watchHistory: [],
    blockedVideos: [],
    shownAlternatives: [],
    contentPatterns: {},
    learningStartTime: Date.now(),
    isLearningMode: true,
    processedItems: new Set(),
    sessionStats: {
        itemsScanned: 0,
        interventionsApplied: 0,
        alternativesShown: 0
    }
};

// Alternative categories for variety
const ALTERNATIVE_CATEGORIES = [
    'python programming tutorial tamil',
    'python programming tutorial english',
    'java tutorial for beginners',
    'javascript tutorial',
    'DSA data structures algorithms',
    'web development course',
    'react tutorial',
    'node.js tutorial',
    'study with me pomodoro',
    'meditation for focus',
    'productivity tips',
    'coding interview preparation'
];

let currentAlternativeIndex = 0;

/**
 * Initialize ZenFeed
 */
function init() {
    console.log('[ZenFeed] 🚀 Smart Mode Initializing...');
    console.log('[ZenFeed] 📊 Learning period: 3 minutes');
    console.log('[ZenFeed] 🎯 Will analyze your patterns and block addictive content');

    loadUserPreferences();
    startSmartScanning();
    startLearningTimer();
}

/**
 * Load user preferences
 */
function loadUserPreferences() {
    try {
        chrome.storage.sync.get(['enableBackend', 'backendUrl', 'watchHistory', 'learningComplete', 'learningCompletedAt'], (result) => {
            // Check if extension context is still valid
            if (chrome.runtime.lastError) {
                console.log('[ZenFeed] Extension context invalidated, skipping preferences');
                return;
            }

            if (result.enableBackend !== undefined) {
                CONFIG.ENABLE_BACKEND = result.enableBackend;
            }
            if (result.backendUrl) {
                CONFIG.BACKEND_URL = result.backendUrl;
            }
            if (result.watchHistory) {
                smartState.watchHistory = result.watchHistory;
            }

            // Check if learning was already completed (within last 24 hours)
            if (result.learningComplete && result.learningCompletedAt) {
                const completedTime = new Date(result.learningCompletedAt);
                const now = new Date();
                const hoursSinceCompletion = (now - completedTime) / (1000 * 60 * 60);

                if (hoursSinceCompletion < 24) {
                    // Learning was completed recently, skip learning period
                    smartState.isLearningMode = false;
                    console.log('[ZenFeed] ✅ Learning already complete (skipping 3-minute wait)');
                    console.log('[ZenFeed] 🎯 Actively blocking addictive content');
                } else {
                    // Reset learning if it's been more than 24 hours
                    console.log('[ZenFeed] 🔄 Resetting learning (24+ hours since last session)');
                }
            }

            console.log('[ZenFeed] ✅ Preferences loaded');
        });
    } catch (error) {
        console.log('[ZenFeed] Could not load preferences (extension may have been reloaded)');
    }
}

/**
 * Start learning timer
 */
function startLearningTimer() {
    // Only start timer if learning is not already complete
    if (!smartState.isLearningMode) {
        return; // Already completed
    }

    setTimeout(() => {
        smartState.isLearningMode = false;
        console.log('[ZenFeed] 🎓 Learning complete! Now actively blocking addictive content.');
        analyzePatterns();

        // Save learning completion to storage
        try {
            chrome.storage.sync.set({
                learningComplete: true,
                learningCompletedAt: new Date().toISOString()
            }, () => {
                if (chrome.runtime.lastError) {
                    return;
                }
                console.log('[ZenFeed] 💾 Learning completion saved');
            });
        } catch (error) {
            // Extension context invalidated
        }
    }, CONFIG.LEARNING_PERIOD_MS);
}

/**
 * Analyze user patterns after learning period
 */
function analyzePatterns() {
    const patterns = {};

    smartState.watchHistory.forEach(item => {
        const type = detectContentType(item.title);
        patterns[type] = (patterns[type] || 0) + 1;
    });

    smartState.contentPatterns = patterns;
    console.log('[ZenFeed] 📊 Detected patterns:', patterns);

    // Find most repeated addictive content
    const addictiveTypes = Object.entries(patterns)
        .filter(([type]) => isAddictiveType(type))
        .sort((a, b) => b[1] - a[1]);

    if (addictiveTypes.length > 0) {
        console.log('[ZenFeed] ⚠️ Most addictive content:', addictiveTypes[0][0]);
    }
}

/**
 * Detect content type from title
 */
function detectContentType(title) {
    const lower = title.toLowerCase();

    if (lower.includes('short') || lower.includes('#shorts')) return 'shorts';
    if (lower.includes('meme') || lower.includes('funny')) return 'memes';
    if (lower.includes('game') || lower.includes('gaming')) return 'gaming';
    if (lower.includes('vlog')) return 'vlogs';
    if (lower.includes('react') || lower.includes('reaction')) return 'reactions';
    if (lower.includes('tutorial') || lower.includes('learn')) return 'educational';
    if (lower.includes('coding') || lower.includes('programming')) return 'coding';

    return 'other';
}

/**
 * Check if content type is addictive
 */
function isAddictiveType(type) {
    return ['shorts', 'memes', 'gaming', 'vlogs', 'reactions'].includes(type);
}

/**
 * Start smart scanning
 */
function startSmartScanning() {
    console.log('[ZenFeed] 🔍 Starting smart scanner...');
    scanFeed();
    setInterval(scanFeed, CONFIG.SCAN_INTERVAL_MS);
}

/**
 * Scan YouTube feed (HOME PAGE + Search + Shorts)
 */
function scanFeed() {
    const platform = detectPlatform();

    if (platform === 'youtube') {
        scanYouTubeFeed();
    }
}

/**
 * Detect platform
 */
function detectPlatform() {
    const hostname = window.location.hostname;
    if (hostname.includes('youtube.com')) return 'youtube';
    return 'unknown';
}

/**
 * Scan YouTube feed - ALL PAGES
 */
function scanYouTubeFeed() {
    // Comprehensive selectors for ALL YouTube pages
    const selectors = [
        // Home page
        'ytd-rich-item-renderer',
        'ytd-rich-grid-media',
        // Search results
        'ytd-video-renderer',
        'ytd-compact-video-renderer',
        // Shorts
        'ytd-reel-item-renderer',
        'ytd-shorts',
        'ytd-reel-video-renderer',
        // Sidebar
        'ytd-compact-video-renderer',
        // Watch page
        'ytd-compact-autoplay-renderer'
    ];

    selectors.forEach(selector => {
        const items = document.querySelectorAll(selector);
        items.forEach(item => processYouTubeItem(item));
    });
}

/**
 * Process a single YouTube video
 */
function processYouTubeItem(element) {
    const itemId = getElementId(element);
    if (smartState.processedItems.has(itemId)) return;

    const metadata = extractYouTubeMetadata(element);
    if (!metadata) return;

    smartState.processedItems.add(itemId);
    smartState.sessionStats.itemsScanned++;

    // Track in watch history
    smartState.watchHistory.push({
        title: metadata.title,
        timestamp: Date.now(),
        type: detectContentType(metadata.title)
    });

    // Keep only last 100 items
    if (smartState.watchHistory.length > 100) {
        smartState.watchHistory = smartState.watchHistory.slice(-100);
    }

    // Save to storage (with error handling)
    try {
        chrome.storage.sync.set({ watchHistory: smartState.watchHistory }, () => {
            if (chrome.runtime.lastError) {
                // Extension was reloaded, ignore error
                return;
            }
        });
    } catch (error) {
        // Extension context invalidated, ignore
    }

    // Classify content
    const score = classifyContent(metadata);

    // Apply intervention (only after learning period)
    if (!smartState.isLearningMode && score >= CONFIG.MIN_ADDICTION_SCORE_FOR_BLOCK) {
        applySmartIntervention(element, metadata, score);
    }
}

/**
 * Extract YouTube metadata
 */
function extractYouTubeMetadata(element) {
    try {
        const titleEl = element.querySelector('#video-title, a#video-title-link, h3');
        const title = titleEl ? (titleEl.innerText || titleEl.textContent || '').trim() : '';

        const durationEl = element.querySelector('ytd-thumbnail-overlay-time-status-renderer span, .ytd-thumbnail-overlay-time-status-renderer span');
        const durationText = durationEl ? durationEl.innerText : '';
        const durationSec = parseDuration(durationText);

        const channelEl = element.querySelector('#channel-name a, ytd-channel-name a');
        const channel = channelEl ? channelEl.innerText.trim() : '';

        const linkEl = element.querySelector('a#video-title-link, a#thumbnail');
        const url = linkEl ? linkEl.href : '';

        if (!title) return null;

        return {
            id: itemId(url),
            title,
            duration_sec: durationSec,
            channel,
            url,
            platform: 'youtube'
        };
    } catch (error) {
        return null;
    }
}

/**
 * Parse duration
 */
function parseDuration(durationText) {
    if (!durationText) return 9999;
    const parts = durationText.split(':').map(Number);
    if (parts.length === 3) return parts[0] * 3600 + parts[1] * 60 + parts[2];
    if (parts.length === 2) return parts[0] * 60 + parts[1];
    if (parts.length === 1) return parts[0];
    return 9999;
}

/**
 * Classify content with smart scoring
 */
function classifyContent(metadata) {
    const title = metadata.title.toLowerCase();
    const duration = metadata.duration_sec;
    let score = 0;

    // 18+ content keywords - HIGHEST PRIORITY
    const adult18PlusKeywords = [
        '18+', 'adult', 'nsfw', 'explicit', 'mature', 'hot', 'sexy',
        'bikini', 'model', 'onlyfans', 'bold', 'spicy', 'sensual'
    ];

    adult18PlusKeywords.forEach(keyword => {
        if (title.includes(keyword)) score += 10; // Maximum penalty
    });

    // Addictive keywords - COMPREHENSIVE LIST
    const addictiveKeywords = [
        'short', '#shorts', 'meme', 'funny', 'compilation', 'try not to laugh',
        'react', 'reaction', 'fails', 'tiktok', 'viral', 'trending',
        'challenge', 'prank', 'roast', 'cringe', 'satisfying', 'asmr',
        'unboxing', 'haul', 'vlog', 'gaming', 'highlights', 'clips',
        'entertainment', 'celebrity', 'drama', 'gossip', 'news',
        'top 10', 'best', 'worst', 'crazy', 'insane', 'epic'
    ];

    addictiveKeywords.forEach(keyword => {
        if (title.includes(keyword)) score += 5;
    });

    // Shorts are HIGHLY addictive
    if (title.includes('#shorts') || title.includes('short') || duration < 60) {
        score += 8;
    }

    // Educational keywords (reduce score)
    const educationalKeywords = [
        'tutorial', 'learn', 'study', 'lecture', 'course', 'guide',
        'how to', 'explained', 'documentary', 'programming', 'coding',
        'python', 'javascript', 'java', 'dsa', 'algorithm', 'data structure',
        'web development', 'software', 'engineering', 'science', 'math',
        'productivity', 'focus', 'meditation', 'tamil tutorial', 'english tutorial'
    ];

    educationalKeywords.forEach(keyword => {
        if (title.includes(keyword)) score -= 5;
    });

    return Math.max(0, Math.min(10, score));
}

/**
 * Check if user already watched this video
 */
function hasUserWatched(videoId) {
    // Check if this video is in watch history
    const watched = smartState.watchHistory.find(item =>
        item.title && videoId && item.title.includes(videoId)
    );
    return !!watched;
}

/**
 * Apply smart intervention with varied alternatives
 */
async function applySmartIntervention(element, metadata, score) {
    // If user already watched this addictive video, COMPLETELY REMOVE IT
    if (hasUserWatched(metadata.id)) {
        element.remove(); // Completely delete from DOM
        console.log(`[ZenFeed] 🗑️ Removed already-watched addictive content: "${metadata.title}"`);
        return;
    }

    // Get VARIED productive alternative
    const alternative = await getVariedAlternative();

    // Hide the original element
    element.style.opacity = '0.3';
    element.style.pointerEvents = 'none';
    element.style.position = 'relative';

    // Create blur overlay that covers the entire video element
    const overlay = document.createElement('div');
    overlay.className = 'zenfeed-block-overlay';
    overlay.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.85);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        z-index: 9999;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 20px;
        box-sizing: border-box;
        border-radius: 12px;
        pointer-events: auto;
    `;

    overlay.innerHTML = `
        <div style="text-align: center; color: white; pointer-events: auto;">
            <div style="font-size: 48px; margin-bottom: 16px;">🚫</div>
            <div style="font-size: 16px; font-weight: 600; margin-bottom: 20px;">Blocked Content</div>
            <div style="display: flex; gap: 12px; flex-wrap: wrap; justify-content: center; margin-bottom: 16px;">
                <a href="${alternative.url}" target="_blank" class="zenfeed-alt-btn" style="
                    background: #3ea6ff;
                    color: white;
                    padding: 10px 20px;
                    border-radius: 20px;
                    text-decoration: none;
                    font-size: 14px;
                    font-weight: 500;
                    display: inline-flex;
                    align-items: center;
                    gap: 6px;
                    cursor: pointer;
                    pointer-events: auto;
                    z-index: 10000;
                ">
                    <span>📚</span>
                    <span>Watch Alternative</span>
                </a>
                <button class="zenfeed-continue-btn" style="
                    background: rgba(255, 255, 255, 0.2);
                    color: white;
                    padding: 10px 20px;
                    border-radius: 20px;
                    border: 1px solid rgba(255, 255, 255, 0.4);
                    font-size: 14px;
                    font-weight: 500;
                    cursor: pointer;
                    pointer-events: auto;
                    z-index: 10000;
                ">
                    Continue Anyway
                </button>
            </div>
            <div style="font-size: 12px; color: #aaa; max-width: 300px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                ${alternative.title}
            </div>
        </div>
    `;

    // Add event listeners after creating the overlay
    const continueBtn = overlay.querySelector('.zenfeed-continue-btn');
    if (continueBtn) {
        continueBtn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            overlay.remove();
            element.style.opacity = '1';
            element.style.pointerEvents = 'auto';
        });
    }

    // Add hover effects
    const altBtn = overlay.querySelector('.zenfeed-alt-btn');
    if (altBtn) {
        altBtn.addEventListener('mouseenter', () => {
            altBtn.style.background = '#4fb3ff';
        });
        altBtn.addEventListener('mouseleave', () => {
            altBtn.style.background = '#3ea6ff';
        });
    }

    if (continueBtn) {
        continueBtn.addEventListener('mouseenter', () => {
            continueBtn.style.background = 'rgba(255, 255, 255, 0.3)';
        });
        continueBtn.addEventListener('mouseleave', () => {
            continueBtn.style.background = 'rgba(255, 255, 255, 0.2)';
        });
    }

    element.appendChild(overlay);

    smartState.blockedVideos.push(metadata.title);
    smartState.sessionStats.interventionsApplied++;

    console.log(`[ZenFeed] ✅ Blocked: "${metadata.title}" → Replaced with: "${alternative.title}"`);
}

/**
 * Get varied productive alternative (different each time)
 */
async function getVariedAlternative() {
    // Rotate through different categories
    const category = ALTERNATIVE_CATEGORIES[currentAlternativeIndex];
    currentAlternativeIndex = (currentAlternativeIndex + 1) % ALTERNATIVE_CATEGORIES.length;

    // Check if already shown this alternative
    if (smartState.shownAlternatives.includes(category)) {
        currentAlternativeIndex = (currentAlternativeIndex + 1) % ALTERNATIVE_CATEGORIES.length;
    }

    smartState.shownAlternatives.push(category);
    smartState.sessionStats.alternativesShown++;

    // Fetch from backend
    try {
        const response = await fetch(`${CONFIG.BACKEND_URL}/recommend?q=${encodeURIComponent(category)}&max_results=1`);
        if (response.ok) {
            const data = await response.json();
            if (data.alternatives && data.alternatives.length > 0) {
                return {
                    title: data.alternatives[0].title,
                    url: data.alternatives[0].url,
                    channel: data.alternatives[0].channel || 'Educational Channel'
                };
            }
        }
    } catch (error) {
        console.log('[ZenFeed] Using fallback alternative');
    }

    // Fallback
    return {
        title: category.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
        url: `https://youtube.com/results?search_query=${encodeURIComponent(category)}`,
        channel: 'ZenFeed Recommendations'
    };
}

/**
 * Apply blur directly to the video thumbnail element
 */
function createReplacementCard(blocked, alternative, score) {
    // Don't create a new card - modify the existing one
    // This ensures perfect fit with YouTube's layout
    const wrapper = document.createElement('div');
    wrapper.className = 'zenfeed-blur-wrapper';
    wrapper.style.cssText = `
        position: relative;
        width: 100%;
        height: 100%;
    `;

    wrapper.innerHTML = `
        <!-- Blur overlay that covers the thumbnail -->
        <div class="zenfeed-blur-overlay" style="
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            background: rgba(0, 0, 0, 0.6);
            z-index: 100;
            border-radius: 12px;
        "></div>
        
        <!-- Content overlay -->
        <div class="zenfeed-content-overlay" style="
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 101;
            padding: 16px;
            box-sizing: border-box;
        ">
            <!-- Blocked icon -->
            <div style="
                font-size: 32px;
                margin-bottom: 8px;
            ">🚫</div>
            
            <!-- Blocked text -->
            <div style="
                color: #fff;
                font-size: 13px;
                font-weight: 600;
                margin-bottom: 12px;
                text-align: center;
            ">Blocked Content</div>
            
            <!-- Buttons -->
            <div style="
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
                justify-content: center;
            ">
                <!-- Watch Alternative button -->
                <a href="${alternative.url}" target="_blank" style="
                    background: #3ea6ff;
                    color: #fff;
                    padding: 8px 14px;
                    border-radius: 18px;
                    text-decoration: none;
                    font-size: 12px;
                    font-weight: 500;
                    display: inline-flex;
                    align-items: center;
                    gap: 4px;
                    transition: background 0.2s;
                " onmouseover="this.style.background='#4fb3ff'" onmouseout="this.style.background='#3ea6ff'">
                    <span>📚</span>
                    <span>Watch Alternative</span>
                </a>
                
                <!-- Continue button -->
                <button onclick="this.closest('.zenfeed-blur-wrapper').remove()" style="
                    background: rgba(255, 255, 255, 0.15);
                    color: #fff;
                    padding: 8px 14px;
                    border-radius: 18px;
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    font-size: 12px;
                    font-weight: 500;
                    cursor: pointer;
                    transition: background 0.2s;
                " onmouseover="this.style.background='rgba(255, 255, 255, 0.25)'" onmouseout="this.style.background='rgba(255, 255, 255, 0.15)'">
                    Continue Anyway
                </button>
            </div>
            
            <!-- Alternative title -->
            <div style="
                color: #aaa;
                font-size: 11px;
                margin-top: 12px;
                text-align: center;
                max-width: 90%;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            ">${alternative.title}</div>
        </div>
    `;

    return wrapper;
}

/**
 * Get element ID
 */
function getElementId(element) {
    const link = element.querySelector('a');
    if (link && link.href) return itemId(link.href);
    return `elem_${Math.random()}`;
}

/**
 * Extract ID from URL
 */
function itemId(url) {
    if (!url) return `random_${Math.random()}`;
    const match = url.match(/[?&]v=([^&]+)/);
    return match ? match[1] : url;
}

// Initialize
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// Listen for messages (with error handling)
try {
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
        try {
            if (request.action === 'getStats') {
                sendResponse(smartState.sessionStats);
            }
        } catch (error) {
            // Extension context invalidated
        }
        return true; // Keep channel open for async response
    });
} catch (error) {
    // Extension context invalidated during listener setup
}

console.log('[ZenFeed] 🎯 Smart Content Script Loaded');
