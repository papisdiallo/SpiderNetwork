$(document).ready(function () {
    let imageString;
    let cropX;
    let cropY;
    let cropWidth;
    let cropHeight;
    let max_size;
    let imageFiles = []
    const modalsId = ["#CreatePostModal", "#UpdatePostModal"]

    $("button[data-bs-dismiss='modal']").on("click", (e) => {
        var form = $(e.target).parent().parent().find(".modal-body").find("form");
        form.length !== 0 ? $(form)[0].reset() : "";
        $("#PreviewImagesContainer").html("")
    });
    $("#CreatePostModal").on("keyup", (e) => {
        if (e.target.tagName !== "INPUT" && e.target.tagName !== "TEXTAREA") return;
        if (e.target.classList.contains("is-invalid")) {

            e.target.classList.remove("is-invalid");
        }
    })
    modalsId.forEach((_id, index) => {
        $(`${_id}`).on("click", (e) => {
            console.log(e.target.id)
            if ($(e.target).attr("id") !== "createPostBtn") return;
            e.preventDefault();
            $(e.target.nextElementSibling).fadeIn()
            e.target.setAttribute("disabled", true);
            var form = $(`${_id} #createPostForm`)[0]
            var data = new FormData(form);

            for (var i = 0; i < imageFiles.length; i++) { // append the uuploaded images to data
                console.log(imageFiles[i])
                data.append('images', imageFiles[i]);
            };

            //make the ajax call here 

            $.ajax({
                url: $(`${_id}`).attr("data-url"),
                data: data, //$("#CreatePostModal #createPostForm").serialize(),
                method: "post",
                processData: false,
                cache: false,
                contentType: false,
                dataType: "json",
                success: (data) => {
                    if (data.success) {
                        setTimeout(() => {
                            $(e.target).next().fadeOut();
                            // take care of the reset form for both later
                            ResetForm('createPostForm', 'PreviewImagesContainer')
                            $(`${_id}`).modal('hide');
                            $(e.target.nextElementSibling).fadeOut()
                            alertUser("Post", "has been created successfully!")// alerting the user 
                        }, 1000)

                    } else {
                        $(`${_id} #createPostForm`).replaceWith(data.formErrors);
                        $(`${_id} .PreviewImagesContainer`).html("");
                        $(`${_id}`).find("form").attr("id", "createPostForm");
                        $(e.target.nextElementSibling).fadeOut()
                    };

                    $(e.target).prop("disabled", false);
                },
                error: (error) => {
                    console.log(error)
                }
            })
        });

    })

    // var postImagesInput = document.getElementById("id_images");

    modalsId.forEach((_id, index) => {
        $(`${_id}`).on("change", (e) => {
            if ($(e.target).attr("id") !== "id_images") return;
            var postImagesPreviewContainer = document.querySelector(`${_id} .PreviewImagesContainer`);
            $(`${_id} .maxFileError`).fadeOut()
            $(postImagesPreviewContainer).html("");
            console.log($(e.target))
            if ($(e.target.files.length) > 5) {
                $(`${_id} .maxFileError`).fadeIn()
                return;
            }

            var row = document.createElement("div")
            row.setAttribute("class", "post-images")
            var second_child_row = document.createElement("div")
            var first_child_row = document.createElement("div")
            $(row).append(first_child_row).append(second_child_row)

            Array.from(e.target.files).forEach((file, i) => {
                const postImageChild = document.createElement("div");
                postImageChild.setAttribute("class", "post-images__child")
                const reader = new FileReader();
                reader.onload = () => {
                    img = document.createElement("img")
                    img.setAttribute("src", reader.result)

                    img.onload = (e) => {
                        // here i will process on resizing the image
                        const canvas = document.createElement("canvas")
                        const max_width = 680
                        const scaleSize = max_width / e.target.width
                        canvas.width = max_width
                        canvas.height = e.target.height * scaleSize
                        var ctx = canvas.getContext("2d") // setting the context of the canvas
                        ctx.drawImage(e.target, 0, 0, canvas.width, canvas.height)
                        const encodedSource = ctx.canvas.toDataURL(e.target, 'image/png', 1)
                        const processedImg = document.createElement("img") // create a processed image and return it.
                        processedImg.src = encodedSource
                        $(postImageChild).append(processedImg)
                        imageFiles.splice(0, imageFiles.length) // clear all the images before adding the new ones
                        imageFiles.push(processedImg)
                    }
                }
                (i === 2 | i === 4) ?
                    $(first_child_row).append(postImageChild)
                    : $(second_child_row).append(postImageChild)

                $(postImagesPreviewContainer).append(row);
                reader.readAsDataURL(file)
                var image_input_div = document.querySelector(`${_id} #createPostForm #div_id_images`);
                document.querySelector(`${_id} #createPostForm`).insertBefore(postImagesPreviewContainer, image_input_div)
            });
        })
    })


    $(".posts-section").on("click", (e) => {
        if (!(e.target.href) && !(e.target.name)) return;
        if (e.target.href) {
            if ((e.target.href).split("/").at(-1) === "#UpdatePostModal") return GetUpdatePost(e);
            if ((e.target.href).split("/").at(-1) === "#DeletePostModal") return DeletePost(e);
            if ((e.target.href).split("/").at(-1) === "#DeleteCommentPostModal") return DeleteCommentPost(e);
        } else {
            if (e.target.getAttribute("name") === "PostLike") return PostLike(e);
            if (e.target.getAttribute("name") === "commentpost") return commentOnPost(e);

        }
    });
    $("#user_profile").on("click", (e) => {
        var profile_slug = window.location.pathname.split("/").at(-2)
        var url = `/connection/update-profile/${profile_slug}/`
        var loading_div = `
            div class="process-comm">
                <div class="spinner">
                <div class="bounce1"></div>
                <div class="bounce2"></div>
                <div class="bounce3"></div>
                </div>
            </div>
        `
        $("#UserProfileModal .modal-body .container-fluid").html(loading_div)
        if ((e.target.href) && (e.target.name)) {
            var target_name = $(e.target).attr("name");
            $.ajax({
                url: url,
                type: "get",
                success: function (data) {
                    if (!(data.error)) {
                        var modal_body = $("#UserProfileModal .modal-body .container-fluid")
                        $(modal_body).html(data.template)
                        max_size = data.max_size; // this  will be use to compare the image with allowed size from the settings.
                        $("#UserProfileForm").children().each((index, el) => {
                            if (el.tagName === "DIV" && !(($(el).attr("id")).includes(target_name))) {
                                $(el).addClass("d-none");
                                $("#UserProfileForm").removeClass("d-none");

                            } else {
                                console.log("this should be an input")
                            }
                        })
                        if (target_name === "avatar") {
                            // creating programmatically the image preview div
                            var imageContainerDiv = $("<div/>", {
                                'id': 'ImageProfilePreview',
                                'class': 'container',
                                'style': 'font-weight:bold; color:black;',
                                'html': `<div style="align-text:center">
                                            <img id="prev_me" src="${data.profileUrl}" alt="Your current profile image" />
                                         </div>
                                        `,
                                // 'click': function () { alert(this.id) },
                            }).appendTo(modal_body);
                            // move this to its own function
                            $("#id_avatar").on("change", (e) => {
                                if (e.target.files[0]) {
                                    var reader = new FileReader();
                                    reader.onload = (e) => {
                                        imageSrc = e.target.result
                                        var imagePreview = document.getElementById("prev_me")
                                        imagePreview.src = imageSrc;
                                        cropper = new Cropper(imagePreview, {
                                            aspectRatio: 1 / 1,
                                            crop: function (e) {
                                                setImageProperties(imageSrc, e.detail.x, e.detail.y, e.detail.width, e.detail.height)
                                            }
                                        })
                                    }
                                    reader.readAsDataURL(e.target.files[0]);
                                }
                            });
                            $("#UserProfileModal #UserProfileForm").on("click", (e) => {

                            })
                        }
                    } else {
                        alert(data.error)
                    }
                },
                error: function (error) {

                }
            })

        } else { return; }
        $("#UserProfileModal #UpdateProfileBtn").on("click", (e) => {
            if (!(target_name === "avatar")) { // we handle the image update differently               
                console.log("the submit btn has been clicked")
                var _form_data = $("#UserProfileForm").serialize()
                e.preventDefault();
                $.ajax({
                    url: url,
                    type: "post",
                    data: _form_data,
                    dataType: "json",
                    success: (data) => {
                        console.log(data.success)
                        if (data.success) {
                            $("#UserProfileModal").modal("hide")
                            $("#UserProfileForm")[0].reset();
                            // Update the UI
                            var span = $("#prof-sections").find(`span.${data.field_name}`)
                            $(span).text(data.new_value)

                        }
                    },
                    error: (error) => {
                        console.log("this is an error", error)
                    }
                })
            } else {
                e.preventDefault()
                console.log("the avatar upload has run")
                CropImage(imageString, cropX, cropY, cropWidth, cropHeight, max_size)
            }
        })
    })



    function setImageProperties(image, x, y, width, height) {
        imageString = image;
        cropX = x;
        cropY = y;
        cropWidth = width;
        cropHeight = height;
    }
    function CheckImageSize(image, max_upload_size) {
        console.log("the check image size function run")
        var startIndex = image.indexOf("base64,") + 7
        var imageBase64 = image.substring(startIndex)
        var decodedImg = atob(imageBase64)
        if (decodedImg >= max_upload_size) {
            return null;
        } else {
            return imageBase64
        }
    }
    // the rolw of this function is to send the image as a string
    // since ajax cannot send image files
    function CropImage(image, cropX, cropY, cropWidth, cropHeight, max_upload_size) {
        console.log(cropX)
        //fisrt check if the size of the image is not greater than size allowed
        // in the settings.py file
        var imageString = CheckImageSize(image, max_upload_size);
        if (imageString !== null) {
            var data = {
                "imageString": imageString,
                "cropX": cropX,
                "cropY": cropY,
                "cropHeight": cropHeight,
                "cropWidth": cropWidth,
                "csrfmiddlewaretoken": csrftoken,
            }
            $.ajax({
                url: "/connection/cropping-image/",
                dataType: "json",
                method: "post",
                data: data,
                success: function (data) {
                    if (data.success) {
                        console.log("there is a success");
                        // window.location.reload();
                    } else {
                        alert(data.error)
                    }
                },
                error: function (error) {

                },
                complete: function () {
                    // hide the loading to tell the user the operation is done
                    alert(" the ajax call is complete ")
                }
            })

        } else {
            alert("Please Upload an image less than")
        }

    }

    function alertUser(key, message) {
        alertify.set('notifier', 'position', 'top-right');
        alertify.set('notifier', 'delay', 7);
        alertify.success(`${key}  ${message}`);

    }
    function ResetForm(formId, imagePreviewId) {
        $("#" + formId)[0].reset()
        $("#" + imagePreviewId).html("")
    }
    function GetUpdatePost(e) {
        var loading = `
        <div class="PreviewImagesContainer">
            <div class="spinner">
                <div class="bounce1"></div>
                <div class="bounce2"></div>
                <div class="bounce3"></div>
            </div>
        </div>
    `
        $("#UpdatePostModal .modal-body .container-fluid").html(loading)
        var post_slug = e.target.id
        $("#UpdatePostModal").attr("data-url", `/social/post-update/${post_slug}/`)
        $.ajax({
            url: `/social/post-update/${post_slug}/`,
            type: "get",
            dataType: "json",
            success: function (data) {
                var updateFormLocal = $("#UpdatePostModal .modal-body .container-fluid")
                updateFormLocal.html(data.template)
                var maxFileError = `
                <div class="maxFileError">
                    <p class="errornote">You cannot upload more than 5 images</p>
                </div>
            `
                updateFormLocal.append(maxFileError);
            },
            error: function (error) {
                console.log("there is an error for updating  this post", error);
            }

        })
    }
    function DeletePost(e) {

        $("#DeletePostModal").on("click", (ev) => {
            if ($(ev.target).attr("id") !== "deletePostBtn") return;
            ev.preventDefault();
            var post_slug = $(e.target).attr("data-slug")
            var url = `/social/post-delete/${post_slug}/`
            var _form = $("#deletePostForm")
            $.ajax({
                url: url,
                data: _form.serialize(),
                type: "post",
                dataType: "json",
                success: function (data) {
                    if (data.success) {
                        $(`#DeletePostModal`).modal('hide');
                        console.log("this post should already deleted")
                        alertUser("Post", "has been deleted successfully");
                    }
                },
                error: function (error) {
                    console.log("error", error)
                }
            })

        })

    }
    function commentOnPost(e) {
        e.preventDefault();
        e.target.setAttribute("disabled", true);
        var _form = $(e.target).parent();
        var post_slug = _form.attr("data-slug");
        $.ajax({
            url: `/social/comment-on-post/${post_slug}/`,
            data: _form.serialize(),
            method: "post",
            success: function (data) {
                if (data.success) {
                    var comment = JSON.parse(data.comment_obj)
                    var commentUl = `
                <ul>
                    <li>
                        <div class="comment-list">
                            <div class="bg-img">
                                <img src="${data.imageUrl}" style="width: 40px;" alt="">
                            </div>
                            <div class="comment"> 
                                <h3>${comment[0].fields["author"][0]}</h3>
                                <div> 
                                    <p>${comment[0].fields["content"]}</p>
                                </div>
                                <a href="#" title="" class="active"><i class="fa fa-reply-all"></i>Reply</a>
                                <span style="display:inline;"><i class="fa fa-clock mx-1"></i></span> ${comment[0].fields["date_commented"]}</span>
                                <span id="comment_like_${data.comment_pk}" class="com-action"><i class="far fa-thumbs-up"></i></span>
                                <span id="comment_delete_${data.comment_pk}" class="com-action">
                                    <a data-bs-toggle="modal" data-slug="comment_${data.comment_pk}" href="#DeleteCommentPostModal"> <i class="fa fa-trash mx-1"></i></a>
                                </span>
                            </div >
                        </div >           
                    </li >
                </ul >
                `
                    var commentsContainer = $(`.post-comment-${post_slug}`)
                    console.log(commentsContainer.children().length)
                    if (commentsContainer.children().length === 1) {
                        var comment_section = document.createElement("div");
                        $(comment_section).attr("class", "comment-section");
                        var comment_sec = document.createElement("div");
                        $(comment_sec).attr("class", "comment-sec");
                        comment_section.appendChild(comment_sec);
                        $(comment_sec).append(commentUl)
                        $(commentsContainer).prepend(comment_section);
                    } else {
                        $(commentsContainer).find(".comment-sec").append(commentUl)
                    }
                    $(e.target).prop("disabled", false);
                    _form[0].reset();
                    var comments_count = $(`.${post_slug}_comments_count`).text()
                    $(`.${post_slug}_comments_count`).text(parseInt(comments_count) + 1)


                }
            },

            error: function (error) {
                console.log("there was an error when commenting on post", error)
            }
        })

    }
    function DeleteCommentPost(e) {
        console.log("the delete comment post ran")
        var data_slug = $(e.target).attr("data-slug").split("_").at(-1);
        var url = `/social/delete-comment-post/${data_slug}/`

        $("#DeleteCommentPostModal").on("click", (ev) => {
            if ($(ev.target).attr("id") !== "deleteCommentPostBtn") return;
            ev.preventDefault();
            var _form = $("#deleteCommentPostForm")
            $.ajax({
                url: url,
                data: _form.serialize(),
                type: "post",
                dataType: "json",
                success: function (data) {
                    if (data.success) {
                        $(`#DeleteCommentPostModal`).modal('hide');
                        var comments_count = $(`.${data.post_slug}_comments_count`).text()
                        console.log(comments_count)
                        $(`.${data.post_slug}_comments_count`).text(parseInt(comments_count) - 1)
                        alertUser("Comment", "has been deleted successfully");
                    }
                },
                error: function (error) {
                    console.log("error", error)
                }
            })
        });
    }

    // setting the csrf token config I guess...
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
    const csrftoken = getCookie('csrftoken');

    function PostLike(e) {
        console.log("the post like function ran");
        var post_slug = $(e.target).attr("data-slug").split("_")
        var slug = post_slug.at(-1)
        var liked_a = post_slug[0]
        console.log(liked_a)
        console.log(slug);
        var url = `/social/like-post/${slug}/`
        data = { "liked_a": liked_a }
        $.ajax({
            url: url,
            type: "post",
            data: data,
            dataType: "json",
            headers: { 'X-CSRFToken': csrftoken },
            mode: 'same-origin',// Do not send CSRF token to another domain.
            success: function (data) {
                console.log(data.is_liked)
                var _icon = e.target.firstElementChild
                var likes_count = $(e.target).find(".likes-count").text()
                if (data.is_liked === "Not accepted") {
                    alert("Sorry! You cannot like your own post!")
                }
                else if (data.is_liked) {
                    $(e.target).find(".likes-count").text(parseInt(likes_count) - 1)
                    $(_icon).removeClass("is-liked").removeClass("fa").addClass("far")
                } else {
                    $(e.target).find(".likes-count").text(parseInt(likes_count) + 1)
                    $(_icon).removeClass("far").addClass("is-liked").addClass("fa")
                }
            },
            error: function () {

            }
        })

    }

});