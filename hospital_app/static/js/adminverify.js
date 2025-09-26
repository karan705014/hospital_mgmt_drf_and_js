document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("adminlogin").addEventListener("submit",async function (e) {
        e.preventDefault();

        const phone = document.getElementById("phone").value;
        const password = document.getElementById("password").value;
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        try {
            const response = await fetch("/adminpage/verify/", {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken
                },
                body: JSON.stringify({phone,password})
            });
            if(!response.ok){
                throw new Error("server error :"+response.status)
            }
            const data =await response.json();
            if (data.success){
                window.location.href ="/adminpage/home/"
            }else{
                    document.getElementById("error").innerText = data.error;
            }



        }catch(error){
            console.error("Error:", error);
            document.getElementById("error").innerText = "Something went wrong, please try again";

        }
    });

});