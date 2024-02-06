var cancelButton = document.getElementById('cart-cancel');
var checkoutButton = document.getElementById('cart-checkout');

cancelButton.addEventListener('click', function() {
    window.location.href = 'user-menu.html';
});
checkoutButton.addEventListener('click', function() {
    window.location.href = 'checkout.html';
});