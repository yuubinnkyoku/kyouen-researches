from merge_verified_s10 import merge,parse_cache
assert parse_cache('a'*32+'\tWIN\n'+'b'*32+'\tLOSS\n')=={'a'*32:'WIN','b'*32:'LOSS'}
merged,overlap=merge({'a':'WIN','b':'LOSS'},{'a':'WIN','c':'LOSS'})
assert merged=={'a':'WIN','b':'LOSS','c':'LOSS'} and overlap==1
for a,b in [({'a':'WIN'},{'a':'LOSS'}),({'b':'LOSS'},{'b':'WIN'})]:
 try:merge(a,b)
 except ValueError as e:assert 'conflict' in str(e)
 else:raise AssertionError('conflicting verdict accepted')
for s in ['a'*32+'\tWIN\n'+'a'*32+'\tWIN\n','a'*32+'\tUNKNOWN\n']:
 try:parse_cache(s)
 except ValueError:pass
 else:raise AssertionError('invalid cache accepted')
print('PASS merge conflict and malformed input tests')
