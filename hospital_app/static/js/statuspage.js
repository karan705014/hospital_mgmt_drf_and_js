document.addEventListener("DOMContentLoaded", () => {
    const tableBody = document.getElementById("appointmentsTable");
    const noAppointmentMsg = document.getElementById("noAppointments");

    async function loadAppointments() {
        try {
            const res = await fetch("/api/status/page/");
            if (!res.ok) {
                tableBody.innerHTML = "";
                noAppointmentMsg.classList.remove("d-none");
                return;

            }
            const data = await res.json()

            if (data.length === 0) {
                tableBody.innerHTML = "";
                noAppointmentMsg.classList.remove("d-none");
                return;

            }
            noAppointmentMsg.classList.add("d-none");//agar appointment hai toh no appointment msg ko chupa liya jaega
            tableBody.innerHTML = "";     

            data.forEach(appt => {
                let statusClass = "";
                if (appt.status === "pending") statusClass = "status-pending";
                else if (appt.status === "approved") statusClass = "status-approved";
                else if (appt.status == "rejected") statusClass = "status-rejected";
//agar data me 5 element hai toh ye foreach loop 5 bar chalega appt ke taur pe ,status class hai css ke liya 

                const row = `
                <tr>
                    <td>${appt.doctor_name}</td>
                    <td>${appt.date}</td>
                    <td>${appt.time} </td>
                    <td><span class="${statusClass}">${appt.status}</span></td>
                </tr>

                `;
                tableBody.innerHTML += row;



            });
        } catch (err) {
            console.error("Error loading appointments:", err);
            tableBody.innerHTML = "";
            noAppointmentMsg.classList.remove("d-none");
        }
    }
    loadAppointments();


});