import streamlit as st
import functions  # your get_todos() and write_todos() functions

# --- Load todos ---
todos = functions.get_todos()

# --- Function to add a new todo ---
def add_todo():
    new = st.session_state["new_todo"].strip()
    if new:
        todos.append(new + "\n")
        functions.write_todos(todos)
        st.session_state["new_todo"] = ""  # clear input

# --- App layout ---
st.title("My Todo App")
st.subheader("This is my todo app.")
st.write("<h1>Increase your <b>productivity!</b></h1>",
             unsafe_allow_html=True)

# Input to add todos
st.text_input("Add a new todo:", key="new_todo")
st.button("Add", on_click=add_todo)

# --- Display todos with Edit and Done buttons ---
to_delete = []

for index, todo in enumerate(todos):
    # Three columns: Todo text | Edit button | Done button
    col_text, col_edit, col_done = st.columns([6, 2, 2])

    # Show the todo text
    with col_text:
        st.write(todo.strip())

    # Edit button with text next to pen
    with col_edit:
        if st.button("✏️ Edit", key=f"edit_{index}"):
            st.session_state[f"editing_{index}"] = True

    # Done button with text next to tick
    with col_done:
        if st.button("✅ Done", key=f"done_{index}"):
            to_delete.append(index)


    # Edit mode input below the row if active
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
            st.rerun()  # safe rerun after editing

# --- Remove completed todos safely ---
if to_delete:
    for index in sorted(to_delete, reverse=True):
        todos.pop(index)
    functions.write_todos(todos)
    st.rerun()  # safe rerun after deletion
