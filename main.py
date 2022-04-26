import bcrypt, json

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
        break
      else:
        if tries == 0:
          print("You ran out of tries!")
          break
        print(f'\nWrong password! You can only try {tries} more time(s)!\n')
        tries -= 1
        continue
    elif begin == "2":
      username = input("\nWhat is your username?\n")
      if username in data:
        print("That username is taken! Try again!\n")
        continue
      else:
        userpass = input(f"\nWhats the password for {username.capitalize()}?\n")
        with open("data.json", "w") as f:
          data[username] = {"password": bcrypt.hashpw(userpass.encode(), bcrypt.gensalt()).decode()}
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