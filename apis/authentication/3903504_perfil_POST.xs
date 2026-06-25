// Add perfil record
query perfil verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    dblink {
      table = "perfil"
    }
  }

  stack {
    db.add perfil {
      enforce_hidden_fields = false
      data = {
        user_id  : $auth.id
        nome     : $input.nome
        email    : $input.email
        curso    : $input.curso
        semestre : $input.semestre
        objetivo : $input.objetivo
        lembretes: $input.lembretes
      }
    } as $perfil
  }

  response = $perfil
}
