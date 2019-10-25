const usernameField = document.querySelector('#id_username'),
    emailField = document.querySelector('#id_email'),
    fieldExistsUsername = document.querySelector('.field-exists.username'),
    fieldAvailableUsername = document.querySelector('.field-available.username'),
    fieldExistsEmail = document.querySelector('.field-exists.email'),
    fieldAvailableEmail = document.querySelector('.field-available.email');


const checkFieldAvailability = (usernameInputElement, emailInputElement) => {

    const xhttp = new XMLHttpRequest();

    emailInputElement.addEventListener('change', () => {
        xhttp.open('GET', `ajax/email_verification?email=${emailInputElement.value}`);
        xhttp.onreadystatechange = () => {
            
            if (xhttp.readyState == 4 && xhttp.status == 200) {
                let response = JSON.parse(xhttp.responseText);
                
                if (response.email_available) {
                    fieldAvailableEmail.style.display = 'block';
                    fieldExistsEmail.style.display = 'none';

                } else {
                    fieldExistsEmail.classList.display = 'block';
                    fieldAvailableEmail.style.display = 'none';
                }
            }
        };
        xhttp.send();
    });

    usernameInputElement.addEventListener('change', () => {
        xhttp.open('GET', `ajax/username_verification?username=${usernameInputElement.value}`);
        xhttp.onreadystatechange = () => {
            
            if (xhttp.readyState == 4 && xhttp.status == 200) {
                let response = JSON.parse(xhttp.responseText);
                
                if (response.username_available) {
                    fieldAvailableUsername.style.display = 'block';
                    fieldExistsUsername.style.display = 'none';
                } else {
                    fieldExistsUsername.style.display = 'block';
                    fieldAvailableUsername.style.display = 'none';
                }
            }
        };
        xhttp.send();
    });
    

};

checkFieldAvailability(usernameField, emailField);