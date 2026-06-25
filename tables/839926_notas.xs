table notas {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    int user_id {
      table = "user"
    }
  
    int disciplinas_id {
      table = "disciplinas"
    }
  
    text nome filters=trim
    decimal nota
    date? data?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]
}