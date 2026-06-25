// Edit tarefas record
query "tarefas/{tarefas_id}" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    int tarefas_id? filters=min:1
    dblink {
      table = "tarefas"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch tarefas {
      field_name = "id"
      field_value = $input.tarefas_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $tarefas
  }

  response = $tarefas
}