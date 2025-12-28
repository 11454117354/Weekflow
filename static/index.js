// Get weeks
(async () => {
    try {
        const response = await fetch("/api/weeks/all/", {credentials: "same-origin"});
        if (!response.ok){
            console.error("Failed to load weeks");
        }

        const weeks = await response.json();
        const weeklist = document.getElementById("week-list");

        weeklist.innerHTML = "";
        
        // week<li>
        weeks.forEach(week => {
            const li = document.createElement("li");
            li.classList.add("week-item");
            li.dataset.weekId = week.id;

            const nameSpan = document.createElement("span");
            nameSpan.innerText = week.name;

            const renameBtn = document.createElement("button");
            renameBtn.innerText = "R";
            renameBtn.classList.add("rename-btn");

            const archiveBtn = document.createElement("button");
            archiveBtn.innerText = "A";
            archiveBtn.classList.add("archive-btn");

            const deleteBtn = document.createElement("button");
            deleteBtn.innerText = "D";
            deleteBtn.classList.add("delete-btn");

            // rename button popup page
            renameBtn.addEventListener("click", e => {
                e.stopPropagation();
                const template = document.getElementById("week-popup-template");
                const popup = template.cloneNode(true);
                popup.id = "";
                popup.style.display = "flex";
                document.body.appendChild(popup);

                const cancelBtn = popup.querySelector(".popup-cancel");
                const confirmBtn = popup.querySelector(".popup-confirm");
                const nameInput = popup.querySelector(".popup-weekname");

                nameInput.value = week.name;

                cancelBtn.addEventListener("click", () => {
                    popup.remove();
                });

                confirmBtn.addEventListener("click", async () => {
                    const newName = nameInput.value.trim();
                    
                    if (!newName){
                        alert("Please fill in all fields");
                        return;
                    }

                    try {
                        const response = await fetch(`/api/weeks/${week.id}/rename/`, {
                            method: "PATCH",
                            credentials: "same-origin",
                            headers: {"Content-Type": "application/json"},
                            body: JSON.stringify({ name: newName })
                        });

                        if (!response.ok) {
                            throw new Error("Failed to rename week")
                        }

                        // modal.classList.remove("show");

                        location.reload();
                    } catch (error) {
                        console.error(error);
                        alert("Error renaming week");
                    }
                    console.log("submit new week name", week.id);

                    popup.remove();
                });

                console.log("rename week", week.id);
            })

            // archive button settings
            archiveBtn.addEventListener("click", async e => {
                e.stopPropagation();

                try {
                    if (week.archived == false){
                        const response = await fetch(`/api/weeks/${week.id}/archived`, {
                            method: "PATCH",
                            credentials: "same-origin",
                            headers: {"Content-Type": "application/json"},
                            body: JSON.stringify({ archived: true })
                        });

                        if (!response.ok) {
                            throw new Error("Failed to archive week")
                        }
                        location.reload();
                    }else if(week.archived == true){
                        const response = await fetch(`/api/weeks/${week.id}/archived`, {
                            method: "PATCH",
                            credentials: "same-origin",
                            headers: {"Content-Type": "application/json"},
                            body: JSON.stringify({ archived: false })
                        });

                        if (!response.ok) {
                            throw new Error("Failed to archive week")
                        }
                        location.reload();
                    }
                } catch (error) {
                        console.error(error);
                        alert("Error renaming week");
                }
                console.log("archived/unarchived a week", week.id);
            })

            // delete button settings
            deleteBtn.addEventListener("click", async e => {
                e.stopPropagation();

                if (!confirm("Are you sure to delete this week(with all tasks inside deleted)?")) return;

                try {
                    const response = await fetch(`/api/weeks/${week.id}/`, {
                        method: "DELETE",
                        credentials: "same-origin",
                    });

                    if (!response.ok) {
                        throw new Error("Failed to delete week")
                    }

                    li.remove();
                } catch (error) {
                    console.error(error);
                    alert("Error deleting week");
                }
            })

            li.appendChild(nameSpan);
            li.appendChild(renameBtn);
            li.appendChild(archiveBtn);
            li.appendChild(deleteBtn);

            weeklist.appendChild(li);
        });
    } catch (error) {
        console.error("Error loading weeks:", error);
    }
})();

// New week popup
const newWeekForm = document.getElementById("newWeek");
const modal = document.getElementById("modal");

newWeekForm.addEventListener("submit", e => {
    e.preventDefault();
    modal.classList.add("show");
});

document.getElementById("cancel").onclick = () => {
    modal.classList.remove("show");
};

document.getElementById("confirm").onclick = async () => {
    const name = document.getElementById("weekname").value.trim();
    const start = document.getElementById("week-start").value;
    const end = document.getElementById("week-end").value;

    if (!name || !start || !end) {
        alert("Please fill in all fields");
        return;
    }

    try {
        const response = await fetch("/api/week/create", {
            method: "POST",
            credentials: "same-origin",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                name: name,
                start_time: start,
                end_time: end
            })
        });

        if (!response.ok) {
            throw new Error("Failed to create new week")
        }

        modal.classList.remove("show");

        location.reload();
    } catch (error) {
        console.error(error);
        alert("Error creating week");
    }
};



// 1.在weeks的下面 新建week按钮 ✅
// 2.删去navbar中的week ✅
// 3.category一个dropdown menu，底下常驻一个新建
// 4.每个week加一个归档、一个删除按钮、一个重命名，归档后没清空的自动归到下一周（新api），已归档的放入下面折叠起来
// 5.tasks
// 6.navbar中的用户名点击形成一个dropdown menu，里面有logout和改密码