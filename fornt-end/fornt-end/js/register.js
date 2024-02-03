function matchPassword() {  
    var pw1 = document.getElementById("password");  
    var pw2 = document.getElementById("retypePassword");  
    if(pw1 != pw2)  
    {   
      alert("Passwords did not match");  
    } else {  
      alert("Password created successfully");  
    }  
  }  