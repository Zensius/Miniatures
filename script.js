
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
