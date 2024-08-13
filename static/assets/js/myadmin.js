
// For Words and Character Counts
//document.addEventListener('DOMContentLoaded', function () {
//    const inputs = document.querySelectorAll('input[type="text"], input[type="password"], textarea');
//
//    inputs.forEach(function (input) {
//        if (input.id !== 'searchbar') {
//            const counter = document.createElement('div');
//            counter.classList.add('char-word-counter');
//            input.parentNode.insertBefore(counter, input.nextSibling);
//
//            const updateCounter = () => {
//                const value = input.value;
//                const charCount = value.length;
//                const wordCount = value.trim().split(/\s+/).filter(Boolean).length;
//                counter.textContent =` Words : ${wordCount} Characters : ${charCount}`;
//            };
//
//            updateCounter();
//
//            input.addEventListener('input', updateCounter);
//     }
//});
//});

document.addEventListener('DOMContentLoaded', function() {
    // Function to update word and character count
    function updateWordCharCount(event) {
        const target = event.target;
        const value = target.value;

        const wordCount = value.trim().split(/\s+/).filter(word => word.length > 0).length;
        const charCount = value.length;

        const countElement = target.parentNode.querySelector('.word-char-count');

        if (countElement) {
            countElement.textContent = `Words: ${wordCount}, Characters: ${charCount}`;
        }
    }

    // Exclude login page and forms that are not user-input forms
    if (!window.location.pathname.includes('login')) {
        const formFields = document.querySelectorAll('form input[type="text"], form input[type="email"], form input[type="password"], form textarea');

        formFields.forEach(field => {
            // Exclude CKEditor 5 fields
            if (!field.classList.contains('ck-editor__editable')) {
                const container = field.parentNode;

                // Create and insert the word and character count element
                let countElement = container.querySelector('.word-char-count');
                if (!countElement) {
                    countElement = document.createElement('div');
                    countElement.className = 'word-char-count';
                    container.appendChild(countElement);
                }

                // Add event listeners for input events
                field.addEventListener('input', updateWordCharCount);
                // Trigger initial count update
                updateWordCharCount({ target: field });
            }
        });
    }
});





$(document).ready(function() {
    // Target the password input elements and add a class
    $('input[type="password"]').addClass('vTextField');
//    $('input[type="text"]').addClass('form-control');
//    $('input[type="email"]').addClass('form-control');
//    $('input[type="password"]').addClass('form-control');
});



// for custom date picker
document.addEventListener('DOMContentLoaded', function() {
    const dateInputs = document.querySelectorAll('.vDateField');
    
    dateInputs.forEach(function(input) {
        // Change input type to date
        input.setAttribute('type', 'date');
        
        // Remove the <span> tag containing the calendar icon
        const span = input.parentNode.querySelector('.datetimeshortcuts');
        if (span) {
            span.parentNode.removeChild(span);
        }
        
        // Remove the <div> elements with the class "char-word-counter"
        const counterDiv = input.parentNode.querySelector('.datetimeshortcuts');
        if (counterDiv) {
            counterDiv.parentNode.removeChild(counterDiv);
     }
});
});