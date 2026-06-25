// Delete tarefas record.
query "tarefas/{tarefas_id}" verb=DELETE {
  api_group = "Authentication"
  auth = "user"

  input {
    int tarefas_id? filters=min:1
  }

  stack {
    db.del tarefas {
      field_name = "id"
      field_value = $input.tarefas_id
    }
  }

  response = null
}