const resizableGrid = function(table) {
    const cols = table.getElementsByTagName('th');
    [].forEach.call(cols, function(col) {
        // Add mouse down event listener
        col.addEventListener('mousedown', function(e) {
            const curCol = e.target;
            const x = e.pageX;
            const w = curCol.offsetWidth;
            
            // Add mousemove event listener
            const mouseMoveHandler = function(e) {
                const dx = e.pageX - x;
                if (w + dx > 100) { // Minimum width check
                    curCol.style.width = (w + dx) + 'px';
                }
            };
            
            // Add mouseup event listener
            const mouseUpHandler = function() {
                document.removeEventListener('mousemove', mouseMoveHandler);
                document.removeEventListener('mouseup', mouseUpHandler);
            };
            
            document.addEventListener('mousemove', mouseMoveHandler);
            document.addEventListener('mouseup', mouseUpHandler);
        });
    });
};

// Initialize resizable columns when document is loaded
document.addEventListener('DOMContentLoaded', function() {
    const tables = document.getElementsByTagName('table');
    [].forEach.call(tables, resizableGrid);
});

// Re-initialize when Streamlit reruns
window.addEventListener('load', function() {
    const tables = document.getElementsByTagName('table');
    [].forEach.call(tables, resizableGrid);
});