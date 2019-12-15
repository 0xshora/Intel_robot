INCLUDE= -I ../../materials/wiringPi/wiringPi
LIBS= -lwiringPi -lm 
# LIBS= -lwiringPi -lm -lpthread -lrt -lcrypto

motor: motor.c motor_func.c getarg.c
	gcc -o motor motor.c motor_func.c getarg.c $(INCLUDE) $(LIBS)  



