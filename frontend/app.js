const API_URL = "http://127.0.0.1:5000/todos";

async function fetchTodos() {
  const response = await fetch(API_URL);
  const todos = await response.json();
  const list = document.getElementById("todoList");
  list.innerHTML = "";

  todos.forEach(todo => {
    const li = document.createElement("li");
    li.textContent = todo.task;

    const delBtn = document.createElement("button");
    delBtn.textContent = "❌";
    delBtn.onclick = () => deleteTodo(todo.id);

    li.appendChild(delBtn);
    list.appendChild(li);
  });
}

async function addTodo() {
  const task = document.getElementById("taskInput").value.trim();
  if (!task) return alert("Task cannot be empty!");

  await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ task }),
  });

  document.getElementById("taskInput").value = "";
  fetchTodos();
}

async function deleteTodo(id) {
  await fetch(`${API_URL}/${id}`, { method: "DELETE" });
  fetchTodos();
}

fetchTodos();
