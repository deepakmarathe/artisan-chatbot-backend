cd user
sh ./login.sh
echo "\n"
sleep 1

sh ./logout.sh
echo "\n"
sleep 1

sh ./register.sh
echo "\n"
sleep 1

sh ./register-form.sh
echo "\n"
sleep 1

cd ../
cd message

sh ./create_message.sh
echo "\n"
sleep 1

sh ./get_message.sh
echo "\n"
sleep 1

sh ./update_message.sh
echo "\n"
sleep 1

sh ./delete_message.sh
echo "\n"
sleep 1
