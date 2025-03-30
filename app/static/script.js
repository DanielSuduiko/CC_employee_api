let token = "";

async function authenticate() {
    token = document.getElementById("token-input").value;

    if (!token) {
        alert("Please enter a token!");
        return;
    }

    // Test token by calling a protected endpoint
    try {
        const res = await fetch("http://localhost:8000/employees/", {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });

        if (!res.ok) {
            const errorData = await res.json();
            throw new Error(errorData.error || "Authentication failed");
        }

        // Success - show API section
        document.getElementById("auth-section").classList.add("hidden");
        document.getElementById("api-section").classList.remove("hidden");

    } catch (error) {
        alert("Authentication failed: " + error.message);
    }
}


function showResponse(data) {
  document.getElementById("response-output").textContent = JSON.stringify(data, null, 2);
}

async function getAllEmployees() {
  const res = await fetch("http://localhost:8000/employees/", {
    headers: { Authorization: `Bearer ${token}` }
  });
  const data = await res.json();
  showResponse(data);
}

function promptEmployeeId() {
  const id = prompt("Enter employee ID:");
  if (id) getEmployeeById(id);
}

async function getEmployeeById(id) {
  const res = await fetch(`http://localhost:8000/employees/${id}`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  const data = await res.json();
  showResponse(data);
}

function promptAddEmployee() {
  const name = prompt("Enter name:");
  const dept = prompt("Enter department:");
  if (name && dept) addEmployee(name, dept);
}

async function addEmployee(name, department) {
  const res = await fetch("http://localhost:8000/employees/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ name, department })
  });
  const data = await res.json();
  showResponse(data);
}

function promptUpdateEmployee() {
  const id = prompt("Enter employee ID to update:");
  const name = prompt("Enter new name:");
  const dept = prompt("Enter new department:");
  if (id && name && dept) updateEmployee(id, name, dept);
}

async function updateEmployee(id, name, department) {
  const res = await fetch(`http://localhost:8000/employees/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ name, department })
  });
  const data = await res.json();
  showResponse(data);
}

function promptDeleteEmployee() {
  const id = prompt("Enter employee ID to delete:");
  if (id) deleteEmployee(id);
}

async function deleteEmployee(id) {
  const res = await fetch(`http://localhost:8000/employees/${id}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` }
  });
  const data = await res.json();
  showResponse(data);
}
