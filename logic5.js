// Folder 5 - JavaScript test file (logic5.js)
console.log("Folder 5 - logic5.js loaded");

function reverseString(text) {
    return text.split("").reverse().join("");
}

document.addEventListener("DOMContentLoaded", () => {
    console.log("Reversed:", reverseString("folder5"));
});


