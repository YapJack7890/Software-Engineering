var notifImg = document.getElementById("notif");
var notification = document.getElementById('notification');
var originalSrc = notifImg.src;
var addMenu = document.getElementById('add-menu');
var discardButton = document.getElementById('discard');
var submitButton = document.getElementById('submit');
var menuForm = document.getElementsByClassName('menu-form');

var imgClick = document.getElementById('imageclick');
var editButton = document.getElementById('edit-button');
var main = document.getElementById('main');

notifImg.addEventListener('click', function(event) {
    notifImg.src = newSrc;
    notification.style.display = 'flex';
    event.stopPropagation();
});

imgClick.addEventListener('click', function(event) {
    itemForm.style.display = 'flex';
    event.stopPropagation();
});

document.addEventListener('click', function() {
    notifImg.src = originalSrc;
    notification.style.display = 'none';
});




