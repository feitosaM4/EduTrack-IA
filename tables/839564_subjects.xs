table subjects {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    // The name of the subject
    text name filters=trim
  
    // The name of the teacher
    text teacher? filters=trim
  
    // The weekly hours/workload of the subject
    int hours?
  
    // Reference to the authenticated user owning this subject
    int user_id? {
      table = "user"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]
}