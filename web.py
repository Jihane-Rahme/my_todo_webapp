import streamlit as st
import functions

todos = functions.get_todos()

def add_todo():
    todo = st.session_state["new_todo"] + "\n"
    todos.append(todo)
    functions.write_todos(todos)

st.title("My Todo App")
st.subheader("This is my todo app.")
st.write("This app is to increase your productivity.")

for index, todo in enumerate(todos):
    col1, col2, col3 = st.columns([6, 1, 1])

    # Checkbox column
    with col1:
        checkbox = st.checkbox(todo.strip(), key=f"check_{index}")

    # Edit button column
    with col2:
        if st.button("✏️", key=f"edit_{index}"):
            st.session_state[f"editing_{index}"] = True

    # Delete if checked
    if checkbox:
        todos.pop(index)
        functions.write_todos(todos)
        st.rerun()

    # Show edit input if editing
    if st.session_state.get(f"editing_{index}", False):
        new_value = st.text_input(
            "Edit todo:",
            value=todo.strip(),
            key=f"input_{index}"
        )

        if st.button("Save", key=f"save_{index}"):
            todos[index] = new_value + "\n"
            functions.write_todos(todos)
            st.session_state[f"editing_{index}"] = False
            st.rerun()
