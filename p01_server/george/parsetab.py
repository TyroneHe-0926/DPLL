
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = b'\xcd\r\x10\x90\x8f\xc1h\x05q\xd1\xc6\x9b\xc8%\xbc\xc8'
    
_lr_action_items = {'BOTTOM':([0,6,7,8,9,10,11,],[2,2,2,2,2,2,2,]),'TOP':([0,6,7,8,9,10,11,],[3,3,3,3,3,3,3,]),'ID':([0,6,7,8,9,10,11,12,13,23,],[4,4,4,4,4,4,4,22,22,22,]),'NOT':([0,6,7,8,9,10,11,],[6,6,6,6,6,6,6,]),'LPAREN':([0,6,7,8,9,10,11,12,13,23,],[7,7,7,7,7,7,7,23,23,23,]),'$end':([1,2,3,4,14,17,18,19,20,21,22,24,25,26,],[0,-1,-2,-3,-9,-10,-11,-12,-13,-7,-17,-8,-16,-22,]),'AND':([1,2,3,4,14,15,17,18,19,20,21,22,24,25,26,],[8,-1,-2,-3,-9,8,-10,8,8,8,-7,-17,-8,-16,-22,]),'OR':([1,2,3,4,14,15,17,18,19,20,21,22,24,25,26,],[9,-1,-2,-3,-9,9,-10,-11,9,9,-7,-17,-8,-16,-22,]),'IMP':([1,2,3,4,14,15,17,18,19,20,21,22,24,25,26,],[10,-1,-2,-3,-9,10,-10,-11,10,10,-7,-17,-8,-16,-22,]),'IFF':([1,2,3,4,14,15,17,18,19,20,21,22,24,25,26,],[11,-1,-2,-3,-9,11,-10,-11,-12,-13,-7,-17,-8,-16,-22,]),'RPAREN':([2,3,4,14,15,16,17,18,19,20,21,22,24,25,26,27,],[-1,-2,-3,-9,25,26,-10,-11,-12,-13,-7,-17,-8,-16,-22,26,]),'EQ':([4,5,16,26,],[-17,12,12,-22,]),'NOT_EQ':([4,5,16,26,],[-17,13,13,-22,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'formula':([0,6,7,8,9,10,11,],[1,14,15,17,18,19,20,]),'term':([0,6,7,8,9,10,11,12,13,23,],[5,5,16,5,5,5,5,21,24,27,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> formula","S'",1,None,None,None),
  ('formula -> BOTTOM','formula',1,'p_formula_bottom','/Users/nday/Downloads/Skeleton/george/../george/frml.py',561),
  ('formula -> TOP','formula',1,'p_formula_top','/Users/nday/Downloads/Skeleton/george/../george/frml.py',566),
  ('formula -> ID','formula',1,'p_formula_id','/Users/nday/Downloads/Skeleton/george/../george/frml.py',571),
  ('term_tuple -> LPAREN term_list RPAREN','term_tuple',3,'p_term_tuple','/Users/nday/Downloads/Skeleton/george/../george/frml.py',576),
  ('term_tuple_seq -> term_tuple','term_tuple_seq',1,'p_term_tuple_seq','/Users/nday/Downloads/Skeleton/george/../george/frml.py',580),
  ('term_tuple_seq -> term_tuple_seq COMMA term_tuple','term_tuple_seq',3,'p_term_tuple_seq','/Users/nday/Downloads/Skeleton/george/../george/frml.py',581),
  ('formula -> term EQ term','formula',3,'p_formula_eq','/Users/nday/Downloads/Skeleton/george/../george/frml.py',588),
  ('formula -> term NOT_EQ term','formula',3,'p_formula_not_eq','/Users/nday/Downloads/Skeleton/george/../george/frml.py',592),
  ('formula -> NOT formula','formula',2,'p_formula_not','/Users/nday/Downloads/Skeleton/george/../george/frml.py',597),
  ('formula -> formula AND formula','formula',3,'p_formula_and','/Users/nday/Downloads/Skeleton/george/../george/frml.py',602),
  ('formula -> formula OR formula','formula',3,'p_formula_or','/Users/nday/Downloads/Skeleton/george/../george/frml.py',616),
  ('formula -> formula IMP formula','formula',3,'p_formula_imp','/Users/nday/Downloads/Skeleton/george/../george/frml.py',630),
  ('formula -> formula IFF formula','formula',3,'p_formula_iff','/Users/nday/Downloads/Skeleton/george/../george/frml.py',634),
  ('id_list -> ID','id_list',1,'p_id_list_1','/Users/nday/Downloads/Skeleton/george/../george/frml.py',638),
  ('id_list -> id_list COMMA ID','id_list',3,'p_id_list_2','/Users/nday/Downloads/Skeleton/george/../george/frml.py',643),
  ('formula -> LPAREN formula RPAREN','formula',3,'p_formula_paren','/Users/nday/Downloads/Skeleton/george/../george/frml.py',648),
  ('term -> ID','term',1,'p_term_id','/Users/nday/Downloads/Skeleton/george/../george/frml.py',653),
  ('member_seq -> COLON id_in_id_seq','member_seq',2,'p_member_seq_1','/Users/nday/Downloads/Skeleton/george/../george/frml.py',657),
  ('member_seq -> <empty>','member_seq',0,'p_member_seq_2','/Users/nday/Downloads/Skeleton/george/../george/frml.py',661),
  ('id_in_id_seq -> ID INN ID','id_in_id_seq',3,'p_id_in_id_seq_1','/Users/nday/Downloads/Skeleton/george/../george/frml.py',665),
  ('id_in_id_seq -> id_in_id_seq COMMA ID INN ID','id_in_id_seq',5,'p_id_in_id_seq_2','/Users/nday/Downloads/Skeleton/george/../george/frml.py',669),
  ('term -> LPAREN term RPAREN','term',3,'p_term_paren','/Users/nday/Downloads/Skeleton/george/../george/frml.py',673),
  ('term_list -> term','term_list',1,'p_term_list_1','/Users/nday/Downloads/Skeleton/george/../george/frml.py',677),
  ('term_list -> term_list COMMA term','term_list',3,'p_term_list_2','/Users/nday/Downloads/Skeleton/george/../george/frml.py',681),
]