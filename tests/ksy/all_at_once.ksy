meta:
  id: all_at_once
seq:
  - id: one_byte
    type: u1
  - id: two_bytes
    size: 2
  - id: three_str
    size: 2
    type: str
    encoding: UTF-8
  - id: four_array
    type: u1
    repeat: expr
    repeat-expr: 2
  - id: sized_struct
    type: substruct
    size: 1
  - id: unsized_struct
    type: substruct
types:
  substruct:
    seq:
      - id: one
        type: u1
instances:
  lazy_inst:
    pos: 0
    type: u1
  value_inst:
    value: one_byte + 1
