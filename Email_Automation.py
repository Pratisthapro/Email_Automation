import os
import io
import json
import smtplib
import snowflake.connector
import pandas as pd
from datetime import datetime
from email.message import EmailMessage
from jinja2 import Template
def send_email(to_email, cc_recipients, subject, html_body):
    msg = EmailMessage()
    msg['From'] = 'alerts@accr.com'
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['Cc'] = ', '.join(cc_recipients)
    msg.set_content(html_body, subtype='html')
    # Use Gmail SMTP
    password = 'kpvunvucyxqqfacw'
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('alerts@innovaccer.com', password)
        smtp.send_message(msg)
    print(f":white_check_mark: Email sent to: {to_email}")
class Runner(object):
    @staticmethod
    def runner(file_object):
        # 1. Snowflake connection
        ctx = snowflake.connector.connect(
            user="DAENNESER",
            password="eJAM",
            account="y14",
            host="ykb41134.in.p1.satoricyber.net",
            warehouse="ORLANDOAPAREHOUSE",
            database="DAP",
            schema="L1"
        )
        cursor = ctx.cursor()
        cursor.autocommit = True
        # 2. Fetch email data
        cursor.execute("""
    SELECT * FROM L1.INNOTE_EMAIL_temp111 WHERE email IN (
  'DRQPEICS@GMAIL.COM',
  'NINOMAFFSM@GMAIL.COM',
  'RPAEL@FILYMC.COM',
  'PATRICK@GETPRLTH.COM',
  'PIMEE@GMAIL.COM',
  'DSLUIS@FAMILYMC.COM',
  'RAZ47@GMAIL.COM',
  'LAR@MSN.COM',
  'SIDNEYAMAOUTLOOK.COM'
)""")
        cols = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=cols)
        #raise Exception(df)
        # 3. Email HTML template
        html_template = """
          <p>Hello {{ first_name }},</p>
          
          <p>We hope this email finds you well.</p>
          
          <p>The Orlando Health and Innovaccer Teams have partnered to refresh the data in your InNote & PCP Dashboard. It has been more than 90 days since you last logged into the platform.</p>
          
          <p>We encourage you to access the InNote application, a seamless point-of-care tool that surfaces Care and Coding Gaps for your Orlando Health patient population, helping you take timely action to improve patient outcomes. In addition, there is a shortcut within InNote that takes you to a report called PCP Dashboard showing how well you are performing in your gap closure.</p>
          
          <p>Here’s a quick summary of the gaps for your practice based on the available data :</p>
          <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; font-family: Arial, sans-serif; font-size: 13px;">
  <tr>
    <td style="width: 150px;">No. of Open Coding Gaps</td>
    <td style="width: 80px; text-align: center;">{{ coding_gap  | int }}</td>
  </tr>
  <tr>
    <td style="width: 150px;">No. of Open Care Gaps</td>
    <td style="width: 80px; text-align: center;">{{ care_gap  | int }}</td>
  </tr>
</table>
         <p>We have also reset your account login. You will receive an email from <a href="mailto:user-assist@innovaccer.com">user-assist@innovaccer.com</a> to update your password. Your existing email and new password can be used to log into both InNote and the PCP Dashboard.</p>
          
          <p>Please let us know if you’d like a refresher demo for a quick catch-up. We’d be happy to assist!</p>
          
          <p>Thank you,</p>
          
          <p>Parul Tak</p>
          
          <hr>
          
          <p><em>The AI Cloud for Healthcare Performance<br>
          101 Mission Street, Suite 1950<br>
          San Francisco, CA 94105</em></p>
          
          <p><a href="https://innovaccer.com" target="_blank">innovaccer.com</a></p>
          """
        template = Template(html_template)
        # 4. Loop through each row and send emails
        for _, row in df.iterrows():
            first_name = row['FIRST NAME'].title()
            to_email = row['EMAIL']
            cc_list = []
            if pd.notna(row['EMAIL_PPC']):
                cc_list.append(row['EMAIL_PPC'])
            if pd.notna(row['INTERNAL_EMAIL']):
                cc_list += [email.strip() for email in row['INTERNAL_EMAIL'].split(',') if email.strip()]
            care_gap = row['OPEN CARE GAP COUNT']
            coding_gap = row['OPEN CODING GAP COUNT']
            practice = row['PRACTICE NAME']
            subject = f"Action Required: Activate Your Orlando Health InNote Account <> {practice}"
            html_body = template.render(
                first_name=first_name,
                care_gap=care_gap,
                coding_gap=coding_gap
            )
            send_email(to_email, cc_list, subject, html_body)
        yield ":white_check_mark: All emails processed."
