// 监听表单提交事件
document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault(); // 阻止默认刷新

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    // 简单前端校验
    if (!username || !password) {
        document.getElementById("msg").innerText = "Please enter username and password.";
        return;
    }

    try {
        const response = await fetch("/api/login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "same-origin", // 保证 session cookie 能发送
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            // 登录成功，跳转到主页或 dashboard
            window.location.href = "/"; 
        } else {
            // 登录失败，显示错误信息
            document.getElementById("msg").innerText = data.message || "Login failed";
        }
    } catch (error) {
        console.error("Login error:", error);
        document.getElementById("msg").innerText = "An error occurred. Please try again.";
    }
});