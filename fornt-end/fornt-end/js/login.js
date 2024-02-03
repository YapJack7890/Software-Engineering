function login(){
    var username = document.getElementById("lusername").value;
    var password = document.getElementById("lpassword").value;

    if(isAdmin(username, password)){
        setUserType("admin");
        window.location.href = "admin-menu.html";
    }else if(isUser(username, password)){
        setUserType("user");
        window.location.href = "user-profile.html";
    }else if(isCanteenWorker(username, password)){
        setUserType("canteen");
        window.location.href = "canteen-orderlist.html";
    }else{
        alert("Wrong username or password");
    }

}
//this is mainly for testing purposes
function isAdmin(username, password){ //this may need to be change when intergrating
    if(username == "admin" && password == "1234"){
        return true;
    }else{
        return false;
    }
}

function isUser(username, password){ 
    if(username == "user" && password == "1234"){
        return true;
    }else{
        return false;
    }
}

function isCanteenWorker(username, password){
    if(username == "canteen" && password == "1234"){
        return true;
    }else{
        return false;
    }
}

function setUserType(userType){
    localStorage.setItem("userType", userType);
}