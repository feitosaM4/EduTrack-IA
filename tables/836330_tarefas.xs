table tarefas {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    int user_id? {
      table = "user"
    }
  
    int disc_id? {
      table = "disciplinas"
    }
  
    decimal nota?
    text nome_tarefa? filters=trim
    text nome? filters=trim
    text status? filters=trim|lower
    date? data?
    text tipo? filters=trim
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]
}