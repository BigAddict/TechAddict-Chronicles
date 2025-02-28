$(document).ready(function () {
    // CSRF protection used by django for POST requests
    var csrf_token = $("input[name=csrfmiddlewaretoken]").val()

    // AJAX request to save/unsave posts
    $(".bookmark").off("click").on("click", function () {
        const $this = $(this); // clicked button
        // Prevent multiple clicks
        if ($this.hasClass('processing')) return;
        $this.addClass('processing');

        const post_id = $this.val();

        $.ajax({
            method: "POST",
            url: "/ac/bookmark/",
            data: {
                post_id: post_id,
                csrfmiddlewaretoken: csrf_token,
            },
            statusCode: {
                200: function (response) {
                    if (response["is_saved"] == true) {
                        $this.html('<i class="fas fa-bookmark"></i>');
                    } else {
                        $this.html('<i class="far fa-bookmark"></i>');
                    }
                },
                401: function (response) {
                    window.location.href = "/accounts/login/";
                }
            },
            complete: function() {
                $this.removeClass('processing');
            }
        })
    })

    // AJAX request to follow/unfollow user
    $(".follow").off("click").on("click", function () {
        const $this = $(this);
        // Prevent multiple clicks
        if ($this.hasClass('processing')) return;
        $this.addClass('processing');

        const user_id = $this.val();

        $.ajax({
            method: "POST",
            url: "/ac/follow/",
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
            },
            complete: function() {
                $this.removeClass('processing');
            }
        })
    });

    // AJAX request to like/unlike posts
    $(".like").off("click").on("click", function () {
        const $this = $(this); // clicked button
        // Prevent multiple clicks
        if ($this.hasClass('processing')) return;
        $this.addClass('processing');

        const post_id = $this.val();

        $.ajax({
            method: "POST",
            url: "/ac/like/",
            data: {
                post_id: post_id,
                csrfmiddlewaretoken: csrf_token,
            },
            statusCode: {
                200: function (response) {
                    const likes = response["likes_count"]
                    if (response["is_liked"] == true) {
                        $this.html('<i class="fas fa-heart text-primary me-2"></i>' + likes);
                    } else {
                        $this.html('<i class="far fa-heart text-primary me-2"></i>' + likes);
                    }
                },
                401: function (response) {
                    window.location.href = "/accounts/login/";
                }
            },
            complete: function() {
                $this.removeClass('processing');
            }
        })
    })
})
