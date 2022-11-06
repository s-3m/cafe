document.addEventListener("DOMContentLoaded", function(event) {

    let element = document.querySelector('.alert');
    if (element) {
        setTimeout(() => {element.remove()}, 3000)
    }

   let source = new EventSource('/listen');
    source.addEventListener("message", function (e) {
        if (e.data !== 'None') {console.log(e.data)}
    }, false)

});



