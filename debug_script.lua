-- Debug script to extract v28 return values
-- This would be injected into the original script to dump values

local original_v28 = v28
local function debug_v28()
    local v93, v94, v95, v96, v97, v98, v99, v100 = original_v28()
    
    print("=== V28 RETURN VALUES DEBUG ===")
    print("v93:", type(v93), v93)
    print("v94:", type(v94), v94)
    print("v95:", type(v95), v95)
    print("v96:", type(v96), v96)
    print("v97:", type(v97), v97)
    print("v98:", type(v98), v98)
    print("v99:", type(v99), v99)
    print("v100:", type(v100), v100)
    print("=== END DEBUG ===")
    
    return v93, v94, v95, v96, v97, v98, v99, v100
end

-- Replace v28 with debug version
v28 = debug_v28
