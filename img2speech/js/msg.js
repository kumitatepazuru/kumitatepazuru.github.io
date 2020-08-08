var id_ = 0;
var showid = [];

function remove_error() {
    document.getElementById(showid[0]).remove();
    showid.shift();
}

function show_msg(type, text) {
    document.getElementById('message').insertAdjacentHTML('beforeend', "<div class='message_box " + type + "' id='" + id_ + "'>" + text + "</div>");
    timeid = setTimeout(remove_error, 5000);
    showid.push(id_);
    id_ += 1;
}