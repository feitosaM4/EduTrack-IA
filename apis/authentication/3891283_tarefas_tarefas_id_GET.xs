// Get tarefas record
query "tarefas/{tarefas_id}" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    int tarefas_id? filters=min:1
  }

  stack {
    db.get tarefas {
      field_name = "id"
      field_value = $input.tarefas_id
    } as $tarefas
  
    precondition ($tarefas != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $tarefas
}