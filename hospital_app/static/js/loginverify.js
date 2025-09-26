document.getElementById('loginForm').addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const payload = Object.fromEntries(formData.entries());

    try {
        const res = await fetch("/api/patient/verify/", {
            method: "post",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
            },
            body: JSON.stringify(payload)


        });
        const data = await res.json();
        if (data.success) {
            window.location.href = "/bookappointment/render/"
        } else {
            alert(data.message)
        }
    }catch(err){
        console.log(err);
        alert("Something went wrong!!")
        
    }
});