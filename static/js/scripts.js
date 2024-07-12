document.addEventListener('DOMContentLoaded', (event) => {
    const detectedObjectsElement = document.getElementById('detected-objects');

    setInterval(() => {
        fetch('/detected_objects')
            .then(response => response.json())
            .then(data => {
                detectedObjectsElement.innerText = `Detected Objects: ${data.detected_objects.join(', ')}`;
            });
    }, 1000);
});
