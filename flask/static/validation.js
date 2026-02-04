function validateForm() {
    let name = document.forms["studentForm"]["name"].value.trim();
    let email = document.forms["studentForm"]["email"].value.trim();
    let gender = document.querySelector('input[name="gender"]:checked');
    let course = document.querySelector('input[name="course"]:checked');

    let nameRegex = /^[A-Za-z ]{3,}$/;
    let emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    // Name validation
    if (!nameRegex.test(name)) {
        alert("Name must contain at least 3 letters and no numbers.");
        return false;
    }

    // Email validation
    if (!emailRegex.test(email)) {
        alert("Please enter a valid email address.");
        return false;
    }

    // Gender validation
    if (!gender) {
        alert("Please select a gender.");
        return false;
    }

    // Course validation
    if (!course) {
        alert("Please select a course.");
        return false;
    }

    return true;
}
