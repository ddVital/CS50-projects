document.addEventListener('DOMContentLoaded', () => {

    // Button to like post
    document.querySelectorAll('.likeForm').forEach(form => {

        const button_like = form.children[0];

        button_like.addEventListener('click', () => {

            if (button_like.dataset.liked == 'false') {

                const postId = button_like.dataset.post;
                const sessionUser = button_like.dataset.sessionUser;
                const fetchURL = '/like/' + postId + '/' + sessionUser;
                var likes = Number(button_like.dataset.likes);

                fetch(fetchURL)
                    .then(response => {
                        console.log(response);
                        return response.text()
                    })
                    .catch(err => {
                        alert(err);
                    })

                button_like.setAttribute('data-liked', 'true');
                button_like.setAttribute('class', 'like');

                likes += 1;
                button_like.setAttribute('data-likes', likes);
                button_like.innerHTML = '<i class="fa fa-heart"></i> ' + likes;

            } else {

                const postId = button_like.dataset.post;
                const sessionUser = button_like.dataset.sessionUser;
                const fetchURL = '/unlike/' + postId + '/' + sessionUser;
                var likes = Number(button_like.dataset.likes);

                fetch(fetchURL)
                    .then(response => {
                        console.log(response);
                        return response.text()
                    })
                    .catch(err => {
                        alert(err);
                    })

                button_like.setAttribute('data-liked', 'false');
                button_like.setAttribute('class', 'unlike');

                likes -= 1;
                button_like.setAttribute('data-likes', likes);
                button_like.innerHTML = '<i class="fa fa-heart"></i> ' + likes;
            }
        });
    });
}) 

function charCount() {
    const postContent = document.querySelector('#post-content-field').value
    const charCount = document.querySelector('#charCount').innerHTML = postContent.length
}

function editPost(id) {
    // change icons
    document.querySelector(`.edit-icon-${id}`).style.display = 'none';
    document.querySelector(`.save-${id}`).style.display = 'block';

    // show content and hide textarea
    document.querySelector(`.edit-${id}`).style.display = 'block';
    document.querySelector(`.post-content-${id}`).style.display = 'none';
}

function savePost(id) {
    // change icons
    document.querySelector(`.edit-icon-${id}`).style.display = 'block';
    document.querySelector(`.save-${id}`).style.display = 'none';

    // show content and hide textarea
    document.querySelector(`.edit-${id}`).style.display = 'none';
    document.querySelector(`.post-content-${id}`).style.display = 'block';
}

function CopyToClipboard(id) {
    /* Get the text field */
    var copyText = document.querySelector(`.input-post-${id}-content`);
  
    /* Select the text field */
    copyText.select();
    copyText.setSelectionRange(0, 99999); /*For mobile devices*/
  
    /* Copy the text inside the text field */
    document.execCommand("copy");
  
    /* Alert the copied text */
    alert("Copied the text: " + copyText.value);
}