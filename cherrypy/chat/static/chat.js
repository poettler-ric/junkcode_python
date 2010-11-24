var lastId = -1;
var user;
var message;

function readMessages(messages) {
    output = $('#messages');
    if (messages.length > 0) {
	$.each(messages, function(index, message) {
		output.val(output.val()
		    + message.user
		    + ': '
		    + message.message
		    + '\n');
		lastId++;
	});
    }
    output.scrollTop(99999); // hope we don't exceed 99999 lines...
}

function sendMessage() {
    user = $.trim($('#user').val());
    message = $.trim($('#message').val());
    data = {
	lastId: lastId,
	user: user,
	message: message
    };
    $.getJSON('/postMessage', data, readMessages);
 }

function retrieveMessages() {
    $.getJSON('/getMessage', { lastId: lastId }, readMessages);
    setTimeout(retrieveMessages, 1000);
}

$(document).ready(function() {
    retrieveMessages();
    $('#message').keydown(function(e) {
	if (e.keyCode == 13) {
	    sendMessage();
	    $('#message').val("");
	}
    });
});
