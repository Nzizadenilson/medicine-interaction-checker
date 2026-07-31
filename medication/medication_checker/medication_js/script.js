const medicine_name = document.getElementById("medicine");
const form = document.getElementById("medicationform");
const results = document.getElementById("results");
const button = document.getElementById("button");
const filter = document.getElementById("filter");

function checkMedicine() {
    if (medicine_name.value.trim() === "") {
        alert("Please enter a medicine name.");
        return false;
    }
    return true;
}

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    if (!checkMedicine()) {
        return;
    }
    button.disabled = true;
    button.textContent = "Searching...";

    try {
        const response = await fetch(`/medicine?medicine=${encodeURIComponent(medicine_name.value)}`);
        const data = await response.json();
        if (data.error) {
            results.innerHTML = `<p>${data.error}</p>`;
        }
        else {
            let output = `
            <div class="medicine-card">
                <h2>${data.name}</h2>
            `;
            if (filter.value === "all" || filter.value === "description") {
               output += `
                   <h3>Description</h3>
                   <p>${data.description}</p>
             `;
            }
            if (filter.value === "all" || filter.value === "warnings") {
               output += `
                   <h3>Warnings</h3>
                   <p>${data.warnings}</p>
             `;
            }
            if (filter.value === "all" || filter.value === "dosage") {
               output += `
                   <h3>Dosage</h3>
                   <p>${data.dosage}</p>
             `;
            }
            if (filter.value === "all" || filter.value === "instructions") {
               output += `
                   <h3>Instructions</h3>
                   <p>${data.instructions}</p>
             `;
            
            }
            output += `</div>`;

            results.innerHTML = output;
        }
    }
    catch (error) {
        results.innerHTML = `<p>Unable to retrieve medicine information.</p>`;

    }
    button.disabled = false;
    button.textContent = "Search";
});
