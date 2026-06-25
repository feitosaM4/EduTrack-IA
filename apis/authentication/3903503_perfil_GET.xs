// Query perfil records for the authenticated user
query perfil verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    db.query perfil {
      where = $db.perfil.user_id == $auth.id
      return = {type: "list"}
    } as $perfil
  }

  response = $perfil
}
