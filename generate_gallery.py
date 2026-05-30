import os
import json

# Configuration
MINIS_DIR = "minis"
OUTPUT_HTML = "index.html"
OUTPUT_JS = "script.js"

def build_gallery():
    if not os.path.exists(MINIS_DIR):
        print(f"Error: '{MINIS_DIR}' folder not found.")
        return

    # 1. Scan for miniatures and their sequential frames
    gallery_data = {}
    miniatures = sorted([d for d in os.listdir(MINIS_DIR) if os.path.isdir(os.path.join(MINIS_DIR, d))])

    for mini in miniatures:
        mini_path = os.path.join(MINIS_DIR, mini)
        # Get all images, sorted so they rotate in order
        images = sorted([
            f"{MINIS_DIR}/{mini}/{img}" 
            for img in os.listdir(mini_path) 
            if img.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
        ])
        if images:
            gallery_data[mini] = images

    # 2. Generate the HTML File
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Miniature 360° Showcase</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #121212; color: #e0e0e0; margin: 0; padding: 20px; }}
        .container {{ max-width: 1100px; margin: 0 auto; display: flex; gap: 30px; }}
        .sidebar {{ width: 250px; background: #1e1e1e; padding: 15px; border-radius: 8px; height: fit-content; }}
        .sidebar h2 {{ margin-top: 0; color: #fff; font-size: 1.2rem; border-bottom: 1px solid #333; padding-bottom: 10px; }}
        .mini-btn {{ display: block; width: 100%; text-align: left; background: none; border: none; color: #aaa; padding: 10px; cursor: pointer; border-radius: 4px; font-size: 1rem; }}
        .mini-btn:hover {{ background: #2a2a2a; color: #fff; }}
        .mini-btn.active {{ background: #ff4b4b; color: #fff; font-weight: bold; }}
        .main-content {{ flex: 1; background: #1e1e1e; padding: 25px; border-radius: 8px; display: flex; flex-direction: column; align-items: center; }}
        .viewer-container {{ width: 100%; max-width: 600px; position: relative; cursor: ew-resize; user-select: none; background: #000; border-radius: 8px; overflow: hidden; }}
        .viewer-container img {{ width: 100%; display: block; pointer-events: none; }}
        .instructions {{ color: #888; font-size: 0.9rem; margin-top: 15px; }}
        h1 {{ text-align: center; color: #fff; margin-bottom: 30px; }}
    </style>
</head>
<body>

    <h1>🎨 Miniature 360° Gallery</h1>
    
    <div class="container">
        <div class="sidebar">
            <h2>My Collection</h2>
            <div id="mini-list"></div>
        </div>
        
        <div class="main-content">
            <h2 id="mini-title">Select a Miniature</h2>
            <div class="viewer-container" id="viewer">
                <img id="viewer-img" src="" alt="Select a miniature to begin">
            </div>
            <p class="instructions">↔️ Click and drag left/right on the image to rotate</p>
        </div>
    </div>

    <script>
        // Inject the image data directly from Python
        const galleryData = {json.dumps(gallery_data)};
    </script>
    <script src="{OUTPUT_JS}"></script>
</body>
</html>
"""

    # 3. Generate the JavaScript File (Handles the true click-and-drag physics)
    js_content = """
const miniListContainer = document.getElementById('mini-list');
const viewerImg = document.getElementById('viewer-img');
const miniTitle = document.getElementById('mini-title');
const viewerContainer = document.getElementById('viewer');

let currentMini = "";
let currentFrameIndex = 0;
let isDragging = false;
let startX = 0;

// Initialize Sidebar Buttons
Object.keys(galleryData).forEach((miniName, index) => {
    const btn = document.createElement('button');
    btn.classList.add('mini-btn');
    btn.textContent = miniName.replace(/_/g, ' ').toUpperCase();
    btn.onclick = () => loadMini(miniName, btn);
    miniListContainer.appendChild(btn);
    
    // Load first mini by default
    if(index === 0) loadMini(miniName, btn);
});

function loadMini(name, btn) {
    document.querySelectorAll('.mini-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    
    currentMini = name;
    currentFrameIndex = 0;
    miniTitle.textContent = name.replace(/_/g, ' ').toUpperCase();
    updateViewer();
}

function updateViewer() {
    if (galleryData[currentMini] && galleryData[currentMini].length > 0) {
        viewerImg.src = galleryData[currentMini][currentFrameIndex];
    }
}

// True Drag-to-Rotate Physics Engine
viewerContainer.addEventListener('mousedown', (e) => {
    isDragging = true;
    startX = e.clientX;
});

window.addEventListener('mouseup', () => isDragging = false);

window.addEventListener('mousemove', (e) => {
    if (!isDragging || !currentMini) return;
    
    const totalFrames = galleryData[currentMini].length;
    if (totalFrames <= 1) return;

    const deltaX = e.clientX - startX;
    // Sensitivity: how many pixels of mouse movement equals switching 1 frame
    const pixelsPerFrame = 12; 

    if (Math.abs(deltaX) > pixelsPerFrame) {
        if (deltaX > 0) {
            // Drag right -> spin one way
            currentFrameIndex = (currentFrameIndex + 1) % totalFrames;
        } else {
            // Drag left -> spin the other way
            currentFrameIndex = (currentFrameIndex - 1 + totalFrames) % totalFrames;
        }
        startX = e.clientX; // Reset tracking point
        updateViewer();
    }
});

// Touch support for mobile phones
viewerContainer.addEventListener('touchstart', (e) => {
    isDragging = true;
    startX = e.touches[0].clientX;
});
window.addEventListener('touchend', () => isDragging = false);
viewerContainer.addEventListener('touchmove', (e) => {
    if (!isDragging || !currentMini) return;
    const totalFrames = galleryData[currentMini].length;
    const deltaX = e.touches[0].clientX - startX;
    const pixelsPerFrame = 12;

    if (Math.abs(deltaX) > pixelsPerFrame) {
        if (deltaX > 0) {
            currentFrameIndex = (currentFrameIndex + 1) % totalFrames;
        } else {
            currentFrameIndex = (currentFrameIndex - 1 + totalFrames) % totalFrames;
        }
        startX = e.touches[0].clientX;
        updateViewer();
    }
});
"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)
    with open(OUTPUT_JS, "w", encoding="utf-8") as f:
        f.write(js_content)

    print("🚀 Success! index.html and script.js generated. Ready for GitHub Pages!")

if __name__ == "__main__":
    build_gallery()