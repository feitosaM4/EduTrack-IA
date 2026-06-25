// Delete perfil record.
query "perfil/{perfil_id}" verb=DELETE {
  api_group = "Authentication"
  auth = "user"

  input {
    int perfil_id? filters=min:1
  }

  stack {
    db.del perfil {
      field_name = "id"
      field_value = $input.perfil_id
    }
  }

  response = null
}