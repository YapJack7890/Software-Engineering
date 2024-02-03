var notifImg = document.getElementById("notif");
var notification = document.getElementById('notification');
var originalSrc = notifImg.src;
var newSrc = "image/Bell Select.png";
var addMenu = document.getElementById('add-menu');
var discardButton = document.getElementById('discard');
var submitButton = document.getElementById('submit');
var menuForm = document.getElementsByClassName('menu-form');
var addDiv = document.getElementById('add-div');
var imgClick = document.getElementById('imageclick');
var itemForm = document.getElementById('item-info');
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

itemForm.addEventListener('click', function(event) {
    event.stopPropagation();
});

document.addEventListener('click', function() {
    notifImg.src = originalSrc;
    itemForm.style.display = 'none';
    notification.style.display = 'none';
});

addMenu.addEventListener('click', function() {
    addDiv.style.display = 'flex';
});

discardButton.addEventListener('click', function() {
    addDiv.style.display = 'none';
});

function displayMenuItem(formData){
    var menuDiv = document.createElement('div');
    var blueP = document.createElement('div');
    var bluebox = document.createElement('div');
    var image = formData.get('image-file');
    var imageUrl = URL.createObjectURL(image);

    menuDiv,innerHTML = '<a href="admin-request.html"><img src="'+ imageUrl +'" alt="Menu Item" id="imageclick"></a>';
    blueP.innerHTML = '<p>'+ formData.get('food-name') +'</p>';
    bluebox.innerHTML = '<label class="switch">'+
                        '<input type ="checkbox">'+
                        '<span class="slider round">'+'</span>'+'<br>'+'</label>' +
                        '<p id="price">'+'RM '+ formData.get('price') +'</p>';
    menuDiv.appendChild(blueP);
    menuDiv.appendChild(bluebox);
    menuDiv.className = 'menu';
    main.appendChild(menuDiv);
}


function increase() {
    var value = parseInt(document.getElementById('number').value);
    if (value < 99) { // limit to 99
        document.getElementById('number').value = value + 1;
    }
}

function decrease() {
    var value = parseInt(document.getElementById('number').value);
    if (value > 1) { // ensure it doesn't go below 1
        document.getElementById('number').value = value - 1;
    }
}

function makeEditable(){
    var editable = document.getElementsByName("edit");
    for (var i = 0; i < editable.length; i++) {
        editable[i].removeAttribute("readonly");
    }

    // Hide the "EDIT" and "DELETE" buttons
    document.getElementById('edit-button').style.display = 'none';
    document.getElementById('delete-button').style.display = 'none';

    // Show the "SAVE" and "DISCARD" buttons
    document.getElementById('save-button').style.display = 'block';
    document.getElementById('discard-button').style.display = 'block';

}

function saveChanges() {
    // Get the input fields
    var foodName = document.getElementById('form-food-name');
    var ingredientList = document.getElementById('form-ingredient-list');
    var requestDescription = document.getElementById('form-request-description');
    var price = document.getElementById('form-price');

    // Store the values
    var foodNameValue = foodName.value;
    var ingredientListValue = ingredientList.value;
    var requestDescriptionValue = requestDescription.value;
    var priceValue = price.value;

    // Save the values to local storage
    localStorage.setItem('foodName', foodNameValue);
    localStorage.setItem('ingredientList', ingredientListValue);
    localStorage.setItem('requestDescription', requestDescriptionValue);
    localStorage.setItem('price', priceValue);

    buttonChange();
}

function buttonChange(){
    // Hide the "SAVE" and "DISCARD" buttons
   document.getElementById('save-button').style.display = 'none';
   document.getElementById('discard-button').style.display = 'none';

   // Show the "EDIT" and "DELETE" buttons
   document.getElementById('edit-button').style.display = 'block';
   document.getElementById('delete-button').style.display = 'block';

   var editable = document.getElementsByName("edit");
    for (var i = 0; i < editable.length; i++) {
        editable[i].setAttribute("readonly", "");
    }
}