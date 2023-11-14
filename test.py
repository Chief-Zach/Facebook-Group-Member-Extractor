from urllib.parse import unquote

var = unquote("%7B%22count%22%3A8%2C%22cursor%22%3A%22AQHRXIwUAAg_8nHbZ9Mauu5RWKehJ7vQziA_zp6oXvjmVh_XBgZ2kfiiy5v2qc6aUbJp%22%2C%22scale%22%3A1%2C%22search%22%3Anull%2C%22id%22%3A%22YXBwX2NvbGxlY3Rpb246MTAwMDY2NDE4NjYwMzQ4OjIzNTYzMTgzNDk6MzI%3D%22%7D&server_timestamps=true&doc_id=6767163196701249")

print(var)
# "variables": "{\"count\": 10, \"cursor\": \"AQHRolqukRQwQFeIqmFcU5qrunFrlRGgQi23J_SqPRrSuLk-wCYmNkV8_IKm-9tA2TqyguT54SpqtFYUXYpSa04FdQ\", \"groupID\": \"387875758242831\", \"recruitingGroupFilterNonCompliant\": false, \"scale\": 1, \"id\": \"387875758242831\"}",
                {"count":8,"cursor":"AQHRXIwUAAg_8nHbZ9Mauu5RWKehJ7vQziA_zp6oXvjmVh_XBgZ2kfiiy5v2qc6aUbJp","scale":1,"search":null,"id":"YXBwX2NvbGxlY3Rpb246MTAwMDY2NDE4NjYwMzQ4OjIzNTYzMTgzNDk6MzI="}&server_timestamps=true&doc_id=6767163196701249
