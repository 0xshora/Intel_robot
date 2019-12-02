
INCLUDE= -I ../../materials/wiringPi/wiringPi
LIBS= -lwiringPi -lm -lpthread -lrt -lcrypto

motor: motor.c motor_func.c input.c
	gcc -o motor motor.c motor_func.c input.c $(INCLUDE) $(LIBS)  

