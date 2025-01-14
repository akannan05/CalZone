console.log('validation.js loaded');

document.querySelectorAll('input').forEach(input => {
    input.addEventListener('focus', function() {
        input.dataset.interacted = true;
    });

    input.addEventListener('input', function() {
        if (input.dataset.interacted) {
            validateInput(input);
        }
    });
});

function validateInput(input) {
    const error = document.getElementById(`${input.id}Error`);
    error.textContent = ''; // Clear previous error message


    if (input.name === 'username') {
        if (input.value.trim() === '') {
            error.textContent = 'Username cannot be empty!';
        } else if (input.value.length > 180) {
            error.textContent = 'Username too big! (Max Size: 180)';
        } else if (!validUsername(input.value)) {
            error.textContent = 'Username contains invalid characters!';
        }
    }

    if (input.name === 'password' || input.name === 'password-repeat') {
        if (input.value.trim() === '') {
            error.textContent = 'Password cannot be empty!';
        } else if (input.value.length > 180) {
            error.textContent = 'Password too big! (Max Size: 180)';
        } else if (!validPassword(input.value)) {
            error.textContent = 'Password contains invalid characters!';
        } 
    }

    if (input.name === 'govt_name') {
        if (input.value.trim() === ''){
            error.textContent = 'Name cannot be empty!';
        } else if (input.value.length > 100) {
            error.textContent = 'Name is to big! (Max Size: 100)';
        } else if (!validGobt(input.value)) {
            error.textContent = 'Name contains invalid characters!';
        }
    }

    return isValid;
}

function validUsername(username) {
    return /^[a-zA-Z0-9-_]+$/.test(username);
}

function validPassword(password) {
    return /^[a-zA-Z0-9-_!@#&\*\$\^]+$/.test(password);
}

function validGovt(name) {
    return /^[a-zA-Z-']+$/.test(password);
}
