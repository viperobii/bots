import re

def code(text: str) -> str:
    return ''.join(f'\\x{ord(c):02x}' for c in text)

def tamper(encoded_code: str) -> str:
    return f'''
local tamper_guard=(function() local check = ("{encoded_code}"):gsub("\\\\x(%x%x)", function(h) return string.char(tonumber(h, 16)) end) local ok = true for i = 1, #check do local b = check:sub(i, i) if not b then ok = false break end end return ok end)()
assert(__tamper_guard, "Script integrity check failed")
'''.strip()

def obfuscate(lua_source: str) -> str:
    encoded = code(lua_source)
    tamper = tamper(encoded)
    return f'''
-- [[ Velonix Obfuscator v1.2.7 ]] return (function() {tamper} local src=("{encoded}"):gsub("\\\\x(%x%x)", function(h) return string.char(tonumber(h, 16)) end) local loader=loadstring or load local run=loader(src) return run() end)() '''.strip()
