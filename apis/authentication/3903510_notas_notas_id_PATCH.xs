// Edit notas record
query "notas/{notas_id}" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    int notas_id? filters=min:1
    dblink {
      table = "notas"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch notas {
      field_name = "id"
      field_value = $input.notas_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $notas
  }

  response = $notas
}