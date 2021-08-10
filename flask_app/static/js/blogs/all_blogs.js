var isPublicBtns = document.querySelectorAll('.make_pub_btn')

for (const pubBtn of isPublicBtns) {
    pubBtn.addEventListener('change', function(){
        var post_id = pubBtn.getAttribute("post_id")
        fetch(`http://localhost:5000/post/${post_id}/update_public/${pubBtn.checked}`)
    })
}