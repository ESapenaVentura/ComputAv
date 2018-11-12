#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int main(void);
int Primo(unsigned long int numero);
int Suma_digitos(int numero, char Buff[]);


int Primo(unsigned long int numero){
	
	int divisor = 1;
	unsigned int i = 7;
	char Buff[10000];
	sprintf(Buff, "%lu", numero);
	int Comp_3 = 0;
	int Comp_5 = 0;
	if (numero % 2 == 0){
		printf("2\n");
		numero = numero / 2;
		}
		if(Suma_digitos(numero, Buff) % 3 == 0){
		printf("3\n");
		numero = numero / 3;
		}
		if((Buff[strlen(Buff) - 1] - '0') == 5 || (Buff[strlen(Buff) - 1] - '0') == 0){
		printf("5\n");
		numero = numero / 5;
		}
	while (numero > 1 && i <= (unsigned int) sqrtl((long double)numero)){
		if (numero % 2 == 0){
		printf("2\n");
		numero = numero / 2;
		}
		if(Suma_digitos(numero, Buff) % 3 == 0){
		printf("3\n");
		numero = numero / 3;
		}
		if((Buff[strlen(Buff) - 1] - '0') == 5 || (Buff[strlen(Buff) - 1] - '0') == 0){
		printf("5\n");
		numero = numero / 5;
		}
			for (i = 7; i < (unsigned int) sqrtl((long double)numero); i += 2){
				if (numero % i == 0){
					printf("%d\n", i);
					numero = numero/i;
					break;
				}
			}
		
	
	}
return numero;
}

int Suma_digitos(int numero, char Buffer[]){
	int suma = 0;
	for (int i = 0; i < strlen(Buffer); i++){
		suma += (Buffer[i] - '0');
	}
	return suma;
}


int main(void){
	int num;
	scanf("%d", &num);
	int resto = Primo(num);
	printf("Resto = %d\n", resto); 
	return 0;
}

