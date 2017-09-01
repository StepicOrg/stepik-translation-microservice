-- example dynamic request script which demonstrates changing
-- the request path and a header for each request
-------------------------------------------------------------
-- NOTE: each wrk thread has an independent Lua scripting
-- context and thus there will be one counter per thread

counter = 1
steps = {20957,20913,20958,20956, 20959,20930,16328, 20955, 20960}

request = function()
   path = "/"
   path = path .. steps[counter] .. "?service_name=yandex&lang=fr&access_token=ZYQej3aYNWPXAC7zGBzlIkt29bfQx9"
   print(path)
   counter = counter + 1
   if counter > #steps then
   	counter = 1
   end
   return wrk.format("GET", path)
end