$(document).ready(function () {
    $("button[data-bs-dismiss='modal']").on("click", (e) => {
        var form = $(e.target).parent().parent().find(".modal-body").find("form");
        $(form)[0].reset()
        $("#PreviewImagesContainer").html("")
    });
    $("#CreatePostModal").on("keyup", (e) => {
        if (e.target.tagName !== "INPUT" && e.target.tagName !== "TEXTAREA") return;
        if (e.target.classList.contains("is-invalid")) {

            e.target.classList.remove("is-invalid");
        }
    })
    $("#CreatePostModal").on("click", (e) => {
        if ($(e.target).attr("id") !== "createPostBtn") return;
        e.preventDefault();
        e.target.setAttribute("disabled", true);
        $(e.target.nextElementSibling).fadeIn()
        var form = $("#createPostForm")[0]
        var data = new FormData(form);
        console.log("this is the data", data)
        for (var i = 0; i < imageFiles.length; i++) {
            console.log(imageFiles[i])
            data.append('images', imageFiles[i]);
        };

        $.ajax({
            url: $("#CreatePostModal").attr("data-url"),
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
                        ResetForm('createPostForm', 'PreviewImagesContainer')
                        $("#CreatePostModal").modal('hide')
                        $(e.target.nextElementSibling).fadeOut()
                        alertUser("Post", "has been created successfully!")// alerting the user 
                    }, 1000)

                } else {
                    $("#createPostForm").replaceWith(data.formErrors);
                    $("#PreviewImagesContainer").html("");
                    $("#CreatePostModal").find("form").attr("id", "createPostForm");
                    $(e.target.nextElementSibling).fadeOut()
                };

                $(e.target).prop("disabled", false);
            },
            error: (error) => {
                console.log(error)
            }
        })
    });

    // var postImagesInput = document.getElementById("id_images");
    var postImagesPreviewContainer = document.getElementById("PreviewImagesContainer")
    let imageFiles = []
    $("#CreatePostModal").on('change', (e) => {
        $(postImagesPreviewContainer).html("")
        if ($(e.target).attr("id") !== "id_images") return;
        var filenames = "";
        for (let i = 0; i < e.target.files.length; i++) {
            filenames += (i > 0 ? ", " : "") + e.target.files[i].name;
        }
        e.target.parentNode.querySelector('.custom-file-label').textContent = filenames;

        //why is the this element returning the document and not the target itself
        // check the length of the files to know what template to make
        const files = e.target.files
        const numberOfImages = files.length
        let gridColumnSize;
        if (numberOfImages > 5 | numberOfImages === 0) return;
        var row = document.createElement("div")
        row.setAttribute("class", "post-images")

        for (file of files) {

            const postImageChild = document.createElement("div");
            postImageChild.setAttribute("class", "post-images__child_down")
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
                    const encodedSource = ctx.canvas.toDataURL(e.target, 'image/png')
                    const processedImg = document.createElement("img") // create a processed image and return it.
                    processedImg.src = encodedSource
                    $(postImageChild).append(processedImg)
                    imageFiles.push(processedImg)
                }
            }
            $(row).prepend(postImageChild)
            $(postImagesPreviewContainer).append(row);
            reader.readAsDataURL(file)
        }
        if (numberOfImages !== 2) {
            $(".post-images div:nth-child(1)").css({
                "grid-column": "1 / " + (gridColumnSize).toString(),
            })
        }
        $(".post-images div:nth-child(1)").removeClass("post-images__child_down").addClass("post-images__child")

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