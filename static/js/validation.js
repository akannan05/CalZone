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

    let isValid = true;

    if (input.name === 'username') {
        if (input.value.trim() === '') {
            error.textContent = 'Username cannot be empty!';
            isValid = false;
        } else if (input.value.length > 180) {
            error.textContent = 'Username too big! (Max Size: 180)';
            isValid = false;
        } else if (!validUsername(input.value)) {
            error.textContent = 'Username contains invalid characters!';
            isValid = false;
        }
    }

    return isValid;
}

function validUsername(username) {
    return /^[a-zA-Z0-9-_]+$/.test(username);
}
