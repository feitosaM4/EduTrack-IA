// Delete professores record.
query "professores/{professores_id}" verb=DELETE {
  api_group = "Authentication"
  auth = "user"

  input {
    int professores_id? filters=min:1
  }

  stack {
    db.del professores {
      field_name = "id"
      field_value = $input.professores_id
    }
  }

  response = null
}