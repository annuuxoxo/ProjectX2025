import os

def analyze_file(file):

  with open (file,'r') as code:
    lines = code.readlines()

  violations = 0
  key_word= 0
  i=0
  total_quote_issues = 0

  for lin in lines:

    l = lin.lstrip()

    if len(l) >= 80:
      violations += 1
    
    if not l.strip().startswith('#') and any(kw in l for kw in ('print(', 'exec(', 'eval(')):
      violations += 1
      key_word += 1
    
    count = 0

    for ch in l:
      if ch in ("'",'"') :
        count += 1

    if count % 2 != 0:
      violations += 1
      total_quote_issues += 1

  #print(violations,count,key_word)
  print(file + ': ')
  print(f"Violations: {violations}")
  print(f"Quote issues: {total_quote_issues}")
  print(f"Risky keywords: {key_word}")

  if violations >= 1 and violations <= 5 and key_word == 0:
    print('LOW RISK')
  elif violations > 5 or key_word >= 1:
    print('HIGH RISK')
  else :
    print('CLEAN')
  print()

folder = 'src'
for file in os.listdir('src'):
  if file.endswith('.py'):
    file_path = os.path.join(folder,file)
  analyze_file(file_path)

