document.addEventListener("DOMContentLoaded", () => {
    const tableBody = document.getElementById("appointmentsTable");
    const noAppointmentMsg = document.getElementById("noAppointments");

    async function loadAppointments() {
        try {
            const res = await fetch("/api/adminpage/dashboard/");
            if (!res.ok) throw new Error("Failed to fetch appointments");

            const data = await res.json();

            if (data.length === 0) {
                tableBody.innerHTML = "";
                noAppointmentMsg.classList.remove("d-none");
                return;
            }

            noAppointmentMsg.classList.add("d-none");
            tableBody.innerHTML = "";

            data.forEach(appt => {
                let statusClass = "";
                if (appt.status === "pending") statusClass = "pending";
                else if (appt.status === "approved") statusClass = "approved";
                else if (appt.status === "rejected") statusClass = "rejected";

                const row = `
                    <tr id="appt-${appt.id}">
                        <td>${appt.patient_name}</td>
                        <td>${appt.doctor_name}</td>
                        <td>${appt.time}</td>
                        <td>${appt.date}</td>
                        <td><span class="status ${statusClass}">${appt.status}</span></td>
                        <td>
                            <button onclick="updateStatus(${appt.id},'approved')">Approve</button>
                            <button onclick="updateStatus(${appt.id},'rejected')">Reject</button>
                            <button onclick="updateStatus(${appt.id},'pending')">Pending</button>
                        </td>
                    </tr>
                `;

                tableBody.innerHTML += row;
            });

        } catch (err) {
            console.log(err);
            tableBody.innerHTML = "";
            noAppointmentMsg.classList.remove("d-none");
        }
    }

    loadAppointments();

    // Make updateStatus globally accessible for inline onclick
    window.updateStatus = async function(appointment_id, status) {
        try {
            const res = await fetch(`/adminpage/update_status/${appointment_id}/${status}/`, {
                method: "POST",
                headers:{
                    "Content-Type":"application/json",
                    "X-CSRFToken":csrftoken
                },
                body: JSON.stringify({})
            });

            if (!res.ok){
                console.log("Status update failed");
                return;
            }

            const data = await res.json();

            // Update only the changed row
            const row = document.getElementById(`appt-${appointment_id}`);
            if (row) {
                const statusSpan = row.querySelector(".status");
                statusSpan.textContent = data.appointment.status;
                statusSpan.className = `status ${data.appointment.status}`;
            }

        } catch (err) {
            console.log(err);
        }
    }
});

// CSRF token helper
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie('csrftoken');
