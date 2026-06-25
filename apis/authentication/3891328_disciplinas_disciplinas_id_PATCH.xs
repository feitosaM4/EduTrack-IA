// Edit disciplinas record
query "disciplinas/{disciplinas_id}" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    int disciplinas_id? filters=min:1
    dblink {
      table = "disciplinas"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch disciplinas {
      field_name = "id"
      field_value = $input.disciplinas_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $model
  }

  response = $model
}