function clickEvent(element) {
    clickedElement = element.target.id;
    console.log(clickedElement);
}
console.log("main.js loaded")
document.addEventListener('DOMContentLoaded', clickEvent);