// Get perfil record
query "perfil/{perfil_id}" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    int perfil_id? filters=min:1
  }

  stack {
    db.get perfil {
      field_name = "id"
      field_value = $input.perfil_id
    } as $perfil
  
    precondition ($perfil != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $perfil
}