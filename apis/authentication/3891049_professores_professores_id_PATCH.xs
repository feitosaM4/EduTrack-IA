// Edit professores record
query "professores/{professores_id}" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    int professores_id? filters=min:1
    text nome? filters=trim
    email email? filters=trim|lower
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch professores {
      field_name = "id"
      field_value = $input.professores_id
      data = ```
        {
          nome: $input.nome
          email: $input.email
        }
        ```|filter_null|filter_empty_text
    } as $professores
  }

  response = $professores
}