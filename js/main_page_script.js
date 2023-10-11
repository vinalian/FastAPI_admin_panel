document.querySelector("#add-item-button").addEventListener("click", function () {
    document.querySelector("#add-item-form").classList.remove("hidden");
});

document.querySelectorAll(".delete-button").forEach(function (button) {
    button.addEventListener("click", function () {
        const row = button.closest("tr");
        const cells = row.querySelectorAll("td");
        const itemId = cells[0].textContent;

        fetch(`/main_page/delete/${itemId}`, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(response => {
            if (response.ok) {
                window.location.href = '/main_page';
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });
});


document.querySelectorAll(".edit-button").forEach(async function (button) {
    button.addEventListener("click", function () {
        document.querySelector("#edit-item-form").classList.remove("hidden");
        const row = button.closest("tr");
        const cells = row.querySelectorAll("td");
        document.querySelector("#edit-item-id").value = cells[0].textContent;
        document.querySelector("#edit-item-name").value = cells[1].textContent;
        document.querySelector("#edit-user-id").value = cells[2].textContent;
        document.querySelector("#edit-item-id").readOnly = true;
    });
});

document.getElementById("edit-item-form").addEventListener(
    "submit", async function (event) {
    event.preventDefault();
    const form = event.target;
    const data = new FormData(form);
    const formData = {};
    data.forEach((value, key) => {
        formData[key] = value;
    });
    console.log(formData)
    const response = await fetch('/main_page', {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    });

    if (response.ok) {
        window.location.href = '/main_page';
    } else {
        console.error('Error!')
    }
});

document.getElementById("edit-item-form").addEventListener(
    "reset", async function (event) {
    event.preventDefault();
    window.location.href = '/main_page';
})


document.getElementById("add-item-form").addEventListener("submit", async function (event) {
    event.preventDefault();
    const form = event.target;
    const data = new FormData(form);
    const formData = {};
    data.forEach((value, key) => {
        formData[key] = value;
    });
    console.log(formData);
    const response = await fetch('/main_page', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    });

    if (response.ok) {
        window.location.href = '/main_page';
    } else {
        console.error('Error!')
    }
});


document.getElementById("add-item-form").addEventListener(
    "reset", async function (event) {
    event.preventDefault();
    window.location.href = '/main_page';
})
