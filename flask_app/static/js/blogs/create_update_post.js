var imageSectionBtn = document.querySelector('#image-section-btn')
var imageSection = document.querySelector('#image-section')

var contentSectionBtn = document.querySelector('#content-section-btn')
var contentSection = document.querySelector('#content-section')

var deleteImgBtns = document.querySelectorAll('.delete-image-btn')

for (const deleteBtn of deleteImgBtns) {   
    deleteBtn.addEventListener('click', function(){
        var img_id = deleteBtn.getAttribute('img_id')
        fetch(`/img/${img_id}/delete`)
        .then(resp => resp.json())
        .then(data => {
            deleteBtn.parentElement.remove()
        })
    })
}

var fileUpload = document.querySelector('.file-upload')

fileUpload.addEventListener('submit', function(e){
    e.preventDefault()
    var form = new FormData();

    var title = fileUpload.children[0].value
    form.append('title', title)

    var post_id = fileUpload.getAttribute('post_id')

    var image = document.querySelector('.file-upload > input[type="file"]').files[0];
    getBase64(image).then(
        data => {
            console.log(data)
            var base64 = data

            form.append('base64', data)

            fetch(`/img/create/${post_id}`, {
                method: 'POST',
                body: form 
            })
            .then(resp => resp.json())
            .then(data => {
                console.log(data);
                if (data['code'] === 200){
                    var attachedImages = document.querySelector('.attached-images > table')
                    attachedImages.innerHTML += `
                    <tr>
                        <td>
                            <img src="${base64}" alt="" width="100">
                        </td>
                        <td>${title}</td>
                        <td>
                            <button class="delete-image-btn" img_id="${data['img_id']}">X</button>
                        </td>
                    </tr>
                    `
                } else {
                    console.log('no');
                    // window.location.reload()
                }
            })
        }
    );
})

function getBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = error => reject(error);
    });
}


// imageSectionBtn.addEventListener('click', function(){
//     var post_id = imageSectionBtn.getAttribute('post_id')
//     var form = new FormData(imageSection);
//     var imageTitle = imageSection.children[0].value
//     var imageLink = imageSection.children[1].value
//     fetch(`/img/create/${post_id}`, {
//         method: 'POST',
//         body: form 
//     })
//     .then(resp => resp.json())
//     .then(data => {
//         console.log(data);
//         if (data['code'] === 200){
//             var attachedImages = document.querySelector('.attached-images')
//             attachedImages.innerHTML += `
//             <div class="d-flex align-items-center mt-3">
//             <img src="${imageLink}" alt="" width="100" class="me-3">
//             <p><button class="delete-image-btn">Remove</button> ${imageTitle}</p>
//             </div>
//             `
//         } else {
//             console.log('no');
//             window.location.reload()
//         }
//     })
// })