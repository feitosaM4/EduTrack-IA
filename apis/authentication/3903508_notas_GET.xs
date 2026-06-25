// Query all notas records for the authenticated user
query notas verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    db.query notas {
      where = $db.notas.user_id == $auth.id
      return = {type: "list"}
    } as $notas
  }

  response = $notas
}
