// ----------------------------------------- Functions -----------------------------------------


async function handleLoginFormSubmit(event) {
  event.preventDefault(); // Impede o envio padrão do formulário

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const response = await fetch("http://localhost:5000/auth", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (response.ok) {
      localStorage.setItem("access_token", data.access_token);
      window.location.href = "/dashboard.html"; 

    } else {
      throw new Error()
    }
  } catch (error) {
    console.error("Erro na requisição:", error);
    loginWarning(response.status)
    
  }
}
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

document.querySelector('#submit_login').addEventListener('click', handleFormSubmit);
// Conecta a função ao envio do formulário
const loginForm = document.getElementById("login-form");
loginForm.addEventListener("submit", handleLoginFormSubmit);
