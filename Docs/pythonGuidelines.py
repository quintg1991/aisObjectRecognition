
# PYTHON STYLE GUIDELINES

# Leave a space between comment syntax and the comment itself
# Lines should end at line 80

# A note on functions
# Good code should be easy enough to follow without the use of comments.
# That said, some snippets of code can benefit from comments when things get
#   hairy. Use your own descretion when commenting complex code.

# Descriptive variable names
theSuperImportantThing = True

# Brief description of what the function does
def forRealThoPythonIsCool():
  # Two space indentation
  if theSuperImportantThing:
    print("I am indeed important")
  else:
    print("Not so important")
  
  # One empty line between unrelated blocks of code
  for line in range(10):
    print("I am line: " + str(line))

forRealThoPythonIsCool()