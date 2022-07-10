(() => {
    "use strict"
    const forms = document.querySelectorAll(".needs-validation")
    Array.from(forms).forEach(form => {
        form.addEventListener("submit", event => {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }
            
            form.classList.add("was-validated")
        }, false)
    })
})()

var myAlert = document.getElementById("alertMessage")

if (myAlert){
    myAlert.addEventListener("closed.bs.alert", function () {
        document.getElementById("username").focus()
    })
}