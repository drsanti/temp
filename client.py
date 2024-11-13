import flet as ft
import requests

# Base URL of your Flask API
FLASK_API_URL = "http://127.0.0.1:5000"

def main(page: ft.Page):
    page.title = "Task Management"
    page.vertical_alignment = ft.MainAxisAlignment.START

    task_list = ft.Column()

    def fetch_tasks():
        # Get the list of tasks from the Flask API
        response = requests.get(f"{FLASK_API_URL}/")
        if response.status_code == 200:
            tasks = response.json()
            task_list.controls.clear()
            for task in tasks:
                task_list.controls.append(ft.Text(f"{task['id']}: {task['name']}"))
            page.update()
        else:
            print("Error fetching tasks:", response.text)

    def add_task(e):
        task_name = task_name_input.value
        if task_name:
            response = requests.post(f"{FLASK_API_URL}/", json={"name": task_name})
            if response.status_code == 201 or response.status_code == 200:
                fetch_tasks()
            else:
                print("Error adding task:", response.text)

    def delete_task(e):
        try:
            task_id = int(task_id_input.value)
            response = requests.delete(f"{FLASK_API_URL}/{task_id}")
            if response.status_code == 200:
                fetch_tasks()
            else:
                print("Error deleting task:", response.text)
        except ValueError:
            print("Please enter a valid task ID.")

    def update_task(e):
        try:
            task_id = int(task_id_input.value)
            task_name = task_name_input.value
            if task_name:
                response = requests.put(f"{FLASK_API_URL}/{task_id}", json={"name": task_name})
                if response.status_code == 200:
                    fetch_tasks()
                else:
                    print("Error updating task:", response.text)
        except ValueError:
            print("Please enter a valid task ID.")

    # UI Elements
    task_name_input = ft.TextField(label="Task Name", autofocus=True)
    task_id_input = ft.TextField(label="Task ID")
    add_task_button = ft.ElevatedButton("Add Task", on_click=add_task)
    delete_task_button = ft.ElevatedButton("Delete Task", on_click=delete_task)
    update_task_button = ft.ElevatedButton("Update Task", on_click=update_task)

    page.add(
        task_name_input,
        task_id_input,
        add_task_button,
        delete_task_button,
        update_task_button,
        task_list,
    )

    # Fetch tasks when the app starts
    fetch_tasks()

# Run the Flet app
ft.app(target=main)
