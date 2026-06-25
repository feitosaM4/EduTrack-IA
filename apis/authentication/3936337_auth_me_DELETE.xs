// Exclui o usuário logado
query "auth/me" verb=DELETE {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    db.del user {
      field_name = "id"
      field_value = $auth.id
    }
  }

  response = null
}