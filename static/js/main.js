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
                    if (response["is_saved"] == true) {
                        $this.html('<i class="fas fa-bookmark"></i>');
                    } else {
                        $this.html('<i class="far fa-bookmark"></i>');
                    }
                },
                401: function (response) {
                    window.location.href = "/accounts/login/";
                }
            }
        })
    })

    // AJAX request to follow/unfollow user
    $(".follow").off("click").on("click", function () {
        const $this = $(this);
        const user_id = $this.val();

        $.ajax({
            method: "POST",
            url: "/accounts/follow/",
            data: {
                user_id: user_id,
                csrfmiddlewaretoken: csrf_token,
            },
            statusCode: {
                200: function (response) {
                    if (response["is_following"] == true) {
                        $this.html('Following');
                        $this.attr("class", "btn btn-sm btn-outline-primary follow");
                    } else {
                        $this.html('Follow');
                        $this.attr("class", "btn btn-sm btn-primary follow");
                    }
                },
                401: function (response) {
                    window.location.href = "/accounts/login/";
                }
            }
        })
    });

})
