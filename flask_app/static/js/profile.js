var sectionBtns = document.querySelectorAll('.section-btn')
sectionBtns.forEach(btn => {
    btn.addEventListener('click', function(){
    sectionName = btn.getAttribute('link')
    console.log(sectionName);
    section = document.querySelector(`#${sectionName}`)
        show_section(btn, section)
    })
});

function show_section(btn, section){
    btnName = btn.getAttribute('name')
    if (section.style.display == 'block'){
        section.style.display = 'none'
        btn.innerHTML = `Show ${btnName}`
    } else {
        section.style.display = 'block'
        btn.innerHTML = `Hide ${btnName}`
    }
}