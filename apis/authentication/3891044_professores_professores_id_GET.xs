// Get professores record
query "professores/{professores_id}" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    int professores_id? filters=min:1
  }

  stack {
    db.get professores {
      field_name = "id"
      field_value = $input.professores_id
    } as $professores
  
    precondition ($professores != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $professores
}