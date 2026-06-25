// Add disciplinas record
query disciplinas verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    dblink {
      table = "disciplinas"
    }
  }

  stack {
    db.add disciplinas {
      enforce_hidden_fields = false
      data = {
        user_id        : $auth.id
        prof_id        : $input.prof_id
        nome_disciplina: $input.nome_disciplina
      }
    } as $model
  }

  response = $model
}