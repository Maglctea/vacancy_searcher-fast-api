let tg = window.Telegram.WebApp;

tg.expand();

const updatedData = {}

const form = document.getElementById("edit-profile-form")
const btn_submit = document.getElementById("btn-submit")

form.addEventListener("change", function (event) {
    const changedElement = event.target;
    if (changedElement.type === "checkbox") {
        updatedData[changedElement.id] = changedElement.checked;
    } else {
        updatedData[changedElement.id] = changedElement.value
    }
    btn_submit.classList.remove('d-none')

});
