function login() {
    let form_login = document.getElementById("popup_login");
    let blur = document.getElementById("blur");
    if (form_login.classList.contains("hide")) {
        form_login.classList.add("show");
        form_login.classList.remove("hide");
        blur.classList.add("show");
        blur.classList.remove("hide");
    } else {
        form_login.classList.remove("show");
        form_login.classList.add("hide");
        blur.classList.add("hide");
        blur.classList.remove("show");
    }
}

function sign_up() {
    let form_login = document.getElementById("popup_sign_up");
    let blur = document.getElementById("blur");
    if (form_login.classList.contains("hide")) {
        form_login.classList.add("show");
        form_login.classList.remove("hide");
        blur.classList.add("show");
        blur.classList.remove("hide");
    } else {
        form_login.classList.remove("show");
        form_login.classList.add("hide");
        blur.classList.add("hide");
        blur.classList.remove("show");
    }
}

function deleteF(Id) {
    fetch('/delete', {
        method: 'POST',
        body: JSON.stringify({ Id: Id }),
    }).then((_res) => {
        window.location.href = "/home";
    });
}
function deleteSubFile(Id, folder_id) {
    fetch('/delete-subfile', {
        method: 'POST',
        body: JSON.stringify({ Id: Id }),
    }).then((_res) => {
        window.location.href = "/folder/" + folder_id;
    });

}
function deleteFolder(Id) {
    fetch('/delete-folder', {
        method: 'POST',
        body: JSON.stringify({ Id: Id }),
    })
        .then((res) => {
            if (res.ok) {
                return res.json();
            } else {
                throw new Error('Error deleting folder');
            }
        })
        .then((_data) => {
            window.location.href = "/home";
        })
        .catch((error) => {
            console.error(error);
        });
}

function deleteSubFolder(Id, parent_folder_id) {
    fetch('/delete-folder', {
        method: 'POST',
        body: JSON.stringify({ Id: Id }),
    })
        .then((res) => {
            if (res.ok) {
                return res.json();
            } else {
                throw new Error('Error deleting folder');
            }
        })
        .then((_data) => {
            window.location.href = "/folder/" + parent_folder_id;
        })
        .catch((error) => {
            console.error(error);
        });
}
function executeF(Id) {
    fetch('/execute', {
        method: 'POST',
        body: JSON.stringify({ Id: Id }),
    }).then((response) => {
        if (!response.ok) {
            throw new Error("HTTP error! Status:", response.status);
        }
        return response.json();
    }).then((res) => res.json)
        .then(data => {
            window.location.href = "/folder/" + folder_id;
        })

}


function executeSubF(Id, folder_id) {
    fetch('/executeSubF', {
        method: 'POST',
        body: JSON.stringify({ Id: Id }),
    }).then((_res) => {
        window.location.href = "/folder/" + folder_id;
    });
}