const medicine_name = document.getElementById("medicine");
const form = document.getElementById("medicationform");
const button = document.getElementById("button");

function checkMedicine() {
    if (medicine_name.value.trim() === "") {
        alert("Please enter a medicine name.");
        return false;
    }
    return true;
}

form.addEventListener("submit", function (event) {
    if (!checkMedicine()) {
        event.preventDefault();
        return;
    }
    button.disabled = true;
    button.textContent = "Searching...";
});
