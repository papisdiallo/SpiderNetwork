$(document).ready(function () {
    // $("button['data-bs-dismiss']").on("click", () => {
    //     console.log("a close has beend clicked"); reset the form any time th user cancels
    // the creation or exit the modal on purpose
    // })
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
            data: $("#createPostForm").serialize(),
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

    $(".post-jb.active").on("click", () => {
        console.log("the post create has been clicked")
    })
})
function alertUser(key, message) {
    alertify.set('notifier', 'position', 'top-right');
    alertify.set('notifier', 'delay', 7);
    alertify.success(`${key}  ${message}`);

}