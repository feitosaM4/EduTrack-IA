// Get notas record
query "notas/{notas_id}" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    int notas_id? filters=min:1
  }

  stack {
    db.get notas {
      field_name = "id"
      field_value = $input.notas_id
    } as $notas
  
    precondition ($notas != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $notas
}