var backButton = document.getElementById('cart-back');
var placeorderButton = document.getElementById('cart-placeorder');

backButton.addEventListener('click', function() {
    window.location.href = 'cart.html';
});
placeorderButton.addEventListener('click', function() {
    window.location.href = '';
});