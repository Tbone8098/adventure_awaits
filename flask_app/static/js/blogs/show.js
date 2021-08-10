var pictureSwitchBtn = document.querySelector('#picture-switch-btn')

var gallery = document.querySelector('#gallery')
var carousel = document.querySelector('#carousel')

pictureSwitchBtn.addEventListener('click', function(){
    if (gallery.style.display === 'none'){
        gallery.style.display = 'block'
        carousel.style.display = 'none'
    } else {
        gallery.style.display = 'none'
        carousel.style.display = 'block'
    }
})