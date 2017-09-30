def get_grade(email):
    if email.startswith('s18') and email.endswith('@179.ru'):
        if email == 's18b1_kartashev@179.ru':
            return 'b3'
        else:
            return email[3:5]