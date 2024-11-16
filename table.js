function initializeTable() {
    const thElements = document.querySelectorAll('th');
    let isResizing = false;
    let currentTh = null;
    let startX = 0;
    let startWidth = 0;

    // Add resize functionality
    thElements.forEach(th => {
        th.addEventListener('mousedown', handleMouseDown);
        th.addEventListener('dblclick', autoSizeColumn);
    });

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);

    // Add control buttons
    addTableControls();
}

function handleMouseDown(e) {
    // Only trigger on the right edge
    if (e.offsetX > e.target.offsetWidth - 8) {
        isResizing = true;
        currentTh = e.target;
        startX = e.pageX;
        startWidth = currentTh.offsetWidth;
        
        // Prevent text selection while resizing
        document.body.style.userSelect = 'none';
    }
}

function handleMouseMove(e) {
    if (!isResizing) return;
    
    const width = startWidth + (e.pageX - startX);
    if (width > 100) { // Minimum width
        currentTh.style.width = `${width}px`;
    }
}

function handleMouseUp() {
    isResizing = false;
    currentTh = null;
    document.body.style.userSelect = '';
}

function autoSizeColumn(e) {
    const th = e.target;
    const index = Array.from(th.parentElement.children).indexOf(th);
    const table = th.closest('table');
    let maxWidth = 0;

    // Check header content width
    const headerWidth = th.scrollWidth;
    maxWidth = Math.max(maxWidth, headerWidth);

    // Check cell contents width
    table.querySelectorAll(`tr td:nth-child(${index + 1})`).forEach(td => {
        const cellWidth = td.scrollWidth;
        maxWidth = Math.max(maxWidth, cellWidth);
    });

    // Add padding
    maxWidth += 40;
    
    // Set width with limits
    th.style.width = `${Math.min(Math.max(maxWidth, 100), 800)}px`;
}

function addTableControls() {
    const container = document.querySelector('.table-container');
    const controls = document.createElement('div');
    controls.className = 'table-controls';
    
    // Auto-size all columns button
    const autoSizeBtn = document.createElement('button');
    autoSizeBtn.className = 'control-button';
    autoSizeBtn.textContent = 'Auto-size All Columns';
    autoSizeBtn.onclick = autoSizeAllColumns;
    
    // Reset columns button
    const resetBtn = document.createElement('button');
    resetBtn.className = 'control-button';
    resetBtn.textContent = 'Reset Columns';
    resetBtn.onclick = resetColumns;
    
    controls.appendChild(autoSizeBtn);
    controls.appendChild(resetBtn);
    container.insertBefore(controls, container.firstChild);
}

function autoSizeAllColumns() {
    const thElements = document.querySelectorAll('th');
    thElements.forEach(th => {
        const event = new MouseEvent('dblclick');
        th.dispatchEvent(event);
    });
}

function resetColumns() {
    const thElements = document.querySelectorAll('th');
    thElements.forEach(th => {
        th.style.width = '';
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeTable);