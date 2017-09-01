wrk -t12 -c100 -d30s -s load_testing_steps.lua https://stepik.org:443/api/steps/ -H "Authorization: Bearer hraZS0UKCCWvrJmzAAmHIUqIkBfykJ"
wrk -t12 -c100 -d30s -s load_testing_lessons.lua https://stepik.org:443/api/lessons/ -H "Authorization: Bearer hraZS0UKCCWvrJmzAAmHIUqIkBfykJ"
wrk -t12 -c100 -d30s -s load_testing_attempts.lua https://stepik.org:443/api/attempts/ -H "Authorization: Bearer hraZS0UKCCWvrJmzAAmHIUqIkBfykJ"
