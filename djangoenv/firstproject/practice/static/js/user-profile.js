var links = document.querySelectorAll('.top-div a');
var addStudentButton = document.getElementById('add');
var formDiv = document.getElementById('form-div');  
var form = document.getElementById('form'); 
var displayFormDiv = document.getElementById('display-form');  
var addButton = document.getElementById('adder');
var cancelButton = document.getElementById('cancel');

links.forEach(function(link) {
    link.addEventListener('click', function() {
        // Remove the 'active' class from all links
        links.forEach(function(link) {
            link.classList.remove('active');
        });

        // Add the 'active' class to the clicked link
        this.classList.add('active');
    });
});

document.getElementById('profile-link').addEventListener('click', function() {
    document.getElementById('profile-section').style.display = 'block';
    document.getElementById('history-section').style.display = 'none';
    document.getElementById('profile-link').style.color = '#A97C4E';
    document.getElementById('history-link').style.color = '#000';
});

document.getElementById('profile-link').addEventListener('mouseover', function() {
    document.getElementById('profile-link').style.color = '#A97C4E'; 
});

document.getElementById('profile-link').addEventListener('mouseout', function() {
    if (document.getElementById('profile-section').style.display == 'block') {
        document.getElementById('profile-link').style.color = '#A97C4E';
    } else {
        document.getElementById('profile-link').style.color = '#000';
    }
});

document.getElementById('history-link').addEventListener('mouseover', function() {
    document.getElementById('history-link').style.color = '#A97C4E'; 
});

document.getElementById('history-link').addEventListener('mouseout', function() {
    if (document.getElementById('history-section').style.display == 'block') {
        document.getElementById('history-link').style.color = '#A97C4E';
    } else {
        document.getElementById('history-link').style.color = '#000';
    }
});

document.getElementById('history-link').addEventListener('click', function() {
    document.getElementById('profile-section').style.display = 'none';
    document.getElementById('history-section').style.display = 'block';
    document.getElementById('profile-link').style.color = '#000';
    document.getElementById('history-link').style.color = '#A97C4E';
});

function displayFormData(formData) {
    // Create a div to display the form data
    var dataDiv = document.createElement('div');

    // Add HTML content to the div
    dataDiv.innerHTML = '<h3>' + formData.get('student-id') + '</h3>' +
                        '<p class="S-name">' + formData.get('student-name') + '</p>' +
                        '<p class="S-gender">' + formData.get('gender') + '</p>' +
                        '<p class="S-grade">Grade' + formData.get('grade') + '</p>' +
                        '<p class="S-race">' + formData.get('race') + '</p>';
    var deleteButton = document.createElement('button');
    deleteButton.innerHTML = 'Delete';

    dataDiv.appendChild(deleteButton);
    // Add a class to the div
    dataDiv.className = 'form-data';
    deleteButton.addEventListener('click', function() {
        this.parentNode.remove();
    });


    // Select the container
    var container = document.getElementById('data-container');

    // Append the div to the container
    container.appendChild(dataDiv);
}

addStudentButton.addEventListener('click', function() {
    formDiv.style.display = 'flex';
});

cancelButton.addEventListener('click', function() {
    formDiv.style.display = 'none';
});

var button = document.getElementById('editButton');
    button.addEventListener('click', function() {
        window.location.href = "{% url 'editstudent' student.id %}";
    });

var menuButton = document.getElementById('menuButton');
    menuButton.addEventListener('click', function() {
        window.location.href = "{% url 'menu' student.id %}";
    });


