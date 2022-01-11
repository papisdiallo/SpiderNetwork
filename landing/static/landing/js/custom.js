$(document).ready(function () {
    $("button[data-bs-dismiss='modal']").on("click", (e) => {
        var form = $(e.target).parent().parent().find(".modal-body").find("form");
        $(form)[0].reset()
    });
    $("#createPostModal").on("keyup", (e) => {
        if (e.target.tagName !== "INPUT" && e.target.tagName !== "TEXTAREA") return;
        if (e.target.classList.contains("is-invalid")) {
            console.log("this is invalid class");
            e.target.classList.remove("is-invalid");
        }
    })
    $("#createPostModal").on("click", (e) => {
        if ($(e.target).attr("id") !== "createPostBtn") return;
        e.preventDefault();
        e.target.setAttribute("disabled", true);
        $(e.target.nextElementSibling).fadeIn()
        $.ajax({
            url: $("#createPostModal").attr("data-url"),
            data: $("#createPostModal #createPostForm").serialize(),
            method: "post",
            dataType: "json",
            success: (data) => {
                if (data.success) {
                    setTimeout(() => {
                        $(e.target).next().fadeOut();
                        $("#createPostForm")[0].reset();
                        $("#createPostModal").modal('hide')
                        $(e.target.nextElementSibling).fadeOut()
                        alertUser("Post", "has been created successfully!")// alerting the user 
                    }, 1000)
                    console.log(data.title)
                } else {
                    $("#createPostForm").replaceWith(data.formErrors);
                    $("#createPostModal").find("form").attr("id", "createPostForm");
                    $(e.target.nextElementSibling).fadeOut()
                };

                $(e.target).prop("disabled", false);
            },
            error: (error) => {
                console.log(error)
            }
        })
    });

    var postImagesInput = document.getElementById("id_images");
    var postImagesPreviewContainer = document.getElementById("PreviewImagesContainer")
    postImagesInput.onchange = (e) => {
        //why is the this element returning the document and not the target itself
        // check the length of the files to know what template to make
        var numberOfImages = e.target.files.length
        if (numberOfImages > 4) return;
        var row = document.createElement("div")
        row.setAttribute("class", "post-images")
        if (numberOfImages === 2) {
            row.style.gridTemplateColumns = "repeat(2, 1fr)";
        } else if (numberOfImages === 3) {
            row.style.gridTemplateColumns = "repeat(2, 1fr)";

        } else if (numberOfImages === 4) {
            row.style.gridTemplateColumns = "repeat(3, 1fr)";

        }
        for (file of e.target.files) {
            const postImageChild = document.createElement("div");
            postImageChild.setAttribute("class", "post-images__child")
            const reader = new FileReader();
            reader.onload = () => {
                img = document.createElement("img")
                img.setAttribute("src", reader.result)
                $(postImageChild).append(img)
            }
            $(row).prepend(postImageChild)
            $(postImagesPreviewContainer).append(row);
            reader.readAsDataURL(file)
        }
        $(".post-images div:nth-child(1)").css(
            "grid-column", "1 / 4"
        )

    }
})
function alertUser(key, message) {
    alertify.set('notifier', 'position', 'top-right');
    alertify.set('notifier', 'delay', 7);
    alertify.success(`${key}  ${message}`);

}