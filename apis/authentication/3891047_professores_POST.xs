// Add professores record
query professores verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    dblink {
      table = "professores"
    }
  }

  stack {
    db.add professores {
      enforce_hidden_fields = false
      data = {
        created_at: "now"
        user_id   : $auth.id
        nome      : $input.nome
        email     : $input.email
      }
    } as $professores
  }

  response = $professores
}