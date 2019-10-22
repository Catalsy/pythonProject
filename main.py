from functions import summary, register_user, main_menu, checkout, logout, login_user

x = input("account? ")

if x == 'y':
    login_user()
else:
    register_user()
# register_user()
main_menu()
total = summary()
checkout(total)
# logout()
# login_user()

