// Edit perfil record
query "perfil/{perfil_id}" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    int perfil_id? filters=min:1
    dblink {
      table = "perfil"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch perfil {
      field_name = "id"
      field_value = $input.perfil_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $perfil
  }

  response = $perfil
}