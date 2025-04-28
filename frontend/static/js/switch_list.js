document.addEventListener('DOMContentLoaded', function () {
    const collapsibleButton = document.querySelector('.collapsible-button');
    const collapsibleContent = document.querySelector('.collapsible-content');

    collapsibleButton.addEventListener('click', function () {
        collapsibleContent.style.display = 
            collapsibleContent.style.display === 'block' ? 'none' : 'block';
    });
});