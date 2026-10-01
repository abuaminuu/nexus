document.addEventListener('DOMContentLoaded', function(){

    // getcookie function to get csrf token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // get post form object
    const postForm = document.getElementById('post-form');

    // post form submission event listener at index
    if (postForm) {
        // add event listener to the form submission
        postForm.addEventListener('submit', function(event){
            // prevent default form submission
            event.preventDefault(); 

            // get content from textarea
            const postContent = document.getElementById('post-content').value.trim();

            // validate content
            if (postContent === '') {
                alert('Post Cannot Be Empty !');
                return;
            }
            // esle
            console.log('Post content: ' + postContent);
            console.log(this.action + ' method: ' + this.method);

            // send the content to the server using fetch
            fetch(`${this.action}`, {
                method: `${this.method}`,
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: new URLSearchParams({ content: postContent })
            })  
            .then(response => {
                // clearr the textarea after submission
                document.getElementById('post-content').value = '';
                // reload the page to show the new post
                window.location.reload();
                console.log('response: ' + response);
            })
            .catch(error => {console.error('Error:', error);});
        });
    }
    
    // get like button
    const likeButton = document.querySelectorAll('.like-button');

    // handles like button for each post
    likeButton.forEach(function(button){
        button.addEventListener('click', function(event){
            let postId = button.dataset.postId;
            let likeCountElement = button.closest('.post-container').querySelector('.likes-count');

            // fetch to like endpoint
            fetch(`/social/like_post/${postId}/`, {
                method:'POST',
                headers: {
                    'Content-Type':'application/json',
                    'X-CSRFToken':getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                // console.log('data: ' + JSON.stringify(data));
                    
                // update the like count display
                if (data.like_status === true){
                    
                    button.textContent = 'Unlike';
                    console.log('like status: ' + data.like_status + ' like count: ' + data.like_count);
                    button.classList.remove('btn-info');
                    button.classList.add('btn-warning');
                    likeCountElement.textContent = data.like_count;
                }

                if (data.like_status === false){
                        button.textContent = 'Like';
                        console.log('like status: ' + data.like_status);
                        button.classList.remove('btn-warning');
                        button.classList.add('btn-info');
                        likeCountElement.textContent = data.like_count;
                }

                // finally return
                return;
            })
            .catch(error => {
                console.log('error: ' + error);
            });
            
        });
    });

    // get edit button that is currently clicked on index
    const editButton = document.querySelectorAll('.edit-post-button');

    // handles edit button for each individual post
    if (editButton) {

        editButton.forEach(function(button){
            button.addEventListener('click', function(event){

                // prevent multiple edits, before creating edit mode,
                // check if theres textarea in this post
                
                // find the parent postcontainer
                let postContainer = button.closest('.post-container');

                let existingTextArea = postContainer.querySelector('.edit-textarea');

                if (existingTextArea){

                alert('onedit mode');
                    return;
                }
                
                // postid from button data attr
                let postId = button.dataset.postId;
                
                // postcontent within this container
                let postContentElement = postContainer.querySelector('.post-text');
                let currentContent = postContentElement.textContent.trim();

                // hide the current content element
                postContentElement.style.display = 'none';

                // create textarea with current text
                let textArea = document.createElement('textarea');
                textArea.value = currentContent;
                textArea.className = 'form-control edit-textarea';
                textArea.rows = 3;

                // insert the textarea where postcontent was
                postContentElement.parentNode.insertBefore(textArea, postContentElement); 
                
                // change edit button to save 
                // button.textContent = 'save0';
                // button.className = 'save-post-button';

                // create/add save button
                let saveButton = document.createElement('button');
                saveButton.type = 'button';
                saveButton.textContent = 'Save/Update';
                saveButton.className = 'btn btn-primary btn-sm px-3 fw-semibold me-2 save-post-button';
                // hide edit button
                // editButton.style.hide = true;
                postContainer.appendChild(saveButton);

                // create/add a cancel button
                let cancelButton = document.createElement('button');
                cancelButton.type = 'button';
                cancelButton.textContent = 'Cancel';
                cancelButton.className = 'btn btn-outline-secondary btn-sm px-3 fw-semibold cancel-edit-button';
                postContainer.appendChild(cancelButton);
                
                // append the buttons to below the textarea
                // 3. Append them below the textarea
                let buttonGroup = document.createElement('div');
                buttonGroup.className = 'mt-2 d-flex align-items-center';
                // buttonGroup.appendChild(saveButton);
                // buttonGroup.appendChild(cancelButton);

                // handle save action
                saveButton.addEventListener('click', function(){
                    let updatedContent = textArea.value;
                    fetch(`/social/edit_post/${postId}/`, {
                        method:'POST',
                        headers: {
                            'Content-Type':'application/json',
                            'X-CSRFToken':getCookie('csrftoken')
                        },
                        body: JSON.stringify({content:updatedContent})
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success){
                            // update the displayed content
                            postContentElement.textContent = updatedContent;
                            postContentElement.style.display = 'block';

                            // remove textarea and cancel button
                            textArea.remove();
                            cancelButton.remove();
                            saveButton.remove();

                        } else {
                            console.log('errorx: ' + data.error);
                        }
                    })
                    .catch(error => {
                        console.log('errory: ' + error);
                    });
                });

                // handle cancel button
                cancelButton.addEventListener('click', function(){
                    postContentElement.style.display = 'block';
                    textArea.remove();
                    saveButton.remove();
                    cancelButton.remove();

                    // reset edit button
                    editButton.textContent  = 'edit';
                    editButton.className= 'edit-post-button';
                    // alert('cancled');
                });

                // console.log('edit button clicked!' + currentContent  + postId+ postContentElement.parentNode);

            });
        });
    }
    
    
    // edit button for profile bio and profile picture
    const editProfileButton = document.querySelector('.edit-profile-button');

    if (editProfileButton) {
        editProfileButton.addEventListener('click', function(){

            // 1. Reveal ONLY the photo upload container (label button stays, raw input stays hidden)
            const photoWrapper = document.querySelector('.photo-upload-wrapper');
            const imageUploader = document.querySelector('input[name="profile-picture-element"]');

            if (photoWrapper) {
                photoWrapper.style.display = 'block';
            }
            // 1. handle profile picture change
            // get image file uploader.

            // show the image uploader
            // imageUploader.style.display = 'block';

            // updated profile picture variable
            let updatedProfilePictureUrl = null;
            
            // Capture selected file when user picks an image
            if (imageUploader) {

                // get the file content if user selects a file
                imageUploader.addEventListener('change', function(event){
                    
                    // handles file selection and get the file object
                    if (imageUploader.files.length > 0){
                        // get the selected file
                        updatedProfilePictureUrl = imageUploader.files[0];
                    
                        console.log('selected file: ' + updatedProfilePictureUrl.name);
                        console.log('selected file type: ' + updatedProfilePictureUrl.type);
                        console.log('selected file size: ' + updatedProfilePictureUrl.size + ' bytes');
                    
                        // TODO checks for size, limit and type.

                    }
                });
            }
            
            // 2. handle bio UI change
            // get the current bio content
            const bioElement = document.querySelector('.profile-bio-element');
            if (!bioElement) {
                console.log('bio element not found!');
                return;
            }

            // create a textarea for bio
            let bioTextArea = document.createElement('textarea');
            bioTextArea.value = bioElement.textContent.trim();
            bioTextArea.className = 'form-control edit-bio-textarea mb-2';
            bioTextArea.rows = 2;

            // replace bio element with textarea
            bioElement.parentNode.replaceChild(bioTextArea, bioElement);
            
            // create a save button for bio
            let saveBioButton = document.createElement('button');
            saveBioButton.textContent = 'Update Profile';
            saveBioButton.className = 'btn btn-sm btn-primary save-profile-button me-2';

            // create a cancel button for bio
            let cancelBioButton = document.createElement('button');
            cancelBioButton.textContent = 'Cancel';
            cancelBioButton.className = 'btn btn-sm btn-secondary cancel-profile-button';
            
            // appends buttons to parent node
            bioTextArea.parentNode.appendChild(saveBioButton);
            bioTextArea.parentNode.appendChild(cancelBioButton);

            // handle save profile action
            saveBioButton.addEventListener('click', function(){

                // // hide the photo upload wrapper
                if (photoWrapper) {
                    photoWrapper.style.display = 'none';
                }

                let updatedBio = bioTextArea.value.trim();
                
                // make sure bio not empty
                if (updatedBio === '') {
                    alert('please add bio/pic!!')
                    return;
                }

                // bundle data as formData object when data is validated and append to formdata
                const formData = new FormData();
                formData.append('bio', updatedBio);
                formData.append('profile_picture', updatedProfilePictureUrl);

                console.log('clients request: ');
                console.log(formData);
                // console.log(formData.get('updatedProfilePictureUrl'));

                fetch(`/social/edit_profile/`, {
                    method:'POST',
                    headers: {
                        'X-CSRFToken':getCookie('csrftoken')
                    },
                    body: formData
                })
                .then(response => response.json())
                .then(data => {

                    // servers response 
                    console.log('servers response: ');
                    console.log(data.success);
                    console.log(data.bio);
                    console.log(data.profile_picture);

                    // when response is success
                    if (data.success){
                        // update image frame instatly with new image url
                        let imageFrame = document.querySelector('.profile-picture-element');
                        if (imageFrame) {
                            console.log('frame exists!' + imageFrame.src);
                        }
                        // add updated image to the iframe
                        imageFrame.src = data.profile_picture_url
                        
                        // Create new paragraph element for bio
                        let newBioElement = document.createElement('textarea'); //p
                        newBioElement.className = 'profile-bio-element';
                        newBioElement.textContent = data.bio;
                        
                        // console.log('ret updata:' + data.bio + 'prof: ' + data.profile_picture);

                        // replace the old bio element with the new one
                        bioTextArea.parentNode.replaceChild(newBioElement, bioTextArea);
                        
                        // remove save and cancel buttons
                        saveBioButton.remove();
                        cancelBioButton.remove();

                        // reload the page to reflect changes
                        window.location.reload();
                        // let pictureBrowserButton = document.querySelector('#profile-picture-element');
                        // pictureBrowserButton.remove();

                    } else {
                        // success id false
                        console.log('error: ' + data.success);
                    }
                })
                .catch(error => {
                    console.log('error: ' + error);
                });
            });

            // handle cancel bio action
            cancelBioButton.addEventListener('click', function(){

                // replace textarea with original bio element
                bioTextArea.parentNode.replaceChild(bioElement, bioTextArea);
                // remove save and cancel buttons
                saveBioButton.remove();
                cancelBioButton.remove();

                // hide the photo upload wrapper again
                if (photoWrapper) {
                   photoWrapper.style.display = 'none';
                }

            });

            // console.log('Buttons created:', saveBioButton, cancelBioButton);
            // console.log('Parent element:', bioTextArea.parentNode);
            // console.log('Child elements:', bioTextArea.parentNode.children);
        
        });
    }

    // end of DOM loaded.
});

