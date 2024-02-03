var notifImg = document.getElementById("notif");
var notification = document.getElementById('notification');
var originalSrc = notifImg.src;
var newSrc = "image/Bell Select.png";

notifImg.addEventListener('click', function(event) {
    notifImg.src = newSrc;
    notification.style.display = 'flex';
    event.stopPropagation();
});

document.addEventListener('click', function() {
    notifImg.src = originalSrc;
    notification.style.display = 'none';
});