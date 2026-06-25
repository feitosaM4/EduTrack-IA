table perfil {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    int user_id {
      table = "user"
    }
  
    text nome filters=trim
    email email filters=trim|lower
    text curso? filters=trim
    text semestre? filters=trim
    text objetivo? filters=trim
    bool lembretes?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]
}