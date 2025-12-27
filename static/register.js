document.getElementById("register_form").addEventListener("submit", async (e) =>{
    e.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const password_confirm = document.getElementById("password_confirm").value.trim();

    if (!username || !password || !password_confirm) {
        document.getElementById("msg").innerText = "Please fill in all blanks!"
        return;
    }

    if (password != password_confirm) {
        document.getElementById("msg").innerText = "Password confirmation failed!"
        return;
    }

    try {
        const response = await fetch("/api/register/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "same-origin",
            body: JSON.stringify({username, password, password_confirm})
        });

        const data = await response.json();

        if (response.ok) {
            window.location.href = "/login";
        } else {
            document.getElementById("msg").innerText = data.message || "Register failed";
        }
    } catch (error) {
        console.error("Login error", error);
        document.getElementById("msg").innerText = "An error occurred. Please try again.";
    }
});