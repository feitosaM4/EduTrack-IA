// Delete notas record.
query "notas/{notas_id}" verb=DELETE {
  api_group = "Authentication"
  auth = "user"

  input {
    int notas_id? filters=min:1
  }

  stack {
    db.del notas {
      field_name = "id"
      field_value = $input.notas_id
    }
  }

  response = null
}