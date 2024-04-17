document.addEventListener('DOMContentLoaded', function() {
    // Make items draggable
    document.querySelectorAll('.drag-item').forEach(item => {
        item.addEventListener('dragstart', e => {
            e.dataTransfer.setData('text/plain', e.target.id);
        });
    });

    // Setup drop placeholders to accept draggables
    document.querySelectorAll('.drop-placeholder').forEach(placeholder => {
        placeholder.addEventListener('dragover', e => {
            e.preventDefault();  // Allow the drop by preventing the default
        });

        placeholder.addEventListener('drop', e => {
            e.preventDefault();
            const id = e.dataTransfer.getData('text/plain');
            const draggableElement = document.getElementById(id);

            // Clear any previous content in the drop target
            while (placeholder.firstChild) {
                placeholder.removeChild(placeholder.firstChild);
            }

            // Append the draggable element to the drop target
            placeholder.appendChild(draggableElement);

            // Update the hidden input with the id of the draggable element
            document.getElementById('step' + placeholder.dataset.step).value = id;
        });
    });
});

document.querySelectorAll('.drop-placeholder').forEach(placeholder => {
    placeholder.addEventListener('drop', e => {
        e.preventDefault();
        const id = e.dataTransfer.getData('text/plain');
        const draggableElement = document.getElementById(id);

        // Ensure only one element in the placeholder
        if (placeholder.children.length > 1) {
            placeholder.removeChild(placeholder.children[0]);
        }

        placeholder.appendChild(draggableElement);
        
        // Update the hidden input for the dropped element
        placeholder.querySelector('input').value = id;
    });
});
