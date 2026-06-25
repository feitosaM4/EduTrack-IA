// Atualiza os dados do usuário logado
query "auth/me" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    text name filters=trim|min:1
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $auth.id
    } as $user1
  
    db.patch user {
      field_name = "id"
      field_value = $auth.id
      data = {name: $input.name}
    } as $user2
  }

  response = $user2
}