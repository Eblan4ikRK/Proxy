--[[
 .____                  ________ ___.    _____                           __                
 |    |    __ _______   \_____  \\_ |___/ ____\_ __  ______ ____ _____ _/  |_  ___________ 
 |    |   |  |  \__  \   /   |   \| __ \   __\  |  \/  ___// ___\\__  \\   __\/  _ \_  __ \
 |    |___|  |  // __ \_/    |    \ \_\ \  | |  |  /\___ \\  \___ / __ \|  | (  <_> )  | \/
 |_______ \____/(____  /\_______  /___  /__| |____//____  >\___  >____  /__|  \____/|__|   
         \/          \/         \/    \/                \/     \/     \/                   
          \_Welcome to LuaObfuscator.com   (Alpha 0.10.9) ~  Much Love, Ferib 

]]--
local v0 = tonumber;
local v1 = string.byte;
local v2 = string.char;
local v3 = string.sub;
local v4 = string.gsub;
local v5 = string.rep;
local v6 = table.concat;
local v7 = table.insert;
local v8 = math.ldexp;
local v9 = getfenv or function()
	return _ENV;
end;
local v10 = setmetatable;
local v11 = pcall;
local v12 = select;
local v13 = unpack or table.unpack;
local v14 = tonumber;
local function v15(v16, v17, ...)
	local v18 = 1;
	local v19;
	v16 = v4(v3(v16, 5), "..", function(v30)
		if (v1(v30, 2) == 81) then
			v19 = v0(v3(v30, 1, 1));
			return "";
		else
			local v89 = v2(v0(v30, 16));
			if v19 then
				local v112 = v5(v89, v19);
				v19 = nil;
				return v112;
			else
				return v89;
			end
		end
	end);
	local function v20(v31, v32, v33)
		if v33 then
			local v90 = (v31 / ((5 - 3) ^ (v32 - (2 - 1)))) % (2 ^ (((v33 - (1 - 0)) - (v32 - ((2 - 0) - 1))) + (620 - (555 + 64))));
			return v90 - (v90 % 1);
		else
			local v91 = 931 - (857 + 74);
			local v92;
			while true do
				if (v91 == ((2205 - (1523 + 114)) - (367 + 201))) then
					v92 = (929 - (214 + 713)) ^ (v32 - (1 + 0));
					return (((v31 % (v92 + v92)) >= v92) and (1 + 0)) or (877 - (254 + 28 + 595));
				end
			end
		end
	end
	local function v21()
		local v34 = 0;
		local v35;
		while true do
			if (v34 == 1) then
				return v35;
			end
			if (((1182 - (32 + 85)) - (68 + 997)) == v34) then
				v35 = v1(v16, v18, v18);
				v18 = v18 + (1271 - (226 + 1044));
				v34 = 4 - 3;
			end
		end
	end
	return v29(v28(), {}, v17)(...);
end
return v15("LOL!023Q0003053Q007072696E7403053Q00684Q6D00043Q00124Q00013Q001203000100024Q00013Q000200012Q00023Q00017Q00", v9(), ...);