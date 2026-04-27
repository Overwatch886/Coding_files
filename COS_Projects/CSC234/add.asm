extern printf

section .data
	ans db "The result is %d", 0

section .text
	global main

main:
	mov rax, 40
	add rax, 50

	sub rsp, 40
	lea rcx, [rel ans]
	mov rdx, rax
	call printf
	add rsp, 40
	ret
