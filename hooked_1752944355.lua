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
	local function v22()
		local v36 = 0;
		local v37;
		local v38;
		while true do
			if (v36 == (0 + 0)) then
				v37, v38 = v1(v16, v18, v18 + 1 + 1);
				v18 = v18 + (959 - (892 + 65));
				v36 = (352 - (87 + 263)) - 1;
			end
			if (v36 == (1 - 0)) then
				return (v38 * (469 - 213)) + v37;
			end
		end
	end
	local function v23()
		local v39 = 180 - (67 + 113);
		local v40;
		local v41;
		local v42;
		local v43;
		while true do
			if (v39 == (1 + 0)) then
				return (v43 * ((74718629 - 33527810) - (17770393 + 6643210))) + (v42 * 65536) + (v41 * (189 + 67)) + v40;
			end
			if (v39 == (0 - 0)) then
				v40, v41, v42, v43 = v1(v16, v18, v18 + 3);
				v18 = v18 + (956 - (802 + 150));
				v39 = 2 - 1;
			end
		end
	end
	local function v24()
		local v44 = 0 + 0;
		local v45;
		local v46;
		local v47;
		local v48;
		local v49;
		local v50;
		while true do
			if (v44 == (997 - ((1970 - (87 + 968)) + 82))) then
				v45 = v23();
				v46 = v23();
				v44 = 2 - 1;
			end
			if (v44 == (1 + (0 - 0))) then
				v47 = 1 - 0;
				v48 = (v20(v46, 1188 - (1069 + 118), (32 - 20) + 8) * ((7 - 5) ^ (113 - 81))) + v45;
				v44 = 4 - 2;
			end
			if (v44 == (6 - 3)) then
				if (v49 == (0 + 0)) then
					if (v48 == (0 - 0)) then
						return v50 * ((0 - 0) + 0);
					else
						v49 = 792 - (368 + 384 + 39);
						v47 = 0 + (0 - 0);
					end
				elseif (v49 == (6433 - 4386)) then
					return ((v48 == (18 - (10 + 1 + 7))) and (v50 * ((886 - (261 + 624)) / (0 - 0)))) or (v50 * NaN);
				end
				return v8(v50, v49 - (1465 - (416 + 26))) * (v47 + (v48 / ((6 - 4) ^ (23 + (79 - 50)))));
			end
			if (v44 == (9 - 7)) then
				v49 = v20(v46, 36 - (1832 - (1703 + 114)), 469 - (145 + 293));
				v50 = ((v20(v46, 1779 - (760 + 987)) == (431 - (44 + 386))) and -((2188 - (376 + 325)) - (784 + 214 + 488))) or (767 - (745 + 21));
				v44 = 1 + 2;
			end
		end
	end
	local function v25(v51)
		local v52;
		if not v51 then
			v51 = v23();
			if (v51 == (0 - 0)) then
				return "";
			end
		end
		v52 = v3(v16, v18, (v18 + v51) - 1);
		v18 = v18 + v51;
		local v53 = {};
		for v69 = 2 - 1, #v52 do
			v53[v69] = v2(v1(v3(v52, v69, v69)));
		end
		return v6(v53);
	end
	local v26 = v23;
	local function v27(...)
		return {...}, v12("#", ...);
	end
	local function v28()
		local v54 = (function()
			return function(v93, v94, v95, v96, v97, v98, v99, v100)
				local v93 = (function()
					return 1763 - (454 + 1309);
				end)();
				local v94 = (function()
					return;
				end)();
				local v95 = (function()
					return;
				end)();
				while true do
					if (v93 == #" ") then
						if (v94 == #"[") then
							v95 = (function()
								return v96() ~= 0;
							end)();
						elseif (v94 == 2) then
							v95 = (function()
								return v97();
							end)();
						elseif (v94 == #"-19") then
							v95 = (function()
								return v98();
							end)();
						end
						v99[v100] = (function()
							return v95;
						end)();
						break;
					end
					if (v93 ~= 0) then
					else
						local v118 = (function()
							return 0;
						end)();
						while true do
							if (v118 ~= 1) then
							else
								v93 = (function()
									return #".";
								end)();
								break;
							end
							if (v118 == (0 + 0)) then
								v94 = (function()
									return v96();
								end)();
								v95 = (function()
									return nil;
								end)();
								v118 = (function()
									return 1 - 0;
								end)();
							end
						end
					end
				end
				return v93, v94, v95, v96, v97, v98, v99, v100;
			end;
		end)();
		local v55 = (function()
			return function(v101, v102, v103)
				local v104 = (function()
					return 0 - 0;
				end)();
				local v105 = (function()
					return;
				end)();
				while true do
					if (v104 == (0 - 0)) then
						v105 = (function()
							return 285 - (134 + 151);
						end)();
						while true do
							if (v105 ~= 0) then
							else
								local v123 = (function()
									return 1665 - (970 + 695);
								end)();
								local v124 = (function()
									return;
								end)();
								while true do
									if (v123 == 0) then
										v124 = (function()
											return 0 - 0;
										end)();
										while true do
											if (v124 == (1990 - (582 + 1408))) then
												local v136 = (function()
													return 0 - 0;
												end)();
												while true do
													if (v136 == (0 - 0)) then
														v101[v102 - #","] = (function()
															return v103();
														end)();
														return v101, v102, v103;
													end
												end
											end
										end
										break;
									end
								end
							end
						end
						break;
					end
				end
			end;
		end)();
		local v56 = (function()
			return {};
		end)();
		local v57 = (function()
			return {};
		end)();
		local v58 = (function()
			return {};
		end)();
		local v59 = (function()
			return {v56,v57,nil,v58};
		end)();
		local v60 = (function()
			return v23();
		end)();
		local v61 = (function()
			return {};
		end)();
		for v71 = #">", v60 do
			FlatIdent_60EA1, Type, Cons, v21, v24, v25, v61, v71 = (function()
				return v54(FlatIdent_60EA1, Type, Cons, v21, v24, v25, v61, v71);
			end)();
		end
		v59[#"nil"] = (function()
			return v21();
		end)();
		for v72 = #".", v23() do
			local v73 = (function()
				return v21();
			end)();
			if (v20(v73, #"!", #"/") ~= (1824 - (1195 + 629))) then
			else
				local v108 = (function()
					return 0 - 0;
				end)();
				local v109 = (function()
					return;
				end)();
				local v110 = (function()
					return;
				end)();
				local v111 = (function()
					return;
				end)();
				while true do
					if ((242 - (187 + 54)) == v108) then
						local v121 = (function()
							return 780 - (162 + 618);
						end)();
						while true do
							if (v121 ~= (0 + 0)) then
							else
								v111 = (function()
									return {v22(),v22(),nil,nil};
								end)();
								if (v109 == 0) then
									local v133 = (function()
										return 0 - 0;
									end)();
									local v134 = (function()
										return;
									end)();
									while true do
										if (v133 ~= (0 - 0)) then
										else
											v134 = (function()
												return 0;
											end)();
											while true do
												if (v134 == (0 + 0)) then
													v111[#"91("] = (function()
														return v22();
													end)();
													v111[#"xnxx"] = (function()
														return v22();
													end)();
													break;
												end
											end
											break;
										end
									end
								elseif (v109 == #".") then
									v111[#"gha"] = (function()
										return v23();
									end)();
								elseif (v109 == 2) then
									v111[#"xnx"] = (function()
										return v23() - ((1638 - (1373 + 263)) ^ 16);
									end)();
								elseif (v109 ~= #"-19") then
								else
									local v141 = (function()
										return 1000 - (451 + 549);
									end)();
									local v142 = (function()
										return;
									end)();
									while true do
										if (v141 ~= (0 - 0)) then
										else
											v142 = (function()
												return 0;
											end)();
											while true do
												if (v142 ~= 0) then
												else
													v111[#"xxx"] = (function()
														return v23() - ((2 - 0) ^ 16);
													end)();
													v111[#".com"] = (function()
														return v22();
													end)();
													break;
												end
											end
											break;
										end
									end
								end
								v121 = (function()
									return 1;
								end)();
							end
							if (v121 ~= 1) then
							else
								v108 = (function()
									return 2 - 0;
								end)();
								break;
							end
						end
					end
					if (v108 ~= (1384 - (746 + 638))) then
					else
						v109 = (function()
							return v20(v73, 2, #"91(");
						end)();
						v110 = (function()
							return v20(v73, #".com", 3 + 3);
						end)();
						v108 = (function()
							return 1 - 0;
						end)();
					end
					if (v108 == (343 - (218 + 123))) then
						if (v20(v110, #".", #":") ~= #"\\") then
						else
							v111[1583 - (1535 + 46)] = (function()
								return v61[v111[2]];
							end)();
						end
						if (v20(v110, 2 + 0, 1 + 1) ~= #"/") then
						else
							v111[#"-19"] = (function()
								return v61[v111[#"-19"]];
							end)();
						end
						v108 = (function()
							return 563 - (306 + 254);
						end)();
					end
					if (v108 ~= 3) then
					else
						if (v20(v110, #"91(", #"91(") == #"]") then
							v111[#"0313"] = (function()
								return v61[v111[#"?id="]];
							end)();
						end
						v56[v72] = (function()
							return v111;
						end)();
						break;
					end
				end
			end
		end
		for v74 = #"\\", v23() do
			v57, v74, v28 = (function()
				return v55(v57, v74, v28);
			end)();
		end
		return v59;
	end
	local function v29(v63, v64, v65)
		local v66 = v63[1 + 0];
		local v67 = v63[1 + (1146 - (466 + 679))];
		local v68 = v63[703 - (271 + 429)];
		return function(...)
			local v75 = v66;
			local v76 = v67;
			local v77 = v68;
			local v78 = v27;
			local v79 = 1 - (0 - 0);
			local v80 = -(1468 - ((2571 - 1672) + 568));
			local v81 = {};
			local v82 = {...};
			local v83 = v12("#", ...) - ((1901 - (106 + 1794)) + 0);
			local v84 = {};
			local v85 = {};
			for v106 = 0 - 0, v83 do
				if ((2183 >= 1607) and (v106 >= v77)) then
					v81[v106 - v77] = v82[v106 + 1 + 0 + 0];
				else
					v85[v106] = v82[v106 + (604 - (268 + 335))];
				end
			end
			local v86 = (v83 - v77) + ((74 + 217) - (60 + 230));
			local v87;
			local v88;
			while true do
				local v107 = 1171 - (418 + 753);
				while true do
					if ((v107 == (573 - (426 + 146))) or (4549 == 1153)) then
						if (v88 <= (1 + 0)) then
							if ((v88 == (0 + 0)) or (4674 < 4672)) then
								v85[v87[1458 - (282 + (3466 - 2292))]] = v65[v87[1 + 2]];
							else
								local v130 = v87[(1437 - 906) - (406 + 123)];
								v85[v130](v85[v130 + (812 - (569 + 242))]);
							end
						elseif (v88 > (5 - 3)) then
							v85[v87[1 + 1]] = v87[1027 - (706 + (432 - (4 + 110)))];
						else
							do
								return;
							end
						end
						v79 = v79 + (1252 - (721 + 530));
						break;
					end
					if (v107 == (1271 - (945 + (910 - (57 + 527))))) then
						v87 = v75[v79];
						v88 = v87[1];
						v107 = 2 - 1;
					end
				end
			end
		end;
	end
	return v29(v28(), {}, v17)(...);
end
-- ====== FULL HOOK INJECTION START ======
print("🚀 FULL HOOK DUMPER активирован!")
print("📊 Начинаем извлечение всех данных из LuaObfuscator.com")
print("")

-- Глобальные переменные для сбора данных
_FULL_DUMP = {
    strings = {},
    functions = {},
    constants = {},
    instructions = {},
    vm_structure = {},
    execution_trace = {}
}

local _string_counter = 0
local _function_counter = 0
local _constant_counter = 0
local _instruction_counter = 0

-- Утилиты
local function safe_tostring(obj)
    if type(obj) == "string" then
        return '"' .. obj .. '"'
    elseif type(obj) == "function" then
        return "function:" .. tostring(obj):sub(10)
    elseif type(obj) == "table" then
        local count = 0
        for _ in pairs(obj) do count = count + 1 end
        return "table[" .. count .. "]"
    else
        return tostring(obj)
    end
end

local function capture_string(str, source, context)
    if type(str) == "string" and #str > 0 then
        _string_counter = _string_counter + 1
        local entry = {
            id = _string_counter,
            value = str,
            length = #str,
            source = source or "unknown",
            context = context or "general",
            timestamp = os.date("%H:%M:%S")
        }
        table.insert(_FULL_DUMP.strings, entry)
        print("📝 [STR " .. _string_counter .. "] (" .. entry.source .. ") '" .. str .. "'")
    end
end

local function capture_function(func, name, source, context)
    if type(func) == "function" then
        _function_counter = _function_counter + 1
        local entry = {
            id = _function_counter,
            name = name or "anonymous",
            address = tostring(func),
            source = source or "unknown",
            context = context or "general",
            timestamp = os.date("%H:%M:%S")
        }
        table.insert(_FULL_DUMP.functions, entry)
        print("🔧 [FNC " .. _function_counter .. "] " .. entry.name .. " (" .. entry.source .. ") " .. entry.address)
    end
end

local function capture_constant(const, index, source, context)
    _constant_counter = _constant_counter + 1
    local entry = {
        id = _constant_counter,
        index = index or _constant_counter,
        value = const,
        type = type(const),
        source = source or "unknown", 
        context = context or "general",
        timestamp = os.date("%H:%M:%S")
    }
    table.insert(_FULL_DUMP.constants, entry)
    print("📋 [CON " .. _constant_counter .. "] [" .. entry.index .. "] " .. entry.type .. ": " .. safe_tostring(const))
    
    -- Автоматически захватываем строки из констант
    if type(const) == "string" then
        capture_string(const, source .. "_constant", context)
    end
end

local function capture_instruction(instr, index, source, context)
    _instruction_counter = _instruction_counter + 1
    local entry = {
        id = _instruction_counter,
        index = index or _instruction_counter,
        instruction = instr,
        source = source or "unknown",
        context = context or "general",
        timestamp = os.date("%H:%M:%S")
    }
    table.insert(_FULL_DUMP.instructions, entry)
    
    local instr_str = ""
    if type(instr) == "table" then
        for i, v in ipairs(instr) do
            instr_str = instr_str .. tostring(v) .. " "
        end
    else
        instr_str = tostring(instr)
    end
    print("⚡ [INS " .. _instruction_counter .. "] [" .. entry.index .. "] " .. instr_str)
end

-- ============= HOOK v28 FUNCTION =============
if v28 then
    print("🎯 Устанавливаем hook на v28...")
    local original_v28 = v28
    
    v28 = function(...)
        print("")
        print("🎯 ===== HOOK v28 TRIGGERED =====")
        print("⏰ Время: " .. os.date("%H:%M:%S"))
        
        -- Вызываем оригинальную функцию
        local vm_result = original_v28(...)
        
        print("📊 v28 result type: " .. type(vm_result))
        
        if type(vm_result) == "table" then
            print("📦 VM structure components: " .. #vm_result)
            
            _FULL_DUMP.vm_structure = {
                type = "table",
                count = #vm_result,
                components = {}
            }
            
            for i = 1, #vm_result do
                local component = vm_result[i]
                local comp_type = type(component)
                print("🔹 Component[" .. i .. "]: " .. comp_type)
                
                local comp_info = {
                    index = i,
                    type = comp_type,
                    details = {}
                }
                
                if comp_type == "table" then
                    local size = 0
                    for _ in pairs(component) do size = size + 1 end
                    print("   📦 Table size: " .. size)
                    comp_info.size = size
                    
                    -- Component 1: Instructions
                    if i == 1 and size > 0 then
                        print("   🔧 EXTRACTING VM INSTRUCTIONS:")
                        local instr_count = 0
                        for j, instr in pairs(component) do
                            instr_count = instr_count + 1
                            if instr_count <= 30 then
                                capture_instruction(instr, j, "v28_component1", "vm_instructions")
                            end
                        end
                        if instr_count > 30 then
                            print("      ... и ещё " .. (instr_count - 30) .. " инструкций")
                        end
                        comp_info.instruction_count = instr_count
                    end
                    
                    -- Component 2: Constants
                    if i == 2 and size > 0 then
                        print("   📚 EXTRACTING CONSTANTS:")
                        local const_count = 0
                        for j, const in pairs(component) do
                            const_count = const_count + 1
                            if const_count <= 100 then
                                capture_constant(const, j, "v28_component2", "vm_constants")
                            end
                        end
                        if const_count > 100 then
                            print("      ... и ещё " .. (const_count - 100) .. " констант")
                        end
                        comp_info.constant_count = const_count
                    end
                    
                    -- Component 4: Functions
                    if i == 4 and size > 0 then
                        print("   ⚙️ EXTRACTING FUNCTIONS:")
                        local func_count = 0
                        for j, func in pairs(component) do
                            func_count = func_count + 1
                            if func_count <= 20 then
                                capture_function(func, "vm_func_" .. j, "v28_component4", "vm_functions")
                            end
                        end
                        comp_info.function_count = func_count
                    end
                end
                
                table.insert(_FULL_DUMP.vm_structure.components, comp_info)
            end
        end
        
        print("🎯 ===== END v28 HOOK =====")
        print("")
        return vm_result
    end
    print("✅ v28 hook установлен!")
else
    print("⚠️ v28 function не найдена")
end

-- ============= HOOK v29 FUNCTION =============
if v29 then
    print("⚡ Устанавливаем hook на v29...")
    local original_v29 = v29
    
    v29 = function(vm_data, env, ...)
        print("")
        print("⚡ ===== HOOK v29 EXECUTION =====")
        print("⏰ Время: " .. os.date("%H:%M:%S"))
        print("📊 VM data type: " .. type(vm_data))
        
        if type(vm_data) == "table" and #vm_data >= 2 then
            -- Извлекаем константы перед выполнением
            local constants = vm_data[2]
            if type(constants) == "table" then
                print("🔤 RUNTIME CONSTANTS EXTRACTION:")
                local runtime_count = 0
                for i, const in pairs(constants) do
                    runtime_count = runtime_count + 1
                    if type(const) == "string" and #const > 0 then
                        print("   🎯 Runtime[" .. i .. "]: '" .. const .. "'")
                        capture_string(const, "v29_runtime", "execution_constants")
                    end
                    if runtime_count <= 50 then
                        capture_constant(const, i, "v29_runtime", "execution_constants")
                    end
                end
                print("📊 Runtime constants processed: " .. runtime_count)
            end
            
            -- Извлекаем инструкции
            local instructions = vm_data[1]
            if type(instructions) == "table" then
                print("🔧 RUNTIME INSTRUCTIONS:")
                local exec_count = 0
                for i, instr in pairs(instructions) do
                    exec_count = exec_count + 1
                    if exec_count <= 20 then
                        capture_instruction(instr, i, "v29_runtime", "execution_instructions")
                    end
                end
                print("📊 Runtime instructions processed: " .. exec_count)
            end
        end
        
        -- Выполняем оригинальный код
        local result = original_v29(vm_data, env, ...)
        print("⚡ ===== END v29 EXECUTION =====")
        print("")
        return result
    end
    print("✅ v29 hook установлен!")
else
    print("⚠️ v29 function не найдена")
end

-- ============= HOOK STRING FUNCTIONS =============
-- Hook string.char
if string and string.char then
    local original_char = string.char
    string.char = function(...)
        local result = original_char(...)
        if type(result) == "string" and #result > 0 and (#result > 1 or string.byte(result) > 31) then
            capture_string(result, "string.char", "string_generation")
        end
        return result
    end
    print("✅ string.char hook установлен!")
end

-- Hook table.concat
if table and table.concat then
    local original_concat = table.concat
    table.concat = function(tbl, sep, ...)
        local result = original_concat(tbl, sep, ...)
        if type(result) == "string" and #result > 0 then
            capture_string(result, "table.concat", "string_assembly")
        end
        return result
    end
    print("✅ table.concat hook установлен!")
end

-- Hook print function
if print then
    local original_print = print
    print = function(...)
        local args = {...}
        for i, arg in ipairs(args) do
            if type(arg) == "string" and #arg > 0 then
                capture_string(arg, "print_output", "program_output")
            end
        end
        return original_print(...)
    end
    print("✅ print hook установлен!")
end

-- ============= FINAL DUMP FUNCTION =============
local function generate_final_report()
    print("")
    print("=" .. string.rep("=", 80))
    print("📊 ФИНАЛЬНЫЙ ОТЧЁТ FULL HOOK DUMPER")
    print("=" .. string.rep("=", 80))
    
    print("🔤 ИЗВЛЕЧЁННЫЕ СТРОКИ (" .. #_FULL_DUMP.strings .. "):")
    for i, str_data in ipairs(_FULL_DUMP.strings) do
        if i <= 20 then
            print("   [" .. str_data.id .. "] (" .. str_data.source .. ") " .. str_data.timestamp .. " '" .. str_data.value .. "'")
        end
    end
    if #_FULL_DUMP.strings > 20 then
        print("   ... и ещё " .. (#_FULL_DUMP.strings - 20) .. " строк")
    end
    
    print("")
    print("🔧 НАЙДЕННЫЕ ФУНКЦИИ (" .. #_FULL_DUMP.functions .. "):")
    for i, func_data in ipairs(_FULL_DUMP.functions) do
        if i <= 15 then
            print("   [" .. func_data.id .. "] " .. func_data.name .. " (" .. func_data.source .. ") " .. func_data.address)
        end
    end
    if #_FULL_DUMP.functions > 15 then
        print("   ... и ещё " .. (#_FULL_DUMP.functions - 15) .. " функций")
    end
    
    print("")
    print("📋 КОНСТАНТЫ (" .. #_FULL_DUMP.constants .. "):")
    for i, const_data in ipairs(_FULL_DUMP.constants) do
        if i <= 25 then
            print("   [" .. const_data.id .. "] [" .. const_data.index .. "] " .. const_data.type .. ": " .. safe_tostring(const_data.value))
        end
    end
    if #_FULL_DUMP.constants > 25 then
        print("   ... и ещё " .. (#_FULL_DUMP.constants - 25) .. " констант")
    end
    
    print("")
    print("⚡ ИНСТРУКЦИИ (" .. #_FULL_DUMP.instructions .. "):")
    for i, instr_data in ipairs(_FULL_DUMP.instructions) do
        if i <= 15 then
            local instr_str = ""
            if type(instr_data.instruction) == "table" then
                for j, v in ipairs(instr_data.instruction) do
                    instr_str = instr_str .. tostring(v) .. " "
                end
            else
                instr_str = tostring(instr_data.instruction)
            end
            print("   [" .. instr_data.id .. "] [" .. instr_data.index .. "] " .. instr_str)
        end
    end
    if #_FULL_DUMP.instructions > 15 then
        print("   ... и ещё " .. (#_FULL_DUMP.instructions - 15) .. " инструкций")
    end
    
    print("")
    print("🎯 АНАЛИЗ РЕЗУЛЬТАТОВ:")
    
    -- Анализ найденных строк для реконструкции
    local runtime_strings = {}
    for _, str_data in ipairs(_FULL_DUMP.strings) do
        if str_data.source == "v29_runtime" or str_data.source == "v28_component2_constant" then
            table.insert(runtime_strings, str_data.value)
        end
    end
    
    print("   🔤 Строк извлечено: " .. #_FULL_DUMP.strings)
    print("   🔧 Функций найдено: " .. #_FULL_DUMP.functions) 
    print("   📋 Констант обработано: " .. #_FULL_DUMP.constants)
    print("   ⚡ Инструкций захвачено: " .. #_FULL_DUMP.instructions)
    
    print("")
    print("🎉 РЕКОНСТРУИРОВАННЫЙ КОД:")
    print("-" .. string.rep("-", 40))
    
    -- Простая реконструкция на основе найденных строк
    local print_found = false
    local string_to_print = nil
    
    for _, str_data in ipairs(_FULL_DUMP.strings) do
        if str_data.value == "print" then
            print_found = true
        elseif print_found and str_data.value ~= "print" and #str_data.value > 0 then
            string_to_print = str_data.value
            break
        end
    end
    
    if print_found and string_to_print then
        print('print("' .. string_to_print .. '")')
    else
        print("-- Анализируйте извлечённые строки выше для реконструкции")
        if #runtime_strings > 0 then
            print("-- Найденные runtime строки:")
            for i, str in ipairs(runtime_strings) do
                if i <= 5 then
                    print("--   '" .. str .. "'")
                end
            end
        end
    end
    
    print("")
    print("=" .. string.rep("=", 80))
    print("✨ HOOK DUMPER завершён: " .. os.date("%H:%M:%S"))
    print("=" .. string.rep("=", 80))
end

-- Устанавливаем финальный отчёт на завершение работы
if _G.getfenv then
    local env = _G.getfenv()
    if env then
        env._FINAL_REPORT = generate_final_report
    end
end

print("")
print("🎉 Все хуки установлены! Начинаем анализ обфусцированного кода...")
print("⏰ Время старта: " .. os.date("%H:%M:%S"))
print("-" .. string.rep("-", 80))

-- ====== FULL HOOK INJECTION END ======


return v15("LOL!023Q0003053Q007072696E7403053Q00684Q6D00043Q00124Q00013Q001203000100024Q00013Q000200012Q00023Q00017Q00", v9(), ...);