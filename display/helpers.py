from display.mails import mail_sent


def send_forget_password_mail(email, token):
    header = "Reset Password | BookHouse"
    link = f'http://127.0.0.1:8000/change_pass/{token}/'
    button = 'RESET PASSWORD'
    content = 'reset your password'
    heading = 'Reset Your Password'
    context = {"email": email, "header": header,
               "link": link, "button": button, "content": content, "heading": heading}
    mail_sent(context)
