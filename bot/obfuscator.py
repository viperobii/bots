# bot/obfuscator.py

def code(text: str) -> str:
    # Converts characters to hex escape format
    return ''.join('\\x{:02x}'.format(ord(c)) for c in text)

def tamper(encoded_code: str) -> str:
    # Lua code block that checks integrity of obfuscated code
    return f'''
local tamper_guard=(function() 
  local check = ("{encoded_code}"):gsub("\\\\x(%x%x)", function(h) return string.char(tonumber(h, 16)) end) 
  local ok = true 
  for i = 1, #check do 
    local b = check:sub(i, i) 
    if not b then ok = false break end 
  end 
  return ok 
end)()
assert(tamper_guard, "Script integrity check failed")
'''.strip()

def obfuscate(lua_source: str) -> str:
    # Main obfuscator function
    encoded = code(lua_source)
    tamper_code = tamper(encoded)
    return f'''
-- [[ Velonix Obfuscator v1.2.7 ]]
return (function()
{tamper_code}
local src=("{encoded}"):gsub("\\\\x(%x%x)", function(h) return string.char(tonumber(h, 16)) end)
local loader=loadstring or load
local run=loader(src)
return run()
end)()
'''.strip()
