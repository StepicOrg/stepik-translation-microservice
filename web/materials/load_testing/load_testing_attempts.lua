-- example dynamic request script which demonstrates changing
-- the request path and a header for each request
-------------------------------------------------------------
-- NOTE: each wrk thread has an independent Lua scripting
-- context and thus there will be one counter per thread

counter = 1
attempts = {23885618, 23885617, 13424158, 13424028, 13424017, 23885618, 23885617, 13424158, 13424028, 13424017}
path = "/"

request = function()
   path = path .. attempts[counter]
   counter = counter + 1
   if counter > #attempts then
   	counter = 1
   end
   return wrk.format(nil, path)
end
