document.getElementById("registerForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    console.log("Form submitted!");

    const formData = new FormData(this);
    const payload = Object.fromEntries(formData.entries());

    try {
        const res = await fetch("/api/register/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
            },
            body: JSON.stringify(payload)
        });

        if (res.ok) {
            const data = await res.json();
            console.log("API Response:", data);
            window.location.href = "/api/register/done/";  //  redirect
        } else {
            const err = await res.json();
            alert("Error: " + JSON.stringify(err));
        }
    } catch (error) {
        console.error(error);
        alert("Something went wrong!");
    }
});