$(document).ready(function () {
    // CSRF protection used by django for POST requests
    var csrf_token = $("input[name=csrfmiddlewaretoken]").val()

    // AJAX request to save/unsave posts
    $(".bookmark").off("click").on("click", function () {
        const $this = $(this); // clicked button
        const post_id = $this.val();

        $.ajax({
            method: "POST",
            url: "/accounts/bookmark/",
            data: {
                post_id: post_id,
                csrfmiddlewaretoken: csrf_token,
            },
            statusCode: {
                200: function (response) {
                    clicked_btn = $("button[value='" + response["post_id"] + "']")
                    if (response["is_bookmarked"] == true) {
                        $this.html('<i class="fas fa-bookmark"></i>');
                    } else {
                        $this.html('<i class="far fa-bookmark"></i>');
                    }
                },
                401: function (response) {
                    window.location.reload();
                }
            }
        })
    })

})
