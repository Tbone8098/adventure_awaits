// ******************** FORM ********************************
let pwBtn = document.querySelectorAll('.pw-btn')

pwBtn.forEach(btn => {
    btn.addEventListener('click', function(e){
        e.preventDefault()
        pw_element = this.previousElementSibling
        if (pw_element.type == 'text'){
            pw_element.type = 'password'
            this.innerText = "Show"
        } else {
            pw_element.type = 'text'
            this.innerText = "Hide"
        }
    })
});