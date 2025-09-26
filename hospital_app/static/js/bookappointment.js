// Load doctors dynamically

async function loadDoctors() {
    try {
        const res = await fetch("/api/book/appointment/");
        const data = await res.json();

        const doctorSelect = document.getElementById('doctorSelect');
        doctorSelect.innerHTML = "";

        data.doctors.forEach(doc => {
            const option = document.createElement("option");  // fixed
            option.value = doc.id;
            option.textContent = `${doc.name} (${doc.specialty})`; 
            doctorSelect.appendChild(option);
        });
    } catch (err) {
        console.error(err);
        alert("Failed to load doctors");
    }
}
document.addEventListener("DOMContentLoaded", loadDoctors);

// Submit form
document.getElementById('appointmentForm').addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const payload = Object.fromEntries(formData.entries());

    try {
        const res = await fetch("/api/book/appointment/", {   // fixed space
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value  // fixed case
            },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (data.success) {
            window.location.href = "/appointment/success/";
        } else {
            alert(data.message);
        }
    } catch (err) {
        console.error(err);
        alert("Something went wrong");
    }
});
