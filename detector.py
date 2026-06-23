
#read the log file
with open("access.log", "r") as file:
    logs = file.readlines()

#sql pattern
sql_patterns = [
    "' OR",
    "OR 1=1",
    "--"
]

#xss pattern
xss_patterns = [
    "<script>",
    "</script>"
]

#display logs
sql_count = 0
xss_count = 0

for line in logs: #check log
    for pattern in sql_patterns: #check sql pattern
        if pattern.lower() in line.lower():
            sql_count += 1
            print("SQL Injection Detected")
            print(line)
            break 

    for pattern in xss_patterns:
       if pattern.lower() in line.lower():
           xss_count += 1
           print("XSS Attack Detected")
           print(line)
           break

#brute force detection
attempts = {} #dictionary

#login count 
for line in logs:
    if "POST /login" in line:
        parts = line.split()
        ip = parts[0]

        if ip not in attempts:
            attempts[ip] = 1
        else:
            attempts[ip] += 1

bruteforce_count = 0
#display
for ip in attempts:
    if attempts[ip] > 2:
         bruteforce_count += 1
         print("Possible Brute Force Attack")
         print("IP:", ip)
         print("Attempts:", attempts[ip])

#summary
print("\n===== ATTACK SUMMARY =====")
print("SQL Injection Attacks:", sql_count)
print("XSS Attacks:", xss_count)
print("Brute Force IPs:", bruteforce_count)

#report
total_attacks = sql_count + xss_count + bruteforce_count
if total_attacks <= 2:
    level = "LOW"
elif total_attacks <= 5:
    level = "MEDIUM"
else:
    level = "HIGH"

with open("report.txt", "w") as report:
    report.write("===== ATTACK SUMMARY =====\n")
    report.write(f"SQL Injection Attacks: {sql_count}\n")
    report.write(f"XSS Attacks: {xss_count}\n")
    report.write(f"Brute Force IPs: {bruteforce_count}\n")
    report.write(f"Total Attacks: {total_attacks}\n")
    report.write(f"Attack Level: {level}\n")
