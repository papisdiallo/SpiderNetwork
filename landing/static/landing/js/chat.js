$(document).ready(function () {

    let _id;
    let _username
    var _id_ = document.getElementById("other_user_id")
    if (_id_ !== null) {
        _id = _id_.textContent
    }
    var _username_ = document.getElementById("current_user_username")
    if (_username_ !== null) {
        _username = _username_.textContent
    }
    var url = `ws://${window.location.host}/ws/personalChat/${_id}/`
    if (window.location.pathname.includes("chat")) {
        var socket = new WebSocket(url)

        socket.onopen = (event) => {
            console.log("CONNECTION OPEN")
        }
        socket.onmessage = (e) => {
            let data = JSON.parse(e.data)
            console.log("data", data) // heer I need to send the data to the message area
            let float = data.username !== _username ? "ta-right" : "st3"
            let st3 = float === "st3" ? "st3" : ""
            var msg_div = `
                <div class="main-message-box ${float}">
                    <div class="message-dt ${st3}">
                        <div class="message-inner-dt">
                            <p>${data.message}.</p>
                        </div>
                        <span>5 minutes ago</span>
                    </div>
                    <div class="messg-usr-img">
                        <img src="${data.avatar_url}" alt="">
                    </div>
                </div>
             `
            $(".messages-line").append(msg_div);
        }
        socket.onerror = (e) => {
            console.log("there is an error", e)
        }
        socket.onclose = (event) => {
            console.log("CONNECTION CLOSE");
        }
        var input_message = document.getElementById("send_message")
        if (input_message !== null) {
            input_message.addEventListener('click', (e) => {
                e.preventDefault();
                var message = $("#message_to_send").val();
                socket.send(JSON.stringify({
                    'message': message,
                    'username': _username,
                }));
                $("#message_to_send").val(" ")
            });
        }
    }

})
