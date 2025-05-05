// ----------------------------------------- Functions -----------------------------------------

function loginProcessing(){
    var username = document.querySelector('#name').value; 
    var password = document.querySelector('#password').value;

    fetch("{{ url_for('login') }}", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username, password: password })
    })
        .then(response => {
            
            if (!response.ok) {
                
                if (response.status === 404) {
                    loginWarning(404);
                    throw new Error("Invalid User");
                } else if (response.status === 401) {
                    loginWarning(401)
                    throw new Error('Wrong Password');
                } else {
                    loginWarning(500)
                    throw new Error('Unexpected Error');
                };
            }
            return response.json();
            })
        
        .then(data => {
            console.log();
        })
        .catch(err => {
            console.log(`Error: ${err.message}`);
        });

};

//----------------

function loginWarning(status) {
    var warning = document.querySelector('#warning');
    
    if (!warning) {
        var main = document.querySelector("main");
        warning = document.createElement('p');
        warning.id = 'warning';
        main.appendChild(warning);
    };
    
    switch(status){
        case 401:
            warning.textContent= 'Invalid User. Try another one.';
            break;

        case 404:
            warning.textContent = 'Wrong Password. Try again.';
            break;
        
        case 500:
            warning.textContent = 'Server Error. Please, try again later.';
            break;
    }
    
};

// ---------------------------------------------------------------------------------------------------
// ----------------------------------------- Event Listeners -----------------------------------------

document.querySelector('#submit_login').addEventListener('click', loginProcessing);