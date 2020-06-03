import smtplib
# using smtplib sending email to the users.


def first_email(user_name, gmail_account):
    """
    The first email sent to the user. This email address is the same one in the data base for this username.
    :param user_name: The user username.
    :param gmail_account: The gmail account that you send the mail to.
    :return:
    """
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:  # open smtplib for gmail.
        smtp.ehlo()  # Identify with the mail server.
        smtp.starttls()  # Encrypt the traffic.
        smtp.ehlo()  # Rerun

        smtp.login('Iron.Dome.game@gmail.com', 'irondome12')  # Email address and password (Login to mail server).

        subject = 'Iron Dome new user!'  # Headline of the message
        body = 'Hey ' + user_name +'!\n' + 'Welcome to Iron Dome! We are very happy you choose to sign in!' + '\n' +\
               'We hope you will have a great time!'  # Content

        msg = f'Subject: {subject}\n\n{body}'  # The message sent to the user name.

        smtp.sendmail('Iron.dome.game@gmail.com', gmail_account, msg)
        # my email account, my email password, user name address


def send_email(user_name, new_password, gmail_account):
    """
    This function send to the username using his gmail a temporary password.
    :param user_name: The user username.
    :param new_password: The username temporary password.
    :param gmail_account: The email address in which the message is sent to.
    """
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:  # open smtplib for gmail.
        smtp.ehlo()  # Identify with the mail server.
        smtp.starttls()  # Encrypt the traffic.
        smtp.ehlo()  # Rerun

        smtp.login('Iron.Dome.game@gmail.com', 'irondome12')  # Email address and password (Login to mail server).

        subject = 'Iron Dome new password'  # Headline of the message
        body = 'Hey ' + user_name +'!\n' + 'Your new password is: ' + new_password  # Content

        msg = f'Subject: {subject}\n\n{body}'  # The message sent to the user name.

        smtp.sendmail('Iron.dome.game@gmail.com', gmail_account, msg)
        # my email account, my email password, user name address
