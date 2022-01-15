$(document).ready(function () {
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
            console.log("just passed the test fo the id")
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
        if (!(e.target.href)) return;
        if ((e.target.href).split("/").at(-1) === "#UpdatePostModal") return GetUpdatePost(e);
        if ((e.target.href).split("/").at(-1) === "#DeletePostModal") return DeletePost(e);

    });

})
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
    console.log("the delete post function ran")

    $("#DeletePostModal").on("click", (ev) => {
        console.log("the delete modal has been clicked");
        if ($(ev.target).attr("id") !== "deletePostBtn") return;
        ev.preventDefault();
        var post_slug = $(e.target).attr("data-slug")
        var url = `/social/post-delete/${post_slug}/`
        // grab the csrf toke from the form and pass 
        // it to the data so that the from will post correctly
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