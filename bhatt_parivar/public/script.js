async function fetchFamilyData() {
    const response = await fetch('family.json');
    const familyData = await response.json();
    return familyData;
}

let familyTree; // Store the family tree instance here
let currentMode = 'light'; // Default mode

// Function to initialize FamilyTree with a specific node size based on screen width
async function initializeFamilyTree() {
    const familyData = await fetchFamilyData();

    // Destroy the existing tree if it exists
    if (familyTree) {
        familyTree.destroy();
    }

    // Set body background color based on the current mode
    if (currentMode === 'dark') {
        document.body.style.backgroundColor = '#333'; // Dark background
    } else {
        document.body.style.backgroundColor = '#fff'; // Light background
    }

    // Calculate node size based on screen width
    let nodeSize = 30; // Default node size (for larger screens)
    if (window.innerWidth <= 600) {
        nodeSize = 20; // Smaller node size for mobile devices
    }

    // Create a new FamilyTree instance with the current mode and dynamic node size
    familyTree = new FamilyTree(document.getElementById("tree"), {
        mode: currentMode,
        mouseScrool: FamilyTree.none,
        nodeBinding: {
            field_0: "name"
        },
        collapsible: true,
        enableSearch: true,
        nodeMouseClick: FamilyTree.action.expandCollapse,
        nodeSize: nodeSize // Set the calculated node size here
    });

    familyTree.load(familyData);

    // Resize nodes based on window size
    resizeNodes();
}

// Function to adjust node size dynamically based on window width
function resizeNodes() {
    const width = window.innerWidth;
    let nodeSize = 30; // Default node size for larger screens

    if (width <= 600) {  // For small screens like mobile
        nodeSize = 20; // Smaller nodes for mobile
    }

    // If FamilyTree is initialized, update the node size
    if (familyTree) {
        familyTree.setOptions({
            nodeSize: nodeSize
        });
    }
}

// Event listener to resize nodes when the window is resized
window.addEventListener('resize', resizeNodes);

// Function to toggle between dark and light modes
function toggleMode() {
    // Switch the mode
    currentMode = currentMode === 'dark' ? 'light' : 'dark';

    // Reinitialize the family tree with the new mode
    initializeFamilyTree();

    // Update button text based on the mode
    document.getElementById("toggleModeButton").innerText = 
        currentMode === 'dark' ? "Switch to Light Mode" : "Switch to Dark Mode";

    // Update button styles based on mode
    const button = document.getElementById("toggleModeButton");
    if (currentMode === 'dark') {
        button.classList.remove('light');
    } else {
        button.classList.add('light');
    }
}

// Initialize the family tree and set up the toggle button event listener
initializeFamilyTree();
document.getElementById("toggleModeButton").addEventListener("click", toggleMode);
