This is a **complete email automation pipeline** 🐼📧
It:
1. Connects to Snowflake
2. Fetches doctor/practice email data
3. Creates personalized HTML emails
4. Sends emails automatically using Gmail SMTP

# 🔷 1. IMPORTS

```python id="pjfg8p"
import os
import io
import json
```

👉 Built-in Python libraries

---

```python id="gqjpv7"
import smtplib
```

👉 Used to send emails

Think:

```text id="l8td9w"
Python talking to Gmail server
```

---

```python id="l1u3lk"
import snowflake.connector
```

👉 Connect Python → Snowflake

---

```python id="ymjv6p"
import pandas as pd
```

👉 Data handling using DataFrames

---

```python id="zjlwmg"
from datetime import datetime
```

👉 Work with dates/time

---

```python id="aj65nb"
from email.message import EmailMessage
```

👉 Create email object

---

```python id="02dcd0"
from jinja2 import Template
```

👉 Create dynamic HTML templates

---

# 🔷 2. EMAIL FUNCTION

```python id="4g32mf"
def send_email(to_email, cc_recipients, subject, html_body):
```

👉 Reusable function to send email

---

# 🔹 Create email object

```python id="mll0ly"
msg = EmailMessage()
```

👉 Empty email container

---

# 🔹 Sender

```python id="thz1ie"
msg['From'] = 'alerts@accr.com'
```

👉 Who sent email

---

# 🔹 Subject

```python id="r4it7f"
msg['Subject'] = subject
```

👉 Dynamic email subject

---

# 🔹 Receiver

```python id="o8cm6w"
msg['To'] = to_email
```

---

# 🔹 CC

```python id="v7cl4h"
msg['Cc'] = ', '.join(cc_recipients)
```

👉 Convert list into comma-separated string

Example:

```python id="2fpb3n"
['a@gmail.com', 'b@gmail.com']
```

becomes:

```text id="6o7bgr"
a@gmail.com,b@gmail.com
```

---

# 🔹 Email body

```python id="5k3rbo"
msg.set_content(html_body, subtype='html')
```

👉 Add HTML content to email

---

# 🔷 Gmail SMTP

```python id="0p3jlwm"
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
```

👉 Connect securely to Gmail server

---

# 🔹 Login

```python id="wbd10v"
smtp.login('alerts@innovaccer.com', password)
```

👉 Authenticate sender

---

# 🔹 Send email

```python id="cvjlwm"
smtp.send_message(msg)
```

👉 Send email

---

# 🔷 3. RUNNER CLASS

```python id="7g0m3r"
class Runner(object):
```

👉 Main workflow controller

---

# 🔷 4. STATIC METHOD

```python id="l9x08z"
@staticmethod
```

👉 No object needed

Call directly:

```python id="gn3bl2"
Runner.runner()
```

---

# 🔷 5. Snowflake connection

```python id="uf5y94"
ctx = snowflake.connector.connect(...)
```

👉 Connect to Snowflake

---

# 🔹 Cursor

```python id="v52qoz"
cursor = ctx.cursor()
```

👉 Tool to run SQL

---

# 🔹 Autocommit

```python id="l89oz4"
cursor.autocommit = True
```

👉 Save changes automatically

---

# 🔷 6. Execute SQL query

```python id="mknn5o"
cursor.execute("""
SELECT * FROM ...
""")
```

👉 Fetch email-related records

---

# 🔷 7. Column names

```python id="0qjlwm"
cols = [col[0] for col in cursor.description]
```

👉 Extract column names

Example:

```text id="1bgmkf"
EMAIL
FIRST NAME
PRACTICE NAME
```

---

# 🔷 8. Fetch rows

```python id="mhmjlwm"
rows = cursor.fetchall()
```

👉 Get all query results

---

# 🔷 9. Create DataFrame

```python id="4qqffr"
df = pd.DataFrame(rows, columns=cols)
```

👉 Convert SQL results → pandas table

---

# 🔷 10. HTML Template

```python id="3xjlwm"
html_template = """
...
"""
```

👉 Email design/template

Contains:

* personalized greeting
* care gaps
* coding gaps
* practice info

---

# 🔷 11. Jinja Template

```python id="0ujlwm"
template = Template(html_template)
```

👉 Makes template dynamic

---

# 🔷 12. Loop through each row

```python id="9xjlwm"
for _, row in df.iterrows():
```

👉 Process one doctor/email at a time

---

# 🔷 13. Extract values

```python id="dljlwm"
first_name = row['FIRST NAME']
```

👉 Get data from DataFrame row

---

# 🔷 14. Handle CC emails

```python id="8mjlwm"
row['INTERNAL_EMAIL'].split(',')
```

👉 Convert:

```text id="yqqr4z"
a@gmail.com,b@gmail.com
```

into:

```python id="wjlwmn"
['a@gmail.com', 'b@gmail.com']
```

---

# 🔷 15. Dynamic subject

```python id="rzjlwm"
subject = f"Action Required..."
```

👉 Personalized subject line

---

# 🔷 16. Render HTML

```python id="26jlwm"
html_body = template.render(...)
```

👉 Replace variables:

```text id="hmjlwm"
{{ first_name }}
{{ care_gap }}
```

with real values

---

# 🔷 17. Send email

```python id="m9jlwm"
send_email(...)
```

👉 Calls earlier function

---

# 🔷 18. Yield final message

```python id="7ajlwm"
yield "✅ All emails processed."
```

👉 Return message slowly (generator behavior)

---

# 🧠 COMPLETE FLOW

```text id="lnjlwm"
Connect Snowflake
      ↓
Fetch doctor data
      ↓
Create DataFrame
      ↓
Loop through rows
      ↓
Generate personalized HTML
      ↓
Send emails
      ↓
Done
```

---

# 🎯 WHY JINJA TEMPLATE USED?

Instead of writing separate email for each doctor:

```text id="jlwmk9"
Hello John
Hello Mary
Hello Alex
```

👉 One template reused dynamically

---

# 🎯 ONE-LINE INTERVIEW ANSWER

> “This pipeline fetches healthcare provider data from Snowflake, dynamically generates personalized HTML emails using Jinja templates, and sends them through Gmail SMTP automation.”

---

# 🐼 FINAL MEMORY FLOW

```text id="jlwmu8"
Snowflake → DataFrame → Template → Email → Send
```
