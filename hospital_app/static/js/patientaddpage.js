document.addEventListener("DOMContentLoaded", function () {
    const tbody = document.getElementById("patientTableBody");
    const msg = document.getElementById("noPatientsMsg");

    // Patients load karne ka function
    async function loadAppointments() {
        try {
            const res = await fetch("/api/patients/");
            const data = await res.json();

            if (data.length === 0) {
                tbody.innerHTML = "";
                msg.style.display = "block";
                return;
            } else {
                msg.style.display = "none";
                tbody.innerHTML = "";
                data.forEach(patient => {
                    tbody.innerHTML += `
                        <tr>
                            <td>${patient.id}</td>
                            <td>${patient.name}</td>
                            <td>${patient.phone}</td>
                            <td>${patient.email}</td>
                            <td>
                                <button class="btn btn-danger btn-sm" onclick="deletePatient(${patient.id})">Delete</button>
                            </td>
                        </tr>
                    `;
                });
            }
        } catch (err) {
            console.log("There was an error", err);
            tbody.innerHTML = "";
            msg.style.display = "block";
            return;
        }
    }

    //  Page load hote hi call karo
    loadAppointments();

    // Patient add karne ka form submit
    document.getElementById("patientForm").addEventListener("submit", async function (e) {
        e.preventDefault();

        const formdata = new FormData(this);
        const patientdata = Object.fromEntries(formdata.entries());

        try {
            const res = await fetch("/api/patients/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"   
                },
                body: JSON.stringify(patientdata)
            });

            await res.json(); // response ko read karna zaroori hai
            loadAppointments(); //  naye patient ke baad list refresh
            this.reset();       // form reset
        } catch (err) {
            console.log("Error adding patient:", err);
        }
    });

    //  Delete patient function
    window.deletePatient = async function (id) {
        try {
            await fetch(`/api/patients/${id}/`, {
                method: 'DELETE'
            });
            loadAppointments(); // delete ke baad refresh
        } catch (err) {
            console.log("Error deleting patient:", err);
        }
    }
});
