import re

def obfuscate(lua_source: str) -> str:
    encoded = code(lua_source)
    tamper_code = tamper(encoded)  # ✅ now it's clear and safe
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


def obfuscate(lua_source: str) -> str:
    encoded = code(lua_source)
    tamper = tamper(encoded)
    return f'''
-- [[ Velonix Obfuscator v1.2.7 ]] return (function() {tamper} local src=("{encoded}"):gsub("\\\\x(%x%x)", function(h) return string.char(tonumber(h, 16)) end) local loader=loadstring or load local run=loader(src) return run() end)() '''.strip()
