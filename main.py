import bcrypt, json, random, string
import smtplib, ssl, os, asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

tries = 5
while True:
  with open("data.json", "r") as f:
    data = json.load(f)

  begin = input("""
+--------+---------------------+---------------+
|   1    |          2          |       3       |
+--------+---------------------+---------------+
| Login  |  Create An Account  |  Global Stats |
+--------+---------------------+---------------+
\n  
""")


  
  if begin in ["1", "2", "3"]:
    if begin == "1":
      username = input("\nWhat is your username?\n")
      if username not in data:
        print("That username is invalid! Try again!\n")
        continue
      loginpass = input(f"\nWhat is the password for {username.capitalize()}?\n")
      password = bytes(loginpass, encoding="utf+8")
      userpw = data[username]["password"]
      if bcrypt.checkpw(password, bytes(userpw, encoding="utf+8")):
        print("Correct! Logged in!")
        profile = input("""       
//==========[]============[]==========\\
||    1     ||     2      ||     3    ||
[]==========[]============[]==========[|
|| Profile  ||  Settings  ||  Log Out ||
\\\==========[]============[]==========//
\n""")
        if profile == "1":
          print("profile")


          
        elif profile == "2":
          settingsmenu = input("""
      
//==================[]================[]=====\\
||        1         ||       2        || css ||
[]==================[]================[] <3s ||
|| Change Password  ||  Change Email  ||  u  ||
[]==================[]================[]=====||
||        3         ||       4        || <3  ||
[]==================[]================[]=====[|
|| Change Username  ||     Log Out    || :)  ||
\\==================[]================[]=====//
\n""")
          if settingsmenu == "1":
            print("w.i.p")
            
          elif settingsmenu == "2":
            print("w.i.p")
            
          elif settingsmenu == "3":
            print("w.i.p")
            
          elif settingsmenu == "4":
            print("Logging out..")
            break
            
          else:
            print("You have to input one of the four numbers above the co-responding box!")
        elif profile == "3":
          print("Logging out!")
          break
        
        # remove this after finishing
        break
        
      else:
        if tries == 0:
          print("You ran out of tries!")
          break
        print(f'\nWrong password! You can only try {tries} more time(s)!\n')
        tries -= 1
        forgor = input("\nDid you forget your password?\ny or n?\n")
        if forgor.lower() in "y":
          myemail = os.environ['myemail']
          theiremail = data[username]["email"]
          password = os.environ['pass']
          
          message = MIMEMultipart("alternative")
          message["Subject"] = "Password Reset"
          message['X-Priority'] = '2'
          message["From"] = myemail
          message["To"] = theiremail
          print(f"\nSent an email to the cooresponding account with the username {username.capitalize()}")
          letters = string.ascii_lowercase
          ''.join(random.choice(letters) for i in range(0, 8))
          givenpass = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(20))
          html = f"""\
            <html>
              <head>
                <link rel='preconnect' href='https://fonts.googleapis.com'>
                <link rel='preconnect' href='https://fonts.gstatic.com' crossorigin>
                <link href='https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,700;1,400&display=swap' rel='stylesheet'>
              </head>
              <body style=\"background:whitesmoke;font-family:Roboto;color:#000000;border-radius: 20px;height:100%;width:100%;text-align:center\">
                <h1>Hello <strong>{username}</strong>!</h1>
                <h3>Your 20 character code for your password reset is <i>{givenpass}</i>!</h3>
                <br>
                <h4>If this wasn't you, don't worry! Your account is completely safe.</h4>
              </body>
            </html>
            """
          
          part = MIMEText(html, "html")
            
          message.attach(part)
          
          context = ssl.create_default_context()
          with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
              server.login(myemail, password)
              server.sendmail(myemail, theiremail, message.as_string())

          aaa = theiremail
          emaildupe = len(theiremail.split("@", 1)[1])
          sa = len(aaa) - emaildupe
          blur = '*' * sa
          emailthing = len(theiremail) - 5
          email = "@" + theiremail.split("@", 1)[1]
          
          confirm = input(f"\nA 20 digit string was sent to your email '{theiremail[0 : 5]}{blur}{email}', please paste it below to change your password.\n")
          if confirm == givenpass:
            newpass = input("\nCorrect! What do you want your new password to be?\n")
            with open("data.json", "w") as f:
              data[username]["password"] = bcrypt.hashpw(newpass.encode(), bcrypt.gensalt()).decode()
              json.dump(data, f, indent=2)
            print(f"Password changed to {newpass}!")
          else:
            print("The code was wrong! Please try again by getting a new code!")
        continue


    
    elif begin == "2":
      username = input("\nWhat is your username?\n")
      if username in data:
        print("That username is taken! Try again!\n")
        continue
      else:
        useremail = input(f"\nWhats your email address? (if you forgot your password you can get an email sent with a recovery)\n")
        userpass = input(f"\nWhats the password for {username.capitalize()}?\n")
        with open("data.json", "w") as f:
          data[username] = {"username": username, "password": bcrypt.hashpw(userpass.encode(), bcrypt.gensalt()).decode(), "email": useremail}
          json.dump(data, f, indent=2)
        print(f"Created account {username.capitalize()}! Make sure to remember your password!")
        break


    
    elif begin == "3":
      print(f"There are currently {len(data)} global users!\n\n")
      list = input("\nWould you like to list some of the users?\n")
      if list.lower() in "y":
        total = 0
        amt = input("\nHow many users would you like to list?\n")
        for user in data:
          if total == int(amt):
            print("\n\n")
            break
          print(data[user]["username"])
          total += 1
        if int(amt) > total:
          print(f"Theres only {len(data)} users to list! So I am unable to list the given amount of {amt}!")   
      continue
  else:
    print("\nMake sure you are inputting '1', '2', or '3'!\n")
    continue