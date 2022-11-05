document.addEventListener("DOMContentLoaded", function(event) {
    let element = document.querySelector('.alert');
    if (element) {
        setTimeout(() => {element.remove()}, 3000)
    }

});



