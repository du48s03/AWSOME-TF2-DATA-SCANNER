import re

def sanitize(string):
  """sanitize the input string. Escaping anyspecial characters except for '!', '&', ':', '_', '^', and '-'
     returns the sanitized string. 
  """
  ret = ""
  for c in string:
    if(c=="'"):
      ret+="''"
    else:
      ret+=c
  return ret
#    if(re.match(r'[^a-zA-Z0-9\!\&\:\_\^\-]', ""+c)):
#      ret+='\\'
#      ret+=c
#    else:
#      ret+=c
#  return ret
