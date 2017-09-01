-- example dynamic request script which demonstrates changing
-- the request path and a header for each request
-------------------------------------------------------------
-- NOTE: each wrk thread has an independent Lua scripting
-- context and thus there will be one counter per thread

counter = 1
steps = {8095, 8074, 8073, 8075, 8076, 9294, 9166, 8077, 8079, 8078}
path = "/"

request = function()
   path = path .. steps[counter]
   counter = counter + 1
   if counter > #steps then
   	counter = 1
   end
   return wrk.format(nil, path)
end