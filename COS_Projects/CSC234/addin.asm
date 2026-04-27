extern printf
extern scanf

section .data
	prompt1 db "Enter the first number: ", 0
	prompt2 db "Enter the second number: ", 0
	user_input db "%d", 0
	answer db "The result of the addition is %d", 10,  0

section .bss
	num1 resd 1
	num2 resd 1

section .text
	global main

main:
	sub rsp, 40
	; ask the user for the first number
	lea rcx, [rel prompt1]
	call printf

	; read first user input
	lea rcx, [rel user_input]
	lea rdx, [rel num1]
	call scanf

	; ask the user for the second number
	lea rcx, [rel prompt2]
	call printf

	; read second user input
	lea rcx, [rel user_input]
	lea rdx, [rel num2]
	call scanf

	; Add the two numbers	
	mov eax, [rel num1]
	add eax, [rel num2]
	
	; Print result
	lea rcx, [rel answer]
	mov edx, eax
	call printf

	add rsp, 40
	ret
