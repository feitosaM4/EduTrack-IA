// Get disciplinas record
query "disciplinas/{disciplinas_id}" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    int disciplinas_id? filters=min:1
  }

  stack {
    db.get disciplinas {
      field_name = "id"
      field_value = $input.disciplinas_id
    } as $model
  
    precondition ($model != null) {
      error_type = "notfound"
      error = "Not Found"
    }
  }

  response = $model
}