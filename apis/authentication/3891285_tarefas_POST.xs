// Add tarefas record
query tarefas verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    dblink {
      table = "tarefas"
    }
  }

  stack {
    db.add tarefas {
      enforce_hidden_fields = false
      data = {
        user_id    : $auth.id
        disc_id    : $input.disc_id
        nota       : $input.nota
        nome_tarefa: $input.nome_tarefa
        nome       : $input.nome
        status     : $input.status
        data       : $input.data
        tipo       : $input.tipo
      }
    } as $tarefas
  }

  response = $tarefas
}