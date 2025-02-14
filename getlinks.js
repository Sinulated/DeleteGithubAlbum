window.artworkUrls = new Set(); // Use a Set to store unique URLs

// Scroll down in fast increments and ensure all content loads
async function iterativeScroll() {
    return new Promise((resolve) => {
        let lastHeight = 0;
        let attempts = 0;
        let maxAttempts = 10; // Number of times to check if no more content is loading

        let scrollInterval = setInterval(() => {
            let currentHeight = document.documentElement.scrollHeight;
            window.scrollBy(0, 600); // Scroll down faster (adjust if needed)

            if (currentHeight === lastHeight) {
                attempts++; // Increase attempt count if nothing new is loading
            } else {
                attempts = 0; // Reset attempts if new content appears
            }

            lastHeight = currentHeight; // Update last known scroll height

            // Stop scrolling when no more content appears after several checks
            if (attempts >= maxAttempts) {
                clearInterval(scrollInterval);
                resolve(); // Proceed to collecting links
            }
        }, 300); // Faster interval (adjust as needed)
    });
}

// Monitor AJAX-loaded content in real time
function monitorNewLinks() {
    const targetNode = document.querySelector(".RMUi2");

    if (!targetNode) return;

    const observer = new MutationObserver(() => {
        collectArtworkLinks(); // Run collection whenever new content appears
    });

    observer.observe(targetNode, { childList: true, subtree: true });
}

// Collect artwork links, ensuring no duplicates
function collectArtworkLinks() {
    document.querySelectorAll(".RMUi2 a").forEach(link => {
        let url = link.href;

        if (url.endsWith("#comments")) {
            return; // Skip links that end with #comments
        }

        if (!link.dataset.collected && url.includes("/art/")) { 
            artworkUrls.add(url);
            link.dataset.collected = "true"; // Mark as collected to prevent duplicates
        }
    });

    console.log(`Collected ${artworkUrls.size} links so far...`); // Log progress
}

// Generate and download the file after ensuring all links are collected
function downloadUrlsFile() {
    if (artworkUrls.size === 0) {
        alert("No artwork links found!");
        return;
    }

    let urlList = Array.from(artworkUrls).join("\n"); // Convert Set to newline-separated string
    let blob = new Blob([urlList], { type: "text/plain" }); // Create a Blob
    let link = document.createElement("a");

    link.href = URL.createObjectURL(blob);
    link.download = "artwork_links.txt"; // Set the filename
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link); // Cleanup
}

// Main execution flow
(async function main() {
    console.log("Setting up real-time link monitoring...");
    monitorNewLinks(); // Start monitoring dynamically added content

    console.log("Scrolling down in fast increments...");
    await iterativeScroll(); // Scroll gradually but quickly until all content is loaded

    console.log("Waiting briefly for any late-loaded elements...");
    await new Promise(resolve => setTimeout(resolve, 2000)); // Short final wait

    console.log("Final link collection...");
    collectArtworkLinks(); // Final pass to ensure all links are collected

    console.log("Collected", artworkUrls.size, "links. Downloading file...");
    downloadUrlsFile(); // Generate and download the file
})();

window.getArtworkUrls = function () {
    return Array.from(window.artworkUrls);
};