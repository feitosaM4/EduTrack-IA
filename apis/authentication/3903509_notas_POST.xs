// Add notas record
query notas verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    dblink {
      table = "notas"
    }
  }

  stack {
    db.add notas {
      enforce_hidden_fields = false
      data = {
        user_id       : $auth.id
        disciplinas_id: $input.disciplinas_id
        nome          : $input.nome
        nota          : $input.nota
        data          : $input.data
      }
    } as $notas
  }

  response = $notas
}
