Using Rpi with camera instead of Smartphone.
1. Run live_stream.py file from For_RaspberryPi folder.
2. Using IP address assigned to Rpi to receive live stream in Laptop. 
    Ex. http://your-pi-address:8000/stream.mjpg
    put above address in collecting_training_data.py or rc_main.py as URL.
3. Collect data using collecting_training_data.py and Train model using train_model.py 
    both files situated in For_Laptop folder.
4. For final step use code in For_arduino folder to run bot.
    and simultaneously run rc_main.py situated in For_Laptop folder.