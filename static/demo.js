
const body = document.getElementById("inventory-body");
const form = document.getElementById("stock-form");
const message = document.getElementById("demo-message");

const storageKey = "data-center-inventory-demo";

// 1. Read the original inventory from Flask's HTML.
const initialStock = Array.from(
    body.querySelectorAll("tr")
).map(tr => ({
    component: tr.dataset.component,
    quantity: Number(tr.dataset.quantity),
    location: tr.dataset.location
}));

// 2. Load temporary inventory from this browser tab.
let stock;

try {
    const saved = JSON.parse(sessionStorage.getItem(storageKey));

    stock = Array.isArray(saved) &&
        saved.length === initialStock.length &&
        saved.every((item, i) =>
            item.component === initialStock[i].component &&
            Number.isInteger(item.quantity) &&
            item.quantity >= 0
        )
        ? saved
        : initialStock.map(item => ({ ...item }));

} catch {
    stock = initialStock.map(item => ({ ...item }));
}

// 3. Update the table and dashboard numbers.
function renderInventory() {
    body.replaceChildren();

    for (const item of stock) {
        const tr = document.createElement("tr");

        for (const value of [
            item.component,
            item.quantity,
            item.location
        ]) {
            const td = document.createElement("td");
            td.textContent = value;
            tr.appendChild(td);
        }

        body.appendChild(tr);
    }

    document.getElementById("total-components").textContent =
        stock.length;

    document.getElementById("total-units").textContent =
        stock.reduce(
            (total, item) => total + item.quantity, 0
        );

    document.getElementById("low-stock").textContent =
        stock.filter(item => item.quantity < 10).length;
}

// 4. Handle receiving and issuing stock.
form.addEventListener("submit", function(event) {
    event.preventDefault();

    const component = form.elements.namedItem("component").value;
    const units = Number(form.elements.namedItem("units").value);
    const action = event.submitter?.value;

    const item = stock.find(row => row.component === component);

    if (!item || !Number.isInteger(units) || units <= 0) {
        message.textContent = "Enter a valid component and quantity.";
        return;
    }

    if (action === "receive") {
        item.quantity += units;

    } else if (action === "issue") {
        if (units > item.quantity) {
            message.textContent = "Insufficient stock!";
            return;
        }

        item.quantity -= units;

    } else {
        message.textContent = "Invalid operation.";
        return;
    }

    // Save only inside the recruiter's browser tab.
    sessionStorage.setItem(storageKey, JSON.stringify(stock));

    renderInventory();

    message.textContent =
        `Successfully ${action === "receive" ? "received" : "issued"} ${units} ${component} units.`;
});

// 5. Reset the demo to the original inventory.
document.getElementById("reset-demo").addEventListener("click", () => {
    stock = initialStock.map(item => ({ ...item }));

    sessionStorage.removeItem(storageKey);

    renderInventory();

    message.textContent = "Demo inventory reset!";
});

// 6. Display the inventory when the page loads.
renderInventory();
