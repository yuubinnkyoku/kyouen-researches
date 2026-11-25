from merge_s10 import merge
base={'0'*32:('WIN',3)}
assert merge(base,{'0'*32:('WIN',3)})==(base,1)
for bad in [('LOSS',3),('WIN',4)]:
 try:merge(base,{'0'*32:bad})
 except ValueError:pass
 else:raise AssertionError('conflict accepted')
print('PASS merge rejects WIN/LOSS and state-count conflicts')
