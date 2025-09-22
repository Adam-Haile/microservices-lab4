from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Todo App</title>
  <style>
    :root {
      --bg: #f6f7f9;
      --card: #ffffff;
      --text: #0f172a;
      --muted: #64748b;
      --primary: #2563eb;
      --border: #e2e8f0;
      --danger: #ef4444;
      --shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
    }
    * { box-sizing: border-box; }
    html, body { height: 100%; }
    body {
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }
    .app {
      max-width: 720px;
      margin: 40px auto;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 24px;
      box-shadow: var(--shadow);
    }
    h1 {
      margin: 0 0 16px;
      font-size: 28px;
      letter-spacing: -0.02em;
    }
    form {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 8px;
      margin-bottom: 16px;
    }
    input[type="text"] {
      width: 100%;
      padding: 12px 14px;
      border-radius: 12px;
      border: 1px solid var(--border);
      outline: none;
      font-size: 16px;
      transition: border-color 0.15s ease, box-shadow 0.15s ease;
      background: var(--card);
    }
    input[type="text"]::placeholder {
      color: #6b7280;
    }
    input[type="text"]:focus {
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }
    button {
      padding: 10px 14px;
      border-radius: 12px;
      border: 1px solid var(--border);
      background: #fff;
      color: var(--text);
      font-size: 14px;
      cursor: pointer;
      transition: background 0.15s ease, border-color 0.15s ease, color 0.15s ease;
    }
    button.primary {
      background: var(--primary);
      color: #fff;
      border-color: var(--primary);
    }
    button:hover { background: #f8fafc; }
    button.primary:hover { filter: brightness(0.95); }
    button:disabled { opacity: 0.6; cursor: not-allowed; }
    ul { list-style: none; padding: 0; margin: 0; }
    .todo-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px 12px;
      border: 1px solid var(--border);
      border-radius: 12px;
      margin: 8px 0;
      gap: 12px;
    }
    .todo {
      display: flex;
      align-items: center;
      gap: 10px;
      flex: 1;
      min-width: 0;
    }
    .todo input[type="checkbox"] { background: var(--card); width: 18px; height: 18px; }
    .todo .text {
      flex: 1;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .todo-item.completed .text { text-decoration: line-through; color: var(--muted); }
    .delete {
      border-color: #fee2e2;
      color: var(--danger);
      background: #fff;
      width: 36px;
      height: 36px;
      display: flex;
      justify-content: center;
      font-size: 20px;
      line-height: 0.6;
    }
    .delete:hover { background: #fff1f2; }
    .footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-top: 12px;
      gap: 12px;
      flex-wrap: wrap;
      color: var(--muted);
      font-size: 14px;
    }
    .filters { display: flex; gap: 6px; }
    .filters button.active { border-color: var(--primary); color: var(--primary); }
    .edit {
      width: 100%;
      padding: 8px 10px;
      border-radius: 10px;
      border: 1px solid var(--border);
      font-size: 16px;
    }
    @media (max-width: 480px) {
      .app { margin: 16px; padding: 16px; }
      form { grid-template-columns: 1fr; }
      form button { width: 100%; }
    }
  </style>
  <link rel="icon" href="data:," />
  <meta name="color-scheme" content="light dark" />
  <meta name="description" content="A minimal Todo app using localStorage." />
  <meta name="theme-color" content="#ffffff" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="default" />
</head>
<body>
  <main class="app" role="application" aria-label="Todo application">
    <h1>Todos</h1>
    <form id="todo-form" autocomplete="off">
      <input id="todo-input" type="text" placeholder="What needs to be done?" aria-label="Add todo" />
      <button type="submit" class="primary" aria-label="Add">Add</button>
    </form>

    <ul id="todo-list" role="list" aria-live="polite" aria-relevant="additions removals text"></ul>

    <div class="footer">
      <span id="todo-count">0 items left</span>
      <div class="filters" role="group" aria-label="filters">
        <button type="button" data-filter="all" class="active">All</button>
        <button type="button" data-filter="active">Active</button>
        <button type="button" data-filter="completed">Completed</button>
      </div>
      <button id="clear-completed" type="button">Clear completed</button>
    </div>
  </main>

  <script>
    (function () {
      const STORAGE_KEY = 'todos_v1';
      let todos = loadTodos();
      let currentFilter = 'all';

      const form = document.getElementById('todo-form');
      const input = document.getElementById('todo-input');
      const list = document.getElementById('todo-list');
      const count = document.getElementById('todo-count');
      const filters = document.querySelectorAll('.filters button');
      const clearCompletedBtn = document.getElementById('clear-completed');

      function loadTodos() {
        try {
          const raw = localStorage.getItem(STORAGE_KEY);
          return raw ? JSON.parse(raw) : [];
        } catch (e) {
          console.warn('Failed to parse todos from localStorage, resetting.', e);
          return [];
        }
      }

      function saveTodos() {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(todos));
      }

      function uid() {
        return Math.random().toString(36).slice(2) + Date.now().toString(36);
      }

      function addTodo(text) {
        const trimmed = text.trim();
        if (!trimmed) return;
        todos.push({ id: uid(), text: trimmed, completed: false, createdAt: Date.now() });
        saveAndRender();
      }

      function toggleTodo(id) {
        const todo = todos.find((t) => t.id === id);
        if (!todo) return;
        todo.completed = !todo.completed;
        saveAndRender();
      }

      function deleteTodo(id) {
        todos = todos.filter((t) => t.id !== id);
        saveAndRender();
      }

      function clearCompleted() {
        todos = todos.filter((t) => !t.completed);
        saveAndRender();
      }

      function setFilter(filter) {
        currentFilter = filter;
        filters.forEach((btn) => btn.classList.toggle('active', btn.dataset.filter === filter));
        render();
      }

      function filteredTodos() {
        if (currentFilter === 'active') return todos.filter((t) => !t.completed);
        if (currentFilter === 'completed') return todos.filter((t) => t.completed);
        return todos;
      }

      function saveAndRender() {
        saveTodos();
        render();
      }

      function render() {
        list.innerHTML = '';
        const items = filteredTodos();
        for (const t of items) {
          const li = document.createElement('li');
          li.className = 'todo-item' + (t.completed ? ' completed' : '');
          li.dataset.id = t.id;

          const label = document.createElement('label');
          label.className = 'todo';

          const checkbox = document.createElement('input');
          checkbox.type = 'checkbox';
          checkbox.checked = t.completed;
          checkbox.addEventListener('change', () => toggleTodo(t.id));

          const span = document.createElement('span');
          span.className = 'text';
          span.textContent = t.text;
          span.title = 'Double-click to edit';

          const del = document.createElement('button');
          del.className = 'delete';
          del.setAttribute('aria-label', 'Delete todo');
          del.textContent = '×';
          del.addEventListener('click', () => deleteTodo(t.id));

          label.appendChild(checkbox);
          label.appendChild(span);
          li.appendChild(label);
          li.appendChild(del);

          // Inline edit on double-click
          span.addEventListener('dblclick', () => {
            const inputEdit = document.createElement('input');
            inputEdit.type = 'text';
            inputEdit.value = t.text;
            inputEdit.className = 'edit';
            li.replaceChild(inputEdit, label);
            inputEdit.focus();
            const finish = (commit) => {
              if (commit) {
                const newText = inputEdit.value.trim();
                if (newText) {
                  t.text = newText;
                } else {
                  deleteTodo(t.id);
                  return;
                }
              }
              saveAndRender();
            };
            inputEdit.addEventListener('keydown', (e) => {
              if (e.key === 'Enter') finish(true);
              if (e.key === 'Escape') finish(false);
            });
            inputEdit.addEventListener('blur', () => finish(true));
          });

          list.appendChild(li);
        }

        const remaining = todos.filter((t) => !t.completed).length;
        count.textContent = `${remaining} ${remaining === 1 ? 'item' : 'items'} left`;
        clearCompletedBtn.disabled = todos.every((t) => !t.completed);
      }

      form.addEventListener('submit', (e) => {
        e.preventDefault();
        addTodo(input.value);
        input.value = '';
      });
      clearCompletedBtn.addEventListener('click', clearCompleted);
      filters.forEach((btn) => btn.addEventListener('click', () => setFilter(btn.dataset.filter)));

      render();
    })();
  </script>
</body>
</html>
    """
